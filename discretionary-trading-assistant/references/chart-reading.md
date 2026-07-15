# Reading Chart Screenshots

A screenshot is a witness statement, not evidence. Extract what it says systematically, rate
your confidence, then verify against live data before building anything on it.

## Extraction procedure

Work through the image in this order and write down what you find:

1. **Identity.** Symbol/pair, exchange or platform (TradingView, IBKR TWS, Kraken, thinkorswim,
   NinjaTrader all have recognizable chrome), timeframe, and — important and often missed — the
   timestamp or rightmost candle's date/time. A perfect setup on a screenshot from last Tuesday
   is trivia.
2. **Price scale.** Read the y-axis values and the current/last price. Derive the approximate
   price of anything you reference from the axis — never eyeball "that looks like about 450"
   without anchoring to gridlines.
3. **Structure.** Trend direction on this timeframe, notable swing highs/lows, gaps,
   consolidations, and where current price sits in the visible range.
4. **Indicators.** Identify each overlay (MAs — note likely period from behavior, VWAP, bands)
   and each pane (RSI, MACD, volume). Read their current values where legible.
5. **The trader's annotations.** Drawn lines, boxes, arrows, text. These are the most important
   part of the image — they tell you what the trader already believes. Read exact prices for
   drawn horizontals off the axis.
6. **What's NOT visible.** Timeframes you can't see, the left side of the chart that's cut off,
   volume if absent, and anything the crop hides. Name these gaps explicitly.

## Confidence labeling

For every price you extract, attach a confidence: **exact** (printed as text on screen, e.g. a
price label or last-price box), **read** (interpolated from the axis, ±a few ticks), or
**guessed** (inferred from context). Analysis and especially sizing must use exact or verified
numbers — if the stop level is "read", confirm it with the trader before computing size.

## Verify, then analyze

Immediately after extraction, if the relevant broker MCP is up:

- Pull the current quote. If the market has moved materially since the screenshot, say so first —
  the setup may already be triggered, invalidated, or gone.
- Pull recent bars on the screenshot's timeframe and sanity-check your structural read (does the
  swing high you identified actually print at the price you read?).

Then hand off to the standard process in setup-analysis.md. The screenshot supplies the thesis
and levels; the live data supplies the truth.

## Asking instead of assuming

If the screenshot leaves ambiguity that changes the analysis, ask — briefly, all at once, not in
dribbles. The usual missing pieces:

- Which line is the intended entry vs. the stop (when multiple horizontals are drawn)
- Long or short (not always obvious from annotations)
- Timeframe, when the platform crops it out
- Whether this is a live position or a candidate

## Multiple screenshots

Traders often send a sequence (daily, then hourly, then 5-minute). Treat them as one top-down
analysis: reconcile the levels across images (the same level should appear at the same price),
and flag any contradiction between frames rather than analyzing each in isolation.
