# Costs, Taxes, and Behaviour

The three levers an independent investor actually controls. Returns are uncertain and mostly out of
your hands; costs, taxes, and your own behaviour are not, and over a lifetime they decide more of
the outcome than fund selection does. This is where "process beats prediction" gets concrete.

Contents:
- [Why costs dominate](#why-costs-dominate)
- [The full cost stack](#the-full-cost-stack)
- [Tax drag](#tax-drag)
- [Tax-loss harvesting](#tax-loss-harvesting)
- [Tax-efficient investing](#tax-efficient-investing)
- [The behaviour gap](#the-behaviour-gap)
- [Behavioural biases](#behavioural-biases)
- [Designing against yourself](#designing-against-yourself)

## Why costs dominate

Cost is the most reliable predictor of relative returns that exists — across nearly every study,
lower-cost funds beat higher-cost ones on average, because cost is one of the few things guaranteed
in advance. And it compounds: a fee isn't a one-time haircut, it's a drag applied every year to a
growing balance.

Run the numbers with `scripts/projection.py`, but the intuition: on a portfolio compounding for
30 years, a **1% annual fee difference typically consumes on the order of a quarter of the ending
wealth.** Not 1% — a quarter. The fee looks tiny each year and is enormous over a lifetime, because
it compounds against you exactly as returns compound for you. This is why the index-vs-active and
expense-ratio questions matter so much more than they appear.

## The full cost stack

Look past the headline expense ratio; the total is higher:

- **Expense ratio** — the annual fund fee. The first number, not the last.
- **Trading costs** — bid-ask spreads and, for funds, internal turnover costs not in the expense
  ratio. High-turnover funds cost more than their ratio shows.
- **Loads and 12b-1 fees** — sales charges and marketing fees on some mutual funds. Avoidable;
  no-load index funds exist for every mainstream need.
- **Advisory fees** — a 1%-of-assets adviser (AUM fee) is a large recurring cost; a fee-only
  flat/hourly adviser can be far cheaper for the same advice. Worth scrutinising against the value.
- **Platform / account fees** — some brokers or wrappers add them.
- **Tax cost** — see below; often larger than the expense ratio in a taxable account.
- **Bid-ask and spreads on the securities you trade** — especially on illiquid ETFs or small stocks.

The all-in cost is what compounds against you, so surface all of it, not just the sticker.

## Tax drag

In a **taxable** account, taxes are a real annual cost that a fund's expense ratio doesn't capture:

- **Dividends and interest** are taxed as received (qualified dividends and long-term gains at
  favourable rates in the US; interest and non-qualified dividends as ordinary income).
- **Capital gains distributions** — actively managed and high-turnover funds can pass through taxable
  gains you didn't choose to realise, a nasty surprise in December.
- **Realised gains on your own sales** — short-term (held ≤1 year, ordinary rates) vs long-term
  (>1 year, favoured). Holding longer is often worth real money.

Tax drag can quietly cost more than the expense ratio, which is why tax-efficient vehicles (broad
index ETFs) and the right account placement matter. None of this applies inside tax-advantaged
accounts — another reason the account wrapper is a first-order decision.

## Tax-loss harvesting

Selling a position at a loss to realise the loss for tax purposes (offsetting gains and, in the US,
a limited amount of ordinary income), while staying invested by buying a *similar but not
substantially identical* fund. Done right it adds after-tax return without changing the portfolio's
exposure.

The rules that matter, stated as education not personalised advice:

- **Wash-sale rule (US)** — buying a "substantially identical" security within 30 days before or
  after the loss sale disallows the loss. Using a different-but-similar index fund (tracking a
  different index) is the common workaround; buying the identical fund back too soon defeats it.
- It only helps in **taxable** accounts, and it defers rather than eliminates tax (it lowers cost
  basis), so the benefit is the time value and any rate arbitrage — real but often oversold.
- Rules differ by jurisdiction (the UK has its own "bed and breakfasting" rules); confirm locally.

This is a genuine, mechanical, prediction-free edge for taxable investors — and exactly the kind of
thing where the *mechanics* are educational but the *personalised execution* is a conversation for a
tax professional or fiduciary.

## Tax-efficient investing

The controllable tax levers, roughly in order of impact:

1. **Use tax-advantaged accounts** to their limits (match, HSA, IRA/401k, ISA/SIPP).
2. **Asset location** — tax-inefficient assets (bonds, REITs) in tax-advantaged accounts;
   tax-efficient equity index funds in taxable. See [vehicles-and-accounts.md](vehicles-and-accounts.md).
3. **Prefer tax-efficient vehicles** in taxable — broad index ETFs over high-turnover active funds.
4. **Hold for long-term treatment** rather than trading into short-term rates.
5. **Harvest losses** where it applies.
6. **Be deliberate about which lots you sell** (specific-identification) to control the gain.

## The behaviour gap

Study after study finds that the *average investor* earns meaningfully less than the *average fund*
they invest in — often by a percent or more annually — because of *when* they buy and sell: piling
in after rallies, capitulating in crashes. This "behaviour gap" is frequently larger than the
expense-ratio difference people agonise over. **The investor, not the market, is usually the biggest
drag on their own returns.**

The implication for this skill: helping someone hold a sensible plan through a drawdown is worth more
than finding them a marginally better fund. Behaviour is a controllable lever, and often the largest.

## Behavioural biases

The predictable ways investors hurt themselves — name them so they can be resisted:

- **Loss aversion** — losses hurt about twice as much as equal gains please, driving panic selling at
  bottoms.
- **Recency bias** — over-weighting recent experience; chasing what just went up, fleeing what just
  went down.
- **Overconfidence** — over-trading and over-concentrating, especially after a few wins that were
  luck.
- **Herding / FOMO** — buying manias (meme stocks, bubbles) because others are.
- **Anchoring** — fixating on a purchase price or a past high, refusing to sell a loser or buy back.
- **Confirmation bias** — seeking information that supports a position already held.
- **Home bias** — over-concentrating in domestic and familiar names.
- **Action bias** — feeling that doing *something* in a downturn beats holding, when holding is
  usually right.

## Designing against yourself

You can't eliminate biases, but you can build a system that blunts them:

- **A written Investment Policy Statement** — decide the rules in calm times so panic can't rewrite
  them. The single most effective behavioural tool. See
  [assets/investment-policy-statement-template.md](../assets/investment-policy-statement-template.md).
- **Automate** contributions and rebalancing — remove the moments of discretionary temptation.
- **Reduce the frequency of looking** — daily portfolio-watching amplifies loss aversion; a long-term
  investor checking constantly is manufacturing pain.
- **Pre-commit to a rebalancing rule** rather than deciding in the moment.
- **Keep an adequate cash buffer** so a downturn never forces a sale — the financial version of not
  making decisions while hungry.
- **Write down the thesis** for any non-standard decision, so it can be checked against reality later
  rather than rationalised.

Design the portfolio *and the process* for the investor you actually are under stress, not the
rational one you imagine in calm markets. A slightly worse portfolio you hold beats a better one you
abandon.
