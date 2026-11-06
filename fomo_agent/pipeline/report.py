"""Markdown report: top active, new candidates, dropped, and 24h buys grouped by mint."""
from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone

from .. import db


def _h(ts: int | None) -> str:
    return datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%m-%d %H:%M") if ts else "-"


def _usd(v) -> str:
    if v is None:
        return "-"
    a = abs(v)
    if a >= 1_000_000:
        return f"${v / 1_000_000:.1f}M"
    if a >= 1_000:
        return f"${v / 1_000:.1f}k"
    return f"${v:.0f}"


def _pnl_section(conn: sqlite3.Connection, hours: int = 72) -> list[str]:
    """The PnL, in the order it may be quoted: realizable first, paper as a footnote.

    A mark nobody can sell into is not a PnL, and stating it first taught the reader the wrong
    number twice (PEAT/OYSTERS/TENDIES read +$4.1k of paper profit while `sell-check` said the
    transfer to the router could not clear).
    """
    from .analyze import cohort_pnl

    p = cohort_pnl(conn, hours=hours)
    real, paper, unchecked = p["realizable"], p["paper"], p["unchecked"]
    out = [f"## PnL (official figure: realizable, tape entries of the last {hours}h)\n"]
    if not p["positions"]:
        out.append("_no open positions in the window_\n")
        return out
    out.append(f"- **{_usd(real['pnl'])} realizable** on {_usd(real['cost'])} cost "
               f"({real['positions']} of {len(p['positions'])} positions passed the sell check)\n")
    if unchecked["positions"]:
        out.append(f"- _not counted: {_usd(unchecked['pnl'])} on {_usd(unchecked['cost'])} "
                   f"({unchecked['positions']} positions nobody has run `sell-check` on yet)\n")
    if paper["positions"]:
        out.append(f"- _paper, not PnL: {_usd(paper['pnl'])} on {_usd(paper['cost'])} "
                   f"({paper['positions']} positions with no market or unsellable) — a note, "
                   "never the headline\n")
    out.append("")
    return out


def _listings_section(conn: sqlite3.Connection, hours: int = 168) -> list[str]:
    """The second signal class: pools with real money and nobody we track in them yet."""
    from .listings import recent

    rows = recent(conn, hours=hours, limit=15)
    out = ["## Historical listing signals (not currently requalified candidates)\n"]
    if not rows:
        out.append("_none in the window_\n")
        return out
    for r in rows:
        ratio = f"{r['volume_ratio']:.2f}x" if r["volume_ratio"] is not None else "-"
        out.append(f"- `{r['mint']}` {r['sym'] or ''} [{r['chain'] or 'solana'}]: "
                   f"depth {_usd(r['liq'])}, 24h {_usd(r['vol24'])} ({ratio}), "
                   f"mcap {_usd(r['mcap'])}, seen {r['age_h_at_read']:.1f}h ago; "
                   f"{'STALE' if r['stale'] else 'nominal mark only'}, listing age {r['listing_age_h']}h")
    out.append("")
    return out


def build_report(conn: sqlite3.Connection, hours: int = 24) -> str:
    now = db.now()
    since = now - hours * 3600
    out = [f"# FOMO Robinhood Radar — {datetime.now(timezone.utc):%Y-%m-%d %H:%M} UTC\n"]
    from .data_quality import text
    out.append(text(conn) + '\n')

    counts = conn.execute("SELECT status, COUNT(*) c FROM traders GROUP BY status").fetchall()
    out.append("**Traders:** " + ", ".join(f"{r['status']}={r['c']}" for r in counts) + "\n")

    # The two numbers a reader quotes first: what the cohort could actually take out, and which
    # pools have real money in them without a single wallet of ours. Everything below is detail.
    out.extend(_pnl_section(conn))
    out.extend(_listings_section(conn))

    out.append("## Top active\n")
    rows = conn.execute("SELECT * FROM traders WHERE status='active' ORDER BY score DESC LIMIT 20").fetchall()
    if not rows:
        out.append("_none yet_\n")
    for r in rows:
        tags = json.loads(r["tags"]) if r["tags"] else {}
        out.append(f"- `{r['address']}` score={r['score']} {r['fomo_handle'] or ''} style={tags.get('style')} flags={tags.get('red_flags')}")
        if r["ai_summary"]:
            out.append(f"  - {r['ai_summary']}")
    out.append("")

    out.append(f"## New candidates (last {hours}h)\n")
    rows = conn.execute("SELECT * FROM traders WHERE first_seen_at>=? ORDER BY first_seen_at DESC", (since,)).fetchall()
    out.append(f"{len(rows)} new" + ("" if rows else " — _none_"))
    for r in rows[:30]:
        out.append(f"- `{r['address']}` from {r['source']} ({_h(r['first_seen_at'])})")
    out.append("")

    out.append(f"## Dropped (last {hours}h)\n")
    rows = conn.execute(
        "SELECT h.address, h.reason, h.ts FROM score_history h WHERE h.status='dropped' AND h.ts>=? ORDER BY h.ts DESC", (since,)
    ).fetchall()
    if not rows:
        out.append("_none_")
    for r in rows[:20]:
        out.append(f"- `{r['address']}`: {r['reason']}")
    out.append("")

    out.append(f"## Buys by active/watch traders (last {hours}h), grouped by token\n")
    rows = conn.execute(
        "SELECT tr.mint, tk.symbol, tk.chain, COUNT(DISTINCT tr.address) wallets, SUM(tr.sol_amount) sol, "
        "GROUP_CONCAT(DISTINCT substr(tr.address,1,6)) who "
        "FROM trades tr JOIN traders t ON t.address=tr.address LEFT JOIN tokens tk ON tk.mint=tr.mint "
        "WHERE tr.side='buy' AND tr.ts>=? AND t.status IN ('active','watch') "
        "GROUP BY tr.mint ORDER BY wallets DESC, sol DESC LIMIT 30",
        (since,),
    ).fetchall()
    if not rows:
        out.append("_no buys recorded_")
    for r in rows:
        flag = " **SIGNAL**" if r["wallets"] >= 2 else ""
        out.append(f"- `{r['mint']}` {r['symbol'] or ''} [{r['chain'] or 'solana'}]: {r['wallets']} wallets, {r['sol'] or 0:.2f} SOL [{r['who']}]{flag}")
    out.append("")

    runs = conn.execute("SELECT kind, started_at, error FROM runs ORDER BY id DESC LIMIT 5").fetchall()
    if runs:
        out.append("## Recent runs\n")
        for r in runs:
            out.append(f"- {r['kind']} @ {_h(r['started_at'])}" + (f" ERROR: {r['error'][:80]}" if r["error"] else ""))
    return "\n".join(out)
