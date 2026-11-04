"""v2 review reproductions: real holdings adapter, temporary DBs, no network."""
import json

import pytest
from fomo_agent import collector as co, db
from fomo_agent.config import settings
from fomo_agent.pipeline import holdings
from fomo_agent.sources.rpc import RpcError


@pytest.fixture
def store(tmp_path, monkeypatch):
    path = tmp_path / 'review.db'
    c = db.connect(path)
    monkeypatch.setattr(settings, 'db_path', path)
    yield c
    c.close()


@pytest.mark.parametrize('partial', [False, True])
def test_real_holdings_rpc_stop_is_failed_then_recovers(store, monkeypatch, partial):
    c = store
    pairs = [('wallet', f'token{i}') for i in range(6 if partial else 1)]
    monkeypatch.setattr(holdings, 'stale_pairs', lambda *a: pairs)
    monkeypatch.setattr(settings, 'rpc_batch_size', 1)

    class RPC:
        requests = 0
        fail = True

        def load_decimals(self, values):
            pass

        def known_decimals(self):
            return {}

        def balances(self, batch):
            self.requests += 1
            if self.fail and (not partial or self.requests == 2):
                raise RpcError('review-only simulated transient RPC failure')
            return {pair: 7.0 for pair in batch}

    rpc = RPC()
    monkeypatch.setattr(co, 'build_steps', lambda: {
        'holdings': (3600, lambda conn: holdings.mark_holdings(conn, rpc=rpc))})

    def runner(args, timeout):
        return co.worker_locked(args[-3], int(args[-1]))

    assert co.run_due(c, ['holdings'], runner=runner) == 1
    row = c.execute('SELECT * FROM runs ORDER BY id DESC').fetchone()
    assert row['error'] == 'transient'
    assert 'stopped' in json.loads(row['stats_json'])
    assert co.last_run(c, 'holdings') is None
    assert c.execute('SELECT count(*) FROM holdings').fetchone()[0] == (5 if partial else 0)
    state = c.execute('SELECT * FROM sammler_recovery').fetchone()
    assert state['reason'] == 'transient' and state['next_at'] >= db.now() + 59
    requests = rpc.requests
    assert co.run_due(c, ['holdings'], runner=runner) == 1
    assert rpc.requests == requests
    c.execute('UPDATE sammler_recovery SET next_at=0'); c.commit()
    rpc.fail = False
    assert co.run_due(c, ['holdings'], runner=runner) == 0
    assert co.last_run(c, 'holdings') is not None
    assert c.execute('SELECT count(*) FROM holdings').fetchone()[0] == len(pairs)


def test_historical_stopped_attempt_is_not_success(store):
    rid = db.run_start(store, 'holdings')
    db.run_finish(store, rid, {'stopped': 'after 0 of 1 pairs'})
    assert co.last_run(store, 'holdings') is None


def test_review_deadline_still_evaluates_health(store, monkeypatch):
    calls = []
    monkeypatch.setattr(co, 'build_steps', lambda: {'holdings': (60, None), 'health': (60, None)})
    clock = iter([0, 0, 0, 2])
    monkeypatch.setattr(co.time, 'monotonic', lambda: next(clock, 2))

    def done(args, timeout):
        calls.append(args[-3])
        db.run_finish(store, int(args[-1]), {'ok': True})
        return 0

    assert co.run_due(store, ['holdings', 'health'], total_timeout=1, runner=done) == 1
    assert calls.count('health') == 1


def test_four_historical_gap_bads_never_suppress_fresh_health(store, monkeypatch):
    co.init_state(store)
    for _ in range(4):
        co.failure_state(store, 'health', 'health', db.now())
    calls = []
    monkeypatch.setattr(co, 'build_steps', lambda: {'health': (60, lambda c: {'ok': False})})

    def runner(args, timeout):
        calls.append(args[-3])
        return co.worker_locked(args[-3], int(args[-1]))

    for _ in range(2):
        assert co.run_due(store, ['health'], runner=runner) == 1
    assert calls == ['health', 'health']
    assert co.last_run(store, 'health') is None
    monkeypatch.setattr(co, 'build_steps', lambda: {'health': (60, lambda c: {'ok': True})})
    assert co.run_due(store, ['health'], runner=runner) == 0


