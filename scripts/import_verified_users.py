"""Einmal-Import: die besten fomoapi-verifizierten User ins Trader-Roster.

Warum: `fomo_users` traegt seit dem FOMOAPI_KEY 236 User mit Adressen, die fomo selbst
bestaetigt hat ("verified by fomoapi") - im Gegensatz zu den bisherigen Naeherungen, die per
Minuten-Uebereinstimmung geraten wurden. Sie landen nirgends automatisch im Roster.

Deckel: Top N nach 24h-Volumen, Status `watch`, score bleibt leer -> sie laufen durch die
normale Scoring-Queue und werden erst danach bewertet. Kein Status eines bestehenden Traders
wird angefasst.
"""
from __future__ import annotations

import sys

sys.path.insert(0, r"O:/Werkstatt/fomo-robinhood-radar")
from fomo_agent import db

TOP_N = 30
CHAIN = "robinhood"


def main() -> None:
    conn = db.connect()
    conn.text_factory = lambda b: b.decode("utf-8", "replace")
    rows = conn.execute(
        "SELECT u.handle, u.onchain_address addr, u.volume_usd, u.trades_cnt, u.pnl_7d "
        "FROM fomo_users u "
        "WHERE COALESCE(u.onchain_address,'') <> '' "
        "  AND u.volume_usd IS NOT NULL AND u.volume_usd > 0 "
        "  AND lower(u.onchain_address) LIKE '0x%' "
        "  AND NOT EXISTS (SELECT 1 FROM traders t WHERE lower(t.address) = lower(u.onchain_address)) "
        "ORDER BY u.volume_usd DESC LIMIT ?", (TOP_N,)).fetchall()

    added, skipped = 0, 0
    for r in rows:
        addr = (r["addr"] or "").strip().lower()
        if len(addr) != 42:
            skipped += 1
            continue
        with db.tx(conn):
            fresh = db.upsert_trader(
                conn, addr,
                chain=CHAIN,
                fomo_handle=r["handle"],
                source="fomoapi_verified",
                status="watch",
                trades_cnt=r["trades_cnt"],
                pnl_7d=r["pnl_7d"],
            )
        added += int(bool(fresh))
    total = conn.execute("SELECT COUNT(*) FROM traders").fetchone()[0]
    by_status = dict(conn.execute(
        "SELECT status, COUNT(*) FROM traders GROUP BY status").fetchall())
    print({"kandidaten": len(rows), "neu": added, "uebersprungen": skipped,
           "trader_gesamt": total, "by_status": by_status})


if __name__ == "__main__":
    main()
