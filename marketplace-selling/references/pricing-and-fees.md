# Pricing and Fees

The core discipline of this whole business: **a price is not profit.** By the time a sale
clears, the channel fee, payment processing, shipping and its materials, the cost of the goods,
and a slice of the return rate have all come out. The recurring, expensive mistake is quoting
margin off the sticker price. Use `scripts/channel_margin.py` for anything real.

Contents:
- [The margin stack](#the-margin-stack)
- [Shipping is a cost centre](#shipping-is-a-cost-centre)
- [The return reserve](#the-return-reserve)
- [Pricing methods](#pricing-methods)
- [Setting a price per channel](#setting-a-price-per-channel)
- [Repricing](#repricing)
- [Overstock lot maths](#overstock-lot-maths)

## The margin stack

Every sale, top to bottom:

```
  Sale price (item + shipping charged to buyer)
– Channel fee            (Etsy ~6.5% of item+ship; Amazon ~15%; FB ~5% or 0 local)
– Payment processing     (~3% + $0.25, where the channel doesn't bundle it)
– Listing/plan cost      (Etsy $0.20; Amazon plan amortised; FBA per-unit if used)
– Shipping actually paid  (label + box + padding + tape; often > what you charged)
– Cost of goods          (materials + your labour for makes; landed cost for resale)
– Return reserve         (return rate × cost of a return)
─────────────────────────
= Net profit
```

Two lines get skipped and both are large: **your own labour** on the maker lines (a terrarium is
mostly time, not moss and glass), and the **return reserve** (below). Leave them out and a
losing product looks like a winner.

## Shipping is a cost centre

Shipping is where these product lines bleed, and it's priced on **weight and dimensions**, not
value — which punishes exactly the heavy, bulky, fragile goods this business makes.

- **Charge it as a real line or bake it into a "free shipping" price** — but either way *pay
  attention to what you actually pay*, because on Etsy the fee is charged on the shipping too.
- **The label is not the whole cost.** Box, padding, tape, and the fragile/live extras (heat
  packs, moss wrap, double-boxing) are real per-order costs — often several dollars for a
  terrarium or plant.
- **Dimensional weight** bills bulky-but-light parcels by size; a big printed or foam-packed item
  can cost far more to ship than its weight implies.
- **Free-shipping thresholds** (Etsy nudges shops toward free US shipping for search
  visibility) mean the shipping cost is now inside your price and eating your margin invisibly —
  it hasn't gone away.
- For **heavy/fragile** goods, local Facebook sale at a lower headline price can net *more* than a
  shipped Etsy sale once breakage returns and shipping vanish. Run both.

The calculator takes a shipping figure and shipping materials separately so the real cost is
visible, not buried.

## The return reserve

Returns are a cost of doing business, not an exception, and they hit these lines unevenly:

- **Live plants and terrariums:** high effective return/refund rate via live-arrival and
  breakage claims — often the biggest hidden cost. A refunded dead plant is a total loss (goods +
  shipping + fee, sometimes non-recoverable).
- **Overstock resale:** returns driven by condition mismatch; often resaleable if graded
  honestly, a write-off if not.
- **Makes to spec:** low returns if the listing set expectations well; high if it oversold.

Model it as a **reserve**: (return rate) × (cost of a return). At a 10% refund rate on a product
that's a total loss when returned, ~10% of the sticker vanishes before any profit. The calculator
takes a `--return-rate` for exactly this.

## Pricing methods

Two, and you want both numbers:

**Cost-plus / keystone.** Cost × a multiple. Traditional retail "keystone" is 2× (a 50% margin),
and handmade often needs **2.5–3×** to survive the fee stack and pay for labour. This sets the
**floor** — the price below which you lose money. The margin script's `--target-margin` mode
solves for it directly.

**Value / market-based.** What the item is worth to the buyer and what comparable listings
charge. A rare variegated plant, a custom terrarium, or a personalised board is priced on
desirability and scarcity, not cost — and cost-plus would leave most of the value on the table.
This is where the maker lines actually make money.

Use cost-plus to find the floor, then price to market above it. **If the market price is below
your cost-plus floor, that product doesn't work on that channel** — the honest answer is don't
sell it there, not shave the margin to nothing.

## Setting a price per channel

Because fees differ, the same net requires different prices per channel. Work backwards from the
net you need:

1. Decide the **net profit** (or margin) you want.
2. Run `channel_margin.py --target-margin` for each channel — it grosses up through that
   channel's fees and your shipping to the price to list.
3. **Sanity-check against comparable listings.** If the required price sits above the market,
   the channel's fees don't support the product; if it sits well below, you may be underpricing
   (and reading as cheap/low-quality — a real conversion problem).

A worked instinct: an item costing $6.50 landed, shipped for ~$5, needs to list around
**$22–26 on Etsy** and **$26–30 on Amazon** to clear a healthy margin after fees — the Amazon
price is higher for the *same* take-home because the referral fee is larger. One price across
both would over- or under-shoot on one of them.

## Repricing

- **Underperforming (views, no sales):** first confirm it's a price problem not a photo problem
  (see [listings-and-seo.md](listings-and-seo.md)). If price, test a drop against comparables —
  but check the floor first; sometimes the right move is a *better listing*, not a lower price.
- **Selling out fast:** you may be underpricing. Raise gradually and watch conversion; a
  scarce plant or a popular custom item can often take more.
- **Fee or cost changed:** platforms raise fees and suppliers raise prices; a product priced fine
  last year can be underwater now. Re-run the stack across the catalogue periodically.
- **Amazon competition:** avoid reflexive race-to-the-bottom repricing — chasing the Buy Box down
  can push a whole category below everyone's cost. Know your floor and hold it.

## Overstock lot maths

Resale pricing runs on the **lot**, not the unit, and the number that matters is net across the
whole lot at a realistic sell-through:

```
Lot revenue  = Σ (unit sale price × units that actually sell)
Lot cost     = lot price + inbound shipping + sorting/repair + (fees + shipping per sold unit)
Sell-through = units sold ÷ units bought      (assume 60–80% for mixed liquidation, not 100%)
```

The dead units carry no revenue but full purchase cost, so they drag the whole lot's margin.
**Before buying a lot, estimate the net at a realistic sell-through** — a lot that's profitable
at 100% sold is often a loss at 65%, which is the number that actually happens. Log realised
sell-through per supplier in the sourcing log so the estimates get better and the lucky-once
suppliers get exposed.
