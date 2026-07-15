# Setup Finding & Analysis

## The top-down process

Always analyze in this order. Skipping straight to the entry timeframe is how traders end up
buying a perfect 5-minute breakout into a daily-chart brick wall.

1. **Higher-timeframe context (daily / 4H).** Trend direction and structure (higher highs/lows or
   the opposite, or a range). Where is price relative to the levels everyone sees — prior
   day/week high-low, big round numbers, major swing points, widely-watched MAs (20/50/200)?
2. **The level.** A trade needs a location: a level where the idea is right quickly or wrong
   quickly. "It's going up" is a narrative; "it holds 4510 or I'm out" is a trade.
3. **The trigger (entry timeframe).** What price behavior at the level turns the idea live —
   reclaim and hold, failed breakdown, break-and-retest, momentum ignition, rejection wick with
   volume. Define it before it happens.
4. **The context filters.** Session and time of day (see asset-classes.md), scheduled news
   (query the news feed), correlated markets (dollar for FX/gold, rates for equities, BTC for
   alts), and current volatility regime versus the setup's assumptions.

## Confluence checklist

Score each factor honestly. A setup doesn't need all of them, but it needs to know which it has.

- [ ] Higher-timeframe trend agrees (or this is explicitly a counter-trend trade, sized smaller)
- [ ] Clear level with history (multiple touches, prior high-volume battle, gap edge)
- [ ] Defined trigger, not "it looks strong"
- [ ] Stop goes behind structure, not at an arbitrary dollar amount
- [ ] Reward ≥ 2× risk to the *first realistic* target (not the moon target)
- [ ] Volume/participation supports the read (where volume data exists)
- [ ] No high-impact scheduled event inside the expected hold window (or the event IS the thesis
      and the trader knows it)
- [ ] Matches a playbook setup from the RAG store, or the trader knows it's off-playbook

## Grading

- **A** — trend, level, and trigger all aligned; clean invalidation; ≥2R to first target; no
  event risk. These are rare. Full size per the risk plan.
- **B** — solid but missing one element (counter-trend, or target only ~1.5R, or level is fresh).
  Tradeable at reduced size.
- **C** — a narrative looking for a trade. Name what's missing and don't produce a ticket.
  Most of what a scan surfaces is a C, and saying so is the job.

## The devil's-advocate pass (mandatory)

Before presenting any A or B setup, write the strongest honest case for the *other side*: who is
positioned against this trade and why might they be right? What does the chart look like to
someone with the opposite bias? If the counter-case is more convincing than the thesis, downgrade
the setup and say why. This pass exists because the trader is often already emotionally long the
idea by the time they ask — your independence is the product.

## Common playbook archetypes

Use these as shared vocabulary, not as an exhaustive or prescriptive list. The trader's own
playbook in the RAG store always takes precedence — query it first.

| Archetype | Core logic | Classic failure mode |
|---|---|---|
| Break and retest | Level breaks, first pullback to it holds | Retest that slices through = trapped, exit fast |
| Pullback in trend | Trend pauses to a rising MA / prior breakout zone | Buying a pullback that is actually a reversal; demand a trigger |
| Failed breakout / stop run | Break of an obvious level immediately reclaimed | Being early — wait for the reclaim, not the poke |
| Opening range breakout | First 15–60 min range breaks with participation | Chop days; check volatility regime and avoid inside days |
| Range fade | Established range, fade the edges with tight stop | The range eventually breaks; never fade fresh momentum into the level |
| VWAP reversion | Extended move snaps back toward VWAP intraday | Trend days don't revert; check the higher-timeframe first |
| Higher-timeframe S/R reaction | Weekly/monthly level first touch | Needs wide stops; size down accordingly |

## Presenting scan results

Cap at 3–5 candidates. For each: symbol, direction, grade, one-line thesis, the actionable level,
and what would trigger it. Full trade plans (per the template) only for A/B setups the trader
shows interest in. Ranked lists of twenty tickers are noise, not analysis.
