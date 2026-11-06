"""Read-only before/after evidence against one real SQLite snapshot; no network."""
from pathlib import Path
import argparse
import importlib.util
import json
import sqlite3
from fomo_agent.pipeline import data_quality, health, report, new_tokens


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--db', required=True)
    p.add_argument('--before-health', required=True)
    p.add_argument('--output', required=True)
    a = p.parse_args()
    c = sqlite3.connect(Path(a.db).resolve().as_uri()+'?mode=ro', uri=True)
    c.row_factory = sqlite3.Row
    c.execute('PRAGMA query_only=ON')
    c.execute('BEGIN')
    spec = importlib.util.spec_from_file_location('fomo_agent.pipeline.health_before', a.before_health)
    assert spec is not None and spec.loader is not None
    before = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(before)
    def rows(sql): return [dict(r) for r in c.execute(sql)]
    identity = rows('SELECT mint,chain FROM tokens ORDER BY mint')
    ledger = rows('SELECT * FROM fomo_credit_month')
    result = {'before_health':before.report(c,local_only=True), 'after_health':health.report(c,local_only=True),
              'quality':data_quality.snapshot(c), 'backoff':rows('SELECT * FROM sammler_recovery'),
              'recent_enrich':rows("SELECT id,started_at,finished_at,error,stats_json FROM runs WHERE kind='enrich_tokens' ORDER BY id DESC LIMIT 5"),
              'refresh_selection':[dict(r) for r in new_tokens.stale_price_tokens(c)],
              'credit_ledger_before':ledger,
              'stable_id_links':rows("SELECT u.user_id,t.address,t.chain,t.source FROM fomo_users u JOIN traders t ON t.fomo_user_id=u.user_id WHERE u.onchain_address IS NULL"),
              'schema':{t:rows('PRAGMA table_info('+t+')') for t in ('tokens','traders','fomo_users','fomo_credit_month','fomo_credit_reservations')}}
    destination = Path(a.output)
    destination.mkdir(parents=True,exist_ok=True)
    (destination/'candidate-report.txt').write_text(report.build_report(c),encoding='utf8')
    result['credit_ledger_after'] = rows('SELECT * FROM fomo_credit_month')
    result['identity_unchanged'] = identity == rows('SELECT mint,chain FROM tokens ORDER BY mint')
    result['total_changes'] = c.total_changes
    result['query_only'] = c.execute('PRAGMA query_only').fetchone()[0]
    (destination/'evidence.json').write_text(json.dumps(result,indent=2),encoding='utf8')
    print(json.dumps({k:result[k] for k in ('credit_ledger_before','credit_ledger_after','identity_unchanged','total_changes','query_only')}))
    print('before', result['before_health']['failing'], 'BAD', 'after', result['after_health']['counts'])
    print('quality',result['quality']['counts'],'without wallet',result['quality']['unresolved_users'],'stable links',len(result['stable_id_links']))
    c.rollback()
    c.close()

if __name__ == '__main__': main()
