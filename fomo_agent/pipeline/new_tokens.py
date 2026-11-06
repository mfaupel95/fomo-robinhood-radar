"""Poll DexScreener for fresh high-mcap tokens; on a new one, trigger discover_holders (if fomo works)."""
from __future__ import annotations

import logging
import sqlite3
import json
import math

from .. import db
from ..config import settings
from ..models import NewToken
from ..enrich_budget import EnrichBudget, Deadline, current
from ..sources.dexscreener import DexScreener, parse_pair
from ..sources.filters import filter_tokens
from ..sources.fomo import norm_addr
from ..sources.fomo import FomoClient, FomoError
from .discover import discover_holders, discover_makers

log = logging.getLogger(__name__)


def fetch_new_tokens(sources: tuple[str, ...] | None = None) -> list[NewToken]:
    """Union of all configured sources, deduped per (chain, mint), thresholds from config."""
    tokens: list[NewToken] = []
    for name in sources or settings.token_sources:
        try:
            if name == "dexscreener":
                tokens.extend(DexScreener().new_tokens())
            elif name == "geckoterminal":
                from ..sources.geckoterminal import GeckoTerminal
                tokens.extend(GeckoTerminal().new_tokens())
            elif name == "codex":
                if not settings.codex_api_key:
                    log.debug("codex source skipped: CODEX_API_KEY not set")
                    continue
                from ..sources.codex import Codex
                tokens.extend(Codex().new_tokens())
            else:
                log.warning("unknown token source %r", name)
        except Exception as e:  # noqa: BLE001 - one source down must not kill the trigger
            log.warning("token source %s failed: %s", name, e)
    return filter_tokens(
        tokens, min_mcap=settings.new_token_min_mcap_usd, max_age_hours=settings.new_token_max_age_hours,
        min_liquidity=settings.new_token_min_liquidity_usd, max_mcap=settings.new_token_max_mcap_usd,
    )


def stale_price_tokens(conn: sqlite3.Connection, limit: int | None = None,
                       max_age_s: int | None = None) -> list[sqlite3.Row]:
    """Tokens a tracked wallet still has money in, that nobody has asked about recently enough.

    Only what a wallet actually bought is worth quoting: pricing every address the tape has ever
    seen would spend hundreds of requests on names nobody holds. The queue turns on when each was
    last *asked* about rather than on whether it has a price, because a token no source indexes
    would otherwise sit at the front of it forever and starve the ones that do.
    """
    now = db.now()
    max_age = now - (settings.price_max_age_s if max_age_s is None else max_age_s)
    cold = now - settings.price_cold_max_age_s
    hot_since = now - settings.price_hot_days * 86400
    return conn.execute(
        "SELECT u.token AS token, u.chain AS chain, MAX(u.hot) AS hot FROM ("
        "  SELECT mint AS token, chain, (ts >= ?) AS hot FROM trades WHERE side='buy' AND ts >= ?"
        "  UNION ALL SELECT token, chain, 1 FROM fomo_positions WHERE closed_at IS NULL"
        "  UNION ALL SELECT h.token, t.chain, 1 FROM holdings h JOIN traders t ON t.address = h.address WHERE h.amount > 0"
        ") u JOIN tokens t ON t.mint = u.token "
        "WHERE u.chain IS NOT NULL AND (t.checked_at IS NULL OR t.checked_at < ?) "
        # a token that cannot be sold is re-quoted once a day, not every two hours: its price
        # marks nothing anybody can realise, and each ask was a single-token call the screener
        # answered 429 to (278 a day, the same two dozen trap tokens)
        "AND (COALESCE(t.sellable, 1) != 0 OR COALESCE(t.checked_at, 0) < ?) "
        "GROUP BY u.token, u.chain "
        # and one the cohort last touched days ago and holds none of goes on the slow clock: the
        # queue was 3,502 tokens every two hours, and the screener said 429 five hundred times a day
        "HAVING MAX(u.hot) = 1 OR COALESCE(MAX(t.checked_at), 0) < ? "
        "ORDER BY MAX(u.hot) DESC, COALESCE(t.checked_at, 0) ASC LIMIT ?",
        (hot_since, now - settings.price_refresh_days * 86400, max_age, now - 86400, cold,
         limit or settings.price_refresh_limit),
    ).fetchall()


