"""Sammler: fuehrt die faelligen run-Schritte aus, ohne sie bei jedem Aufruf zu wiederholen.

Warum nicht `run --once`: das setzt alle Intervalle auf "faellig" (-inf) und macht damit bei
einem 2-h-Cron JEDEN fomoapi-Schritt mit - 84 statt 31 Credits am Tag. Hier wird der letzte
Lauf je Schritt aus der `runs`-Tabelle gelesen, also ueberlebt das Intervall den Prozess.

Budget-Regel (Max): die 1.000 Credits im Monat duerfen verbraucht werden, mehr nicht.
"""
from __future__ import annotations

import sys

sys.path.insert(0, r"O:/Werkstatt/fomo-robinhood-radar")

from fomo_agent import db
from fomo_agent.config import settings
from fomo_agent.pipeline import collect_api, holdings as hd, listings, new_tokens as nt, score as sc, track as tr

# kind -> (intervall_s, aufruf)
def build_steps():
    band = settings.fomoapi_key
    return {
        "fomoapi_24h": (2 * 3600, lambda c: collect_api.collect(c, ("24h",), None) if band else {"skipped": "no key"}),
        "fomoapi_7d": (6 * 3600, lambda c: collect_api.collect(c, ("7d",), None) if band else {"skipped": "no key"}),
        "fomoapi_theses": (8 * 3600, lambda c: collect_api.collect(c, (), 1) if band else {"skipped": "no key"}),
        "enrich_tokens": (settings.track_interval, nt.enrich_tokens),
        "holdings": (settings.track_interval, hd.mark_holdings),
        "score": (settings.track_interval * 10, sc.score_all),
        "listings": (settings.new_tokens_interval, listings.sweep),
    }


def last_run(conn, kind: str):
    row = conn.execute("SELECT MAX(started_at) FROM runs WHERE kind=? AND finished_at IS NOT NULL",
                       (kind,)).fetchone()
    return row[0] if row and row[0] else None


def run_step(kind: str, fn) -> dict:
    """Wie cli._run: eine `runs`-Zeile drumherum, Fehler werden protokolliert statt geworfen."""
    conn = db.connect()
    rid = db.run_start(conn, kind)
    try:
        stats = fn(conn)
        db.run_finish(conn, rid, stats)
        return stats
    except Exception as e:  # noqa: BLE001 - ein Schritt darf den Sammler nicht kippen
        db.run_finish(conn, rid, error=repr(e)[:500])
        return {"error": f"{type(e).__name__}: {str(e)[:120]}"}


def main() -> None:
    conn = db.connect()
    conn.text_factory = lambda b: b.decode("utf-8", "replace")
    now = db.now()
    done = []
    for kind, (interval, fn) in build_steps().items():
        last = last_run(conn, kind)
        if last is not None and now - last < interval:
            continue
        stats = run_step(kind, fn)
        done.append(kind)
        print(f"{kind}: {stats}")
    if not done:
        print("")  # leer = nichts faellig -> kein Versand (Watchdog-Muster)


if __name__ == "__main__":
    main()
