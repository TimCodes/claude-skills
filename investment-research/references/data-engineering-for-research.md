# Data Engineering for Investment Research

The part of this skill that separates rigorous research from plausible-looking nonsense. Investment
data is riddled with biases that flatter results, and most bad conclusions come not from bad
analysis but from bad or misunderstood data. Getting the data engineering right is the edge.

Contents:
- [Data sources](#data-sources)
- [The biases that make investment data lie](#the-biases-that-make-investment-data-lie)
- [Point-in-time data](#point-in-time-data)
- [Building a screener](#building-a-screener)
- [Backtesting hygiene](#backtesting-hygiene)
- [A reproducible research pipeline](#a-reproducible-research-pipeline)
- [Statistical discipline](#statistical-discipline)
- [Practical stack](#practical-stack)

## Data sources

Match the source to the question, and know each one's limits and terms of use.

| Source | Data | Notes |
|---|---|---|
| **Fund issuers** (Vanguard, iShares, Fidelity, Schwab, SSGA) | Holdings, fees, fact sheets | Authoritative for their own funds; free |
| **SEC EDGAR** | Filings, fund holdings (13F, N-PORT), company financials | Free, authoritative, point-in-time by nature; needs parsing |
| **Yahoo Finance / stooq** (via `yfinance`, direct) | Prices, basic fundamentals | Free, convenient; **adjusted** prices, gaps, occasional errors — fine for exploration, not for high-stakes backtests |
| **FRED** (St. Louis Fed) | Macro, rates, inflation, yields | Free, excellent, clean, API |
| **Nasdaq Data Link / Tiingo / Alpha Vantage / Polygon** | Prices, fundamentals, some point-in-time | Freemium; read the licence and rate limits |
| **Norgate, CRSP, Compustat, Bloomberg/Refinitiv** | Survivorship-free, point-in-time, institutional | Paid (some very expensive); the gold standard for serious backtesting |

The free tier is genuinely fine for learning, allocation work, and rough comparison. The moment a
conclusion depends on precise historical returns or backtested strategy performance, **data quality
becomes the binding constraint** — free adjusted-price data with survivorship bias will mislead, and
the honest move is either to get clean data or to caveat the result heavily.

Always record the **source and the retrieval date** with any dataset; investment data is revised,
and reproducibility requires knowing which vintage you used.

## The biases that make investment data lie

These are the reason a strategy looks brilliant on a screen and fails live. Name and check each one
before trusting any historical result:

- **Survivorship bias** — datasets that quietly drop delisted, merged, and dead funds/companies. The
  survivors look stronger than the real population was, inflating average returns and hiding the
  failures. The single most common way backtests overstate returns.
- **Look-ahead bias** — using information in a backtest that wasn't available at the time: today's
  index membership applied to the past, restated financials, or a signal computed with data
  published later. Makes strategies look prescient.
- **Backfill / inclusion bias** — a database adds a fund's history only once it's successful,
  backfilling its good past and omitting the ones that never made it.
- **Data-snooping / overfitting** — testing many variations until one "works" on the sample. With
  enough tries, random noise produces a beautiful backtest that predicts nothing. The more
  parameters and the more tests, the worse.
- **Time-period bias** — a result true only for the chosen window. Test across regimes.
- **Restatement / point-in-time** — fundamentals get restated; using the final figure assumes
  knowledge you didn't have then.
- **Selection bias in "top funds"** lists — ranking the survivors overstates the category.

The mindset: assume a good-looking historical result is biased until you've ruled these out. The
StrategyVisualizer / strategy-factory work in this user's world lives or dies on exactly this
discipline — purged cross-validation, out-of-sample gates, and honest pre-registration exist to
fight these biases.

## Point-in-time data

The antidote to look-ahead bias: data as it *actually appeared on each historical date* — the index
constituents then, the financials as first reported, the prices unadjusted for splits/dividends that
hadn't happened yet. Institutional datasets (CRSP, Compustat point-in-time) provide this; most free
sources don't. When you can't get point-in-time data, say so and treat any strategy result as
optimistic — because it is.

## Building a screener

A screener filters a universe by rules to surface candidates for research (not to buy blindly).
Sound construction:

1. **Define the universe explicitly** and include the dead names if the screen is historical
   (survivorship again).
2. **Encode criteria as reproducible code**, not manual filtering — e.g. expense ratio below X,
   assets above Y, category, yield, factor exposure.
3. **Handle missing data deliberately** — decide whether a missing field excludes or passes a
   name; silent NaN handling changes results.
4. **Output candidates for due diligence**, then apply the fund/stock checklist from
   [research-and-due-diligence.md](research-and-due-diligence.md). A screen is the start of
   research, not the end.
5. **Version the screen and its date** so results are reproducible.

## Backtesting hygiene

If a strategy is backtested, it must pass real hygiene or its numbers are worthless. The essentials:

- **Out-of-sample and walk-forward** — reserve data the strategy never saw; better, use
  walk-forward or purged/embargoed cross-validation so training and testing don't leak across time.
- **Realistic costs** — commissions, bid-ask spread, slippage, market impact, and taxes. Many
  "profitable" strategies are just unpriced trading costs.
- **No look-ahead** — every signal uses only data available at that timestamp; align data by the
  date it was *knowable*, not the date it refers to.
- **Survivorship-free universe** — include the delisted.
- **Account for regime** — test across bull, bear, high- and low-rate periods; a strategy tuned to
  one regime breaks in the next.
- **Limit degrees of freedom** — few parameters, and penalise the temptation to keep tweaking. Track
  how many variations you tried; the more you test, the more you must discount a good result.
- **Compare to the honest benchmark** — the low-cost index net of everything, not cash.
- **Distinguish backtest from live** — a backtest is a hypothesis. Only a live, costed, audited
  track record is evidence, and even a good backtest usually degrades substantially live.

The blunt rule: **a backtest's job is to reject bad ideas, not to prove good ones.** Treat an
impressive backtest as a reason for suspicion and further testing, not for capital.

## A reproducible research pipeline

Bring software-engineering discipline to research — it's what a data-engineering background buys:

- **Version control** the code and, where feasible, the data (or at least a manifest with source,
  vintage, and checksum).
- **Deterministic, parameterised pipelines** — raw data → cleaning → features → analysis → report,
  each stage rerunnable and inspectable, seeds fixed.
- **Separate raw from derived data**; never edit raw in place. Keep the transformation in code so
  it's auditable.
- **Log data lineage** — where each input came from and when, so a result can be traced and redone.
- **Pre-register the hypothesis and the decision rule** before running the test, to resist the human
  urge to rationalise whatever the data shows. (This is exactly the discipline in the user's own
  campaign-pre-registration practice.)
- **Cache and rate-limit** API calls; respect terms of service; store pulled data so analysis is
  reproducible without re-hitting the source.

## Statistical discipline

- **Financial returns are not normal** — fat tails, skew, and volatility clustering mean models
  assuming normality understate extreme risk. Say so.
- **Small samples are noise** — a few years, or a few dozen trades, can't distinguish skill from
  luck. Demand adequate sample size and be explicit about significance.
- **Multiple-testing correction** — if you tried twenty signals, the best one's "significance" is
  inflated; adjust for it or treat it as a hypothesis to retest fresh.
- **Report uncertainty** — ranges, confidence intervals, and scenario analysis, not point forecasts.
  The future is a distribution; presenting it as a number is dishonest.
- **Correlation isn't causation, and in-sample fit isn't predictive power.**

## Practical stack

For an independent investor with coding ability: **Python** with `pandas` for data, `numpy`/`scipy`
for stats, `yfinance`/`pandas-datareader`/`requests` for data access, `matplotlib` for plots, and
`statsmodels` for regressions and factor analysis. `vectorbt`, `backtrader`, or `zipline`-style
frameworks for backtesting — used with all the hygiene above, not as a black box. Store data in
Parquet or a small database; keep notebooks for exploration but move anything reused into versioned
modules. Offer to write these pipelines when the user wants to build rather than just discuss —
that's squarely within this skill's remit, and doing the engineering well is the differentiator.