def undated_tokens(conn: sqlite3.Connection, limit: int) -> list[sqlite3.Row]:
    """Tokens with a pool but no launch time, the ones a reader is looking at first.

    A launch time is permanent, so this queue only ever shrinks. It is ordered by how recently the
    cohort traded the token because the fresh feed ranks by how early each wallet was, and a token
    nobody is buying today does not need a date tonight.
    """
    return conn.execute(
        "SELECT t.mint AS token, t.chain AS chain, t.pool_address AS pool, MAX(tr.ts) AS seen "
        "FROM tokens t JOIN trades tr ON tr.mint = t.mint "
        "WHERE t.created_at IS NULL AND t.pool_address IS NOT NULL AND t.chain IS NOT NULL "
        "GROUP BY t.mint ORDER BY seen DESC LIMIT ?", (limit,),
    ).fetchall()


def unnamed_tokens(conn: sqlite3.Connection, limit: int, max_age_s: int | None = None) -> list[sqlite3.Row]:
    """Addresses we have no name for, most recently traded first, skipping ones just asked about."""
    max_age = db.now() - (settings.price_max_age_s if max_age_s is None else max_age_s)
    return conn.execute(
        "SELECT u.token AS token, u.chain AS chain FROM ("
        "  SELECT mint AS token, chain, MAX(ts) AS seen FROM trades GROUP BY mint, chain"
        "  UNION ALL SELECT token, chain, 0 FROM fomo_positions"
        ") u LEFT JOIN tokens t ON t.mint = u.token "
        "WHERE u.chain IS NOT NULL AND (t.mint IS NULL OR t.symbol IS NULL) "
        "  AND (t.checked_at IS NULL OR t.checked_at < ?) "
        "GROUP BY u.token, u.chain ORDER BY MAX(u.seen) DESC LIMIT ?",
        (max_age, limit),
    ).fetchall()


def lookup_tokens(chain: str, mints: list[str], dex: DexScreener | None = None,
                  gecko: "GeckoTerminal | None" = None) -> tuple[list, int]:
    """Everything known about these addresses, from whichever source covers the chain.

    GeckoTerminal answers by address and returns the symbol, the decimals, the reserve and the
    price in one call, so it goes first. DexScreener is asked only about what came back empty —
    it indexes Solana and Base well and Robinhood Chain barely at all (measured 2026-09-08: three
    of thirty held tokens, and a price for none of them).
    """
    from ..sources.geckoterminal import GeckoTerminal

    found: dict[str, object] = {}
    requests = 0
    try:
        gecko = gecko or GeckoTerminal()
        for t in gecko.tokens(chain, mints):
            found[t.mint] = t
        requests += (len(mints) + 29) // 30
    except Exception as e:  # noqa: BLE001 - enrichment is optional, and one source down is not fatal
        if isinstance(e, Deadline):
            raise
        if current.get():
            current.get().record('geckoterminal', 'lookup', 'failure', chain=chain, mints=mints, error_type=type(e).__name__)
        log.warning("geckoterminal lookup failed for %s: %s", chain, e)

    missing = [m for m in mints if m not in found]
    if missing:
        try:
            pairs = (dex or DexScreener()).pairs_for(chain, missing)
            requests += (len(missing) + 29) // 30
            for p in pairs:
                t = parse_pair(p)
                if t and t.mint not in found:
                    found[t.mint] = t
        except Exception as e:  # noqa: BLE001
            if isinstance(e, Deadline):
                if not found:
                    raise
                current.get().record('dexscreener', 'lookup', 'deadline', chain=chain, mints=missing)
                return list(found.values()), requests
            if current.get():
                current.get().record('dexscreener', 'lookup', 'failure', chain=chain, mints=missing, error_type=type(e).__name__)
            log.warning("dexscreener lookup failed for %s: %s", chain, e)
    return list(found.values()), requests


