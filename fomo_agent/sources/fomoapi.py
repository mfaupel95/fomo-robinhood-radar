"""fomoapi.io — the fomo half of the pipeline over plain HTTP, instead of through a browser.

For months the only way to read fomo from a server was to keep a signed-in Chrome running on it:
Cloudflare refuses direct calls, so an extension made the requests inside a real page and posted
the results back. It worked, and it cost a Xvfb display, a VNC server, a packed extension with its
own signing key, and a login that had to be done by hand through a remote desktop.

On 2026-09-10 fomo restricted that account. Not for anything clever — the collector was pulling
three leaderboards and two dozen wallet lookups every thirty minutes, which is what a scraper looks
like from the other side. This is the route that does not depend on one account staying in favour.

Two things make it cheap enough to matter:

  · the leaderboard costs one credit and already carries each trader's verified Solana and EVM
    wallets, so the ten-credit resolution endpoint is never needed. Checked against wallets this
    project had inferred independently: four of four exact, and the ones it adds have no fills on
    Robinhood Chain at all, which matches what the tape says about them.
  · one thesis page returns fifty recent notes across every token on the chain, so theses stop
    being a per-token cost.

What it does NOT replace is the tape. Their swap endpoint is a window on the last hundred fills per
trader with no way past it, documented as such. Ours is 109,669 fills and counting, read from the
chain for nothing. The two are not competing.
"""
from __future__ import annotations

import logging
from typing import Any, Iterable

import httpx

from ..config import settings
from ..credit_guard import reserve
from ..models import TraderRow
from .fomo import norm_addr

log = logging.getLogger(__name__)

BASE = "https://api.fomoapi.io"

# What each call costs, from the API's own /v1. Tracked so a pass can say what it spent rather than
# leaving the first 402 to be the moment anybody finds out.
CREDITS = {"leaderboard": 1, "thesis": 5, "normal": 1, "resolution": 10}


class FomoApiError(RuntimeError):
    pass


class OutOfCredits(FomoApiError):
    """402. Not a failure to retry — the month's budget is gone until it refills."""


class AuthenticationError(FomoApiError):
    """Permanent rejection; no automatic refresh or key rotation."""


class FomoApi:
    """Thin client. Fails soft everywhere except on being out of credits, which is worth shouting."""

    def __init__(self, key: str | None = None, client: httpx.Client | None = None):
        self.key = key or settings.fomoapi_key
        if not self.key:
            raise FomoApiError("FOMOAPI_KEY is not set (free key at https://fomoapi.io/dashboard)")
        self.http = client or httpx.Client(
            base_url=BASE, timeout=40,
            headers={"authorization": f"Bearer {self.key}", "accept": "application/json"},
        )
        self.requests = 0
        self.credits = 0.0

    def _get(self, path: str, cost: float, **params) -> Any:
        reserve(cost)
        self.credits += cost  # retain failed and ambiguous consumption
        self.requests += 1
        r = self.http.get(path, params={k: v for k, v in params.items() if v is not None})
        if r.status_code == 402:
            raise OutOfCredits(f"{path}: monthly credits exhausted")
        if r.status_code in (401, 403):
            raise AuthenticationError("fomoapi authentication rejected; operator required")
        r.raise_for_status()
        return r.json()

    def leaderboard(self, window: str = "24h", limit: int = 150) -> list[TraderRow]:
        """One window of the board. One credit whatever the limit, so always ask for the lot."""
        return parse_leaderboard(self._get(f"/v2/leaderboard/{window}", CREDITS["leaderboard"],
                                           limit=limit), window)

    def theses(self, chain: str = "robinhood", pages: int = 1) -> list[dict]:
        """Recent notes across every token on one chain. Fifty a page, five credits a page."""
        out: list[dict] = []
        for page in range(1, pages + 1):
            payload = self._get("/v2/thesis", CREDITS["thesis"], chain=chain,
                                pages=None if page == 1 else page)
            rows = parse_theses(payload)
            out.extend(rows)
            if len(rows) < 50:
                break
        return out


# ---------------------------------------------------------------- parsers


def _f(v: Any) -> float | None:
    try:
        return float(v) if v is not None else None
    except (TypeError, ValueError):
        return None


def parse_leaderboard(payload: Any, window: str) -> list[TraderRow]:
    """Their board into ours.

    The window lives in the URL rather than the row, so `pnlUsd` means whichever window was asked
    for. It is written into the matching column and the others left alone, so three calls fill in
    three figures without one overwriting another.
    """
    rows = (payload or {}).get("traders") or []
    out: list[TraderRow] = []
    for t in rows:
        handle = t.get("handle")
        if not handle:
            continue
        wallets = t.get("wallets") or {}
        evm = wallets.get("evm")
        pnl = _f(t.get("pnlUsd"))
        out.append(TraderRow(
            # No user id in this response, and the handle is what everything else joins on anyway.
            address=norm_addr(evm) if evm else handle,
            fomo_user_id=None,
            fomo_handle=handle,
            profile_address=None,
            evm_address=norm_addr(evm) if evm else None,
            chain="robinhood",
            pnl_24h=pnl if window == "24h" else None,
            pnl_7d=pnl if window == "7d" else None,
            pnl_30d=pnl if window == "30d" else None,
            trades_cnt=t.get("trades"),
            volume_usd=_f(t.get("volumeUsd")),
            source=f"fomoapi_{window}",
        ))
    return out


def parse_theses(payload: Any) -> list[dict]:
    """One page of notes. A row without text or a token is not a thesis and is dropped."""
    rows = (payload or {}).get("theses") or []
    out = []
    for t in rows:
        text = (t.get("text") or "").strip()
        token = t.get("token") or {}
        mint = token.get("address")
        handle = t.get("handle")
        if not (text and mint and handle):
            continue
        out.append({
            "handle": handle,
            "mint": norm_addr(mint),
            "symbol": token.get("symbol"),
            "text": text,
            "pnl_usd": _f(t.get("unrealizedPnlUsd")),
            "realized_usd": _f(t.get("realizedPnlUsd")),
            "cost_usd": _f(t.get("equity")),
            "at": t.get("ts"),
            "chain": t.get("chain"),
        })
    return out


def wallets_from(rows: Iterable[TraderRow]) -> dict[str, str]:
    """handle -> verified EVM wallet, for the rows that carry one."""
    return {r.fomo_handle: r.evm_address for r in rows if r.fomo_handle and r.evm_address}
