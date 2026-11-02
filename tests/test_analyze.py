"""The two questions the CLI answers offline: what about this token, what about this trader."""
import json

import pytest

from fomo_agent import db
from fomo_agent.pipeline import analyze
from fomo_agent.pipeline.analyze import (analyze_token, analyze_trader, conviction, find_trader,
                                         format_token, format_trader)
from fomo_agent.sources.rpc import USDG

ACE = "0x" + "a" * 40      # scores 85
MID = "0x" + "b" * 40      # scores 62
DUD = "0x" + "c" * 40      # scores 30
TOKEN = "0x" + "d" * 40


@pytest.fixture()
def conn(tmp_path):
    c = db.connect(tmp_path / "analyze.db")
    now = db.now()
    with db.tx(c):
        for addr, handle, uid, score, status in ((ACE, "ace", "u1", 85, "active"),
                                                 (MID, "mid", "u2", 62, "watch"),
                                                 (DUD, "dud", "u3", 30, "dropped")):
            db.upsert_trader(c, addr, chain="robinhood", fomo_handle=handle, fomo_user_id=uid,
                             score=score, status=status, pnl_30d=1_000_000.0,
                             ai_summary=f"{handle} verdict", ai_model="claude-opus-5",
                             tags=json.dumps({"style": ["swing"], "red_flags": []}),
                             stats_json=json.dumps({"win_rate": 0.55, "fills": 40}))
        db.upsert_token(c, TOKEN, chain="robinhood", symbol="PONS", liquidity_usd=500_000,
                        mcap_usd=40_000_000)
        for tid, uid, pnl, cost in (("p1", "u1", 900_000.0, 30_000.0), ("p2", "u2", 40_000.0, 8_000.0)):
            c.execute("INSERT INTO fomo_positions(trade_id, user_id, token, chain, unrealized_pnl, "
                      "cost_basis, seen_at) VALUES(?,?,?,?,?,?,?)",
                      (tid, uid, TOKEN, "robinhood", pnl, cost, now))
        for i, (addr, side, usd, ago) in enumerate(((ACE, "buy", 5_000.0, 3600),
                                                    (MID, "buy", 2_000.0, 1800),
                                                    (DUD, "sell", 900.0, 600))):
            db.insert_trade(c, sig=f"0xtx{i}", address=addr, chain="robinhood", mint=TOKEN,
                            side=side, usd_value=usd, ts=now - ago, source="rpc")
    return c


def test_conviction_weighs_quality_over_headcount():
    """One trader scoring 85 outweighs a crowd of mediocre wallets."""
    assert conviction([85]) > conviction([40] * 4)
    assert conviction([]) == 0
    assert conviction([None, 0, 50]) == pytest.approx(0.25)


def test_token_report_reads_holders_and_flow(conn):
    a = analyze_token(conn, TOKEN, hours=48)
    assert a["symbol"] == "PONS" and not a["is_quote"]
    assert [h["handle"] for h in a["holders"]] == ["ace", "mid"], "best score first"
    assert a["trusted_holders"] == 2 and a["avg_score"] == pytest.approx(73.5)
    assert a["cohort_cost"] == 38_000 and a["cohort_pnl"] == 940_000
    assert a["bought_usd"] == 7_000 and a["sold_usd"] == 900
    assert a["trusted_buyers"] == 2, "the wallet scoring 30 does not count"


def test_token_report_flags_a_quote_asset(conn):
    a = analyze_token(conn, USDG)
    assert a["is_quote"]
    assert "quote asset" in format_token(a)


def test_token_report_survives_an_unknown_address(conn):
    a = analyze_token(conn, "0x" + "9" * 40)
    assert a["holders"] == [] and a["flow"] == [] and a["conviction"] == 0
    assert "nobody on the watchlist" in format_token(a)


def test_trader_lookup_takes_a_handle_or_an_address(conn):
    assert find_trader(conn, "ace")["address"] == ACE
    assert find_trader(conn, ACE.upper())["fomo_handle"] == "ace"
    assert find_trader(conn, "nobody") is None
    assert analyze_trader(conn, "nobody") is None


