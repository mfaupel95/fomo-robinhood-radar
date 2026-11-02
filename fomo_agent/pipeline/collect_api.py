"""One collection pass over fomoapi.io. Replaces the browser for the fomo half of the pipeline.

Same tables, same downstream, different road. What arrives here that never arrived through the
browser is the **verified wallet**: fomo's own API only ever returned an internal account with no
on-chain history, so this project inferred the trading wallet by intersecting who traded the same
token in the same minute. That inference is good — checked against these verified answers, four of
four exact — but it needed a dozen swap lookups per trader and it could not resolve a wallet that
trades quietly.

The wallets that arrive verified are linked directly. Where one contradicts a wallet we inferred,
nothing is overwritten: the conflict is recorded, because two claims on the same trader is a thing
to look at rather than a thing to resolve by whichever source spoke last.

Budget is the constraint that shapes the schedule. A free key is 1,000 credits a month, which is
32 a day, and the two calls are not worth the same: the first live pass bought 18 new traders and
125 verified wallets for 2 credits, and 16 notes for 5. So the 24h board runs every two hours
(12 a day), and the 7d board and one page of notes every eight (18 a day) — 30 a day, 900 a month,
with the guard below as the backstop rather than the plan.
"""
from __future__ import annotations

import calendar
import logging
import sqlite3
import time

from .. import db
from ..config import settings
from ..sources.fomoapi import CREDITS, FomoApi, OutOfCredits

log = logging.getLogger(__name__)


def store_rows(conn: sqlite3.Connection, rows, source: str) -> int:
    """Upsert the board, keyed by handle rather than by fomo's user id.

    The browser route carried fomo's own `userId` on every row and everything downstream keys on
    it. This feed does not carry one, and inventing one per row would give a trader we already know
    a second, empty record. So a handle we have is updated in place, and one we do not gets a
    synthetic id that says where it came from.
    """
    n_new = 0
    with db.tx(conn):
        for r in rows:
            if not r.fomo_handle:
                continue
            row = conn.execute("SELECT user_id FROM fomo_users WHERE handle = ?",
                               (r.fomo_handle,)).fetchone()
            uid = row["user_id"] if row else f"api:{r.fomo_handle}"
            n_new += db.upsert_fomo_user(
                conn, uid, handle=r.fomo_handle, evm_address=r.evm_address,
                pnl_24h=r.pnl_24h, pnl_7d=r.pnl_7d, pnl_30d=r.pnl_30d,
                trades_cnt=r.trades_cnt, volume_usd=r.volume_usd, source=source,
            )
    return n_new


def link_wallets(conn: sqlite3.Connection, rows) -> dict:
    """Attach the verified wallets, and say what happened to each.

    `new` is a trader the tape can now be read for. `agrees` is our own inference confirmed by an
    independent source, which is the number worth keeping an eye on: the day it stops being high,
    the resolver has drifted.
    """
    stats = {"new": 0, "agrees": 0, "conflicts": 0}
    with db.tx(conn):
        for r in rows:
            if not (r.fomo_handle and r.evm_address):
                continue
            row = conn.execute(
                "SELECT user_id, onchain_address FROM fomo_users WHERE handle = ?",
                (r.fomo_handle,),
            ).fetchone()
            if row is None:
                continue
            ours = (row["onchain_address"] or "").lower()
            theirs = r.evm_address.lower()
            if not ours:
                conn.execute(
                    "UPDATE fomo_users SET onchain_address=?, onchain_at=?, onchain_note=? "
                    "WHERE user_id=?", (theirs, db.now(), "verified by fomoapi", row["user_id"]))
                stats["new"] += 1
            elif ours == theirs:
                stats["agrees"] += 1
            else:
                conn.execute(
                    "UPDATE fomo_users SET onchain_note=? WHERE user_id=?",
                    (f"conflict: we inferred {ours}, fomoapi verifies {theirs}", row["user_id"]))
                stats["conflicts"] += 1
                log.warning("wallet conflict for %s: ours=%s theirs=%s", r.fomo_handle, ours, theirs)
    return stats


