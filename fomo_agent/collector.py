"""Bounded collector used by regular ticks and recovery. No orders or sends."""
from __future__ import annotations
import argparse
import calendar
import os
from pathlib import Path
import subprocess
import sys
import threading
import time
from . import db
from .config import settings
from .credit_guard import BudgetBlocked, reserve
from .sources.fomoapi import AuthenticationError, OutOfCredits

class SingleInstance:
    def __init__(self, path):
        self.path = str(Path(path).resolve()) + '.sammler.lock'
    def __enter__(self):
        self.f = open(self.path, 'a+b')
        self.f.seek(0)
        if os.name == 'nt':
            import msvcrt
            if not os.path.getsize(self.path):
                self.f.write(b'0'); self.f.flush()
            self.f.seek(0)
            try: msvcrt.locking(self.f.fileno(), msvcrt.LK_NBLCK, 1)
            except OSError:
                self.f.close(); raise BlockingIOError('collector already active')
        else:
            import fcntl
            try: fcntl.flock(self.f, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except OSError:
                self.f.close(); raise BlockingIOError('collector already active')
        return self
    def __exit__(self, *args): self.f.close()

def build_steps():
    from .pipeline import collect_api, holdings, listings, new_tokens, score, track, discover, health
    def paid(c, windows, pages):
        if not settings.fomoapi_key: raise AuthenticationError('credential missing')
        return collect_api.collect(c, windows, pages)
    return {
        'discover_trenches': (86400, discover.discover_trenches),
        'fomoapi_24h': (7200, lambda c: paid(c, ('24h',), 0)),
        'fomoapi_7d': (21600, lambda c: paid(c, ('7d',), 0)),
        'fomoapi_theses': (28800, lambda c: paid(c, (), 1)),
        'track': (settings.track_interval, track.track_all),
        'enrich_tokens': (settings.track_interval, new_tokens.enrich_tokens),
        'holdings': (settings.track_interval, holdings.mark_holdings),
        'score': (settings.track_interval * 10, score.score_all),
        'listings': (settings.new_tokens_interval, listings.sweep),
        'health': (settings.track_interval, lambda c: health.report(c, local_only=True)),
    }

def last_run(c, kind):
    return c.execute("SELECT MAX(finished_at) FROM runs WHERE kind=? AND finished_at IS NOT NULL AND error IS NULL AND coalesce(json_extract(stats_json,'$.errors'),0)=0 AND json_extract(stats_json,'$.stopped') IS NULL AND json_extract(stats_json,'$.skipped') IS NULL AND json_extract(stats_json,'$.budget_stop') IS NULL AND json_extract(stats_json,'$.out_of_credits') IS NULL", (kind,)).fetchone()[0]

def init_state(c):
    c.execute('CREATE TABLE IF NOT EXISTS sammler_recovery (kind TEXT PRIMARY KEY, failures INTEGER NOT NULL, next_at INTEGER NOT NULL, reason TEXT, run_id INTEGER)'); c.commit()

def failure_state(c, kind, reason, now):
    r = c.execute('SELECT failures FROM sammler_recovery WHERE kind=?', (kind,)).fetchone()
    n = (r[0] if r else 0) + 1
    delay = min(3600, 60 * 2 ** min(n - 1, 6)) if n <= 3 else 21600
    if reason in ('auth', 'permanent'): delay = 2147483647 - now
    elif reason == 'budget':
        t = time.gmtime(now)
        y, m = (t.tm_year + 1, 1) if t.tm_mon == 12 else (t.tm_year, t.tm_mon + 1)
        delay = calendar.timegm((y, m, 1, 0, 0, 0)) - now
    c.execute('INSERT OR REPLACE INTO sammler_recovery VALUES (?,?,?,?,NULL)', (kind, n, now + delay, reason)); c.commit()

def classify(e):
    import httpx
    if isinstance(e, AuthenticationError): return 'auth'
    if isinstance(e, (BudgetBlocked, OutOfCredits)): return 'budget'
    if isinstance(e, (httpx.TimeoutException, httpx.TransportError)): return 'transient'
    if isinstance(e, httpx.HTTPStatusError):
        if e.response.status_code in (401, 403): return 'auth'
        if e.response.status_code == 402: return 'budget'
        if e.response.status_code == 429 or e.response.status_code >= 500: return 'transient'
    return 'permanent'

def worker(kind, rid):
    # Child retains a kernel lock if its supervising parent crashes.
    timer = threading.Timer(30 if kind == 'health' else 120, lambda: os._exit(124))
    timer.daemon = True
    timer.start()
    try:
        with SingleInstance(str(settings.db_path) + '.worker'):
            return worker_locked(kind, rid)
    finally:
        timer.cancel()


def worker_locked(kind, rid):
    c = db.connect()
    try:
        stats = build_steps()[kind][1](c)
        if kind == 'health' and not stats.get('ok'):
            db.run_finish(c, rid, stats, 'health'); return 1
        if stats.get('budget_stop') or stats.get('out_of_credits'): raise BudgetBlocked('budget blocked')
        if stats.get('error') or stats.get('errors') or stats.get('skipped') or 'stopped' in stats:
            db.run_finish(c, rid, stats, 'transient'); return 1
        db.run_finish(c, rid, stats); return 0
    except Exception as e:
        db.run_finish(c, rid, error=classify(e)); return 1
    finally: c.close()

def bounded(args, timeout):
    env = dict(os.environ)
    env.pop('PYTHONHOME', None)
    env['PYTHONPATH'] = str(Path(__file__).resolve().parents[1])
    p = subprocess.Popen(args, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try: return p.wait(timeout=timeout)
    except subprocess.TimeoutExpired:
        if os.name == 'nt': subprocess.run(['taskkill', '/PID', str(p.pid), '/T', '/F'], capture_output=True, timeout=15)
        else: p.kill()
        p.wait(timeout=15)
        return 124

def run_due(c, kinds, step_timeout=120, total_timeout=600, runner=bounded):
    # Last-resort self-expiry also bounds SQLite/metadata stalls. An orphan child
    # retains its worker lock and its independent 120s self-expiry.
    total_timeout = min(600, max(61, total_timeout))
    deadline = time.monotonic() + total_timeout
    timer = threading.Timer(total_timeout, lambda: os._exit(124))
    timer.daemon = True
    timer.start()
    try:
        return _run_due(c, kinds, step_timeout, deadline, runner)
    finally:
        timer.cancel()


def _run_due(c, kinds, step_timeout, deadline, runner):
    init_state(c)
    # Reserve 30s of execution + 30s kill/reap for local closing health.
    # 61s is the minimum supported tick; cleanup is inside, not after, its deadline.
    failed = False
    steps = build_steps()
    closing_health = 'health' in steps
    collection_deadline = deadline - (60 if closing_health else 30)
    for kind in [k for k in kinds if k != 'health'] + (['health'] if closing_health else []):
        diagnostic = kind == 'health'
        now = db.now(); last = last_run(c, kind)
        if not diagnostic and last is not None and now - last < steps[kind][0]: continue
        state = c.execute('SELECT * FROM sammler_recovery WHERE kind=?', (kind,)).fetchone()
        if not diagnostic and state and state['next_at'] > now:
            print(f'{kind}: blocked ({state["reason"]})'); failed = True; continue
        remaining = (deadline - 30 if diagnostic else collection_deadline - 30) - time.monotonic()
        if not diagnostic and remaining <= 0:
            print('collector: collection deadline reached'); failed = True; continue
        if diagnostic and time.monotonic() >= collection_deadline:
            failed = True
        if state and state['run_id']:
            c.execute("UPDATE runs SET finished_at=?,error='transient' WHERE id=? AND finished_at IS NULL", (now, state['run_id'])); c.commit()
        rid = db.run_start(c, kind)
        failures = state['failures'] if state else 0
        c.execute('INSERT OR REPLACE INTO sammler_recovery VALUES (?,?,?,?,?)', (kind, failures, now + step_timeout + 30, 'in_flight', rid)); c.commit()
        entry = Path(__file__).resolve().parents[1] / 'scripts' / 'sammler.py'
        remaining = min(remaining, deadline - 30 - time.monotonic())
        try:
            rc = runner([sys.executable, str(entry), '--step', kind, '--run-id', str(rid)], min(step_timeout, 30 if diagnostic else 120, max(0.001, remaining)))
        except Exception as e:
            db.run_finish(c, rid, error=classify(e)); rc = 1
        row = c.execute('SELECT error,finished_at FROM runs WHERE id=?', (rid,)).fetchone()
        if rc or row['error'] or row['finished_at'] is None:
            reason = row['error'] or 'transient'
            if row['finished_at'] is None: db.run_finish(c, rid, error=reason)
            if diagnostic:
                c.execute('DELETE FROM sammler_recovery WHERE kind=?', (kind,)); c.commit()
            else: failure_state(c, kind, reason, db.now())
            print(f'{kind}: failed ({reason})'); failed = True
        else:
            c.execute('DELETE FROM sammler_recovery WHERE kind=?', (kind,)); c.commit()
            print(f'{kind}: success run={rid}')
    return int(failed)

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--only', nargs='+'); p.add_argument('--step', choices=list(build_steps()))
    p.add_argument('--run-id', type=int); p.add_argument('--step-timeout', type=int, default=120)
    p.add_argument('--total-timeout', type=int, default=600, help='tick seconds, clamped to 61..600 including health/cleanup')
    a = p.parse_args()
    if a.step: return worker(a.step, a.run_id)
    kinds = a.only or list(build_steps())
    if any(k not in build_steps() for k in kinds): p.error('unknown step')
    try:
        with SingleInstance(settings.db_path):
            with SingleInstance(str(settings.db_path) + '.worker'):
                pass  # refuse recovery while an orphan worker still owns the DB
            c = db.connect()
            try:
                try: reserve(0)  # bootstrap BEFORE creating our first unfinished paid run
                except Exception as e:
                    print(f'collector: bootstrap failed ({classify(e)})')
                    run_due(c, ['health'], min(120, max(1, a.step_timeout)), min(600, max(61, a.total_timeout)))
                    return 1
                return run_due(c, kinds, min(120, max(1, a.step_timeout)), min(600, max(61, a.total_timeout)))
            finally: c.close()
    except BlockingIOError:
        print('collector: already active; no second start'); return 0

if __name__ == '__main__': raise SystemExit(main())