def test_trader_report_carries_the_verdict_and_the_book(conn):
    a = analyze_trader(conn, "ace", hours=48)
    assert a["score"] == 85 and a["status"] == "active"
    assert a["summary"] == "ace verdict"
    assert [p["sym"] for p in a["positions"]] == ["PONS"]
    assert a["open_pnl"] == 900_000
    assert a["bought_usd"] == 5_000 and a["sold_usd"] == 0
    assert [c["handle"] for c in a["company"]] == ["mid"], "shares the PONS position"

    text = format_trader(a)
    assert "ace" in text and "PONS" in text and "$900.0k" in text


def test_reports_render_without_scores_or_prices(conn):
    """Nothing here may crash on the half-filled rows that discovery produces."""
    with db.tx(conn):
        db.upsert_trader(conn, "0x" + "e" * 40, chain="robinhood", fomo_handle="fresh",
                         fomo_user_id="u4", status="candidate")
        db.insert_trade(conn, sig="0xtx9", address="0x" + "e" * 40, chain="robinhood", mint=TOKEN,
                        side="buy", usd_value=None, ts=db.now(), source="rpc")
    assert format_token(analyze_token(conn, TOKEN))
    assert format_trader(analyze_trader(conn, "fresh"))


# ---------------------------------------------------------------- bot heuristic

def ctx(trades, tokens, hold):
    return {"last_7d": {"trades": trades, "unique_tokens": tokens, "median_hold_min": hold}}


def test_bot_heuristic_needs_all_three_conditions():
    """Frequency alone is not a bot — the best early-entry traders here are also very fast."""
    from fomo_agent.pipeline.score import looks_automated

    # 600 trades confined to six tokens at a two-minute hold: inventory cycling
    assert looks_automated(ctx(600, 6, 2))
    # the same frequency spread over 100 tokens is a person hunting launches
    assert looks_automated(ctx(600, 100, 2)) is None
    # narrow and fast, but not frequent enough to be automated
    assert looks_automated(ctx(40, 4, 1)) is None
    # narrow and frequent, but held long enough for a thesis
    assert looks_automated(ctx(600, 6, 240)) is None
    # a half-filled context must never trip it
    assert looks_automated({}) is None
    assert looks_automated(ctx(600, 6, None)) is None
    assert looks_automated(ctx(600, 0, 1)) is None


def test_drop_automated_takes_the_bot_out_of_the_queue(conn):
    from fomo_agent import db as _db
    from fomo_agent.pipeline.score import drop_automated

    bot = "0x" + "f" * 40
    with _db.tx(conn):
        _db.upsert_trader(conn, bot, chain="robinhood", status="tracking")
        # 110 round trips over two tokens, each held a minute: high frequency, no breadth
        now = _db.now()
        for i in range(110):
            mint = TOKEN if i % 2 else "0x" + "e" * 40
            _db.insert_trade(conn, sig=f"0xbotb{i}", address=bot, chain="robinhood", mint=mint,
                             side="buy", usd_value=10.0, ts=now - 3600 - i * 600, source="rpc")
            _db.insert_trade(conn, sig=f"0xbots{i}", address=bot, chain="robinhood", mint=mint,
                             side="sell", usd_value=10.0, ts=now - 3540 - i * 600, source="rpc")
    rows = conn.execute("SELECT * FROM traders WHERE address IN (?, ?)", (bot, ACE)).fetchall()
    keep, dropped = drop_automated(conn, rows)

    assert dropped == 1 and [r["address"] for r in keep] == [ACE]
    row = _db.get_trader(conn, bot)
    assert row["status"] == "dropped" and row["ai_model"] == "heuristic:bot"
    assert "automated" in row["ai_summary"]


