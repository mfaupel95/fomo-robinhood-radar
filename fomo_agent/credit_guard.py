"""Durable, fail-closed monthly reservations. Never refund an uncertain request."""
from __future__ import annotations

import calendar
import sqlite3
import time
from pathlib import Path

from .config import settings


class BudgetBlocked(RuntimeError):
    pass


def reserve(cost: float, path: Path | str | None = None, at: int | None = None) -> float:
    if cost < 0 or cost > 1000:
        raise BudgetBlocked('invalid credit cost')
    now = int(time.time()) if at is None else at
    t = time.gmtime(now)
    month = time.strftime('%Y-%m', t)
    start = calendar.timegm((t.tm_year, t.tm_mon, 1, 0, 0, 0))
    cap = min(1000, settings.fomoapi_monthly_credits or 1000)
    c = sqlite3.connect(str(path or settings.db_path), timeout=10)
    try:
        c.execute('BEGIN IMMEDIATE')
        c.execute('CREATE TABLE IF NOT EXISTS fomo_credit_month (month TEXT PRIMARY KEY, used REAL NOT NULL)')
        c.execute('CREATE TABLE IF NOT EXISTS fomo_credit_reservations (id INTEGER PRIMARY KEY, month TEXT, at INTEGER, cost REAL NOT NULL)')
        row = c.execute('SELECT used FROM fomo_credit_month WHERE month=?', (month,)).fetchone()
        if row is None:
            # Bootstrap once, atomically. Historical failed/unfinished paid passes have
            # unknown consumption: do not invent headroom by treating them as zero.
            uncertain = c.execute("SELECT count(*) FROM runs WHERE kind LIKE 'fomoapi%' AND started_at>=? AND (error IS NOT NULL OR finished_at IS NULL) AND coalesce(error,'') NOT LIKE 'FomoApiError(''FOMOAPI_KEY is not set %'", (start,)).fetchone()[0]
            used = c.execute("SELECT coalesce(sum(json_extract(stats_json,'$.credits')),0) FROM runs WHERE kind LIKE 'fomoapi%' AND started_at>=?", (start,)).fetchone()[0]
            used = 1000 if uncertain else float(used)
            c.execute('INSERT INTO fomo_credit_month VALUES (?,?)', (month, used))
        else:
            used = row[0]
        if used + cost > cap:
            c.commit()  # preserve fail-closed bootstrap, even on denial
            raise BudgetBlocked('monthly credit ceiling reached; operator review required')
        if cost == 0:
            c.commit()
            return used
        c.execute('UPDATE fomo_credit_month SET used=used+? WHERE month=?', (cost, month))
        c.execute('INSERT INTO fomo_credit_reservations(month,at,cost) VALUES (?,?,?)', (month, now, cost))
        c.commit()  # must be durable BEFORE the network call
        return used + cost
    finally:
        c.close()
