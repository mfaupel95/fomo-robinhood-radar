#!/usr/bin/env bash
# Keep the watchlist fresh while nobody is at the keyboard.
# Tracking runs on the free Robinhood RPC, so a pass costs nothing from the Codex budget.
set -u
PY="env -u PYTHONPATH .venv/Scripts/python"
export PYTHONIOENCODING=utf-8
passes=${1:-20}
sleep_s=${2:-720}
for i in $(seq 1 "$passes"); do
  echo "=== pass $i/$passes $(date -u +%H:%M:%S) ==="
  $PY -m fomo_agent.cli track --limit 302 2>&1 | tail -1
  $PY -m fomo_agent.cli enrich-tokens --limit 300 2>&1 | tail -1
  [ "$i" -lt "$passes" ] && sleep "$sleep_s"
done
echo "=== loop done ==="