def enrich_tokens(conn: sqlite3.Connection, dex: DexScreener | None = None, limit: int = 300,
                  budget_s: float | None = None) -> dict:
    """One bounded pass, with crash-surviving diagnostics in the existing runs table."""
    rid = db.run_start(conn, 'enrich_diagnostic')
    stats: dict = {'looked_up': 0, 'named': 0, 'priced': 0, 'requests': 0, 'dated': 0}
    budget = EnrichBudget(settings.enrich_budget_s if budget_s is None else budget_s)
    def persist():
        conn.execute('UPDATE runs SET stats_json=? WHERE id=?',
                     (json.dumps({**stats, **budget.snapshot()}), rid))
        conn.commit()
    budget.persist = persist
    token = current.set(budget)
    try:
        persist()
        _enrich_tokens(conn, dex, limit, stats)
        budget.check()
    except Deadline:
        stats['stopped'] = 'deadline'
        budget.record('enrich', 'batch', 'deadline')
    except Exception as exc:
        stats['stopped'] = 'failure'
        budget.record('enrich', 'batch', 'failure', error_type=type(exc).__name__)
        raise
    finally:
        current.reset(token)
        stats.update(budget.snapshot())
        stats['requests'] = stats['attempts']
        stats['errors'] = stats['failures']
        db.run_finish(conn, rid, stats, stats.get('stopped'))
    return stats


def _enrich_tokens(conn: sqlite3.Connection, dex, limit, stats) -> dict:
    """Name the tokens we only know by address, and re-quote the ones somebody is holding.

    Positions and fills both arrive as bare contract addresses, and an open position that cannot be
    priced is half an answer. Thirty addresses go per request, so a few hundred tokens cost a
    handful of them and no Codex budget. Names come first: an unnamed token on the signal feed is
    the one a reader is looking at right now.

    A name is permanent and a price is not, so the second pass re-asks about the tokens somebody is
    holding — bounded per pass, longest-unasked first, so the cost stays flat however large the
    book grows. Every address asked about is stamped whether or not an answer came back; that is
    what keeps the tokens no source indexes from monopolising the queue.
    """
    rows = unnamed_tokens(conn, limit)
    by_chain: dict[str, list[str]] = {}
    for r in rows:
        by_chain.setdefault(r["chain"], []).append(r["token"])
    for r in stale_price_tokens(conn):
        by_chain.setdefault(r["chain"], []).append(r["token"])

    stats['looked_up'] = len(rows)
    budget = current.get()
    batches = [(chain, mints[i:i+30]) for chain, values in by_chain.items()
               for mints in [sorted(set(values))] for i in range(0, len(mints), 30)]
    stats['stale'] = []
    for chain, mints in batches:
        for mint in mints:
            row = conn.execute('SELECT price_at FROM tokens WHERE mint=? AND chain=?', (mint, chain)).fetchone()
            if not row or row['price_at'] is None or row['price_at'] < db.now()-settings.price_max_age_s:
                stats['stale'].append({'chain': chain, 'mint': mint, 'price_at': row['price_at'] if row else None, 'stale': True})
    for chain, mints in batches:
        budget.check()
        budget.record('enrich', 'batch', 'attempt', chain=chain, mints=mints)
        tokens, requests = lookup_tokens(chain, mints, dex=dex)
        now = db.now()
        stats["requests"] += requests
        with db.tx(conn):
            for t in tokens:
                if t.chain != chain or t.mint not in mints:
                    continue
                valid_price = t.price_usd is not None and math.isfinite(t.price_usd) and t.price_usd > 0
                db.upsert_token(conn, t.mint, chain=t.chain, symbol=t.symbol, mcap_usd=t.mcap_usd,
                                liquidity_usd=t.liquidity_usd, volume_usd=t.volume_usd,
                                created_at=t.created_at,
                                decimals=t.decimals, price_usd=t.price_usd if valid_price else None,
                                pool_address=t.pool_address,
                                price_at=now if valid_price else None,
                                checked_at=now)
                stats["named"] += 1
                stats["priced"] += valid_price
            # An address nobody could answer for is stamped too, so it goes to the back of the
            # queue instead of being re-requested every pass for the rest of the project.
            answered = {t.mint for t in tokens}
            for mint in mints:
                if mint not in answered:
                    db.upsert_token(conn, mint, chain=chain, checked_at=now)
        for mint in mints:
            row = conn.execute('SELECT price_usd, price_at FROM tokens WHERE mint=? AND chain=?', (mint, chain)).fetchone()
            stats['stale'] = [r for r in stats['stale'] if (r['chain'], r['mint']) != (chain, mint)]
            if row and (row['price_at'] is None or row['price_at'] < now-settings.price_max_age_s):
                stats['stale'].append({'chain': chain, 'mint': mint, 'price_at': row['price_at'], 'stale': True})
        budget.record('enrich', 'batch', 'success', chain=chain, mints=mints, priced=stats['priced'])
        budget.check()
    # Third pass: when each pool opened. Only the pool endpoint carries it, so a token found on
    # our own tape arrives undated however well it is priced — and the fresh feed is ranked on
    # exactly that number. Cheap and permanent: thirty pools a request, and a token dated once is
    # never asked again.
    stats["dated"] = 0
    undated = undated_tokens(conn, settings.date_refresh_limit)
    if undated:
        from ..sources.geckoterminal import GeckoTerminal

        gt = GeckoTerminal()
        by_chain_pools: dict[str, dict[str, str]] = {}
        for r in undated:
            by_chain_pools.setdefault(r["chain"], {})[norm_addr(r["pool"])] = r["token"]
        for chain, pools in by_chain_pools.items():
            try:
                budget.check()
                ages = gt.pool_ages(chain, list(pools))
            except Exception as e:  # noqa: BLE001 - one dead source must not stop the pass
                if isinstance(e, Deadline):
                    raise
                log.warning("pool ages on %s failed: %s", chain, e)
                continue
            stats["requests"] += 1
            with db.tx(conn):
                for pool, created in ages.items():
                    mint = pools.get(pool)
                    if mint:
                        db.upsert_token(conn, mint, chain=chain, created_at=created)
                        stats["dated"] += 1

    # Fourth pass: can they be sold. The tokens the cohort touched today, a dozen a pass, the
    # stale ones first. A verdict of no is final and is not asked again.
    try:
        budget.check()
        from .safety import sweep
        stats["sell_check"] = sweep(conn, limit=settings.sell_check_per_pass)
    except Exception as e:  # noqa: BLE001 - the check is a guard, not the pass
        if isinstance(e, Deadline):
            raise
        log.warning("sell check sweep failed: %s", e)

    log.info("token enrichment: %s", stats)
    return stats


