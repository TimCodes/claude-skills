# Research and Due Diligence

How to actually evaluate an investment — a fund, an ETF, or a claim someone is making about one.
The goal is not to predict its return but to understand what it is, what it costs, what it holds,
what risk it carries, and whether its story survives scrutiny.

Contents:
- [Evaluating a fund or ETF](#evaluating-a-fund-or-etf)
- [Reading a prospectus and fact sheet](#reading-a-prospectus-and-fact-sheet)
- [The metrics that matter and how they mislead](#the-metrics-that-matter-and-how-they-mislead)
- [Evaluating an individual stock](#evaluating-an-individual-stock)
- [Factor investing](#factor-investing)
- [Interrogating a performance claim](#interrogating-a-performance-claim)
- [Red flags](#red-flags)
- [Primary sources](#primary-sources)

## Evaluating a fund or ETF

Work the checklist in [assets/fund-due-diligence-template.md](../assets/fund-due-diligence-template.md).
The core questions, in order:

1. **What does it actually hold?** Look through the marketing name to the holdings, sector and
   geographic weights, and number of positions. A "diversified" fund concentrated 30% in one
   sector or a handful of mega-caps is not what the name implies.
2. **What does it cost, all-in?** Expense ratio first, but also trading spreads, any load or 12b-1
   fee, and turnover-driven tax cost. Cost is the most reliable predictor of relative fund
   performance that exists — low cost correlates with better net returns across almost every study.
3. **What's the strategy, and is it mechanical or discretionary?** An index fund's rules are
   knowable; an active fund's edge must be explainable and durable, not just historically present.
4. **What's the risk profile?** Volatility, worst drawdown, and how it behaved in real stress
   (2008, 2020, 2022) — not just the average return.
5. **Structure and domicile** — ETF vs mutual fund tax treatment, fund size and liquidity, the
   issuer's reputation, and how long the strategy has actually run live.

## Reading a prospectus and fact sheet

The fact sheet is marketing; the prospectus is the legal document — read both, trust the second.
Where to look:

- **Expense ratio and fees** — the fee table in the prospectus is authoritative; the headline
  number can omit things. Note loads, redemption fees, and 12b-1 fees.
- **Objective and principal strategies** — what it's actually trying to do and how.
- **Principal risks** — read this section; it names the ways the fund can hurt you, in the issuer's
  own words.
- **Holdings and turnover** — high turnover means higher trading costs and, in taxable accounts,
  higher tax drag.
- **Benchmark and performance** — against the *right* index, over meaningful periods, net of fees.
- **Inception date** — a strategy live for 2 years has essentially no track record; be wary of
  funds marketed on backtested "hypothetical" performance before inception.

## The metrics that matter and how they mislead

Every headline metric has a failure mode. Report them with their caveats:

| Metric | What it's for | How it misleads |
|---|---|---|
| **Expense ratio** | All-in annual cost | Omits spreads, loads, and tax drag — the *total* cost is higher |
| **Total return** | Historical result | Period-dependent; cherry-picked windows flatter; past ≠ future |
| **Yield** | Income rate | A very high yield often signals elevated risk or return *of* capital, not a free lunch |
| **Sharpe ratio** | Return per unit of volatility | Assumes volatility = risk; blind to fat tails, illiquidity, and smoothed marks |
| **Max drawdown** | Worst peak-to-trough | Only captures the past worst; the next one can be deeper |
| **Alpha / beta** | Excess return / market sensitivity | Estimated over a period; unstable; small samples are noise |
| **Star ratings** | Convenience score | Backward-looking; weakly predictive of future returns at best |
| **Tracking error** | Index-following fidelity | Only meaningful for index funds |

The recurring lesson: **a single number, confidently quoted, hides its assumptions.** Sharpe treats
a smooth-but-illiquid private fund as low-risk; yield can be a distress signal; total return is
whatever the chosen window makes it. Always pair the metric with what it can't see.

## Evaluating an individual stock

Most independent investors should not pick individual stocks as their core — it concentrates risk
and demands research most can't sustain against professionals. When analysing one anyway (for a
small satellite position, or education), the honest framing is *understanding the business and its
valuation*, not predicting the price:

- **Business** — what it does, its economics, competitive position (moat), and durability.
- **Financials** — revenue and earnings trend, margins, debt, cash flow, return on capital.
- **Valuation** — price relative to earnings, cash flow, sales, and growth; cheap or expensive vs
  its own history and peers. Valuation is a probability statement, not a timing signal.
- **Risks** — what could impair the business; concentration, cyclicality, regulation, key-person.

State clearly that single-stock outcomes have enormous variance and that position-sizing (small,
diversified) matters more than being right on any one name.

## Factor investing

Academic research identifies persistent return *factors* — historically compensated tilts beyond
the market: **value** (cheap vs expensive), **size** (small vs large), **momentum**, **quality**
(profitable, stable), **low volatility**, and in bonds **term** and **credit**. Factor funds tilt
toward these deliberately.

The honest state of it: the premia are real in long historical data but **inconsistent over any
period an investor actually lives through** — value underperformed for over a decade, testing most
investors' patience past breaking. Factors add complexity, sometimes cost, and behavioural risk
(abandoning a tilt mid-underperformance locks in the loss). They can have a place for an investor
who understands and will hold them through long droughts, but they are not free money and they are
not a fix for a portfolio's fundamentals.

## Interrogating a performance claim

When someone (a fund, a newsletter, a forum) claims a strategy or fund "returns X%," run it through:

1. **Live or backtested?** A live, audited track record is evidence; a backtest is a hypothesis. The
   gap between them is where most claims die — see the bias list in
   [data-engineering-for-research.md](data-engineering-for-research.md).
2. **What period, and is it cherry-picked?** Any strategy looks great over its best window. Demand
   the full period including the bad years, and the worst drawdown.
3. **Net of what?** Fees, taxes, spreads, and slippage. Gross returns are fiction for an investor.
4. **Risk-adjusted and survivorship-adjusted?** A high return from high leverage or hidden risk
   isn't skill. A "top fund" list that quietly dropped the dead funds overstates the category.
5. **Compared to what?** Beating cash is trivial; beating the appropriate low-cost index net of
   everything is the bar.
6. **Sample size and luck?** Five years of outperformance across thousands of funds is what pure
   chance produces. Persistence and an explainable mechanism separate skill from noise, and even
   then only weakly.

Most impressive-sounding claims fail at step 1, 3, or 5. Applying these questions calmly is more
valuable to an investor than any specific recommendation.

## Red flags

Treat these as reasons to walk away, not puzzles to solve:

- **Guaranteed or unusually steady high returns** — the hallmark of fraud (Madoff's "returns" were
  suspiciously smooth). Real risk assets are volatile.
- **Pressure and urgency** — "limited time," "act now." Good investments don't expire tomorrow.
- **Opacity** — you can't understand how it makes money, or can't see the holdings.
- **Complexity that obscures rather than serves** — layers that mostly hide fees.
- **Unregistered products or unlicensed sellers**, and anything pushed via DM, social media hype,
  or "exclusive" access.
- **Performance shown only as a backtest or "hypothetical,"** especially pre-inception.
- **Fees that dwarf the expected edge.**

## Primary sources

Prefer these over summaries and influencers:

- **Fund prospectuses, fact sheets, and annual reports** — from the issuer directly.
- **Regulator databases** — SEC EDGAR (US filings), FINRA BrokerCheck and the SEC IAPD (check
  whether an adviser/firm is registered and their history), FCA register (UK).
- **Fund issuers' own data** (Vanguard, iShares/BlackRock, Fidelity, Schwab, State Street).
- **SPIVA reports** (S&P) — the standard scorecard on active vs index performance.
- **Independent research and data** (Morningstar for holdings/fees, with its ratings taken
  skeptically).
- **Academic sources** for factor and market-efficiency evidence, not marketing white papers.

Always note the *as-of* date. Fund data, yields, and holdings change, and stale figures mislead.
