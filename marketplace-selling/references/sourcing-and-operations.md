# Sourcing and Operations

The day-to-day: buying stock to resell, tracking what's happening, fulfilling orders, handling
returns, and keeping the accounts alive. This is where a business is actually run or lost.

Contents:
- [Sourcing overstock and liquidation](#sourcing-overstock-and-liquidation)
- [Evaluating a lot before buying](#evaluating-a-lot-before-buying)
- [The order log](#the-order-log)
- [Metrics that matter](#metrics-that-matter)
- [Fulfilment and shipping](#fulfilment-and-shipping)
- [Returns and disputes](#returns-and-disputes)
- [Account health](#account-health)
- [Inventory and reordering](#inventory-and-reordering)
- [A weekly operating loop](#a-weekly-operating-loop)

## Sourcing overstock and liquidation

Where resale stock comes from, roughly cheapest-and-riskiest to safest:

- **Liquidation marketplaces** (B-Stock, Liquidation.com, direct retailer liquidation) — pallets
  and truckloads of returns/overstock/shelf-pulls. Cheap per unit, mixed condition, variable
  manifests. The core resale supply, and the core risk.
- **Overstock/wholesale closeouts** — surplus new stock from distributors. Higher cost, better
  condition, cleaner provenance and invoices.
- **Local sources** — store closing sales, auctions, estate lots, clearance arbitrage. Hit or
  miss; good for Facebook flipping.

Two things separate a business from a gamble here: **buying against a known channel and price**
(don't buy stock you have no proven place to sell), and **provenance you can defend** (see
account health).

## Evaluating a lot before buying

Run this checklist before committing money — the margin on resale is made or lost at purchase:

1. **Manifested or unmanifested?** A manifest lists contents and retail value; unmanifested is a
   gamble priced accordingly. Never pay near retail for unmanifested.
2. **Condition grade** — new / open-box / customer-return / shelf-pull / salvage. Returns and
   salvage need inspection and carry higher downstream return rates.
3. **Realistic sell-through**, not the manifest's retail total. Assume a chunk never sells; model
   the lot at 60–80% for mixed liquidation. See the lot maths in
   [pricing-and-fees.md](pricing-and-fees.md).
4. **Landed cost per unit** = lot price + inbound freight + sorting/repair time, divided by units
   you'll actually sell.
5. **Channel fit and gating** — *before buying*, confirm the category isn't gated on your target
   channel and that these goods can be listed. On Amazon, confirm the invoice will pass if asked.
6. **Authenticity and recall screen** — branded goods you can't vouch for, recalled electronics,
   expired consumables, and hazmat are all landmines. Counterfeits mean a permanent ban.
7. **Storage and cash** — a cheap pallet that ties up cash and floor space for six months has a
   real carrying cost. Factor it.

If the lot isn't clearly profitable at a realistic sell-through *and* cleanly sellable on a
channel you have, the answer is don't buy it. Enthusiasm for a low per-unit price is how resellers
end up with a garage of unsellable stock.

## The order log

Tracking turns "it feels like we're doing okay" into knowing which products and channels actually
pay. Schema, matching [assets/order-log-template.csv](../assets/order-log-template.csv), read by
`scripts/sales_metrics.py`:

| Column | Meaning |
|---|---|
| `order_id` | Unique order/transaction ID |
| `date` | ISO date (`YYYY-MM-DD`) |
| `channel` | `etsy` / `amazon` / `facebook` |
| `product_line` | `plants` / `3dprint` / `terrarium` / `wood` / `resale` |
| `sku` | Your product identifier |
| `qty` | Units in the order |
| `sale_price` | Item price charged (total for the line) |
| `shipping_charged` | Shipping charged to the buyer |
| `channel_fees` | Total platform + payment fees on the order |
| `shipping_cost` | What you actually paid to ship (label + materials) |
| `cost_of_goods` | Landed cost or make-cost, incl. your labour valuation |
| `status` | `completed` / `refunded` / `partial-refund` / `cancelled` |
| `refund_amount` | Amount refunded, if any |
| `return_reason` | Free text or controlled (`damaged` / `not-as-described` / `changed-mind` / `dead-on-arrival`) |
| `notes` | Free text |

Log **refunds and their reasons with the same care as sales** — the return pattern by product
line is one of the most decision-relevant things the metrics can show, and it's invisible if
refunds aren't recorded.

## Metrics that matter

Run `python scripts/sales_metrics.py logs/orders.csv`.

- **Net margin by channel and product line** — the headline. Reveals the line that looks busy
  but nets nothing (usually live goods after refunds, or resale after the dead units).
- **Fee drag** — fees + shipping as a share of revenue, per channel. Makes the "a price is not
  profit" point concrete and shows when a channel's economics have quietly turned.
- **Return/refund rate by product line** — plants and terrariums will run high; the question is
  whether the surviving margin still works.
- **Contribution per SKU** — which listings actually make money. The long tail of near-zero SKUs
  is worth pruning to focus photography and restock effort.
- **Revenue and order mix** across lines — the portfolio view, for deciding where to push.

Watch **trends**: fee drag creeping up, a product line's refund rate rising, a channel's net
margin sliding. As everywhere in this skill, the trend warns earlier than the level.

## Fulfilment and shipping

- **Dispatch time is a ranking and account-health metric** on Etsy and Amazon — set an honest
  processing time and beat it. Made-to-order items need a longer stated time, not a missed
  deadline.
- **Pack for the product:** live plants insulated with heat/cold packs and moisture control;
  terrariums double-boxed with secured substrate; wood and glass cushioned against edge impact;
  resale goods in right-sized boxes to avoid dimensional-weight penalties.
- **Buy postage through the channel** where it's discounted (Etsy/Amazon labels) and get
  **tracking on everything** — it's the evidence in a "not received" dispute.
- **Weather holds** for live goods: don't ship into a heatwave or freeze; state the policy in the
  listing so a delay isn't a complaint.
- **FBA vs self-ship** (Amazon): FBA buys Prime and hands off logistics but adds per-unit and
  storage fees and long-term-storage penalties on stale stock — good for fast-moving commodity
  resale, bad for slow or seasonal stock.

## Returns and disputes

- **Legitimate returns:** handle fast and politely; on Etsy and Amazon a graceful refund usually
  costs less than the metric damage and bad review of a fought one.
- **Live-arrival / breakage claims:** require a photo (state this in the policy), then replace or
  refund per your stated terms. A clear up-front policy converts most of these from disputes into
  routine.
- **A-to-z claims (Amazon) and chargebacks:** respond within the window with tracking and
  evidence — an unanswered claim is an automatic loss and an account ding. Tracking on every
  order is what wins these.
- **Facebook fraud patterns:** overpayment scams, "ship before funds clear," fake payment
  screenshots, off-platform redirection. Cash or cleared instant payment only; never ship on a
  promise.
- **Serial-refund abuse:** a buyer who repeatedly claims non-receipt or damage is a pattern worth
  noting; platforms have reporting for it.

## Account health

Directive 2, made concrete. A channel ban ends that revenue stream, often permanently:

- **Amazon** enforces on late-dispatch rate, order-defect rate, cancellation rate, authenticity
  and IP complaints, and policy violations — largely automated, with slow appeals. Keep metrics
  green, keep invoices, respond to every claim.
- **Etsy** can suspend for reselling non-handmade goods, IP infringement, or payment-account
  issues (a reserve or hold on funds is an early warning sign to take seriously).
- **Facebook Commerce** bans for prohibited categories, live-animal/plant policy trips, and
  "suspicious activity," and is notoriously hard to appeal.

The through-line: **don't bet the account to save a few dollars on one order or one questionable
lot.** When a listing or a fulfilment choice skirts a policy, the expected cost isn't the fee —
it's a share of losing the whole channel. Flag it before it posts.

## Inventory and reordering

- **Made lines:** track your realistic make-rate; don't list stock you can't produce in the
  stated dispatch window. Live plants have a propagation lead time measured in months — restock
  can't be rushed, so guard mother stock and pipeline ahead.
- **Resale:** track sell-through per SKU and per supplier; reorder the fast movers from proven
  suppliers, and stop rebuying the slow tail.
- **Cross-listing:** don't oversell one unit across channels — buffer stock, sync tools, or
  single-channel one-offs (see [channels.md](channels.md)).
- **Dead stock:** stock that hasn't moved in a season is tying up cash and space at a real
  carrying cost. Liquidate it cheap on Facebook and redeploy — holding it hoping for full price
  usually costs more than the discount.

## A weekly operating loop

A rhythm that keeps the business ahead of its problems rather than reacting:

- **Daily** — fulfil and dispatch orders within the processing window; answer buyer messages
  (response time is a metric); check for and respond to any claims/disputes immediately.
- **Weekly** — log the week's orders and refunds; scan account-health dashboards on each channel;
  restock fast movers and flag dead stock; review any new sourcing offers against the checklist.
- **Monthly** — run `sales_metrics.py`; review net margin and fee drag by channel and line; prune
  or reprice the loss-making tail; re-run pricing on anything hit by a fee or cost change;
  reconcile realised sell-through against sourcing estimates.
- **Seasonally** — plan ahead of the spikes (holidays for terrariums/gifts, spring for plants);
  build made-line stock before the rush; time resale buys to demand.

The monthly metrics pass is the one that gets skipped and the one that catches the slow leaks —
the creeping fee drag and the product line that's quietly been losing money for two months.
