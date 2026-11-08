"""Acceptance of existing v5 price semantics, no new enrichment implementation."""
from types import SimpleNamespace
import pytest
from fomo_agent import db
from fomo_agent.pipeline import new_tokens as nt

@pytest.mark.parametrize('price', [None, 0, -1, float('nan'), float('inf'), float('-inf'), 8.0])
def test_refresh_success_requires_positive_finite_response(tmp_path, monkeypatch, price):
    c = db.connect(tmp_path / 'fixture.db')
    old = db.now() - 999999
    db.upsert_token(c, 'a', chain='robinhood', price_usd=8, price_at=old)
    c.commit()
    monkeypatch.setattr(nt, 'unnamed_tokens', lambda *a: [{'chain': 'robinhood', 'token': 'a'}])
    monkeypatch.setattr(nt, 'stale_price_tokens', lambda *a: [])
    monkeypatch.setattr(nt, 'undated_tokens', lambda *a: [])
    monkeypatch.setattr('fomo_agent.pipeline.safety.sweep', lambda *a, **kw: {})
    token = SimpleNamespace(mint='a', chain='robinhood', symbol='A', mcap_usd=None,
                            liquidity_usd=None, volume_usd=None, created_at=None,
                            decimals=None, price_usd=price, pool_address=None)
    monkeypatch.setattr(nt, 'lookup_tokens', lambda *a, **kw: ([token], 1))
    result = nt.enrich_tokens(c)
    row = c.execute("SELECT price_usd,price_at,checked_at FROM tokens WHERE mint='a'").fetchone()
    assert row['price_usd'] == 8
    assert row['checked_at'] > old
    if price == 8:
        assert row['price_at'] > old and result['priced'] == 1
    else:
        assert row['price_at'] == old and result['priced'] == 0
    c.close()
