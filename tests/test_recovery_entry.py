import os
import subprocess
import sys
from pathlib import Path
import pytest
from fomo_agent import db, collector as co, credit_guard as cg
from fomo_agent.config import settings


def test_orphan_worker_blocks_regular_and_recovery(tmp_path, monkeypatch):
    p=tmp_path/'orphan.db'; c=db.connect(p)
    monkeypatch.setattr(settings,'db_path',p)
    monkeypatch.setattr(sys,'argv',['sammler','--only','holdings'])
    with co.SingleInstance(str(p)+'.worker'):
        assert co.main()==0
        assert c.execute('SELECT count(*) FROM runs').fetchone()[0]==0
    c.close()


def test_entry_from_other_cwd_and_repeat_does_not_start_work(tmp_path):
    p=tmp_path/'other.db';c=db.connect(p)
    rid=db.run_start(c,'holdings');db.run_finish(c,rid,{'held':0});c.close()
    env=dict(os.environ);env.pop('PYTHONHOME',None);env.pop('PYTHONPATH',None)
    env['DB_PATH']=str(p)
    entry=Path(co.__file__).resolve().parents[1]/'scripts/sammler.py'
    for _ in range(2):
        r=subprocess.run([sys.executable,str(entry),'--only','holdings'],cwd=tmp_path,env=env,capture_output=True,timeout=20)
        # Collection stays skipped; mandatory local health diagnoses the empty fixture.
        assert r.returncode==1, r.stderr.decode(errors='replace')
    c=db.connect(p)
    assert c.execute("SELECT count(*) FROM runs WHERE kind='holdings'").fetchone()[0]==1
    assert c.execute("SELECT count(*) FROM runs WHERE kind='health'").fetchone()[0]==2
    c.close()


def test_known_missing_key_is_not_unknown_network_spend(tmp_path,monkeypatch):
    p=tmp_path/'key.db';c=db.connect(p)
    monkeypatch.setattr(settings,'fomoapi_monthly_credits',1000)
    rid=db.run_start(c,'fomoapi')
    db.run_finish(c,rid,error="FomoApiError('FOMOAPI_KEY is not set (free key at https://fomoapi.io/dashboard)')")
    assert cg.reserve(1,p)==1
    c.close()


def test_health_failure_stays_visible_and_does_not_become_success(tmp_path,monkeypatch):
    p=tmp_path/'health.db';c=db.connect(p)
    monkeypatch.setattr(settings,'db_path',p)
    monkeypatch.setattr(co,'build_steps',lambda:{'health':(60,lambda c:{'ok':False,'failing':1,'checks':[{'name':'watcher gaps','ok':False}]})})
    rid=db.run_start(c,'health')
    assert co.worker_locked('health',rid)==1
    assert co.last_run(c,'health') is None
    assert c.execute('SELECT error FROM runs WHERE id=?',(rid,)).fetchone()[0]=='health'
    c.close()
