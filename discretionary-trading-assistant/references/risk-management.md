# Risk Management & Position Sizing

Risk is computed before reward, every time. The sizing question is never "how much can I make"
but "how many units can I hold so that being wrong costs exactly one risk unit".

## The risk unit (1R)

`1R = account equity × risk-per-trade %`

Default risk-per-trade is **1%** if the trader profile doesn't specify one — but state the
default aloud the first time you use it and confirm. B-grade setups: half size (0.5R). If the
trader's profile defines different tiers, theirs win.

Pull current equity from the broker MCP when available rather than using a remembered number —
equity changes daily and stale equity silently mis-sizes every trade.

## Sizing by asset class

Always show the arithmetic in the trade plan, not just the result.

### Stocks
```
shares = floor( 1R$ / (entry − stop) )
```
Check: position notional vs buying power; shortability and locate cost for shorts; round down.

### Futures
```
risk per contract = (ticks between entry and stop) × tick value
contracts = floor( 1R$ / risk per contract )
```
- Resolve tick size and tick value from the broker's contract lookup — do not trust memory, specs
  change and micros/minis differ 10×. A reference table is in asset-classes.md but the MCP wins.
- If 1 contract already risks more than 1R, the trade is too big for the account at that stop —
  say so. Suggest the micro contract if one exists; never suggest widening the risk% to fit.
- Check margin: contracts × initial margin must fit comfortably inside available funds.

### Forex
```
pip value (USD-quote pairs, e.g. EURUSD) = 0.0001 × position size   (≈ $10 per pip per standard lot)
lots = 1R$ / (stop distance in pips × pip value per lot)
```
For non-USD-quote pairs, convert pip value to account currency using the current cross rate
(pull it — don't estimate). JPY pairs: a pip is 0.01, not 0.0001. Round down to the broker's
lot granularity.

### Crypto (Kraken)
```
units = 1R$ / (entry − stop)      — spot, fractional units are fine
```
Leverage/margin: size from the stop exactly as above — leverage changes margin required, not the
correct size. Flag the liquidation price if using margin and require it to be far beyond the stop.
For holds beyond a day on margin/futures, include funding cost in the plan.

## Portfolio heat

Before any new ticket:

1. Pull all open positions from both brokers.
2. Heat is what can still be lost from here, so measure stop-to-current-price:
   `position heat = (current price − stop) × size` for longs (inverted for shorts). A position
   whose stop is at or beyond breakeven contributes zero heat.
3. Total heat = sum, plus the proposed trade's 1R.
4. Default ceiling: **3R total heat** and **6% of equity**, unless the profile says otherwise.
   Over the ceiling → the new trade waits or something gets trimmed. Present that choice; don't
   make it.

**Correlation haircut:** positions that move together are one position for heat purposes. Long
ES + long NQ, long EURUSD + short DXY futures, long BTC + long ETH + long alts — count each
cluster at ~1.5× the largest single risk in it, not the naive sum, and warn the trader that
their "three trades" is one bet.

## Circuit breakers

Enforce from the trader profile; defaults if none exist:

| Breaker | Default | On trip |
|---|---|---|
| Max daily loss | 3R or 3% | No new tickets today; say it directly |
| Max concurrent positions | 4 | New ideas go on watch, not on |
| Event blackout | No new positions in final 15 min before FOMC/CPI/NFP-class events on affected instruments | Wait for the release and the first reaction to settle |
| Consecutive-loss cooldown | After 3 straight losses, halve size until a green trade | Protects against tilt |

A tripped breaker is stated plainly, once, with the rule quoted. The trader can override —
it's their account — but the override goes in the journal entry verbatim.

## R-multiples and expectancy (for reviews)

- Record every closed trade's result in R (realized P&L ÷ planned 1R at entry).
- `Expectancy = (win% × avg win R) − (loss% × avg loss R)` per setup type.
- Watch for the two classic leaks: average loss > 1R (stops not honored) and expectancy positive
  overall but negative in one setup type the trader keeps forcing.

## Pre-ticket checklist

Every trade plan gets this, answered, at the bottom:

- [ ] Size computed from stop, arithmetic shown, rounded down
- [ ] 1R ≤ profile risk%; B-grade at half
- [ ] Total heat after entry ≤ ceiling (correlation-adjusted)
- [ ] Margin/buying power verified from broker
- [ ] No breaker tripped
- [ ] News/calendar checked for the hold window