def test_a_fresh_token_still_answers_from_its_buyers(conn):
    """The bug this covers: a token nobody holds yet looked empty on the page.

    Positions come from fomo's snapshot of a trader's three biggest bags, so a token that has not
    grown into anyone's top three shows no holders — while trusted wallets are already buying it.
    Reading conviction only from holders made the feed and the token page disagree about the same
    token, one saying 13.3 and the other 0.0.
    """
    fresh = "0x" + "f" * 40
    with db.tx(conn):
        db.upsert_token(conn, fresh, chain="robinhood", symbol="CME", liquidity_usd=81_000)
        for i, (addr, side, usd_v) in enumerate(((ACE, "buy", 4_000.0), (ACE, "buy", 2_000.0),
                                                 (MID, "buy", 1_000.0), (MID, "sell", 500.0),
                                                 (DUD, "buy", 9_000.0))):
            db.insert_trade(conn, sig=f"0xfresh{i}", address=addr, chain="robinhood", mint=fresh,
                            side=side, usd_value=usd_v, ts=db.now() - 600, source="rpc")

    a = analyze_token(conn, fresh)
    assert a["holders"] == [], "nobody holds it yet, which is the whole point"
    assert a["conviction"] == 0, "holder conviction is genuinely zero"

    assert [b["handle"] for b in a["buyers"]] == ["ace", "mid", "dud"], "best score first"
    assert a["buyer_conviction"] == pytest.approx(0.85 ** 2 + 0.62 ** 2), "the wallet scoring 30 does not count"
    assert a["buyer_conviction"] > 0, "the page has something real to show"

    ace = a["buyers"][0]
    assert ace["bought"] == 6_000 and ace["sold"] == 0 and ace["fills"] == 2, "fills roll up per wallet"
    mid = a["buyers"][1]
    assert mid["bought"] == 1_000 and mid["sold"] == 500, "both sides are kept"


def test_buyer_conviction_matches_what_the_feed_ranks_by(conn):
    """One token, one number: the feed and the token page must not disagree."""
    from fomo_agent.pipeline.analyze import signals

    sig = next(s for s in signals(conn, "robinhood", hours=24) if s["sym"] == "PONS")
    tok = analyze_token(conn, TOKEN, hours=24)
    assert tok["buyer_conviction"] == pytest.approx(sig["conviction"])


# ---------------------------------------------------------------- the book

def test_position_state_reads_how_much_of_the_entry_is_left():
    """The four things a wallet's buys and sells can say about a position, and the one they cannot."""
    from fomo_agent.pipeline.analyze import position_state

    assert position_state(100, 0) == ("open", 0.0)
    state, exit_pct = position_state(100, 40)
    assert state == "trimmed" and exit_pct == pytest.approx(0.4)
    assert position_state(100, 99)[0] == "closed", "dust left behind is still a closed position"
    assert position_state(100, 100)[0] == "closed"
    assert position_state(0, 500)[0] == "pre-tape", "sold what we never saw bought"
    assert position_state(100, 300)[0] == "pre-tape"
    assert position_state(None, None)[0] == "unknown", "fills recorded without sizes"


def test_the_book_separates_what_is_held_from_what_came_back_out(conn):
    """A round trip, a trim and a position still running, all from one wallet's tape."""
    from fomo_agent.pipeline.analyze import book

    won, cut, run = ("0x" + "1" * 40), ("0x" + "2" * 40), ("0x" + "3" * 40)
    now = db.now()
    with db.tx(conn):
        for mint, sym, price in ((won, "WON", None), (cut, "CUT", 0.002), (run, "RUN", 0.5)):
            db.upsert_token(conn, mint, chain="robinhood", symbol=sym, price_usd=price,
                            price_at=now if price else None)
        rows = (
            (won, "buy", 1_000.0, 1_000_000.0), (won, "sell", 4_000.0, 1_000_000.0),   # sold out
            (cut, "buy", 2_000.0, 1_000_000.0), (cut, "sell", 1_500.0, 250_000.0),     # quarter out
            (run, "buy", 500.0, 1_000.0),                                              # untouched
        )
        for i, (mint, side, usd_v, amt) in enumerate(rows):
            db.insert_trade(conn, sig=f"0xbook{i}", address=ACE, chain="robinhood", mint=mint,
                            side=side, usd_value=usd_v, token_amount=amt, ts=now - 900,
                            source="rpc")

    b = book(conn, ACE, "u1")
    held = {p["sym"]: p for p in b["positions"]}
    assert "WON" not in held, "a position sold out entirely is not still held"
    assert held["CUT"]["state"] == "trimmed" and held["RUN"]["state"] == "open"
    # three quarters of a $2k entry left, priced at 750k tokens x $0.002
    assert held["CUT"]["cost"] == pytest.approx(1_500) and held["CUT"]["value"] == pytest.approx(1_500)
    assert held["RUN"]["value"] == pytest.approx(500), "1000 tokens at 50c"

    out = {p["sym"]: p for p in b["closed"]}
    assert set(out) == {"WON", "CUT"}, "a trim belongs here too, for the part that left"
    assert out["WON"]["realized"] == pytest.approx(3_000), "out less in, sold to nothing"
    assert out["CUT"]["realized"] == pytest.approx(1_000), "out less the quarter it cost"
    assert b["closed"][0]["sym"] == "WON", "ranked by what came back out"
    assert b["round_trips"] == 1 and b["wins"] == 1, "only the position sold out entirely is decided"


