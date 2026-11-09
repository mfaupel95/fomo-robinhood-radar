"""Operational features retained on the merged fork baseline; fixture-only."""
import ast
import runpy
from pathlib import Path
from types import SimpleNamespace

import pytest
from pydantic import ValidationError

from fomo_agent import db
from fomo_agent.models import ScoreResult, Trade
from fomo_agent.pipeline import holdings, track, watch

W = "0x" + "a1" * 20
M = "0x" + "b2" * 20


def seed(tmp_path, status="idle", age=0, chain="robinhood"):
    conn = db.connect(tmp_path / "fixture.db")
    with db.tx(conn):
        db.upsert_trader(conn, W, chain=chain, status=status)
        db.insert_trade(conn, sig="stored-by-other-writer", address=W, chain=chain,
                        mint=M, side="buy", usd_value=100, ts=db.now() - age,
                        source="rpc", kind="trade")
    return conn


def test_advisory_tags_do_not_discard_verdict():
    result = ScoreResult(score=15, status="dropped", confidence=.6, summary="fixture",
                         style=["swing", "ghost", " HOLDER "], red_flags=["idle", "bot", 3])
    assert result.style == ["swing", "holder"]
    assert result.red_flags == ["bot"]
    assert result.status == "dropped"


@pytest.mark.parametrize("field,value", [("score", 101), ("confidence", 2), ("status", "invented")])
def test_verdict_fields_stay_strict(field, value):
    data = dict(score=15, status="dropped", confidence=.6, summary="fixture")
    data[field] = value
    with pytest.raises(ValidationError):
        ScoreResult(**data)


def test_external_fill_promoted_by_track_all(tmp_path):
    conn = seed(tmp_path)
    class Empty:
        def supports(self, chain): return True
        def get_trades(self, address, chain="robinhood", since_ts=None): return []
    result = track.track_all(conn, trackers=[Empty()])
    assert result["promoted_idle"] == 1
    assert db.get_trader(conn, W)["status"] == "tracking"
    assert track.promote_idle(conn) == 0


def test_watcher_fill_promotes_idle_in_same_tick(tmp_path, monkeypatch):
    conn = db.connect(tmp_path / "watch.db")
    with db.tx(conn):
        db.upsert_trader(conn, W, chain="robinhood", status="idle")
    fill = Trade(sig="watch-fill", address=W, chain="robinhood", mint=M,
                 side="buy", usd_value=100, ts=db.now(), source="rpc", kind="trade")
    class RPC:
        def head(self): return 1000, db.now()
        def load_decimals(self, values): pass
        def known_decimals(self): return {}
        def scan(self, wallets, first, last): return {W: [fill]}
    monkeypatch.setattr(watch, "hot_now", lambda *a, **k: [])
    monkeypatch.setattr(watch, "tell_followers", lambda *a, **k: 0)
    monkeypatch.setattr(watch.noise, "sweep", lambda *a, **k: [])
    monkeypatch.setattr(watch.pro.Cursor, "advance", lambda *a, **k: [])
    stats = watch.tick(conn, watch.Watch(rpc=RPC()))
    assert stats["fills"] == stats["promoted_idle"] == 1
    assert db.get_trader(conn, W)["status"] == "tracking"


@pytest.mark.parametrize("status,age,chain,expected", [
    ("dropped", 7 * 86400, "robinhood", True),
    ("dropped", 7 * 86400 + 1, "robinhood", False),
    ("active", 30 * 86400, "robinhood", True),
    ("dropped", 0, "solana", False),
])
def test_holdings_recent_dropped_boundary(tmp_path, monkeypatch, status, age, chain, expected):
    monkeypatch.setattr(db, "now", lambda: 2_000_000_000)
    conn = seed(tmp_path, status, age, chain)
    assert ((W, M) in holdings.stale_pairs(conn)) is expected
    if status == "dropped":
        assert track.promote_idle(conn) == 0


def test_dropped_scan_cannot_displace_core_roster(tmp_path):
    conn = seed(tmp_path, "dropped")
    core = "0x" + "c3" * 20
    with db.tx(conn):
        db.upsert_trader(conn, core, chain="robinhood", status="active")
    seen = []
    class Recorder:
        def supports(self, chain): return True
        def get_trades(self, address, chain="robinhood", since_ts=None):
            seen.append(address)
            return []
    track.track_all(conn, trackers=[Recorder()], limit=1)
    assert seen == [core]
    seen.clear()
    track.track_all(conn, trackers=[Recorder()], limit=2)
    assert seen == [core, W]
    assert "dropped" not in track.TRACKED
    assert W not in watch.roster(conn)


def test_config_blank_dotenv_restores_existing_environment(monkeypatch):
    import dotenv
    monkeypatch.setenv("FOMO_CONFIG_FIXTURE", "existing")
    monkeypatch.setattr(dotenv, "find_dotenv", lambda **kw: "fixture-only")
    def fake_load(*args, **kwargs):
        monkeypatch.setenv("FOMO_CONFIG_FIXTURE", "")
    monkeypatch.setattr(dotenv, "load_dotenv", fake_load)
    scope = runpy.run_path(str(Path(__file__).parents[1] / "fomo_agent/config.py"))
    assert scope["os"].environ["FOMO_CONFIG_FIXTURE"] == "existing"


def test_cli_split_steps_execute_correct_collection_contract(monkeypatch):
    # Execute only the steps expression, never run the real CLI or another source.
    import fomo_agent.cli as cli
    from fomo_agent.pipeline import collect_api
    tree = ast.parse(Path(cli.__file__).read_text(encoding="utf-8"))
    fn = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "run")
    expr = next(n.value for n in fn.body if isinstance(n, ast.Assign)
                and any(isinstance(t, ast.Name) and t.id == "steps" for t in n.targets))
    split = ast.List(elts=[n for n in expr.elts if n.elts[0].value.startswith("fomoapi_")], ctx=ast.Load())
    calls = []
    monkeypatch.setattr(collect_api, "collect", lambda c, windows, theses: calls.append((windows, theses)))
    scope = {"settings": SimpleNamespace(fomoapi_key="fixture-only")}
    steps = eval(compile(ast.fix_missing_locations(ast.Expression(split)), "fixture-steps", "eval"), scope)
    assert [(name, interval) for name, interval, _ in steps] == [
        ("fomoapi_24h", 7200), ("fomoapi_7d", 21600), ("fomoapi_theses", 28800)]
    for _, _, action in steps:
        action(None)
    assert calls == [(("24h",), None), (("7d",), None), ((), 1)]
