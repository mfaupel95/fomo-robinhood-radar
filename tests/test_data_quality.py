import pytest
from typer.testing import CliRunner
from fomo_agent import db, collector
from fomo_agent.pipeline import health


def test_missing_evidence_is_unknown(tmp_path):
    c = db.connect(tmp_path / 'q.db')
    r = health.report(c, local_only=True)
    rows = {x['name']: x for x in r['checks']}
    for name in ('router', 'watcher gaps', 'collect scans'):
        assert rows[name]['status'] == 'UNKNOWN'
        assert rows[name]['ok'] is None
    assert r['unknown'] >= 3
    assert r['failing'] == sum(x['status'] == 'BAD' for x in r['checks'])
    assert sum(r['counts'].values()) == len(r['checks'])
    assert r['ok'] is False


def test_report_unknown_is_not_clear(monkeypatch):
    monkeypatch.setattr(health, 'checks', lambda *a, **k: [{'name':'coverage', 'ok':None, 'status':'UNKNOWN', 'detail':'missing'}])
    r = health.report(None)
    assert r['status'] == 'UNKNOWN' and r['failing'] == 0 and not r['ok']
    from fomo_agent.bot.words import fmt_health
    assert 'UNKNOWN' in fmt_health(r) and 'ALL CLEAR' not in fmt_health(r)


@pytest.mark.parametrize('status,code', [('UNKNOWN',2), ('BAD',1), ('OK',0)])
def test_cli_exit_and_quiet_visibility(monkeypatch, status, code):
    from fomo_agent.cli import app
    class C:
        def close(self): pass
    monkeypatch.setattr(db, 'connect', lambda: C())
    monkeypatch.setattr(health, 'report', lambda c: {'ok':status=='OK', 'status':status, 'failing':int(status=='BAD'), 'unknown':int(status=='UNKNOWN'), 'checks':[{'name':'coverage','status':status,'ok':True if status=='OK' else False if status=='BAD' else None,'detail':'evidence'}]})
    r = CliRunner().invoke(app, ['health','--quiet'])
    assert r.exit_code == code, r.output
    assert (status in r.output) if status != 'OK' else not r.output


def test_unknown_health_worker_is_not_failed_or_retried(tmp_path, monkeypatch):
    c = db.connect(tmp_path / 'w.db')
    monkeypatch.setattr(db, 'connect', lambda: c)
    monkeypatch.setattr(collector, 'build_steps', lambda: {'health':(1,lambda c:{'ok':False,'status':'UNKNOWN','failing':0,'unknown':1})})
    rid = db.run_start(c, 'health')
    # close is part of worker contract; inspect persisted row with a second connection
    path = tmp_path / 'w.db'
    assert collector.worker_locked('health', rid) == 0
    import sqlite3
    with sqlite3.connect(path) as read:
        assert read.execute('select error from runs where id=?',(rid,)).fetchone()[0] is None


def test_stale_marks_are_explicit_in_report(tmp_path):
    from fomo_agent.pipeline.report import build_report
    from fomo_agent.pipeline.data_quality import snapshot
    c = db.connect(tmp_path / 'stale.db')
    mint = '0x' + 'a' * 40
    with db.tx(c):
        db.upsert_token(c, mint, chain='robinhood', symbol='SAME', price_usd=9, price_at=1)
    s = snapshot(c)
    assert s['counts']['fresh'] == 0 and s['tokens'][0]['stale']
    text = build_report(c)
    assert mint in text and 'robinhood' in text and 'STALE' in text
    assert 'NEVER executable proceeds' in text and 'UNKNOWN' in text


def test_listing_history_does_not_invent_sellability(tmp_path):
    from fomo_agent.pipeline import listings
    c = db.connect(tmp_path / 'list.db')
    mint = '0x' + 'b' * 40
    with db.tx(c):
        db.upsert_token(c, mint, chain='robinhood', created_at=db.now()-86400*5, price_at=1)
        c.execute('INSERT INTO listing_signals(mint,chain,ts,age_s) VALUES (?,?,?,?)', (mint,'robinhood',db.now()-3600,10))
    row = listings.recent(c)[0]
    assert row['sellable'] is None
    assert row['listing_age_h'] >= 120 and row['stale']


def test_invalid_chain_identity_is_reported_not_repaired():
    from fomo_agent.pipeline.data_quality import valid_token
    mint = '0x' + 'b' * 40
    assert valid_token('solana', mint) is False
    assert valid_token('robinhood', mint) is True
    assert valid_token('robinhood', mint[:12]) is False