def test_a_position_older_than_the_tape_is_reported_as_neither(conn):
    """Selling what we never saw bought cannot be priced, so it must not become a windfall."""
    from fomo_agent.pipeline.analyze import book

    old = "0x" + "4" * 40
    with db.tx(conn):
        db.upsert_token(conn, old, chain="robinhood", symbol="OLD")
        db.insert_trade(conn, sig="0xold", address=MID, chain="robinhood", mint=old, side="sell",
                        usd_value=90_000.0, token_amount=5_000.0, ts=db.now() - 300, source="rpc")

    b = book(conn, MID, "u2")
    assert "OLD" not in {p["sym"] for p in b["positions"]}
    assert "OLD" not in {p["sym"] for p in b["closed"]}, "$90k of profit we cannot claim"
    assert b["pre_tape"] == 1, "and the reader is told it was left out"


def test_the_book_keeps_fomo_marks_and_the_quote_asset_out(conn):
    """fomo prices a whole position; the tape only prices what it watched. USDG is neither."""
    from fomo_agent.pipeline.analyze import book

    with db.tx(conn):
        db.upsert_token(conn, USDG, chain="robinhood", symbol="USDG", price_usd=1.0)
        db.insert_trade(conn, sig="0xusdg", address=ACE, chain="robinhood", mint=USDG, side="buy",
                        usd_value=50_000.0, token_amount=50_000.0, ts=db.now() - 60, source="rpc")

    b = book(conn, ACE, "u1")
    assert "USDG" not in {p["sym"] for p in b["positions"]}, "holding a stablecoin is holding cash"
    pons = next(p for p in b["positions"] if p["sym"] == "PONS")
    assert pons["src"] == "fomo" and pons["pnl"] == 900_000, "fomo's mark covers the whole position"


