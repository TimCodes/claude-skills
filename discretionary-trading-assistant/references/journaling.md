# Journaling & Review (RAG store)

The journal is the trader's long-term memory and the raw material for every review. Log
generously — storage is cheap, hindsight without records is fiction.

## What gets logged, and when

| Event | Log |
|---|---|
| Trade plan produced | The full plan (template fields), grade, and the devil's-advocate case — even if never taken. Untaken A-setups are data about missed edge; taken C-setups are data about discipline. |
| Order filled | Fill price/size/time from the broker's acknowledgment, slippage vs plan |
| Management action | Stop/target moves with the stated reason |
| Position closed | Exit price/time, realized R, and a one-line honest cause: "target", "stop", "discretionary exit — reason", "time stop" |
| Rule override | The rule, the breach, and the trader's stated reason, verbatim |
| Session notes | Anything the trader dictates: emotional state, market character, lessons |

## Journal entry schema

Store as a structured document in the RAG store. Keep field names stable — reviews depend on
querying them consistently.

```yaml
type: trade            # trade | plan_only | session_note | profile
date: 2026-07-14
symbol: MES            # exact contract/pair as resolved
asset_class: futures   # futures | stocks | forex | crypto
direction: long
setup_type: break-and-retest   # from the playbook vocabulary
grade: B
planned:
  entry: 5610.25
  stop: 5601.25
  targets: [5628.00]
  size: 2
  risk_usd: 90
  risk_r: 0.5          # B-grade half size
actual:
  entry: 5610.50
  exit: 5628.00
  result_r: +1.9
  cause: target
context:
  session: RTH open
  events: none within hold window
  heat_at_entry: 1.5R
notes: >
  Devil's advocate flagged overhead daily supply at 5635; target set below it — that's why
  target 5628 not 5640. Held cleanly.
overrides: []
```

For `plan_only` entries, omit `actual`. Screenshots: store a brief description of the chart and
extracted levels (the RAG store may not hold images; the description is what future retrieval
needs anyway).

## The trader profile document

One `type: profile` document, updated in place:

```yaml
type: profile
account_equity_ref: pull live; last known 52000 (2026-07-14)
risk_per_trade: 1%
b_grade_multiplier: 0.5
max_daily_loss: 3R
max_heat: 3R / 6%
max_concurrent: 4
instruments: [MES, MNQ, MCL, EURUSD, BTC/USD, ETH/USD]
playbook: [break-and-retest, failed-breakout, pullback-in-trend]
sessions: RTH open + London/NY overlap; no overnight index holds
notes: no trading day after a 3R loss day
```

## Review workflows

When the trader asks for a review ("how did I do this month", "why do I keep losing on
breakouts"):

1. Query the journal for the relevant slice (period, setup type, symbol, or asset class).
2. Compute per slice: trade count, win rate, average win R, average loss R, expectancy,
   largest loss, and R distribution.
3. Split by grade and by taken-vs-plan-only. The two highest-value comparisons:
   - **Expectancy of A/B setups vs C setups actually taken** — measures discipline's price tag.
   - **Average loss vs planned 1R** — over 1R means stops aren't being honored.
4. Look for behavioral patterns the numbers hint at: size creep after wins, revenge entries
   within 30 minutes of a stop-out, overrides clustering on losing days, one symbol eating a
   disproportionate share of losses.
5. Report process-first: lead with what the data says about rule-following, then outcomes.
   One or two concrete, checkable suggestions beat a lecture. If the sample is small (<20 trades
   in a slice), say the numbers are noise-level and hold conclusions loosely.

## Retrieval before analysis

Before analyzing any new setup, query the journal for prior trades on the same symbol and same
setup type. "You've traded this failed-breakout on MNQ four times: +2.1R, −1R, −1R, +1.8R, and
both losers were in the Asian session" is exactly the kind of memory a solo trader lacks.
