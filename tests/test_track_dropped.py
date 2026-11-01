

def _seeded(tmp_path, statuses):
    from fomo_agent import db
    conn = db.connect(tmp_path / "t2.db")
    with db.tx(conn):
        for i, status in enumerate(statuses):
            db.upsert_trader(conn, "0x" + f"{i:040x}", chain="robinhood",
                             status=status, score=50)
    return conn


def test_a_dropped_wallet_is_scanned_but_never_ahead_of_a_judged_one(tmp_path):
    """Dropped wallets are read for their fills (6 of 7 fills on 2026-11-01 came from that
    group), but widening the scan must never cost a tracked wallet its tick."""
    from fomo_agent.pipeline import track

    assert "dropped" in track.TRACKED_SCAN
    assert "dropped" not in track.TRACKED, "holdings/backfill/roster keep the narrow list"

    conn = _seeded(tmp_path, ["active"] * 3 + ["dropped"] * 9)
    seen: list[str] = []

    class Recorder:
        def supports(self, chain):
            return True

        def get_trades(self, address, chain="robinhood", since_ts=None):
            seen.append(address)
            return []

    track.track_all(conn, trackers=[Recorder()], limit=5)
    statuses = {r["address"]: r["status"]
                for r in conn.execute("SELECT address, status FROM traders")}
    scanned = [statuses[a] for a in seen]
    assert scanned[:3] == ["active", "active", "active"], "the roster goes first"
    assert "dropped" in scanned, "and the rest of the budget reads the dropped ones"