@pytest.mark.parametrize('reason', ['budget', 'auth', 'transient', 'exception'])
def test_closing_health_after_collection_failure(store, monkeypatch, reason):
    calls = []
    monkeypatch.setattr(co, 'build_steps', lambda: {'fomoapi_24h': (60, None), 'health': (60, None)})

    def runner(args, timeout):
        kind, rid = args[-3], int(args[-1])
        calls.append(kind)
        if kind == 'health':
            db.run_finish(store, rid, {'ok': True}); return 0
        if reason == 'exception':
            raise OSError('review runner failed')
        db.run_finish(store, rid, error=reason); return 1

    assert co.run_due(store, ['fomoapi_24h', 'health'], runner=runner) == 1
    assert calls == ['fomoapi_24h', 'health']
    # A blocked collection still receives a fresh closing health.
    assert co.run_due(store, ['fomoapi_24h', 'health'], runner=runner) == 1
    assert calls[-1] == 'health' and calls.count('health') == 2


def test_collection_reserves_health_and_cleanup_inside_total(store, monkeypatch):
    clock = [0.0]
    calls = []
    monkeypatch.setattr(co.time, 'monotonic', lambda: clock[0])
    monkeypatch.setattr(co, 'build_steps', lambda: {'holdings': (60, None), 'health': (60, None)})

    def timeout(args, limit):
        calls.append((args[-3], limit))
        clock[0] += limit + 30  # worst-case existing bounded kill/reap allowance
        return 124

    assert co.run_due(store, ['holdings', 'health'], total_timeout=180, runner=timeout) == 1
    assert [kind for kind, _ in calls] == ['holdings', 'health']
    assert clock[0] <= 180
    assert calls[-1][1] > 0


@pytest.mark.parametrize('error', [co.BudgetBlocked('test'), co.AuthenticationError('test'), OSError('test')])
def test_bootstrap_failure_still_closes_with_health(store, monkeypatch, error):
    monkeypatch.setattr(co.sys, 'argv', ['sammler', '--only', 'holdings'])
    monkeypatch.setattr(co, 'reserve', lambda cost: (_ for _ in ()).throw(error))
    calls = []
    monkeypatch.setattr(co, 'build_steps', lambda: {
        'holdings': (60, lambda c: calls.append('holdings') or {}),
        'health': (60, lambda c: calls.append('health') or {'ok': True})})
    # Exercise main and real run_due/worker result handling without subprocess/network.
    original = co.run_due

    def inline(c, kinds, step_timeout, total_timeout):
        return original(c, kinds, step_timeout, total_timeout,
                        runner=lambda args, timeout: co.worker_locked(args[-3], int(args[-1])))

    monkeypatch.setattr(co, 'run_due', inline)
    assert co.main() == 1
    assert calls == ['health']


def test_real_local_health_keeps_historical_gap_bad_without_network(store, monkeypatch):
    from fomo_agent.pipeline import health
    now = db.now()
    with db.tx(store):
        for i in range(22):
            stamp = now - 5000 + i * 60 if i < 11 else now - 1000 + (i - 11) * 60
            store.execute("INSERT INTO trades(sig,address,chain,mint,side,ts,source) VALUES (?, 'w', 'robinhood', 't', 'buy', ?, 'rpc')", (f's{i}', stamp))
    result = health.report(store, local_only=True)
    gap = next(check for check in result['checks'] if check['name'] == 'watcher gaps')
    assert not result['ok'] and not gap['ok']
    assert '56 min' in gap['detail']
    # The no-fill/active-roster fallback must also stay local and fail closed.
    store.execute('DELETE FROM trades')
    store.execute("INSERT INTO traders(address,chain,status) VALUES ('w','robinhood','active')")
    store.commit()
    monkeypatch.setattr(health, 'RobinhoodRPC', lambda: pytest.fail('closing health attempted network'))
    router = health.router_alive(store, local_only=True)
    assert not router['ok'] and 'local closing health' in router['detail']


def test_supervisor_deadline_watchdog_is_cancelled(store, monkeypatch):
    events = []

    class Timer:
        def __init__(self, seconds, callback):
            events.append(seconds)

        def start(self):
            events.append('start')

        def cancel(self):
            events.append('cancel')

    monkeypatch.setattr(co.threading, 'Timer', Timer)
    monkeypatch.setattr(co, 'build_steps', lambda: {})
    assert co.run_due(store, [], total_timeout=180) == 0
    assert events == [180, 'start', 'cancel']
