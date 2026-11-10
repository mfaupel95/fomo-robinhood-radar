import concurrent.futures
import json
import os
import sqlite3
import subprocess
import sys
import time

import httpx
import pytest
from fomo_agent import db, collector as co, credit_guard as cg
from fomo_agent.config import settings
from fomo_agent.sources.fomoapi import FomoApi, AuthenticationError, OutOfCredits

@pytest.fixture
def store(tmp_path, monkeypatch):
    p = tmp_path / 'test.db'
    c = db.connect(p)
    monkeypatch.setattr(settings, 'db_path', p)
    monkeypatch.setattr(settings, 'fomoapi_monthly_credits', 1000)
    yield c, p
    c.close()

def test_parallel_reservations_and_crash_never_refund(store):
    c, p = store
    c.execute("INSERT INTO runs(kind,started_at,finished_at,stats_json) VALUES ('fomoapi',?,?,?)", (db.now(),db.now(),json.dumps({'credits':995}))); c.commit()
    def take(_):
        try: cg.reserve(1, p); return True
        except cg.BudgetBlocked: return False
    with concurrent.futures.ThreadPoolExecutor(max_workers=12) as pool:
        assert sum(pool.map(take, range(30))) == 5
    assert c.execute('SELECT used FROM fomo_credit_month').fetchone()[0] == 1000
    with pytest.raises(cg.BudgetBlocked): cg.reserve(1,p)
    assert c.execute('SELECT count(*) FROM fomo_credit_reservations').fetchone()[0] == 5

def test_unknown_historical_consumption_blocks(store):
    c,p=store
    db.run_start(c,'fomoapi_24h')
    with pytest.raises(cg.BudgetBlocked): cg.reserve(1,p)

def test_zero_config_does_not_disable_hard_limit(store,monkeypatch):
    c,p=store
    monkeypatch.setattr(settings,'fomoapi_monthly_credits',0)
    cg.reserve(1000,p)
    with pytest.raises(cg.BudgetBlocked): cg.reserve(1,p)

@pytest.mark.parametrize('status,exc,category', [(401,AuthenticationError,'auth'),(403,AuthenticationError,'auth'),(402,OutOfCredits,'budget'),(503,httpx.HTTPStatusError,'transient'),(429,httpx.HTTPStatusError,'transient')])
def test_http_failure_consumes_reservation(store,status,exc,category):
    c,p=store
    def reply(req): return httpx.Response(status,json={},request=req)
    api=FomoApi('test-only',httpx.Client(base_url='https://test.invalid',transport=httpx.MockTransport(reply)))
    with pytest.raises(exc) as e: api.leaderboard()
    assert co.classify(e.value)==category
    assert c.execute('SELECT used FROM fomo_credit_month').fetchone()[0]==1

def test_timeout_is_reserved_before_network(store):
    c,p=store
    def hang(req):
        assert c.execute('SELECT used FROM fomo_credit_month').fetchone()[0]==1
        raise httpx.ReadTimeout('test')
    api=FomoApi('test-only',httpx.Client(base_url='https://test.invalid',transport=httpx.MockTransport(hang)))
    with pytest.raises(httpx.ReadTimeout): api.leaderboard()
    assert api.credits==1

def test_attempt_is_not_success_and_recovery_cooldown(store,monkeypatch):
    c,p=store
    monkeypatch.setattr(co,'build_steps',lambda:{'holdings':(3600,None)})
    calls=[]
    def fail(args,timeout): calls.append(args); return 124
    assert co.run_due(c,['holdings'],runner=fail)==1
    assert co.last_run(c,'holdings') is None
    assert co.run_due(c,['holdings'],runner=fail)==1
    assert len(calls)==1
    c.execute('UPDATE sammler_recovery SET next_at=0');c.commit()
    def good(args,timeout):
        rid=int(args[-1]); db.run_finish(c,rid,{'updated':1}); return 0
    assert co.run_due(c,['holdings'],runner=good)==0
    assert co.last_run(c,'holdings') is not None
    assert co.run_due(c,['holdings'],runner=fail)==0
    assert len(calls)==1

@pytest.mark.parametrize('reason',['auth','budget','permanent'])
def test_permanent_failures_do_not_retry_each_tick(store,reason):
    c,p=store;co.init_state(c);now=db.now()
    co.failure_state(c,'fomoapi_24h',reason,now)
    assert c.execute('SELECT next_at FROM sammler_recovery').fetchone()[0]>now+3600

def test_transient_backoff_is_persistent_and_bounded(store):
    c,p=store;co.init_state(c);now=db.now()
    delays=[]
    for _ in range(5):
        co.failure_state(c,'holdings','transient',now)
        delays.append(c.execute('SELECT next_at FROM sammler_recovery').fetchone()[0]-now)
    assert delays==[60,120,240,21600,21600]

def test_parallel_process_start_is_excluded(store):
    c,p=store
    code='from fomo_agent.collector import SingleInstance; import sys;\ntry:\n with SingleInstance(sys.argv[1]): sys.exit(9)\nexcept BlockingIOError: sys.exit(0)'
    env=dict(os.environ);env['PYTHONPATH']=str(__import__('pathlib').Path(co.__file__).resolve().parents[1]);env.pop('PYTHONHOME',None)
    with co.SingleInstance(p):
        r=subprocess.run([sys.executable,'-c',code,str(p)],env=env,capture_output=True,timeout=15)
        assert r.returncode==0
    with co.SingleInstance(p): pass

@pytest.mark.skipif(os.name != 'nt', reason='Windows native process/handle API required')
def test_real_hanger_is_killed_bounded():
    before=time.monotonic()
    assert co.bounded([sys.executable,'-c','import time; time.sleep(60)'],0.3)==124
    assert time.monotonic()-before<10

def test_fast_board_does_not_buy_theses(store,monkeypatch):
    c,p=store
    from fomo_agent.pipeline import collect_api
    monkeypatch.setattr(settings,'fomoapi_key','test-only')
    got=[]
    monkeypatch.setattr(collect_api,'collect',lambda c,w,p:got.append((w,p)) or {})
    co.build_steps()['fomoapi_24h'][1](c)
    assert got==[(('24h',),0)]
