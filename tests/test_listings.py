"""The second signal class: a pool with real money in it and no cohort.

The three cases are the measured ones from 2026-11-01, which is what this rule exists for: PONS
and the two "Claude" mints ran past every feed because the burst rule asks whose money arrived and
nobody on the roster had bought them.
"""
from __future__ import annotations

import pytest

from fomo_agent import db
from fomo_agent.config import settings
from fomo_agent.pipeline import listings
from fomo_agent.sources import dexscreener, geckoterminal

PONS = "0xbd7686c5d3d65e70bf94754d5f33139ace126dc3"
CLAUDE_A = "0xf83b5f2b4961c16d375a9252a771fe32d1e0388b"
CLAUDE_B = "0x0e9f220347ab7f2b0f4ba9b2e0dff20b50480b07"
OTHER = "0x" + "9" * 40
WALLET = "0x" + "a" * 40

# (mint, symbol, mcap, liquidity, 24h volume) as DexScreener answered on 2026-11-01 10:15 UTC
MEASURED = [
    (PONS, "PONS", 190_400_000, 66_400_000, 50_000_000),
    (CLAUDE_A, "Claude", 10_200_000, 10_250_000, 6_600_000),
    (CLAUDE_B, "Claude", 10_200_000, 10_270_000, 13_050_000),
]


def seed(conn, now, rows, created_ago_s=3600, sellable=None):
    with db.tx(conn):
        for mint, sym, mcap, liq, vol in rows:
            db.upsert_token(conn, mint, chain="robinhood", symbol=sym, mcap_usd=mcap,
                            liquidity_usd=liq, volume_usd=vol, created_at=now - created_ago_s,
                            sellable=sellable)


def test_todays_three_listings_are_judged_on_turnover_against_depth(tmp_path):
    """With the bar as agreed (volume >= depth) only the $13.05M one clears it — measured, not
    assumed: PONS trades 0.75x its depth in a day, the $6.6M Claude 0.64x."""
    conn = db.connect(tmp_path / "listings.db")
    now = db.now()
    seed(conn, now, MEASURED)
    got = listings.candidates(conn, "robinhood", now=now)
    assert [(c["mint"], c["volume_ratio"]) for c in got] == [(CLAUDE_B, 1.271)]


def test_the_ratio_is_the_only_thing_keeping_the_other_two_out(tmp_path):
    """PONS at $66.4M of depth is the largest listing of the week; it fails on turnover alone.
    Lowering the bar to 0.6 (LISTING_MIN_VOLUME_RATIO) catches all three — a decision, not a bug."""
    conn = db.connect(tmp_path / "listings.db")
    now = db.now()
    seed(conn, now, MEASURED)
    got = listings.candidates(conn, "robinhood", now=now, min_volume_ratio=0.6)
    assert {c["mint"] for c in got} == {PONS, CLAUDE_A, CLAUDE_B}
    assert [round(c["volume_ratio"], 2) for c in got] == [1.27, 0.75, 0.64], "hottest first"


def test_a_pool_below_a_million_of_depth_is_not_a_listing_signal(tmp_path):
    conn = db.connect(tmp_path / "listings.db")
    now = db.now()
    seed(conn, now, [(OTHER, "DUST", 900_000, 999_999, 5_000_000)])
    assert listings.candidates(conn, "robinhood", now=now) == []


def test_volume_unknown_is_not_a_zero_and_never_qualifies(tmp_path):
    conn = db.connect(tmp_path / "listings.db")
    now = db.now()
    with db.tx(conn):
        db.upsert_token(conn, OTHER, chain="robinhood", symbol="NOVOL", mcap_usd=5_000_000,
                        liquidity_usd=2_000_000, created_at=now - 600)
    assert listings.candidates(conn, "robinhood", now=now) == []


