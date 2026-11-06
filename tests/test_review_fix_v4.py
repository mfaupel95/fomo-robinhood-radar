"""Offline regressions for review R1/R2; only fixture databases and own children."""
import json
import os
from pathlib import Path
import sqlite3
import subprocess
import sys

import httpx
import pytest

from fomo_agent import collector, db
from fomo_agent.config import settings
from fomo_agent.enrich_budget import EnrichBudget, current
from fomo_agent.pipeline import new_tokens, safety
from fomo_agent.ratelimit import SharedLimitUnavailable, SharedRateLimiter


@pytest.fixture(autouse=True)
def offline(monkeypatch):
    import socket
    def forbidden(*a, **kw):
        raise AssertionError('network forbidden')
    monkeypatch.setattr(socket.socket, 'connect', forbidden)


@pytest.mark.parametrize('guarded,notify,expected', [(False, True, 1), (False, False, 0), (True, True, 0), (True, False, 0)])
def test_safety_persists_without_disabling_normal_caller(tmp_path, monkeypatch, guarded, notify, expected):
    path = tmp_path / 'safety.db'
    c = db.connect(path)
    mint = '0x' + '1' * 40
    db.upsert_token(c, mint, chain='robinhood', liquidity_usd=100, pool_address='0x'+'2'*40)
    c.commit()
    monkeypatch.setattr(safety, 'holders_to_try', lambda *a: ['0x'+'3'*40])
    monkeypatch.setattr(safety, 'probe_transfer', lambda *a: ('blocked', 'fixture blocked'))
    sends = []
    monkeypatch.setattr(safety, 'void_pushes', lambda *a: sends.append(a))
    token = current.set(EnrichBudget(5) if guarded else None)
    try:
        assert safety.check(c, mint, rpc=object(), force=True, notify=notify)['sellable'] == 0
    finally:
        current.reset(token)
        c.close()
    observer = db.connect(path)
    row = observer.execute('SELECT sellable,sell_note,sell_checked_at FROM tokens WHERE mint=?', (mint,)).fetchone()
    assert tuple(row) == (0, 'fixture blocked', row['sell_checked_at'])
    assert row['sell_checked_at'] > 0
    observer.close()
    assert len(sends) == expected


def test_enrich_explicitly_passes_no_dispatch(tmp_path, monkeypatch):
    c = db.connect(tmp_path/'enrich.db')
    seen = []
    def sweep(conn, **kw):
        seen.append(kw['notify'])
        return {}
    monkeypatch.setattr(safety, 'sweep', sweep)
    new_tokens.enrich_tokens(c)
    assert seen == [False]
    assert current.get() is None
    c.close()


@pytest.mark.parametrize('mode', ['missing', 'corrupt', 'claim', 'already_broken', 'locked'])
@pytest.mark.parametrize('method', ['wait', 'take'])
def test_guarded_limiter_never_counts_locally(tmp_path, monkeypatch, mode, method):
    path = tmp_path/'limit.db'
    if mode == 'missing':
        path = tmp_path/'missing'/'limit.db'
    if mode == 'corrupt':
        path.write_bytes(b'not a sqlite database')
    limiter = SharedRateLimiter(3, 'fixture', path, reserve=1, min_gap_s=.1)
    blocker = None
    if mode == 'locked':
        limiter._db().execute('PRAGMA busy_timeout=10')
        blocker = sqlite3.connect(path)
        blocker.execute('BEGIN IMMEDIATE')
    if mode == 'claim':
        def broken(*a):
            raise sqlite3.OperationalError('fixture claim failure')
        monkeypatch.setattr(limiter, '_claim', broken)
    if mode == 'already_broken':
        limiter.path = tmp_path/'missing'/'limit.db'
        assert limiter.take()  # legacy caller, before entering guarded enrichment
    before = limiter.total
    budget = EnrichBudget(3)
    token = current.set(budget)
    try:
        with pytest.raises(SharedLimitUnavailable) as exc:
            getattr(limiter, method)()
    finally:
        current.reset(token)
        if blocker is not None:
            blocker.rollback()
            blocker.close()
    assert limiter.total == before
    event = budget.events[-1]
    assert event['classification'] == collector.classify(exc.value) == 'transient'
    assert event['retry_policy'] == 'collector_backoff'
    assert event['shared_reservation'] is False


