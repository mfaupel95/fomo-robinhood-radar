"""Settings the suite must not inherit from the machine it runs on.

`config.settings` reads the real .env, and on the server that .env has the PRO gate switched on:
every feed test would then be answered "this feed is PRO". The gate is off here unless a test
turns it on itself (tests/test_pro.py does, through its own fixture).
"""
import pytest

from fomo_agent.config import settings


@pytest.fixture(autouse=True)
def _no_gate_unless_asked(monkeypatch, tmp_path):
    # the box-wide rate limit lives in a file next to the DB; here, next to the test's
    monkeypatch.setattr(settings, "ratelimit_path", tmp_path / "ratelimit.db")
    monkeypatch.setattr(settings, "pro_price_usd", 0.0)
    monkeypatch.setattr(settings, "pro_grace_until", 0)
    monkeypatch.setattr(settings, "pro_trial_days", 0)
    # the server's .env names a spare RPC endpoint; a test that wants one sets it itself
    monkeypatch.setattr(settings, "rpc_urls", [])
    # X posting is off unless a test switches it on
    monkeypatch.setattr(settings, "x_enabled", False)
    # the older fixtures place a cohort's buys seconds apart; the span rule is tested on its own
    monkeypatch.setattr(settings, "hot_min_span_s", 0)
    # Pin documented burst defaults in tests only, independently of operator settings.
    monkeypatch.setattr(settings, "hot_min_score", 60)
    monkeypatch.setattr(settings, "hot_delta", 1.0)
    # the second signal class's bars are the operator's (.env), and the box has its own: pin the
    # documented defaults here so a test measures the rule and not what somebody typed today
    monkeypatch.setattr(settings, "listing_min_liq_usd", 1_000_000.0)
    monkeypatch.setattr(settings, "listing_min_volume_ratio", 1.0)
    monkeypatch.setattr(settings, "listing_max_age_h", 72)