def test_one_roster_fill_hands_the_token_back_to_the_cohort_rule(tmp_path):
    """The moment a wallet we track buys, this is a burst candidate and not a lead."""
    conn = db.connect(tmp_path / "listings.db")
    now = db.now()
    seed(conn, now, MEASURED)
    with db.tx(conn):
        db.upsert_trader(conn, WALLET, chain="robinhood", score=70, status="watch")
        db.insert_trade(conn, sig="f1", address=WALLET, chain="robinhood", mint=CLAUDE_B,
                        side="buy", usd_value=500.0, token_amount=10.0, ts=now - 60, source="rpc")
    assert [c["mint"] for c in listings.candidates(conn, "robinhood", now=now)] == []


def test_an_old_listing_is_not_news(tmp_path):
    conn = db.connect(tmp_path / "listings.db")
    now = db.now()
    seed(conn, now, [(OTHER, "OLD", 50_000_000, 20_000_000, 40_000_000)],
         created_ago_s=10 * 86400)
    assert listings.candidates(conn, "robinhood", now=now) == []


def test_a_token_nobody_can_sell_is_not_a_lead(tmp_path):
    conn = db.connect(tmp_path / "listings.db")
    now = db.now()
    seed(conn, now, MEASURED, sellable=0)
    assert listings.candidates(conn, "robinhood", now=now) == []


def test_a_pool_is_recorded_once_however_long_it_stays_liquid(tmp_path):
    conn = db.connect(tmp_path / "listings.db")
    now = db.now()
    seed(conn, now, MEASURED)
    assert listings.sweep(conn, "robinhood", now=now)["new"] == 1
    assert listings.sweep(conn, "robinhood", now=now + 600)["new"] == 0
    assert len(conn.execute("SELECT 1 FROM listing_signals").fetchall()) == 1
    rec = listings.recent(conn, "robinhood", now=now + 3600)
    assert [r["mint"] for r in rec] == [CLAUDE_B]
    assert rec[0]["ts"] == now, "the first moment it qualified is what the reader is told"


def test_a_lead_carries_todays_pool_and_not_the_one_it_was_found_with(tmp_path):
    conn = db.connect(tmp_path / "listings.db")
    now = db.now()
    seed(conn, now, MEASURED)
    listings.sweep(conn, "robinhood", now=now)
    with db.tx(conn):
        db.upsert_token(conn, CLAUDE_B, liquidity_usd=25_000_000, volume_usd=40_000_000)
    r = listings.recent(conn, "robinhood", now=now + 600)[0]
    assert r["liq"] == 25_000_000 and round(r["volume_ratio"], 3) == 1.6


def test_the_sweep_reads_the_tokens_table_and_writes_no_run(tmp_path):
    """It must be runnable beside the cron loop: no runs row, no delete, one short write."""
    conn = db.connect(tmp_path / "listings.db")
    now = db.now()
    seed(conn, now, MEASURED)
    before = conn.execute("SELECT COUNT(*) FROM runs").fetchone()[0]
    listings.sweep(conn, "robinhood", now=now)
    assert conn.execute("SELECT COUNT(*) FROM runs").fetchone()[0] == before


# ---------------------------------------------------------------- where the numbers come from

def test_dexscreener_pair_keeps_the_pools_turnover():
    t = dexscreener.parse_pair({
        "chainId": "robinhood", "pairAddress": OTHER, "dexId": "uniswap",
        "baseToken": {"address": PONS, "symbol": "PONS"},
        "marketCap": "190400000", "liquidity": {"usd": 66_400_000},
        "volume": {"h24": 50_000_000, "h6": 20_000_000},
        "priceUsd": "0.001",
    })
    assert t.volume_usd == 50_000_000


def test_geckoterminal_pool_keeps_the_pools_turnover():
    t = geckoterminal.parse_pool({
        "attributes": {"address": OTHER, "name": "PONS / USDG", "reserve_in_usd": "66400000",
                       "volume_usd": {"h24": "50000000"}, "pool_created_at": "2026-11-01T00:00:00Z"},
        "relationships": {"base_token": {"data": {"id": "robinhood_" + PONS}}},
    })
    assert t.volume_usd == 50_000_000


def test_the_thresholds_are_settings_not_constants():
    assert settings.listing_min_liq_usd == 1_000_000
    assert settings.listing_min_volume_ratio == 1.0
    assert settings.listing_max_age_h == 72
