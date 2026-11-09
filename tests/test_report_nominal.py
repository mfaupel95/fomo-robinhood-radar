"""A sell check is not a size-specific executable quote."""
from fomo_agent.pipeline import report


def test_sell_checked_marks_are_not_official_executable_pnl(monkeypatch):
    from fomo_agent.pipeline import analyze
    monkeypatch.setattr(analyze, 'cohort_pnl', lambda *a, **k: {
        'positions': [{}],
        'realizable': {'pnl': 10, 'cost': 100, 'positions': 1},
        'paper': {'pnl': 0, 'cost': 0, 'positions': 0},
        'unchecked': {'pnl': 0, 'cost': 0, 'positions': 0},
    })
    text = '\n'.join(report._pnl_section(None))
    assert 'official figure: realizable' not in text
    assert 'realizable**' not in text
    assert 'nominal' in text.lower()
    assert 'NEVER executable proceeds' in text
    assert 'freshness' in text.lower()
