"""The second signal class: a new listing with a real market behind it and no cohort.

The burst rule in hot.py answers "whose money arrived, all at once". It cannot answer for a name
nobody on the roster has touched, and that blind spot is not theoretical: on 2026-11-01 PONS listed
with $66.4M of pool depth and $50M of turnover in a day, and two "Claude" tokens ran +744% and
+609% on $10.25M pools, while every feed stayed silent — because the gate asked for a wallet cohort
and there was none.

So this rule asks about the pool instead, and it asks three things:

  * depth      — liquidity of at least `listing_min_liq_usd` (default $1M). Below that a launch is
                 somebody's weekend, not a market.
  * turnover   — 24h volume of at least `listing_min_volume_ratio` times that depth (default 1.0):
                 the pool has traded more than it holds, which is a market with two sides rather
                 than a mint with one buyer.
  * no cohort  — not one roster fill on the token, ever. This is what makes it a *different* kind
                 of signal: the moment a wallet we track buys, the burst rule and the signals feed
                 own the name and this one steps back.

Plus age: a listing older than `listing_max_age_h` is not news.

What it is not: a buy. There is no smart money in it, so it says "watch this" and never "this
cohort is in". Everything is read from the `tokens` table, which the new-token and enrichment
passes already fill, so a pass costs no request and cannot block the cron loop that writes them.
"""
from __future__ import annotations

import logging
import sqlite3

from .. import db
from ..config import settings

log = logging.getLogger(__name__)

# Real fills only: a dust row or a seeded distribution is not somebody entering the name.
ROSTER_FILLS = ("SELECT COUNT(*) FROM trades tr WHERE tr.mint = t.mint "
                "AND COALESCE(tr.kind, 'trade') = 'trade'")


def _ratio(volume: float | None, liquidity: float | None) -> float | None:
    if not volume or not liquidity:
        return None
    return round(volume / liquidity, 3)


def candidates(conn: sqlite3.Connection, chain: str | None = None, now: int | None = None,
               min_liq_usd: float | None = None, min_volume_ratio: float | None = None,
               max_age_h: float | None = None, limit: int = 50) -> list[dict]:
    """New listings with depth, turnover and not one roster fill — the freshest first.

    The age is the pool's own launch time where we have it and our first sight of the token
    otherwise; a token we found today that launched a week ago is still a new listing to us, and
    one we cannot date at all is left out rather than guessed at.
    """
    now = now or db.now()
    min_liq = settings.listing_min_liq_usd if min_liq_usd is None else min_liq_usd
    ratio = settings.listing_min_volume_ratio if min_volume_ratio is None else min_volume_ratio
    age_h = settings.listing_max_age_h if max_age_h is None else max_age_h
    since = now - age_h * 3600
    rows = conn.execute(
        "SELECT t.mint mint, t.chain chain, COALESCE(t.symbol, substr(t.mint, 1, 8)) sym, "
        "  t.liquidity_usd liq, t.volume_usd vol24, t.mcap_usd mcap, "
        "  COALESCE(t.created_at, t.first_seen_at) t0, t.sellable sellable, "
        f"  ({ROSTER_FILLS}) roster_fills "
        "FROM tokens t "
        "WHERE t.liquidity_usd >= ? AND t.volume_usd IS NOT NULL AND t.volume_usd > 0 "
        "  AND t.volume_usd >= ? * t.liquidity_usd "
        "  AND COALESCE(t.created_at, t.first_seen_at) >= ? "
        # a token nobody can sell is not a lead, however deep its pool looks (trap pools)
        "  AND COALESCE(t.sellable, 1) != 0 "
        + ("  AND t.chain = ? " if chain else "")
        + "ORDER BY (t.volume_usd / t.liquidity_usd) DESC, t.volume_usd DESC LIMIT ?",
        [min_liq, ratio, since, *([chain] if chain else []), limit],
    ).fetchall()
    out = []
    for r in rows:
        if r["roster_fills"]:
            continue          # the cohort owns this one now; the burst rule reports it
        out.append({
            "mint": r["mint"], "chain": r["chain"], "sym": r["sym"],
            "liq": r["liq"], "vol24": r["vol24"], "mcap": r["mcap"],
            "volume_ratio": _ratio(r["vol24"], r["liq"]),
            "t0": r["t0"], "age_s": (now - r["t0"]) if r["t0"] else None,
            "roster_fills": 0, "sellable": r["sellable"],
        })
    return out


