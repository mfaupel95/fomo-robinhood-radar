"""Cache invalidation must work on newly booted ephemeral runners too."""
import pytest
import fomo_agent.sources.rpc as rpc_module
from fomo_agent.config import settings
from fomo_agent.sources.rpc import RobinhoodRPC


@pytest.mark.parametrize("uptime", [10.0, 100000.0])
def test_first_scan_and_roster_change_are_not_cached(uptime, monkeypatch):
    monkeypatch.setattr(rpc_module.time, "monotonic", lambda: uptime)
    monkeypatch.setattr(settings, "rpc_min_interval_s", 900)
    calls = []
    wallet = "0x" + "a" * 40
    other = "0x" + "b" * 40
    rpc = RobinhoodRPC(url="http://offline.invalid")
    monkeypatch.setattr(rpc, "block_number", lambda: 1000000)

    def scan(wallets, first, last):
        calls.append(tuple(wallets))
        return {}

    monkeypatch.setattr(rpc, "scan", scan)
    try:
        rpc.prime([wallet])
        assert rpc.get_trades(wallet, "robinhood") == []
        assert calls == [(wallet,)], "an invalidated cache must perform its first scan"
        rpc.get_trades(wallet, "robinhood")
        assert len(calls) == 1, "an actual empty result is cached"
        rpc.prime([wallet, other])
        rpc.get_trades(other, "robinhood")
        assert len(calls) == 2, "a roster change invalidates the cached empty result"
    finally:
        rpc.http.close()