def test_limiter_failure_stops_enrich_before_any_http_and_backs_off(tmp_path, monkeypatch):
    path = tmp_path/'fixture.db'
    monkeypatch.setattr(settings, 'db_path', path)
    monkeypatch.setattr(settings, 'ratelimit_path', tmp_path/'missing'/'limit.db')
    c = db.connect(path)
    mint = '0x'+'1'*40
    db.upsert_token(c, mint, chain='robinhood')
    c.commit()
    monkeypatch.setattr(new_tokens, 'unnamed_tokens', lambda *a: [{'chain':'robinhood','token':mint}])
    monkeypatch.setattr(new_tokens, 'stale_price_tokens', lambda *a: [])
    calls = []
    monkeypatch.setattr(httpx.Client, 'send', lambda *a, **kw: calls.append(a) or pytest.fail('HTTP before shared reservation'))
    monkeypatch.setattr(collector, 'build_steps', lambda: {'enrich_tokens': (0, new_tokens.enrich_tokens)})
    def own_worker(args, timeout):
        return collector.worker_locked('enrich_tokens', int(args[-1]))
    assert collector.run_due(c, ['enrich_tokens'], runner=own_worker) == 1
    row = c.execute("SELECT * FROM sammler_recovery WHERE kind='enrich_tokens'").fetchone()
    assert row['reason'] == 'transient' and row['failures'] == 1
    assert 55 <= row['next_at'] - db.now() <= 60
    diagnostic = c.execute("SELECT error,stats_json FROM runs WHERE kind='enrich_diagnostic'").fetchone()
    payload = json.loads(diagnostic['stats_json'])
    assert diagnostic['error'] == 'failure'
    assert any(e.get('classification') == 'transient' and e['operation'] == 'shared_claim' for e in payload['events'])
    assert calls == []
    assert c.execute("SELECT count(*) FROM sqlite_master WHERE name='fomo_credit_reservations'").fetchone()[0] == 0
    c.close()


def test_real_processes_share_guarded_reserve_and_spacing(tmp_path):
    path = tmp_path/'shared.db'
    # Initialize before launching contenders, avoiding schema-creation timing as a fixture variable.
    init = SharedRateLimiter(5, 'fixture', path)
    init._db().close()
    code = '''import json,sys
from fomo_agent.ratelimit import SharedRateLimiter
from fomo_agent.enrich_budget import EnrichBudget,current,Deadline
r=SharedRateLimiter(5,'fixture',sys.argv[1],reserve=1,min_gap_s=.08)
t=current.set(EnrichBudget(.8))
n=0
try:
 for i in range(4):
  try: r.wait();n+=1
  except Deadline: break
finally: current.reset(t)
print(json.dumps(n))
'''
    env = dict(os.environ)
    env.pop('PYTHONHOME', None)
    env['PYTHONPATH'] = str(Path(collector.__file__).resolve().parents[1])
    env['PYTHON_DOTENV_DISABLED'] = '1'
    children = [subprocess.Popen([sys.executable, '-c', code, str(path)], env=env, cwd=tmp_path,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE) for _ in range(4)]
    counts = []
    try:
        for p in children:
            out, err = p.communicate(timeout=15)
            assert p.returncode == 0, err.decode(errors='replace')
            counts.append(json.loads(out))
    finally:
        for p in children:
            if p.poll() is None:
                p.kill(); p.wait(timeout=5)
    with sqlite3.connect(path) as c:
        stamps = [r[0] for r in c.execute("SELECT ts FROM calls WHERE name='fixture' ORDER BY ts")]
    assert sum(counts) == len(stamps) == 4
    assert all(b-a >= .075 for a,b in zip(stamps, stamps[1:]))
    impatient = SharedRateLimiter(5, 'fixture', path)
    assert impatient.take() and not impatient.take()  # fifth slot remains reserved for ordinary callers
