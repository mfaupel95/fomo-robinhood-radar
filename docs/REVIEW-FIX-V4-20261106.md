# R1/R2 review correction — NOT ACTIVATED

Base: f0b12a66514ee5223be4f104f64a6d4d75ff9597. Independent review is dispatched separately; this change grants no activation or merge permission.

R1: enrich explicitly invokes safety.sweep(notify=False), propagated to check. An active EnrichBudget context additionally forbids check's notification dispatcher even if a nested caller supplies notify=True. Safety verdict/note/check timestamp are still committed. Outside enrichment, existing Safety callers retain their normal default notification behavior; notify=False is also available explicitly. Suppressed notifications are not queued for later delivery and no delivery guarantee is claimed.

R2: SharedRateLimiter.wait with an explicit budget or the active enrichment context must obtain a shared claim, including when a previous unguarded caller marked the instance broken. Guarded take also enforces shared reserve and spacing; guarded room refuses a non-atomic preflight. SQLite claim errors raise SharedLimitUnavailable, record error type/shared_reservation=false/transient/collector_backoff in the enrichment diagnostics, and propagate through lookup/date/safety optional-error catches. Collector classifies the exception transient; the existing persistent backoff remains unchanged (60/120/240 seconds, then six hours). Ordinary unguarded callers keep legacy local fallback, deliberately not changed globally. This is not the separate atomic 1000-credit guard.

Offline regressions cover normal/explicitly muted/context-guarded safety plus persisted findings; missing/corrupt/failed/already-broken limiter; real enrich -> worker -> recovery failure and 60s persisted backoff with no HTTP; four concurrent real child processes sharing reserve and minimum spacing. Original v3 reviewer tests remain external and unchanged.

No original DB, production import, live HTTP, messages, orders, restarts or integration. Cooperative SQLite/lock/DNS limits remain subject to the unchanged independent 120s worker self-timer; startup and cleanup are not a <=120s wallclock guarantee.

Unresolved: actual running worker import SHA and original DB-derived lock path; independent acceptance and Max's activation authorization; central house report and analyze/CLI/report/API/bot/board PnL consumers. sellable=1 is not proof of a fresh price or size-dependent executable net proceeds. See external ABSCHLUSS-v4-fix.md for exact test outputs and final commit.
