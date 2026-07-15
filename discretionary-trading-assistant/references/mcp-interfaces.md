# MCP Server Interfaces

The skill assumes four MCP servers. Exact tool names will differ from what's written here —
these are *capability roles*, not literal signatures. At session start, list the connected
servers' tools and map each tool you find onto a role below. If a tool's behavior is ambiguous,
prefer a cheap read-only call to discover its shape over guessing.

## 1. Broker proxy — Interactive Brokers (stocks, futures, forex, options)

Expected capability roles:

| Role | Typical operations | Notes |
|---|---|---|
| Market data | quote/snapshot, historical bars (1m→1D), depth/book | Use for verification of every price you reason about |
| Contract lookup | resolve symbol → contract (expiry, exchange, multiplier, tick size) | Futures: always resolve the *specific* contract month; never assume front month without checking |
| Account | balances, buying power, margin, open positions, open orders | Needed for heat checks before any new ticket |
| Orders | place / modify / cancel; order status | **Confirmation-gated** — see below |
| P&L | realized/unrealized by position | For management and journaling |

## 2. Exchange proxy — Kraken (crypto)

| Role | Typical operations | Notes |
|---|---|---|
| Market data | ticker, OHLC, order book, recent trades | Pairs use Kraken naming (XBT for BTC in some endpoints) |
| Account | balances, open positions/orders | Spot balances are per-asset, not per-position |
| Orders | place / modify / cancel | **Confirmation-gated** |
| Fees/funding | fee tier, margin/funding info if using Kraken margin or futures | Funding cost matters for holds > a day |

## 3. News feed

| Role | Typical operations | Notes |
|---|---|---|
| Headline search | by symbol, keyword, time range | Run for every symbol before finalizing a plan |
| Economic calendar | scheduled events with impact rating | Check at session start and before any plan whose hold period crosses an event |
| Sentiment/summary | if offered | Treat as one input, never as the thesis |

## 4. RAG store (strategies, playbook, journal, profile)

| Role | Typical operations | Notes |
|---|---|---|
| Query/retrieve | semantic search over stored docs | Query for: trader profile, playbook setups matching current conditions, prior trades on this symbol/setup |
| Upsert/store | add or update documents | Used for journaling (see journaling.md) and profile updates |

## Order safety protocol (applies to both brokers)

- An order-placing tool may only be called after the trader confirms the exact ticket in
  conversation: symbol/contract, direction, quantity, order type, limit/stop prices, and time in
  force. Restate the ticket and get an explicit yes. One confirmation covers one order (a bracket
  entry+stop+target counts as one ticket if presented together).
- After placing, immediately query order status and read back the broker's response verbatim
  (order id, status, fill price). Never report an order as placed based only on your own call —
  confirm from the broker's acknowledgment.
- Never park stop or target orders "to be activated later" without the trader knowing they are
  live orders.
- If an order tool errors, report the exact error and do not retry with modified parameters
  without asking — a rejected order is often the risk system doing its job (margin, size limits).

## Graceful degradation

| Missing server | What you lose | How to proceed |
|---|---|---|
| IBKR proxy | live quotes/positions for stocks/futures/forex | Analyze from screenshots and trader-supplied prices; label everything **unverified**; no sizing against live margin |
| Kraken proxy | crypto data and orders | Same as above for crypto pairs |
| News feed | catalyst awareness | State clearly that you cannot rule out scheduled events; ask the trader to check the calendar for high-impact releases before acting |
| RAG store | profile, playbook, journal | Ask for account size and risk unit each session; journal to a local markdown file in the working directory and tell the trader where it is so it can be imported later |

Never silently pretend a capability exists. If the trader asks for something a missing server
would provide, say which server is missing and what you did instead.
