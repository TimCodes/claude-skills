# Portfolio Construction and Risk

How the pieces fit together. An individual fund can be excellent and a portfolio of them still be
fragile — construction is about the whole, and the whole is driven by asset allocation far more
than by security selection.

Contents:
- [Allocation is the dominant decision](#allocation-is-the-dominant-decision)
- [Defining risk before return](#defining-risk-before-return)
- [Diversification and correlation](#diversification-and-correlation)
- [Modern portfolio theory, honestly](#modern-portfolio-theory-honestly)
- [Model portfolios as reference points](#model-portfolios-as-reference-points)
- [Rebalancing](#rebalancing)
- [Risk metrics](#risk-metrics)
- [Sequence-of-returns and withdrawals](#sequence-of-returns-and-withdrawals)
- [Common construction mistakes](#common-construction-mistakes)

## Allocation is the dominant decision

The split across asset classes — broadly, **stocks vs bonds vs cash**, then geography and size
within them — explains the large majority of a portfolio's return variability over time. Picking
the "best" fund inside a class matters far less than getting the class weights right for the goal.

This is liberating for an independent investor: you do not need to find winning securities. You
need a sensible allocation, cheap broad exposure to each class, and the discipline to hold it. Spend
the analytical effort on the allocation and the behaviour, not on chasing funds.

The allocation is driven by **time horizon** and **risk capacity**, not by market views. Longer
horizon → more equity (time to recover from drawdowns); shorter horizon or money needed soon → more
bonds and cash (can't afford a deep drawdown at the wrong moment).

## Defining risk before return

"Risk" is not one thing. Separate:

- **Risk capacity** — the *objective* ability to absorb loss: time horizon, liquidity needs, income
  stability, how much of the goal depends on this money. A 25-year-old funding retirement has high
  capacity; a 64-year-old two years from drawing income has low capacity, regardless of feelings.
- **Risk tolerance** — the *subjective* willingness to endure volatility without abandoning the
  plan. Real, and it caps how aggressive a portfolio can be *and be held*.
- **Risk required** — the return (and thus risk) actually needed to hit the goal. Sometimes lower
  than an investor assumes; taking more risk than needed is its own mistake.

The allocation should satisfy the *minimum* of capacity and tolerance, aimed at the required
return. A portfolio calibrated to capacity but beyond tolerance gets sold at the bottom — the worst
outcome. Establish all three before proposing any allocation.

## Diversification and correlation

Diversification is the one genuine "free lunch": combining assets that don't move together lowers
portfolio volatility for a given expected return, because their ups and downs partly cancel.

- The benefit depends on **correlation** — assets with low or negative correlation diversify;
  assets that move together don't, however different they look.
- **Correlations rise in crises.** The painful truth is that many risk assets fall together exactly
  when diversification is most wanted (2008). Genuinely defensive ballast is usually high-quality
  government bonds and cash, not just "different stocks."
- **Diversify across the axes that matter:** asset class, geography, and (for bonds) duration and
  credit — not across ten funds that all hold the same large-cap stocks (false diversification).
- There's a **point of diminishing returns**: a handful of broad, well-chosen funds diversifies
  better than twenty overlapping ones, which mostly adds complexity and tracking-your-own-portfolio
  cost.

## Modern portfolio theory, honestly

MPT (Markowitz) formalises the above: for a set of assets with expected returns, volatilities, and
correlations, there's an "efficient frontier" of portfolios maximising return per unit of
volatility. It's the conceptual foundation of diversification and worth understanding.

Its practical limits, which matter more than its elegance:

- **Inputs are estimates, and the output is exquisitely sensitive to them.** Small changes in
  assumed returns swing the "optimal" portfolio wildly. Naive mean-variance optimisation produces
  concentrated, unstable allocations that perform badly out of sample — "garbage in, garbage out."
- **It uses volatility as risk**, missing fat tails, illiquidity, and regime change.
- **Correlations and volatilities are not stable**, especially in crises.

So use MPT for *intuition* (diversification helps; there's a risk-return trade-off), not as an
optimiser to trust blindly. Robust, simple allocations (broad, low-cost, roughly balanced) tend to
beat precisely-optimised ones in the real world. This is a place to be explicitly skeptical of
sophisticated-looking machinery.

## Model portfolios as reference points

Not recommendations — reference architectures to reason from and adapt:

- **Total-market index + total bond, at a stock/bond ratio set by horizon** (e.g. 80/20, 60/40) —
  the simple, robust core most independent investors are well served by.
- **Three-fund portfolio** — total US market, total international, total bond. Global diversification
  in three cheap funds.
- **Target-date fund** — the same idea in one ticker, auto-adjusting over time. Hard to beat for
  hands-off retirement money.
- **"Lazy" all-weather style** — spread across stocks, long and short bonds, and real assets to be
  robust across regimes; lower drawdown, typically lower long-run return than an equity-heavy mix.

The right one depends on the individual's horizon, tolerance, and whether they'll actually maintain
it. A 60/40 held for 30 years beats a "perfect" allocation abandoned in year three.

## Rebalancing

Over time, winners grow and drift the portfolio away from its target allocation, quietly raising
risk. Rebalancing sells what's grown and buys what's lagged, restoring the target — a mechanical
discipline that enforces "sell high, buy low" and, more importantly, controls risk.

- **Methods:** on a schedule (e.g. annually) or by threshold (when a class drifts more than X% from
  target). Threshold is slightly more efficient; calendar is simpler to stick to.
- **Prefer rebalancing with new contributions** (direct new money to the underweight class) — it
  rebalances without selling, avoiding taxes and costs.
- **Mind taxes** — rebalancing by selling in a taxable account realises gains; do it in
  tax-advantaged accounts, or with contributions, where possible.
- **Don't over-rebalance** — frequent tweaking adds cost and taxes for little benefit. Annually or
  on a meaningful threshold is plenty.

## Risk metrics

`scripts/portfolio_analyzer.py` computes these from a return series; read them with the caveats
from [research-and-due-diligence.md](research-and-due-diligence.md):

- **Volatility (standard deviation)** — dispersion of returns; the common risk proxy, blind to tails.
- **Maximum drawdown** — worst peak-to-trough loss; often more behaviourally relevant than
  volatility, because it's the pain that makes people sell.
- **Sharpe ratio** — excess return per unit of volatility; useful for comparison, not gospel.
- **Sortino** — like Sharpe but penalising only downside volatility.
- **Correlation matrix** — whether holdings actually diversify each other.
- **Beta** — sensitivity to the broad market.

Use them to *understand* a portfolio's risk, not to optimise to a decimal. The map is not the
territory, and the next crisis won't match the last one's statistics.

## Sequence-of-returns and withdrawals

For anyone drawing down (retirement), the *order* of returns matters, not just the average: a big
loss early in withdrawal, while selling to fund spending, can permanently impair a portfolio even
if the long-run average is fine. This is **sequence-of-returns risk**, and it's why near-retirement
risk capacity drops sharply.

Frameworks (rules of thumb, not guarantees): the "4% rule" as a *starting* withdrawal reference,
bond/cash buffers to avoid selling equities into a downturn, and flexible spending. `scripts/projection.py`
can illustrate accumulation; withdrawal sustainability is genuinely uncertain and depends on
sequence, so present ranges and scenarios, never a single confident number.

## Common construction mistakes

- **Chasing last year's winner** — buying what just went up, the reliable way to buy high.
- **False diversification** — many funds, same underlying exposure.
- **Too much home-country bias** — over-concentrating in domestic stocks.
- **Allocation mismatched to horizon** — too aggressive for money needed soon, or too conservative
  for a 30-year goal (inflation risk).
- **Tinkering** — reacting to news and headlines; the portfolio's worst enemy is usually its owner.
- **Ignoring costs and taxes** in the pursuit of a marginally "better" fund.
- **No written plan**, so decisions get made emotionally in the moment — which the Investment
  Policy Statement exists to prevent.