def test_the_chain_balance_outranks_what_the_tape_watched(conn):
    """What a wallet holds is a fact; what we saw it buy is a window onto one."""
    from fomo_agent.pipeline.analyze import book, position_state

    # the chain settles the three cases the tape argues about
    assert position_state(100, 40, balance=0)[0] == "closed", "nothing left, whatever we watched"
    assert position_state(100, 40, balance=60)[0] == "trimmed"
    assert position_state(100, 0, balance=100)[0] == "open"
    assert position_state(100, 0, balance=5_000)[0] == "held", "holds what it bought before us"
    assert position_state(None, None, balance=42)[0] == "held", "sizeless fills, real balance"

    old, sold = ("0x" + "7" * 40), ("0x" + "8" * 40)
    now = db.now()
    with db.tx(conn):
        db.upsert_token(conn, old, chain="robinhood", symbol="OLD", price_usd=2.0, price_at=now)
        db.upsert_token(conn, sold, chain="robinhood", symbol="SOLD", price_usd=1.0, price_at=now)
        db.insert_trade(conn, sig="0xold1", address=ACE, chain="robinhood", mint=old, side="buy",
                        usd_value=1_000.0, token_amount=100.0, ts=now - 900, source="rpc")
        db.insert_trade(conn, sig="0xsold1", address=ACE, chain="robinhood", mint=sold, side="buy",
                        usd_value=300.0, token_amount=300.0, ts=now - 900, source="rpc")
        db.insert_trade(conn, sig="0xsold2", address=ACE, chain="robinhood", mint=sold, side="sell",
                        usd_value=900.0, token_amount=300.0, ts=now - 300, source="rpc")
        # it holds ten times what we watched it buy, and nothing at all of the other
        db.save_holdings(conn, {(ACE, old): 1_000.0, (ACE, sold): 0.0})

    b = book(conn, ACE, None)
    held = next(p for p in b["positions"] if p["sym"] == "OLD")
    assert held["state"] == "held" and held["held"] == 1_000
    assert held["value"] == pytest.approx(2_000), "priced on what it holds, not on what we saw"
    assert held["pnl"] is None, "the entry predates us, so the profit is not ours to state"

    assert "SOLD" not in {p["sym"] for p in b["positions"]}, "the chain says it is gone"
    out = next(p for p in b["closed"] if p["sym"] == "SOLD")
    assert out["realized"] == pytest.approx(600), "and the round trip is scored"


def test_a_token_lists_the_wallets_whose_balance_says_they_hold_it(conn):
    """fomo publishes three bags per trader; a balance has no such limit."""
    mint = "0x" + "9" * 40
    now = db.now()
    with db.tx(conn):
        db.upsert_token(conn, mint, chain="robinhood", symbol="HOLD", price_usd=0.5, price_at=now)
        # ace holds it and fomo does not carry the position; mid held it and sold out
        db.save_holdings(conn, {(ACE, mint): 1_000.0, (MID, mint): 0.0})

    a = analyze_token(conn, mint)
    assert [h["handle"] for h in a["holders"]] == ["ace"], "a zero balance is not a holder"
    assert a["holders"][0]["value"] == pytest.approx(500), "1000 tokens at 50c"
    assert a["cohort_value"] == pytest.approx(500)
    assert a["conviction"] == pytest.approx(0.85 ** 2), "holder conviction is real now"
    assert a["holders"][0]["pnl"] is None, "no fomo mark, so no profit claimed"


# ---------------------------------------------------------------- fresh launches

def test_earliness_decays_from_the_launch():
    """Full weight at the pool opening, half an hour later, almost nothing the next day."""
    from fomo_agent.pipeline.analyze import earliness

    t0 = 1_700_000_000
    assert earliness(t0, t0) == 1.0
    assert earliness(t0 + 3600, t0) == pytest.approx(0.5)
    assert earliness(t0 + 36000, t0) == pytest.approx(1 / 11)
    assert earliness(t0 - 60, t0) == 1.0, "a buy before the launch is as early as it gets"

    # This used to return 1.0, on the principle that a gap in our data must not punish a wallet.
    # The principle is right and the consequence was not: in a ranked feed, scoring an undated
    # token as if it were bought at the pool opening does not spare the wallet, it corrupts the
    # order. Measured live, eight of the top ten launches showed "?" and outranked tokens with
    # real entries of one and ten minutes. Undated now ranks where an hour-old entry ranks.
    assert earliness(t0, None) == 0.5, "an undated token must not outrank a measured one"
    assert earliness(t0, None) == earliness(t0 + 3600, t0), "worth exactly an hour-old entry"
    assert earliness(t0 + 600, t0) > earliness(t0, None), "ten minutes measured beats unknown"


def test_heat_ranks_the_early_wallet_over_the_late_one():
    """The same buy an hour later is a different decision, and heat says so."""
    from fomo_agent.pipeline.analyze import conviction, heat

    t0 = 1_700_000_000
    early = [{"score": 80, "ts": t0 + 120}, {"score": 80, "ts": t0 + 300}]
    late = [{"score": 80, "ts": t0 + 7200}, {"score": 80, "ts": t0 + 9000}]
    assert conviction([80, 80]) == pytest.approx(1.28), "conviction cannot tell them apart"
    assert heat(early, t0) > heat(late, t0) * 2
    # An undated launch is discounted rather than waved through, so it cannot beat the token whose
    # buyers we actually watched arrive early.
    assert heat(early, None) == pytest.approx(conviction([80, 80]) * 0.5)
    assert heat(early, t0) > heat(early, None), "measured and early beats undated"


