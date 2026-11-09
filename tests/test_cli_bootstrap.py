"""Real CLI split action and reservation; MockTransport and scratch DB only."""
import ast
from pathlib import Path
import httpx
from fomo_agent import db, cli, credit_guard
from fomo_agent.config import settings
from fomo_agent.pipeline import collect_api
from fomo_agent.sources.fomoapi import FomoApi


def action():
    tree = ast.parse(Path(cli.__file__).read_text(encoding='utf-8'))
    fn = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'run')
    steps = next(n.value for n in fn.body if isinstance(n, ast.Assign)
                 and any(isinstance(t, ast.Name) and t.id == 'steps' for t in n.targets))
    entry = next(n for n in steps.elts if n.elts[0].value == 'fomoapi_24h')
    return eval(compile(ast.fix_missing_locations(ast.Expression(entry)), 'review-step', 'eval'),
                {'settings': settings})[2]


def setup(tmp_path, monkeypatch):
    path = tmp_path / 'first-month.db'
    monkeypatch.setattr(settings, 'db_path', path)
    monkeypatch.setattr(settings, 'fomoapi_key', 'fixture-only')
    monkeypatch.setattr(settings, 'fomoapi_monthly_credits', 1000)
    monkeypatch.setattr(settings, 'fomoapi_thesis_pages', 0)
    c = db.connect(path)
    c.close()
    calls = []

    def reply(request):
        calls.append(request.url.path)
        return httpx.Response(200, json=[])

    api = FomoApi('fixture-only', httpx.Client(base_url='https://fixture.invalid',
                                            transport=httpx.MockTransport(reply)))
    monkeypatch.setattr(collect_api, 'FomoApi', lambda: api)
    return path, calls


def test_new_cli_split_initializes_month_before_own_run(tmp_path, monkeypatch):
    path, calls = setup(tmp_path, monkeypatch)
    result = cli._run('fomoapi_24h', action())
    with db.connect(path) as c:
        used = c.execute('select used from fomo_credit_month').fetchone()[0]
        error = c.execute('select error from runs order by id desc limit 1').fetchone()[0]
    assert result is not None, f'own run blocked: used={used}, error={error}, mock_calls={len(calls)}'
    assert used == 1 and len(calls) == 1


def test_same_action_after_collector_bootstrap_succeeds(tmp_path, monkeypatch):
    path, calls = setup(tmp_path, monkeypatch)
    assert credit_guard.reserve(0, path) == 0
    assert cli._run('fomoapi_24h', action()) is not None
    assert len(calls) == 1
    with db.connect(path) as c:
        assert c.execute('select used from fomo_credit_month').fetchone()[0] == 1


def test_unknown_history_still_blocks_without_http(tmp_path, monkeypatch):
    path, calls = setup(tmp_path, monkeypatch)
    with db.connect(path) as c:
        db.run_start(c, 'fomoapi_7d')
    result = cli._run('fomoapi_24h', action())
    # collect reports a budget stop before requesting; the durable cap must remain closed.
    assert result is None or result.get('budget_stop')
    assert calls == []
    with db.connect(path) as c:
        assert c.execute('select used from fomo_credit_month').fetchone()[0] == 1000
