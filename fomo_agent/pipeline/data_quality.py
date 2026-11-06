"""Local-only evidence report. Never resolves identities or refreshes markets."""
from __future__ import annotations
import re
import sqlite3
from .. import db
from ..config import settings


def valid_token(chain, token):
    if chain in ('robinhood', 'ethereum', 'base', 'bsc', 'arbitrum', 'polygon'):
        return bool(re.fullmatch(r'0x[0-9a-fA-F]{40}', token or ''))
    if chain == 'solana':
        # Decode base58, not merely a display-length check.
        alphabet = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
        try:
            n = 0
            for char in token:
                n = n * 58 + alphabet.index(char)
            size = (n.bit_length() + 7) // 8 + len(token) - len(token.lstrip('1'))
            return size == 32
        except (ValueError, TypeError):
            return False
    return None


def snapshot(conn: sqlite3.Connection) -> dict:
    now = db.now()
    tokens = [dict(r) for r in conn.execute('SELECT mint,chain,symbol,price_usd,price_at,checked_at,created_at,first_seen_at FROM tokens')]
    for row in tokens:
        row['identity_valid'] = valid_token(row['chain'], row['mint'])
        row['price_age_s'] = now - row['price_at'] if row['price_at'] is not None else None
        age = row['price_age_s']
        row['stale'] = row['price_usd'] is None or age is None or not 0 <= age <= settings.price_max_age_s
    users = conn.execute('SELECT COUNT(*) FROM fomo_users WHERE onchain_address IS NULL').fetchone()[0]
    # No handle/prefix joins. A missing authoritative identity link remains missing.
    without_any = conn.execute('SELECT COUNT(*) FROM fomo_users WHERE onchain_address IS NULL AND evm_address IS NULL AND profile_address IS NULL').fetchone()[0]
    return {'at':now, 'tokens':tokens, 'unresolved_users':users, 'users_without_any_address':without_any,
            'price_max_age_s':settings.price_max_age_s,
            'counts':{'tokens':len(tokens),'invalid_identity':sum(t['identity_valid'] is False for t in tokens),
                      'priced':sum(t['price_usd'] is not None for t in tokens),
                      'fresh':sum(not t['stale'] for t in tokens)}}


def text(conn: sqlite3.Connection) -> str:
    from .health import report
    evidence = snapshot(conn)
    h = report(conn, local_only=True)
    out = [f"Health: {h['status']} {h['counts']}",
           'UNKNOWN is missing evidence, not clearance and not a paid-retry instruction.',
           f"Wallets: {evidence['unresolved_users']} users without onchain wallet; {evidence['users_without_any_address']} without any stored address.",
           f"Prices: {evidence['counts']}; freshness limit {evidence['price_max_age_s']}s.",
           'All values are nominal marks, NEVER executable proceeds; size/slippage/fees/exit unknown.',
           'Tokens (full stored identity, no symbol or prefix substitution):']
    for t in sorted(evidence['tokens'], key=lambda r:r['first_seen_at'] or 0, reverse=True)[:6]:
        out.append(f"{t['chain']} {t['mint']} {t['symbol'] or '-'} identity={t['identity_valid']} price_at={t['price_at']} {'STALE' if t['stale'] else 'fresh nominal'} created_at={t['created_at']} (historical listing timestamp)")
    out.append('Current top wealth: excluded here unless balance AND price freshness are proved; stale marks are not current wealth.')
    return '\n'.join(out)