def test_fresh_lists_only_what_the_cohort_has_just_started_buying(conn):
    """A name the cohort has held for a week is a signal, not a launch."""
    from fomo_agent.pipeline.analyze import fresh

    now = db.now()
    new, old, thin = ("0x" + c * 40 for c in "abc")
    with db.tx(conn):
        db.upsert_token(conn, new, chain="robinhood", symbol="NEW", liquidity_usd=90_000,
                        created_at=now - 3600)
        db.upsert_token(conn, old, chain="robinhood", symbol="OLD", liquidity_usd=90_000,
                        created_at=now - 3600)
        db.upsert_token(conn, thin, chain="robinhood", symbol="THIN", liquidity_usd=29,
                        created_at=now - 3600)
        rows = [
            (ACE, new, now - 1800), (MID, new, now - 1500),
            (ACE, thin, now - 1800), (MID, thin, now - 1500),
            # the cohort was already in OLD three days ago, so today's buy is not an entry
            (ACE, old, now - 3 * 86400), (ACE, old, now - 900), (MID, old, now - 800),
        ]
        for i, (addr, mint, ts) in enumerate(rows):
            db.insert_trade(conn, sig=f"0xfresh{i}", address=addr, chain="robinhood", mint=mint,
                            side="buy", usd_value=1_000.0, ts=ts, source="rpc")

    f = fresh(conn, "robinhood", hours=24)
    listed = [t["sym"] for t in f["tokens"]]
    assert "NEW" in listed
    assert "OLD" not in listed, "the cohort was already in it, so today's buy is not an entry"
    assert "THIN" not in listed, "nothing left in the pool"
    assert f["drained"] == 1, "the pool with $29 left is counted, not silently dropped"

    t = next(x for x in f["tokens"] if x["sym"] == "NEW")
    assert t["buyers"] == 2 and t["heat"] > 0
    assert t["lead_minutes"] == pytest.approx(30, abs=1), "half an hour after the pool opened"
    assert [e["handle"] for e in t["entries"]] == ["ace", "mid"], "earliest buyer first"

    loose = fresh(conn, "robinhood", hours=24, min_liquidity=0)
    assert loose["drained"] == 0 and "THIN" in [x["sym"] for x in loose["tokens"]], \
        "liquidity only filters; it never reorders"
    young = [x["sym"] for x in fresh(conn, "robinhood", hours=24, max_age_h=0)["tokens"]]
    assert "NEW" not in young, "an hour old is too old when the cap is zero"
    assert fresh(conn, "robinhood", hours=24, min_buyers=3)["tokens"] == []


# ---------------------------------------------------------------- health

def test_a_moved_router_is_told_apart_from_a_quiet_market(conn):
    """No fills is ambiguous. Transfers with no fills is not."""
    from fomo_agent.pipeline.health import router_alive

    class Chain:
        def __init__(self, moved):
            self.moved = moved

        def block_number(self):
            return 1_000_000

        def transfers(self, wallets, first, last, outgoing):
            return self.moved

    # the fixture's wallets traded an hour ago, so the tape speaks for itself
    assert router_alive(conn, Chain([]))["ok"]

    conn.execute("DELETE FROM trades")
    quiet = router_alive(conn, Chain([]))
    assert quiet["ok"] and "still" in quiet["detail"], "a quiet cohort is not a broken router"

    moved = router_alive(conn, Chain([{"tx": "0x1"}, {"tx": "0x2"}]))
    assert not moved["ok"]
    assert "RPC_ROUTERS" in moved["detail"], "and the message says which setting to look at"

    class Broken(Chain):
        def block_number(self):
            raise RuntimeError("endpoint down")

    assert router_alive(conn, Broken([]))["ok"], "a check that cannot run must not cry wolf"


