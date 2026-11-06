"""DexScreener public API (no key). Used only as a trigger for fresh tokens on configured chains.

Endpoints (public, documented):
  GET /token-profiles/latest/v1          -> latest tokens with profiles   (60 rpm)
  GET /token-boosts/latest/v1            -> latest boosted tokens         (60 rpm)
  GET /token-boosts/top/v1               -> most boosted tokens           (60 rpm)
  GET /tokens/v1/{chain}/{a1,a2,...}     -> pairs for up to 30 mints      (300 rpm)

Note: the "New Pairs" / "Trending" lists in the web UI have no public endpoint; the feeds
above only contain tokens that bought a profile or a boost. Coverage is narrower than the UI.
"""
from __future__ import annotations

from typing import Iterable

import httpx

from ..config import settings
from ..models import NewToken, norm_addr
from ..enrich_budget import current
from .filters import filter_tokens

BASE = "https://api.dexscreener.com"
_BATCH = 30
FEEDS = ("/token-profiles/latest/v1", "/token-boosts/latest/v1", "/token-boosts/top/v1")


class DexScreener:
    def __init__(self, client: httpx.Client | None = None, chains: Iterable[str] | None = None):
        self.http = client or httpx.Client(base_url=BASE, timeout=20, headers={"accept": "application/json"})
        self.chains = tuple(chains) if chains else settings.dex_chains

    def _get(self, path: str) -> list | dict:
        budget = current.get()
        r = budget.get(self.http, path, source='dexscreener') if budget else self.http.get(path)
        r.raise_for_status()
        return r.json()

    def latest_mints(self) -> dict[str, list[str]]:
        """chain -> deduped token addresses from all feeds, for configured chains only."""
        out: dict[str, list[str]] = {c: [] for c in self.chains}
        seen: set[tuple[str, str]] = set()
        for path in FEEDS:
            try:
                items = self._get(path)
            except httpx.HTTPError:
                continue
            for it in items if isinstance(items, list) else []:
                chain, addr = it.get("chainId"), it.get("tokenAddress")
                if chain in out and addr and (chain, addr) not in seen:
                    seen.add((chain, addr))
                    out[chain].append(addr)
        return out

    def pairs_for(self, chain: str, mints: Iterable[str]) -> list[dict]:
        mints = list(mints)
        pairs: list[dict] = []
        for i in range(0, len(mints), _BATCH):
            chunk = ",".join(mints[i : i + _BATCH])
            data = self._get(f"/tokens/v1/{chain}/{chunk}")
            pairs.extend(data if isinstance(data, list) else [])
        return pairs

    def new_tokens(self, min_mcap: float | None = None, max_age_hours: float | None = None) -> list[NewToken]:
        """Fresh tokens above the mcap threshold across configured chains. Thresholds default to config."""
        min_mcap = settings.new_token_min_mcap_usd if min_mcap is None else min_mcap
        max_age_hours = settings.new_token_max_age_hours if max_age_hours is None else max_age_hours
        pairs: list[dict] = []
        for chain, mints in self.latest_mints().items():
            if mints:
                pairs.extend(self.pairs_for(chain, mints))
        return filter_pairs(pairs, min_mcap=min_mcap, max_age_hours=max_age_hours)

    # backward-compatible alias
    new_solana_tokens = new_tokens


def parse_pair(p: dict) -> NewToken | None:
    base = p.get("baseToken") or {}
    mint = base.get("address")
    if not mint:
        return None
    created_ms = p.get("pairCreatedAt")
    liq = (p.get("liquidity") or {}).get("usd")
    # arrives as a string; it is what marks an open position to market
    price = p.get("priceUsd")
    # the pool's turnover, in the same response as its depth: the second signal class is judged on
    # the two together (pipeline/listings.py), so it is read here rather than asked for later
    volume = (p.get("volume") or {}).get("h24")
    return NewToken(
        mint=norm_addr(mint),
        chain=p.get("chainId") or "solana",
        symbol=base.get("symbol"),
        mcap_usd=p.get("marketCap") or p.get("fdv"),
        liquidity_usd=liq,
        volume_usd=float(volume) if volume not in (None, "") else None,
        price_usd=float(price) if price not in (None, "") else None,
        created_at=int(created_ms / 1000) if created_ms else None,
        dex=p.get("dexId"),
        pair_address=p.get("pairAddress"),
        source="dexscreener",
    )


def filter_pairs(pairs: list[dict], *, min_mcap: float, max_age_hours: float, now_ts: int | None = None) -> list[NewToken]:
    """Pure function: raw pairs -> best per (chain, mint) -> thresholds. Testable offline."""
    tokens = [t for t in map(parse_pair, pairs) if t]
    return filter_tokens(tokens, min_mcap=min_mcap, max_age_hours=max_age_hours, now_ts=now_ts)
