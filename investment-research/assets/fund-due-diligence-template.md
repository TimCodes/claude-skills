# Fund Due Diligence — [Fund name / ticker]

**Analyst:** [name] · **Date:** [YYYY-MM-DD] · **Data as of:** [date — investment data goes stale]

> This is a research worksheet, not a recommendation. It captures what a fund *is*, what it
> costs, and what it risks, so a decision can be made on evidence. Verify every figure against
> the prospectus and fact sheet, not a third-party summary.

## Identity

| | |
|---|---|
| Name / ticker | |
| Issuer | |
| Structure | [ETF / mutual fund / other] |
| Inception date | [a short live history = little real track record] |
| Fund size (AUM) | [very small funds risk closure; very large can hit capacity in some strategies] |
| Domicile | [affects tax treatment] |
| Benchmark index | |

## Strategy

- Objective (from the prospectus): ______________________
- Index-tracking or active? ______________________
- If active: what is the claimed edge, and is it durable and explainable — not just past
  performance? ______________________
- Mechanical rules / methodology: ______________________

## Cost — all-in, not just the headline

| Cost | Value | Notes |
|---|---|---|
| Expense ratio | | From the prospectus fee table, not marketing |
| Loads (front/back) | | Avoid; no-load equivalents exist |
| 12b-1 / distribution fee | | |
| Bid-ask spread (ETF) | | Matters for trading; check on a normal day |
| Turnover | | High turnover → higher hidden trading cost + tax drag |
| Premium/discount to NAV (ETF) | | |

Run the expense ratio through `scripts/projection.py` against a low-cost alternative to see the
30-year fee drag in dollars.

## Holdings

- What it actually holds (look through the name): ______________________
- Number of positions: ____   Top 10 as % of fund: ____
- Sector concentration: ______________________
- Geographic concentration: ______________________
- Overlap with what I already own: [false diversification check] ______________________

## Risk

| | |
|---|---|
| Volatility (std dev) | |
| Max drawdown (and when) | |
| Behaviour in 2008 / 2020 / 2022 | [real stress tests beat the average] |
| Interest-rate sensitivity (bonds: duration) | |
| Credit quality (bonds) | |
| Liquidity | |
| Principal risks (from prospectus) | [read this section in the issuer's own words] |

## Performance — read skeptically

- Return vs the *right* benchmark, net of fees, over meaningful periods: ______________________
- Is any shown performance live, or backtested/hypothetical (esp. pre-inception)? ______________
- Does the window look cherry-picked? Check the bad years too: ______________________
- Tax cost (capital gains distribution history, taxable accounts): ______________________

## Red-flag check

- [ ] No guaranteed/implausibly-steady returns claimed
- [ ] Holdings are transparent and understandable
- [ ] Fees don't dwarf any plausible edge
- [ ] Issuer/seller is registered (verified via SEC IAPD / FINRA BrokerCheck / FCA)
- [ ] No pressure/urgency in how it's being sold
- [ ] Performance shown is live, not just a backtest

## Verdict (analysis, not advice)

- What role would this play in a portfolio, and what does it compete against? ______________
- The one or two questions that decide whether it fits *this investor's* situation
  (horizon, account, existing holdings): ______________
- If those are personal-situation questions, that's the signal to take the decision to a
  fee-only fiduciary rather than resolve it here.