def test_health_puts_the_failures_first(conn):
    from fomo_agent.pipeline.health import report

    r = report(conn, rpc=None)
    names = [c["name"] for c in r["checks"]]
    assert "fomo collection" in names and "on-chain tape" in names
    oks = [c["ok"] for c in r["checks"]]
    assert oks == sorted(oks), "worst first, so the first line is the one that matters"
    assert r["failing"] == sum(1 for c in r["checks"] if not c["ok"])


# ---------------------------------------------------------------- exits


@pytest.fixture()
def leaving(tmp_path):
    """One token, four wallets, four different ways of not being in it any more."""
    c = db.connect(tmp_path / "exits.db")
    now = db.now()
    LEFT, TRIM, PRE, LOW = ("0x" + x * 40 for x in "abcd")
    with db.tx(c):
        db.upsert_token(c, TOKEN, chain="robinhood", symbol="PONS", liquidity_usd=500_000)
        for addr, handle, score in ((LEFT, "left", 88), (TRIM, "trim", 74),
                                    (PRE, "pre", 80), (LOW, "low", 30)):
            db.upsert_trader(c, addr, chain="robinhood", fomo_handle=handle, score=score,
                             status="active")
        rows = [
            # sold all but a dust remainder of what we watched it buy: an exit (CLOSED_AT is 0.98)
            (LEFT, "buy", 10_000.0, 1000.0, 7200), (LEFT, "sell", 26_000.0, 990.0, 900),
            # shaved a tenth off a winner: portfolio management, not an exit
            (TRIM, "buy", 10_000.0, 1000.0, 7200), (TRIM, "sell", 3_000.0, 100.0, 900),
            # sold more than the tape ever saw it buy: it was in before we were, size unknowable
            (PRE, "buy", 500.0, 50.0, 7200), (PRE, "sell", 40_000.0, 900.0, 900),
            # left too, but nobody is copying a wallet scoring 30
            (LOW, "buy", 10_000.0, 1000.0, 7200), (LOW, "sell", 20_000.0, 950.0, 900),
        ]
        for i, (addr, side, usd, amt, ago) in enumerate(rows):
            db.insert_trade(c, sig=f"0xex{i}", address=addr, chain="robinhood", mint=TOKEN,
                            side=side, usd_value=usd, token_amount=amt, ts=now - ago, source="rpc")
    return c, {"left": LEFT, "trim": TRIM, "pre": PRE, "low": LOW}


def test_a_trim_is_not_an_exit(leaving):
    c, w = leaving
    # on its own, one departure is not a signal
    assert analyze.exits(c, hours=6, min_sellers=2) == []
    out = analyze.exits(c, hours=6, min_sellers=1)
    assert len(out) == 1
    t = out[0]
    assert t["sym"] == "PONS"
    assert t["who"] == ["left"], "the trim, the pre-tape wallet and the 30 are all excluded"
    assert t["sellers"] == 1 and t["gone"] == 1
    assert t["conviction"] == pytest.approx(0.7744)


def test_exit_needs_the_position_to_be_mostly_gone(leaving):
    c, w = leaving
    # drop the bar low enough and the trim counts, which is exactly what min_exit is for
    out = analyze.exits(c, hours=6, min_sellers=1, min_exit=0.05)
    assert sorted(out[0]["who"]) == ["left", "trim"]
    assert out[0]["gone"] == 1, "only one of them is actually out"


def test_a_sale_outside_the_window_is_not_news(leaving):
    c, _ = leaving
    assert analyze.exits(c, hours=0, min_sellers=1) == []


