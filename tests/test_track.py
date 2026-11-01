

def test_a_lost_roster_scan_is_one_warning_not_one_per_wallet(tmp_path, caplog):
    """Three lost scans wrote 1,596 lines; the fact is one line and a count."""
    import logging
    from fomo_agent import db
    from fomo_agent.pipeline import track

    conn = db.connect(tmp_path / "t.db")
    with db.tx(conn):
        for i in range(5):
            db.upsert_trader(conn, "0x" + f"{i:040x}", chain="robinhood", status="active")

    class Broken:
        requests = 0

        def supports(self, chain):
            return True

        def get_trades(self, address, chain="robinhood", since_ts=None):
            raise RuntimeError("scan failed earlier this pass: rate limited after 4 attempts")

    with caplog.at_level(logging.WARNING):
        stats = track.track_all(conn, trackers=[Broken()])
    assert stats["errors"] == 5 and stats["skipped"] == 5
    lines = [r.message for r in caplog.records if "scan failed" in r.message or "skipped" in r.message]
    assert lines == ["track: 5 wallets skipped after the roster scan failed this pass"]


# --- idle is an observation state, and a first fill is the way out of it ------------------
# The flip lived inside `track_wallet` only, so it fired just when the scheduled pass itself
# inserted the fill. In normal operation the chain watcher stores a first fill one tick after it
# happens — and the wallet then stayed `idle` for good: still scanned, never in the scoring
# queue. On the live tape that was ten wallets and 44 fills, one of them $44.6k, none judged.


def _idle_wallet(conn, db, address, handle="quiet"):
    with db.tx(conn):
        db.upsert_trader(conn, address, chain="robinhood", fomo_handle=handle, status="idle")


def _fill(conn, db, address, sig="s1", usd=250.0):
    with db.tx(conn):
        db.insert_trade(conn, sig=sig, address=address, chain="robinhood", mint="0x" + "11" * 20,
                        side="buy", usd_value=usd, ts=db.now(), source="rpc", kind="trade")


def test_a_fill_stored_outside_the_pass_still_promotes_the_idle_wallet(tmp_path):
    from fomo_agent import db
    from fomo_agent.pipeline import track

    conn = db.connect(tmp_path / "idle.db")
    w = "0x" + "c1" * 20
    _idle_wallet(conn, db, w)
    _fill(conn, db, w)

    assert track.promote_idle(conn) == 1
    assert db.get_trader(conn, w)["status"] == "tracking"
    assert track.promote_idle(conn) == 0   # idempotent, not a repeated promotion


def test_an_idle_wallet_without_fills_stays_idle(tmp_path):
    """No fills on the tape is the definition of idle: it must not be dragged into judging."""
    from fomo_agent import db
    from fomo_agent.pipeline import track

    conn = db.connect(tmp_path / "still.db")
    w = "0x" + "c2" * 20
    _idle_wallet(conn, db, w)

    assert track.promote_idle(conn) == 0
    assert db.get_trader(conn, w)["status"] == "idle"


def test_dropped_is_a_verdict_and_is_not_promoted(tmp_path):
    """`dropped` is a judged verdict, not an observation state — a fill must not overwrite it."""
    from fomo_agent import db
    from fomo_agent.pipeline import track

    conn = db.connect(tmp_path / "dropped.db")
    w = "0x" + "c3" * 20
    with db.tx(conn):
        db.upsert_trader(conn, w, chain="robinhood", fomo_handle="botty", status="dropped")
    _fill(conn, db, w, sig="s3")

    assert track.promote_idle(conn) == 0
    assert db.get_trader(conn, w)["status"] == "dropped"
