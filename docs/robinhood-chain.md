# Robinhood Chain, as measured

Everything here was read off the chain in September 2026 and is what `sources/rpc.py` is built on.
None of it is documented publicly, so re-measure before trusting it if something stops working.

## The chain

| | |
|---|---|
| chain id | `4663` (`0x1237`) |
| public RPC | `https://rpc.mainnet.chain.robinhood.com` |
| block time | ~0.1008s — about ten blocks a second |
| throughput | ~47,000 ERC-20 Transfer logs per 1,000 blocks (~470/s) |
| DexScreener / Codex id | `robinhood` |

## Talking to the RPC

- **It rejects the default httpx user agent with 403.** Any browser-shaped UA works; `RPC_USER_AGENT`
  carries one. This is the single most likely reason a fresh clone sees nothing.
- **It 429s on bursts** well before it returns anything wrong. `RPC_MAX_PER_MIN` throttles, and every
  429 is retried with a growing backoff.
- **`eth_getLogs` serves about 200,000 blocks per query** — roughly 5.6 hours. Ask for a million and
  it answers `{"code": -32000, "message": "log query timed out"}`. Deeper history needs chunking.
- **Topic arrays work.** `topics: [TRANSFER, [w1, w2, … w300], null]` means "sender is any of these",
  which is what lets two requests cover an entire roster. This is the whole reason Codex is optional.
- **JSON-RPC batching works.** Forty `eth_getTransactionReceipt` calls in one POST come back in about
  a second.
- **Block timestamps are worth interpolating, not fetching.** Two probes date every log in a recent
  window to the second. Over months the chain's pace has changed enough that a straight line drifts
  by hours, so `RobinhoodRPC.block_at` refines its estimate against the block it lands on.

## What a fomo trade looks like

A relayer submits the transaction, so **the trader's wallet is never its `from`**. Searching by
sender finds nothing; searching Transfer logs by topic finds everything.

Every fill routes through one contract:

```
router  0x0729e2a4716d9f7dd17858d5d504426d228697f7     (RPC_ROUTERS, live since 2026-10-30)
router  0xb92fe925dc43a0ecde6c8b1a2709c170ec4fff4f     (retired, kept as a second entry)
```

The 2026-10-30 measurement that replaced the old one: across 147 tracked wallets and 24h of
Transfer logs, the old contract faced **0** legs while `0x0729e2a4…` carried **166** legs
(88 buys / 78 sells, 67 distinct tokens, 45 wallets). A tracker pass with it configured then
wrote the first two fills since 2026-10-26. Re-derive it the same way if the tape goes quiet
again: tally the counterparty of every wallet Transfer leg, and the address that appears on
both sides across many tokens is the router.

- token moves **router → wallet** = a buy
- token moves **wallet → router** = a sell
- any other counterparty is an airdrop, a transfer between a user's own accounts, or an LP move —
  and those are the majority of a wallet's log traffic

Measured over one 5.6-hour window across 302 wallets: 1,018 routed fills in 1,018 distinct
transactions. **Exactly one fill per transaction**, which is what makes the size unambiguous.

## Pricing a fill

The trade's size is the largest single hop of a quote asset inside the transaction. A swap moves the
same money through several hops — deposit, pool, payout — so summing them double-counts.

| | address | decimals | |
|---|---|---|---|
| USDG | `0x5fc5360d0400a0fd4f2af552add042d716f1d168` | 6 | dollar stablecoin; every pool prices against it |
| WETH | `0x0bd7d308f8e1639fab988df18a8011f41eacad73` | 18 | needs a USD price, taken from DexScreener |

Note that WETH here is **not** the OP-stack standard `0x4200…0006`, which does not exist on this
chain.

**Both are quote assets, never positions.** Sources that book a swap from the pool's side file "sold
token X for USDG" as a *USDG purchase*; left in, the stablecoin every trade passes through tops any
signal feed. `QUOTE_TOKENS` in `sources/rpc.py` is the list, and everything user-facing excludes it.

## Accuracy

Checked against the robinhoodtrenches.com tape over the same window:

| | |
|---|---|
| overlapping fills | 209 |
| side agrees | 209 / 209 |
| token agrees | 209 / 209 |
| median dollar error | 0.00% |
| within 5% | 184 / 209 |

The outliers are multi-hop aggregator routes where the largest quote hop belongs to a leg of the
route rather than the trader's own. Codex disagrees far more often, but that is a difference of
convention — it books the pool's side of the swap — rather than an error in either.

## Cost

A full pass over the roster: two `eth_getLogs`, two block probes, and one batched receipt call per
40 fills. About 30 requests for 302 wallets, none of them metered. Wallet resolution costs one
`eth_getLogs` per window (`RESOLVE_WINDOWS`, default 12) plus a few block probes that are cached
across the whole pass.