def test_the_balance_settles_it(tmp_path):
    """The tape says trimmed, the chain says empty. The chain wins."""
    c = db.connect(tmp_path / "bal.db")
    now = db.now()
    addr = "0x" + "e" * 40
    with db.tx(c):
        db.upsert_token(c, TOKEN, chain="robinhood", symbol="PONS")
        db.upsert_trader(c, addr, chain="robinhood", fomo_handle="empty", score=90, status="active")
        db.insert_trade(c, sig="0xb1", address=addr, chain="robinhood", mint=TOKEN, side="buy",
                        usd_value=10_000.0, token_amount=1000.0, ts=now - 7200, source="rpc")
        db.insert_trade(c, sig="0xb2", address=addr, chain="robinhood", mint=TOKEN, side="sell",
                        usd_value=9_000.0, token_amount=600.0, ts=now - 600, source="rpc")
        c.execute("INSERT INTO holdings(address, token, amount, ts) VALUES(?,?,?,?)",
                  (addr, TOKEN, 0.0, now))
    out = analyze.exits(c, hours=6, min_sellers=1)
    assert out and out[0]["gone"] == 1, "a zero balance is closed however partial the tape looks"


def test_an_empty_delivery_is_not_a_collection(tmp_path):
    """The extension posts whatever it managed to fetch, which can be nothing at all.

    A signed-out browser, an expired bearer or a broken collect() all still write a run row, and
    the health check used to read that as a healthy collection — the exact silent failure the
    check exists to catch.
    """
    from fomo_agent.pipeline.health import checks

    c = db.connect(tmp_path / "h.db")
    now = db.now()
    with db.tx(c):
        rid = db.run_start(c, "fomo_ingest")
        c.execute("UPDATE runs SET finished_at=?, stats_json=? WHERE id=?",
                  (now - 60, '{"periods": {}, "new_users": 0}', rid))
    got = {k["name"]: k for k in checks(c, rpc=None)}
    assert got["fomo collection"]["ok"] is False, "a delivery carrying no leaderboard proves nothing"

    with db.tx(c):
        rid = db.run_start(c, "fomo_ingest")
        c.execute("UPDATE runs SET finished_at=?, stats_json=? WHERE id=?",
                  (now - 60, '{"periods": {"24h": 150}, "new_users": 3}', rid))
    got = {k["name"]: k for k in checks(c, rpc=None)}
    assert got["fomo collection"]["ok"] is True


def test_a_split_collect_step_still_reads_as_a_fresh_collection(tmp_path):
    """The one `fomoapi` run step became three per-cadence steps, and the check kept querying the
    old names — so it froze at the last row written under them and would have gone red while the
    collector was ticking happily."""
    from fomo_agent.pipeline.health import checks

    c = db.connect(tmp_path / "h.db")
    now = db.now()
    with db.tx(c):
        rid = db.run_start(c, "fomoapi_24h")
        c.execute("UPDATE runs SET finished_at=?, stats_json=? WHERE id=?",
                  (now - 600, '{"windows": {"24h": 150}, "credits": 6.0}', rid))
    got = {k["name"]: k for k in checks(c, rpc=None)}
    assert got["fomo collection"]["ok"] is True, got["fomo collection"]["detail"]


def test_the_heartbeat_goes_quiet_when_something_is_broken(monkeypatch):
    """Silence is the alarm, so a failing pipeline must stop pinging rather than ping differently."""
    from fomo_agent.pipeline import health

    calls = []

    class FakeClient:
        def __enter__(self): return self
        def __exit__(self, *a): return False
        def get(self, url):
            calls.append(url)
            return type("R", (), {"status_code": 200})()

    monkeypatch.setattr(health.httpx, "Client", lambda **kw: FakeClient())
    assert "pinged ok" in health.heartbeat(True, url="https://hc.example/abc")
    assert calls == ["https://hc.example/abc"]

    assert "pinged fail" in health.heartbeat(False, url="https://hc.example/abc")
    assert calls[-1] == "https://hc.example/abc/fail"

    # nobody configured: say so rather than pretending to have pinged
    assert "nothing is watching" in health.heartbeat(True, url="")


def test_a_broken_monitor_never_breaks_the_pipeline(monkeypatch):
    from fomo_agent.pipeline import health

    class Boom:
        def __enter__(self): raise OSError("dns is gone")
        def __exit__(self, *a): return False

    monkeypatch.setattr(health.httpx, "Client", lambda **kw: Boom())
    assert "unreachable" in health.heartbeat(True, url="https://hc.example/abc")
