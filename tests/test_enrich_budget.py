"""Offline regression contract: no original DB or network."""
import json
from types import SimpleNamespace

import httpx
import pytest

from fomo_agent import db
from fomo_agent.pipeline import new_tokens as nt
from fomo_agent.sources.geckoterminal import GeckoTerminal


class Clock:
    def __init__(self): self.t = 1000.0
    def now(self): return self.t
    def sleep(self, seconds): self.t += seconds


def test_slow_source_has_request_and_total_deadline(monkeypatch):
    from fomo_agent.enrich_budget import EnrichBudget, Deadline
    clock = Clock()
    budget = EnrichBudget(5, clock=clock.now, sleep=clock.sleep)
    def slow(request):
        assert max(request.extensions['timeout'].values()) <= 1.25
        clock.sleep(6)
        return httpx.Response(200, json={'data': []})
    gt = GeckoTerminal(client=httpx.Client(transport=httpx.MockTransport(slow), base_url='https://example.test'), budget=budget)
    gt.limiter = SimpleNamespace(wait=lambda **kw: None)
    with pytest.raises(Deadline): gt._get('/slow')
    assert budget.events[-1]['outcome'] == 'deadline'


def test_429_keeps_backoff_but_stops_at_total_budget(monkeypatch):
    monkeypatch.setattr('fomo_agent.sources.geckoterminal.settings.gecko_min_interval_s', 0)
    from fomo_agent.enrich_budget import EnrichBudget, Deadline
    clock = Clock()
    budget = EnrichBudget(20, clock=clock.now, sleep=clock.sleep)
    calls = []
    def busy(request):
        calls.append(request)
        return httpx.Response(429)
    gt = GeckoTerminal(client=httpx.Client(transport=httpx.MockTransport(busy), base_url='https://example.test'), budget=budget)
    gt.limiter = SimpleNamespace(wait=lambda **kw: None)
    with pytest.raises(Deadline): gt._get('/busy')
    assert len(calls) == 2
    assert clock.t == 1015
    assert [e['outcome'] for e in budget.events].count('http_429') == 2


@pytest.mark.parametrize('mode', ['partial', 'failure', 'repeat'])
def test_persistent_partial_failure_and_success_time(tmp_path, monkeypatch, mode):
    c = db.connect(tmp_path / 'fixture.db')
    now = db.now()
    for mint in ('a', 'b'):
        db.upsert_token(c, mint, chain='robinhood', price_usd=7, price_at=now-999999)
    c.commit()
    monkeypatch.setattr(nt, 'unnamed_tokens', lambda *a: [{'chain':'robinhood','token':m} for m in ('a','b')])
    monkeypatch.setattr(nt, 'stale_price_tokens', lambda *a: [])
    monkeypatch.setattr(nt, 'undated_tokens', lambda *a: [])
    def tokens(self, chain, mints):
        self.budget.record('geckoterminal', 'request', 'attempt', chain=chain, mints=mints)
        if mode == 'failure': raise httpx.ReadTimeout('fixture')
        return [SimpleNamespace(mint='a',chain=chain,symbol='A',mcap_usd=None,liquidity_usd=None,volume_usd=None,created_at=None,decimals=None,price_usd=8,pool_address=None)]
    monkeypatch.setattr(GeckoTerminal, 'tokens', tokens)
    class Dex:
        def pairs_for(self, *a): raise httpx.ReadTimeout('fixture')
    first = nt.enrich_tokens(c, dex=Dex(), budget_s=2)
    if mode == 'repeat': nt.enrich_tokens(c, dex=Dex(), budget_s=2)
    b = c.execute("SELECT * FROM tokens WHERE mint='b'").fetchone()
    assert b['price_usd'] == 7 and b['price_at'] == now-999999
    assert b['checked_at'] >= now
    assert first['priced'] == (0 if mode == 'failure' else 1)
    runs = c.execute("SELECT stats_json FROM runs WHERE kind='enrich_diagnostic' ORDER BY id").fetchall()
    assert len(runs) == (2 if mode == 'repeat' else 1)
    diagnostic = json.loads(runs[-1][0])
    assert diagnostic['events'] and 'b' in {r['mint'] for r in diagnostic['stale']}
    assert diagnostic['failures'] >= 1
    c.close()


