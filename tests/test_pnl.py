"""The PnL that may be quoted: what the cohort could take out, and what is only paper.

The rule (Max, 2026-11-01): the official number is the realizable one. A mark nobody can sell into
is a footnote, never a headline — PEAT/OYSTERS/TENDIES carried +$4.1k of paper profit for two days
while `sell-check` said the transfer to the router could not clear.
"""
from __future__ import annotations

from fomo_agent import db
from fomo_agent.pipeline import analyze
from fomo_agent.pipeline.report import build_report

WALLET = "0x" + "a" * 40
SELLABLE = "0x" + "1" * 40
TRAP = "0x" + "2" * 40
UNMARKED = "0x" + "3" * 40
UNCHECKED = "0x" + "4" * 40


def seed(conn, now):
    with db.tx(conn):
        db.upsert_trader(conn, WALLET, chain="robinhood", fomo_handle="w", score=70, status="watch")
        # a market: 1,000 tokens bought for $1,000, marked at $2 = +$1,000 realizable
        db.upsert_token(conn, SELLABLE, chain="robinhood", symbol="REAL", price_usd=2.0, sellable=1)
        db.insert_trade(conn, sig="a", address=WALLET, chain="robinhood", mint=SELLABLE,
                        side="buy", usd_value=1000.0, token_amount=1000.0,
                        ts=now - 3600, source="rpc")
        # an indexer echo with an anti-whale cap: 100 tokens for $500, marked at $50 = +$4,500 paper
        db.upsert_token(conn, TRAP, chain="robinhood", symbol="PAPER", price_usd=50.0, sellable=0)
        db.insert_trade(conn, sig="b", address=WALLET, chain="robinhood", mint=TRAP,
                        side="buy", usd_value=500.0, token_amount=100.0,
                        ts=now - 7200, source="rpc")
        # no price at all: worth nothing we can prove
        db.upsert_token(conn, UNMARKED, chain="robinhood", symbol="NOMARK")
        db.insert_trade(conn, sig="c", address=WALLET, chain="robinhood", mint=UNMARKED,
                        side="buy", usd_value=200.0, token_amount=200.0,
                        ts=now - 7200, source="rpc")
        # marked, but nobody has run sell-check on it: +$600 that must not enter the PnL
        db.upsert_token(conn, UNCHECKED, chain="robinhood", symbol="NOCK", price_usd=4.0)
        db.insert_trade(conn, sig="d", address=WALLET, chain="robinhood", mint=UNCHECKED,
                        side="buy", usd_value=200.0, token_amount=200.0,
                        ts=now - 7200, source="rpc")


def test_the_official_number_is_the_realizable_one(tmp_path):
    conn = db.connect(tmp_path / "pnl.db")
    now = db.now()
    seed(conn, now)
    p = analyze.cohort_pnl(conn, hours=72, now=now)
    assert p["realizable"]["pnl"] == 1000.0
    assert p["realizable"]["cost"] == 1000.0
    assert p["realizable"]["positions"] == 1
    assert p["paper"]["pnl"] == 4500.0, "the trap mark is counted, and counted apart"
    assert p["paper"]["cost"] == 700.0, "both paper positions, at what they cost"
    assert p["paper"]["positions"] == 2, "the unsellable one and the one nobody can price"
    assert p["unchecked"]["pnl"] == 600.0, "a mark without a sell-check is not money either"
    assert p["pnl_usd"] == 1000.0, "the headline never adds the paper or the unchecked"


def test_each_position_says_why_it_is_paper(tmp_path):
    conn = db.connect(tmp_path / "pnl.db")
    now = db.now()
    seed(conn, now)
    p = analyze.cohort_pnl(conn, hours=72, now=now)
    why = {r["sym"]: (r["kind"], r["why"]) for r in p["positions"]}
    assert why["REAL"] == ("realizable", None)
    assert why["PAPER"] == ("paper", "unsellable")
    assert why["NOMARK"] == ("paper", "no mark")
    assert why["NOCK"] == ("unchecked", "not checked")
    assert p["positions"][0]["kind"] == "realizable", "realizable first, whatever its size"


def test_the_report_leads_with_the_realizable_figure_and_marks_the_paper(tmp_path):
    conn = db.connect(tmp_path / "pnl.db")
    now = db.now()
    seed(conn, now)
    md = build_report(conn)
    pnl = md.index("## PnL")
    real = md.index("realizable")
    unchecked = md.index("not counted")
    paper = md.index("paper, not PnL")
    assert pnl < real < unchecked < paper, "realizable first, every other figure after it"
    assert "$1.0k realizable" in md and "$4.5k" in md and "$600" in md
    assert "never the headline" in md


def test_a_book_with_nothing_open_says_so_instead_of_zero(tmp_path):
    conn = db.connect(tmp_path / "pnl.db")
    p = analyze.cohort_pnl(conn, hours=72)
    assert p["positions"] == [] and p["pnl_usd"] == 0.0
    assert "no open positions" in build_report(conn)


def test_only_wallets_with_a_real_fill_in_the_window_are_counted(tmp_path):
    """A dust transfer is not an entry, and a position opened before the window is not this PnL."""
    conn = db.connect(tmp_path / "pnl.db")
    now = db.now()
    seed(conn, now)
    old = analyze.cohort_pnl(conn, hours=1, now=now + 4 * 3600)
    assert old["positions"] == []
    p = analyze.cohort_pnl(conn, hours=72, now=now + 4 * 3600)
    assert p["realizable"]["pnl"] == 1000.0