def store_theses(conn: sqlite3.Connection, rows: list[dict]) -> dict:
    """Keep the notes whose author we already know.

    A handle we have never collected has no verdict either, and a thesis is only published beside a
    score — so storing one would be storing something that can never be shown.
    """
    stats = {"seen": len(rows), "stored": 0, "new": 0, "unknown_author": 0}
    with db.tx(conn):
        for t in rows:
            row = conn.execute("SELECT user_id FROM fomo_users WHERE handle = ?",
                               (t["handle"],)).fetchone()
            if row is None:
                stats["unknown_author"] += 1
                continue
            db.upsert_token(conn, t["mint"], chain=t.get("chain") or "robinhood",
                            symbol=t.get("symbol"))
            # No trade id in this feed, so one note per author per token — which is also what an
            # edited thesis should do: replace itself rather than pile up.
            fresh = db.upsert_thesis(
                conn, trade_id=f"api:{t['handle']}:{t['mint']}", user_id=row["user_id"],
                mint=t["mint"], text=t["text"], pnl_usd=t.get("pnl_usd"),
                cost_usd=t.get("cost_usd"), is_dev=False)
            stats["stored"] += 1
            stats["new"] += 1 if fresh else 0
    return stats


FOMO_RUN_KINDS = ("fomoapi", "fomo_ingest", "fomoapi_24h", "fomoapi_7d", "fomoapi_theses")


def spent_this_month(conn: sqlite3.Connection, at: int | None = None) -> float:
    """Credits already spent since the first of the month, from the run log.

    Every pass writes what it cost into its own `runs` row, so the ledger already exists and does
    not need a second table. It resets with the calendar month because that is when the plan does.
    The run loop split the one `fomoapi` step into per-cadence steps (24h board, 7d board,
    theses), so every kind that spends credits has to be named here - a query pinned to the old
    single kind kept counting yesterday's rows and under-reported the month (70 spent while the
    passes had really burned 76).
    """
    t = time.gmtime(at or db.now())
    start = calendar.timegm((t.tm_year, t.tm_mon, 1, 0, 0, 0, 0, 0, 0))
    row = conn.execute(
        "SELECT COALESCE(SUM(json_extract(stats_json, '$.credits')), 0) FROM runs "
        f"WHERE kind IN ({','.join('?' * len(FOMO_RUN_KINDS))}) AND started_at >= ?",
        (*FOMO_RUN_KINDS, start)).fetchone()
    return float(row[0] or 0.0)


def collect(conn: sqlite3.Connection, windows: tuple[str, ...] = ("24h", "7d"),
            thesis_pages: int | None = None, api: FomoApi | None = None,
            cap: int | None = None) -> dict:
    """A full pass: the boards, the wallets they carry, and a page of theses.

    The month's budget is checked before each call rather than discovered at the first 402. On a
    free key that matters: a pass that runs out halfway leaves the boards collected and the notes
    missing, every two hours, silently, until somebody happens to look. Here the boards are bought
    first and the notes only if what remains covers them, so the thing that degrades under pressure
    is the cheapest thing to lose.
    """
    api = api or FomoApi()
    cap = settings.fomoapi_monthly_credits if cap is None else cap
    spent = spent_this_month(conn)
    stats: dict = {"windows": {}, "credits": 0.0, "requests": 0, "month_spent": spent}

    def afford(cost: float) -> bool:
        return not cap or spent + api.credits + cost <= cap

    try:
        for window in windows:
            if not afford(CREDITS["leaderboard"]):
                stats["budget_stop"] = f"{spent + api.credits:.0f}/{cap} credits used this month"
                break
            rows = api.leaderboard(window)
            stats["windows"][window] = len(rows)
            stats["new_users"] = stats.get("new_users", 0) + store_rows(
                conn, rows, f"fomoapi_{window}")
            for k, v in link_wallets(conn, rows).items():
                stats[k] = stats.get(k, 0) + v

        pages = settings.fomoapi_thesis_pages if thesis_pages is None else thesis_pages
        if pages and not afford(CREDITS["thesis"] * pages):
            stats["budget_stop"] = f"{spent + api.credits:.0f}/{cap} credits used this month"
            pages = 0
        if pages:
            stats["theses"] = store_theses(conn, api.theses(pages=pages))
    except OutOfCredits as e:
        # Not an error to retry into. Say it once, loudly, and keep whatever the pass already got.
        log.error("fomoapi: %s — the pass stops here until the month refills", e)
        stats["out_of_credits"] = True
    finally:
        stats["credits"] = api.credits
        stats["requests"] = api.requests
        stats["month_spent"] = round(spent + api.credits, 1)
    if stats.get("budget_stop"):
        log.warning("fomoapi: %s — skipping the rest of the pass", stats["budget_stop"])
    log.info("fomoapi collection: %s", stats)
    return stats
