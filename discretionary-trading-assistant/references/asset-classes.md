# Asset-Class Mechanics

Instrument-specific facts that change the analysis or the arithmetic. When a broker MCP can
answer authoritatively (contract specs, margin, hours), prefer it over this file — this file is
the fallback and the checklist of what to look up.

## Futures (via IBKR)

**Contract resolution.** Always resolve the specific contract month via the broker's contract
lookup. Near quarterly expiry (equity indexes: Mar/Jun/Sep/Dec, ~2nd Thursday roll), confirm
which month carries the volume before quoting prices or placing anything.

**Common specs — verify against the MCP before sizing:**

| Contract | Tick | Tick value | Micro version |
|---|---|---|---|
| ES (S&P 500) | 0.25 | $12.50 | MES $1.25 |
| NQ (Nasdaq 100) | 0.25 | $5.00 | MNQ $0.50 |
| RTY (Russell 2000) | 0.10 | $5.00 | M2K $0.50 |
| YM (Dow) | 1.00 | $5.00 | MYM $0.50 |
| CL (WTI crude) | 0.01 | $10.00 | MCL $1.00 |
| GC (Gold) | 0.10 | $10.00 | MGC $1.00 |
| ZN (10-yr note) | 1/64 | $15.625 | — |
| 6E (Euro FX) | 0.00005 | $6.25 | M6E $1.25 |

**Sessions.** CME equity index futures trade nearly 23h (17:00–16:00 CT with a 15-min break),
but liquidity concentrates in RTH (08:30–15:00 CT). Overnight moves happen on thin books — stops
overnight need extra room or shouldn't be there at all. Note the daily settlement and maintenance
break can cancel some order types depending on TIF.

**Margin.** Intraday vs overnight margin can differ several-fold. A position sized fine for the
session may get a margin call at 16:00 CT — check overnight margin for any hold past the close.

## Stocks (via IBKR)

- **Hours.** RTH 09:30–16:00 ET; pre/post sessions are thin, spreads wide, and many order types
  behave differently. Levels from extended hours are less reliable.
- **PDT.** Accounts under $25k equity are limited to 3 day trades per 5 business days — check
  the account's flag before proposing intraday round-trips.
- **Earnings.** Query the news feed/calendar for the earnings date of any stock plan. Holding a
  sized position through earnings is a different trade than the chart trade — say so.
- **Shorts.** Confirm shortability and borrow cost via the broker. Halts (LULD) can strand any
  position in fast movers.
- **Gaps.** Stocks gap; a stop does not limit loss across a gap. For overnight holds in
  gappy names, size from a realistic gap scenario, not just the technical stop.

## Forex (via IBKR)

- **Sessions.** Sydney → Tokyo → London → New York. Liquidity and range peak at the
  London/NY overlap (~08:00–12:00 ET). Asian-session ranges in EUR/GBP pairs are often chop;
  session context belongs in every FX analysis.
- **Pip math.** One pip = 0.0001, except JPY-quoted pairs where it's 0.01. Pip value depends on
  the quote currency — convert to account currency at current rates (see risk-management.md).
- **Rollover/swap.** Positions held through 17:00 ET pay/earn swap; triple on Wednesdays.
  Material for multi-day holds, decisive for carry-negative pairs.
- **News.** FX is the most calendar-driven class: NFP, CPI, central bank decisions move majors
  many multiples of normal range. The event blackout breaker applies with extra force.

## Crypto (via Kraken)

- **24/7.** No close means no gap risk but also no natural risk-off point — stops must be live
  orders on the exchange (confirmed placed), not mental or session-bound.
- **Weekends.** Liquidity thins badly; weekend moves reverse Monday often enough that weekend
  breakout setups deserve a grade haircut.
- **Pair naming.** Kraken uses XBT for Bitcoin in several endpoints; verify the exact pair string
  via the MCP before quoting or ordering.
- **Volatility regime.** Crypto's "normal" daily range is an equity's bad month. Stops sized by
  structure will be wide; that's fine — the size formula absorbs it (fewer units, same 1R).
  Never tighten a stop to afford more units.
- **Margin/funding.** On margin or futures, funding accrues continuously — include the estimated
  cost in any plan held over a day and always compute the liquidation price. Liquidation price
  inside 2× the stop distance means the position is over-leveraged regardless of the sizing math.
- **Correlation.** Alts are high-beta BTC most days. Multiple alt longs = one leveraged BTC long
  for heat purposes.

## Cross-market context worth checking

| Trading | Glance at |
|---|---|
| Equity index futures | Rates (ZN/yields), VIX, prior day's close/high/low |
| Gold | DXY, real yields |
| Oil | Inventory day (Wed EIA), DXY |
| FX majors | DXY, rate differentials, the relevant central bank calendar |
| Crypto | BTC dominance, equity risk tone (ES correlation regimes come and go) |