def poll_new_tokens(conn: sqlite3.Connection, dex: DexScreener | None = None, fomo: FomoClient | None = None,
                    discover: bool | None = None) -> dict:
    """Store fresh tokens; for the biggest new ones, pull their buyers as trader candidates."""
    found = dex.new_tokens() if dex else fetch_new_tokens()
    stats = {"checked": len(found), "new": 0, "holders_runs": 0, "maker_runs": 0, "candidates": 0, "errors": 0}
    fresh: list[NewToken] = []
    for t in found:
        with db.tx(conn):
            created = db.upsert_token(
                conn, t.mint, chain=t.chain, symbol=t.symbol, mcap_usd=t.mcap_usd,
                liquidity_usd=t.liquidity_usd, volume_usd=t.volume_usd, created_at=t.created_at,
            )
        if not created:
            continue
        stats["new"] += 1
        fresh.append(t)
        log.info("new token %s %s (%s) mcap=%.0f", t.chain, t.symbol, t.mint[:8], t.mcap_usd or 0)
        if fomo is not None:
            try:
                discover_holders(conn, t.mint, fomo)
                stats["holders_runs"] += 1
            except FomoError as e:
                stats["errors"] += 1
                log.warning("holders for %s failed: %s", t.mint[:8], e)

    # Codex discovery on the biggest fresh tokens (1 request each, so it is capped)
    use_codex = settings.codex_api_key and "codex" in settings.token_sources if discover is None else discover
    if use_codex:
        fresh.sort(key=lambda t: -(t.mcap_usd or 0))
        for t in fresh[: settings.discover_tokens_per_pass]:
            try:
                r = discover_makers(conn, t.mint, t.chain)
                stats["maker_runs"] += 1
                stats["candidates"] += r["new"]
            except Exception as e:  # noqa: BLE001
                stats["errors"] += 1
                log.warning("makers for %s failed: %s", t.mint[:8], e)
    return stats
