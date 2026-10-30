"""Pydantic models shared across sources and pipeline."""
from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

WSOL_MINT = "So11111111111111111111111111111111111111112"
STABLE_MINTS = {
    "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v": "USDC",
    "Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB": "USDT",
}
QUOTE_MINTS = {WSOL_MINT, *STABLE_MINTS}

# decimals of known quote/liquidity tokens, used to convert raw amounts to human units
QUOTE_DECIMALS: dict[str, int] = {
    WSOL_MINT: 9,
    "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v": 6,   # USDC (solana)
    "Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB": 6,   # USDT (solana)
    "0x4200000000000000000000000000000000000006": 18,    # WETH (base / OP-stack L2s)
}


def norm_addr(addr: str) -> str:
    """EVM addresses are case-insensitive: store lowercase so sources agree. Solana base58 is left as is."""
    return addr.lower() if addr.startswith("0x") else addr


class TraderRow(BaseModel):
    """Normalized leaderboard entry from fomo.

    `address` is the profile address and is NOT what trades on-chain: fomo swaps run from a
    separate per-chain execution wallet, resolved via FomoClient.execution_addresses().
    """
    address: str
    fomo_user_id: str | None = None
    fomo_handle: str | None = None
    profile_address: str | None = None
    evm_address: str | None = None
    chain: str = "solana"
    pnl_24h: float | None = None
    pnl_7d: float | None = None
    pnl_30d: float | None = None
    win_rate: float | None = None
    trades_cnt: int | None = None
    volume_usd: float | None = None
    source: str


class HolderRow(BaseModel):
    """Normalized token-holder entry from fomo (with PnL when available)."""
    address: str
    fomo_user_id: str | None = None
    fomo_handle: str | None = None
    profile_address: str | None = None
    evm_address: str | None = None
    mint: str
    pnl_usd: float | None = None
    realized_pnl_usd: float | None = None
    cost_basis_usd: float | None = None
    value_usd: float | None = None
    balance: float | None = None
    avg_hold_seconds: int | None = None
    is_dev: bool = False
    # fomo's own id for the position, and the note the trader attached to it. The note is the only
    # field in this whole system that is stated rather than inferred.
    trade_id: str | None = None
    thesis: str | None = None


class NewToken(BaseModel):
    mint: str
    chain: str = "solana"
    symbol: str | None = None
    mcap_usd: float | None = None
    liquidity_usd: float | None = None
    price_usd: float | None = None
    decimals: int | None = None
    # the deepest pool this token trades in; the candle endpoint takes no other handle
    pool_address: str | None = None
    created_at: int | None = None  # unix seconds
    dex: str | None = None
    pair_address: str | None = None
    source: str = "dexscreener"
    # holder-quality signals (codex only for now); not persisted yet, available for scoring context
    holders: int | None = None
    top10_pct: float | None = None
    sniper_pct: float | None = None
    bundler_pct: float | None = None


class Trade(BaseModel):
    sig: str
    address: str
    chain: str = "solana"
    mint: str
    side: Literal["buy", "sell"]
    sol_amount: float | None = None
    token_amount: float | None = None
    usd_value: float | None = None
    ts: int
    source: str = "helius"
    # whose trade it is: `flow` came through fomo and is judged for size on insert, `direct` was
    # sent to the router by an outside key and is nobody's; see pipeline/provenance.py
    kind: str | None = None


class ScoreResult(BaseModel):
    """Strict schema for Claude scoring output."""
    score: int = Field(ge=0, le=100)
    status: Literal["active", "watch", "dropped"]
    style: list[Literal["sniper", "swing", "scalper", "holder", "copy-follower"]] = []
    red_flags: list[Literal["bot", "bundler", "insider-like", "wash", "one-hit", "distributing"]] = []
    summary: str
    confidence: float = Field(ge=0, le=1)