def record(conn: sqlite3.Connection, c: dict, now: int | None = None) -> bool:
    """Write a listing down once, and say whether this was the first time we saw it qualify.

    One row per mint: a token that stays liquid for three days is one lead, not seventy-two. The
    numbers are refreshed on the row so the feed shows today's pool, but `ts` stays the moment it
    first qualified — that is what the reader is being told.
    """
    now = now or db.now()
    existed = conn.execute("SELECT 1 FROM listing_signals WHERE mint=?",
                           (c["mint"],)).fetchone() is not None
    with db.tx(conn):
        conn.execute(
            "INSERT INTO listing_signals(mint, chain, ts, symbol, liquidity_usd, volume_usd, "
            "  mcap_usd, volume_ratio, age_s) VALUES(?,?,?,?,?,?,?,?,?) "
            "ON CONFLICT(mint) DO UPDATE SET symbol=excluded.symbol, "
            "  liquidity_usd=excluded.liquidity_usd, volume_usd=excluded.volume_usd, "
            "  mcap_usd=excluded.mcap_usd, volume_ratio=excluded.volume_ratio",
            (c["mint"], c.get("chain"), now, c.get("sym"), c.get("liq"), c.get("vol24"),
             c.get("mcap"), c.get("volume_ratio"), c.get("age_s")))
    return not existed


def sweep(conn: sqlite3.Connection, chain: str | None = None, now: int | None = None) -> dict:
    """One pass of the rule: look at every new listing, record the ones that qualify.

    Read-only against `tokens` and one short write per new lead, so it can run beside the cron
    loop without holding a lock on anything the track pass writes.
    """
    now = now or db.now()
    found = candidates(conn, chain, now)
    new = [c for c in found if record(conn, c, now)]
    for c in new:
        log.info("liquid listing %s %s: $%.0f depth, $%.0f in 24h (%.2fx), 0 roster fills",
                 c.get("chain"), c["sym"], c["liq"] or 0, c["vol24"] or 0, c["volume_ratio"] or 0)
    return {"seen": len(found), "new": len(new),
            "mints": [c["mint"] for c in new]}


def recent(conn: sqlite3.Connection, chain: str | None = None, hours: int = 168,
           limit: int = 50, now: int | None = None) -> list[dict]:
    """Every lead the rule recorded in the window, newest first, with today's pool on it."""
    now = now or db.now()
    rows = conn.execute(
        "SELECT s.*, COALESCE(t.symbol, s.symbol, substr(s.mint, 1, 8)) sym, "
        "  COALESCE(t.liquidity_usd, s.liquidity_usd) liq, "
        "  COALESCE(t.volume_usd, s.volume_usd) vol24, "
        "  COALESCE(t.sellable, 1) sellable "
        "FROM listing_signals s LEFT JOIN tokens t ON t.mint = s.mint "
        "WHERE s.ts >= ?" + (" AND s.chain = ?" if chain else "") + " ORDER BY s.ts DESC LIMIT ?",
        [now - hours * 3600, *([chain] if chain else []), limit],
    ).fetchall()
    return [{
        "mint": r["mint"], "chain": r["chain"], "sym": r["sym"], "ts": r["ts"],
        "age_h_at_read": round((now - r["ts"]) / 3600, 1),
        "liq": r["liq"], "vol24": r["vol24"], "mcap": r["mcap_usd"],
        "volume_ratio": _ratio(r["vol24"], r["liq"]),
        "listing_age_h": round((r["age_s"] or 0) / 3600, 1) if r["age_s"] is not None else None,
        "sellable": r["sellable"],
    } for r in rows]