def test_completed_batch_survives_next_batch_deadline(tmp_path, monkeypatch):
    from fomo_agent.enrich_budget import EnrichBudget, Deadline
    clock = Clock()
    monkeypatch.setattr(nt, 'EnrichBudget', lambda seconds: EnrichBudget(seconds, clock=clock.now, sleep=clock.sleep))
    path = tmp_path / 'partial.db'
    c = db.connect(path)
    mints = [f'{i:040x}' for i in range(31)]
    monkeypatch.setattr(nt, 'unnamed_tokens', lambda *a: [{'chain':'robinhood', 'token':m} for m in mints])
    monkeypatch.setattr(nt, 'stale_price_tokens', lambda *a: [])
    def lookup(chain, batch, **kw):
        observer = db.connect(path)
        live = json.loads(observer.execute("SELECT stats_json FROM runs WHERE kind='enrich_diagnostic'").fetchone()[0])
        assert live['events'][-1]['outcome'] == 'attempt'
        observer.close()
        if batch == mints[30:]:
            clock.sleep(3)
            raise Deadline('fixture')
        return [SimpleNamespace(mint=m,chain=chain,symbol='A',mcap_usd=None,liquidity_usd=None,volume_usd=None,created_at=None,decimals=None,price_usd=8,pool_address=None) for m in batch], 1
    monkeypatch.setattr(nt, 'lookup_tokens', lookup)
    stats = nt.enrich_tokens(c, budget_s=2)
    assert stats['stopped'] == 'deadline' and stats['priced'] == 30
    assert c.execute('SELECT count(*) FROM tokens WHERE price_at IS NOT NULL').fetchone()[0] == 30
    assert c.execute('SELECT count(*) FROM tokens WHERE mint=?', (mints[-1],)).fetchone()[0] == 0
    assert stats['stale'] == [{'chain':'robinhood','mint':mints[-1],'price_at':None,'stale':True}]
    c.close()


def test_successful_unchanged_price_is_a_refresh_and_repeat_is_not_due(tmp_path, monkeypatch):
    c = db.connect(tmp_path / 'repeat.db')
    now = db.now()
    db.upsert_token(c, 'a', chain='robinhood', price_usd=8, price_at=now-999999)
    c.commit()
    monkeypatch.setattr(nt, 'stale_price_tokens', lambda *a: [])
    monkeypatch.setattr(nt, 'undated_tokens', lambda *a: [])
    monkeypatch.setattr('fomo_agent.pipeline.safety.sweep', lambda *a, **kw: {})
    calls = []
    def tokens(self, chain, mints):
        calls.append(mints)
        return [SimpleNamespace(mint='a',chain=chain,symbol='A',mcap_usd=None,liquidity_usd=None,volume_usd=None,created_at=None,decimals=None,price_usd=8,pool_address=None)]
    monkeypatch.setattr(GeckoTerminal, 'tokens', tokens)
    # Use the real unnamed queue, sourced from a stored position.
    c.execute("INSERT INTO fomo_positions(trade_id,token,chain) VALUES('fixture','a','robinhood')")
    c.commit()
    assert nt.enrich_tokens(c)['priced'] == 1
    price_at = c.execute("SELECT price_at FROM tokens WHERE mint='a'").fetchone()[0]
    assert price_at >= now
    assert nt.enrich_tokens(c)['priced'] == 0
    assert len(calls) == 1
    assert c.execute("SELECT price_at FROM tokens WHERE mint='a'").fetchone()[0] == price_at
    c.close()


def test_shared_limiter_preserves_reserve_and_declines_overbudget_wait(tmp_path, monkeypatch):
    from fomo_agent.enrich_budget import EnrichBudget, Deadline
    from fomo_agent.ratelimit import SharedRateLimiter
    clock = Clock()
    monkeypatch.setattr('fomo_agent.ratelimit.time.time', clock.now)
    limiter = SharedRateLimiter(3, 'fixture', tmp_path/'limit.db', reserve=1)
    limiter.wait(budget=EnrichBudget(1, clock=clock.now, sleep=clock.sleep))
    limiter.wait(budget=EnrichBudget(1, clock=clock.now, sleep=clock.sleep))
    with pytest.raises(Deadline):
        limiter.wait(budget=EnrichBudget(1, clock=clock.now, sleep=clock.sleep))
    assert limiter.total == 2 and clock.t == 1000
