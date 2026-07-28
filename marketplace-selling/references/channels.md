# Channels

Fee numbers here are typical figures and they change — platforms revise fee schedules
regularly, and they vary by country and category. Treat them as starting points for the maths,
verify the current rate on the platform's own fee page before a real pricing decision, and let
`scripts/channel_margin.py` do the calculation with the rate you confirm.

Contents:
- [At a glance](#at-a-glance)
- [Etsy](#etsy)
- [Amazon](#amazon)
- [Facebook Marketplace and Shops](#facebook-marketplace-and-shops)
- [Choosing a channel](#choosing-a-channel)
- [Cross-listing](#cross-listing)

## At a glance

| | Etsy | Amazon | Facebook |
|---|---|---|---|
| **Best for** | Handmade, custom, niche, decorative | Commodity products with steady demand and clean logistics | Local sales, bulky items, fast liquidation |
| **Typical take rate** | ~10–11% + payment processing | 8–20% referral (commonly 15%) + plan + any FBA | ~0% local; ~5% for shipped Shops checkout |
| **Buyer intent** | Browsing for something special | Searching for a specific thing to buy now | Bargain-hunting, local pickup |
| **Trust level** | High (platform mediates) | High (Amazon guarantees) | Low (buyer beware, scam-prone) |
| **Fragile/live goods** | Allowed, common | Heavily restricted for live plants | Local hand-off avoids shipping risk entirely |
| **Setup friction** | Low | High (verification, gating) | Very low |

## Etsy

The natural home for four of the five lines: plantlets, terrariums, 3D-printed decorative and
custom goods, and woodworking. Overstock resale generally does **not** belong here — Etsy
requires items to be handmade, vintage (20+ years), or a craft supply, and reselling
new manufactured goods violates policy and risks the shop.

**Fees**, stacked, roughly:
- **Listing fee** $0.20 per listing, per 4 months or per sale (multi-quantity relists).
- **Transaction fee** ~6.5% of the item price *plus the shipping you charge* — a point people
  miss, so "free shipping" isn't free of fees.
- **Payment processing** ~3% + $0.25 (varies by country).
- **Offsite Ads fee** 12% or 15% of an order that came through an Etsy-placed ad. Mandatory for
  shops over a revenue threshold; a real and unpredictable cost on those orders.
- **Optional Etsy Ads** (onsite) — a chosen daily budget, separate from the above.
- A **regulatory operating fee** applies in some countries.

All in, budget **~10–11% plus payment processing**, and more on Offsite-Ads orders. The
calculator models the base case; the Offsite Ads hit is occasional and can't be predicted per
order.

**What wins on Etsy:** strong SEO (see [listings-and-seo.md](listings-and-seo.md)), genuinely
good photos, a coherent shop brand, reviews, and either uniqueness or personalisation. Etsy's
search rewards listings that convert, so the first sales and reviews on a listing matter
disproportionately.

**Watch:** the handmade/reselling policy above; trademarked-character prints (same IP rules as
the `3d-printing` skill); and star-seller metrics (dispatch time, reviews, message response),
which affect visibility.

## Amazon

The right channel for **commodity products with real demand and clean logistics** — which,
across these five lines, mostly means **resold overstock in categories that aren't gated**, and
possibly repeatable 3D-printed or wood products that behave like a catalogue SKU. It is a poor
fit for one-of-a-kind items, live plants, and anything you can't restock on demand.

**Fees:**
- **Referral fee** 8–20% by category, **most commonly 15%**. Charged on the total including
  shipping.
- **Selling plan** — Individual $0.99/item, or Professional $39.99/month. Past ~40 items/month
  the Professional plan is cheaper, and it's required for many features and categories.
- **FBA (Fulfilled by Amazon)** — Amazon stores, picks, packs and ships. Per-unit fulfilment
  fee by size/weight plus monthly storage (and painful long-term storage fees on stale stock).
  Buys the Prime badge and hands off logistics.
- **FBM (Fulfilled by Merchant)** — you ship. No FBA fees, but you own delivery performance and
  don't get Prime unless approved for Seller-Fulfilled Prime.

**Gating and approval.** Many categories and brands are **gated** — you must apply and often
show **invoices from an authorised supplier** to sell in them. This is the crux for overstock
resale: liquidation stock frequently can't clear Amazon's invoice requirements, so a lot that's
cheap to buy can be *unsellable* on Amazon even when genuine. Check gating and invoice
acceptability **before** buying to resell, not after.

**Live plants** are heavily restricted and largely prohibited or gated on Amazon; treat
plantlets and terrariums as not-for-Amazon unless the user has specifically cleared it.

**Account health is unforgiving.** Amazon suspends on metrics (late shipment, defect rate,
policy violations, authenticity complaints) with automated enforcement and slow, uncertain
appeals. An account with money tied up in FBA inventory is especially exposed. This is the
channel where directive 2 bites hardest.

## Facebook Marketplace and Shops

Two different things under one roof:

- **Marketplace (local)** — free to list, no selling fee on local cash/pickup deals. The right
  channel for **bulky, heavy, fragile, or fast-to-liquidate** items: large terrariums,
  furniture-scale woodworking, and overstock lots you want gone. Local hand-off **eliminates
  shipping cost and breakage risk entirely**, which is a genuine structural advantage for glass
  and wood.
- **Shops / checkout (shipped)** — a real storefront with on-platform checkout, integrated with
  Instagram. A **selling fee around 5% per shipment** (with a small-order minimum). Lower take
  than Etsy or Amazon, but far less buyer traffic and trust for a new shop.

**Strengths:** no/low fees, huge audience, instant listing, excellent for local and bulky
goods, and a good release valve for slow inventory.

**Weaknesses:** low trust and high scam exposure (overpayment scams, fake-payment "I've sent
it, ship now" pressure, off-platform redirection); minimal buyer protection; and **Commerce
account bans** that can hit for policy trips (live animals, certain plant claims, prohibited
categories) and are hard to appeal.

**Safety rules for local deals** (real, worth stating to the user): meet in public or a police
"safe exchange" spot, cash or an instantly-verified payment only, never ship before cleared
funds, and never move the conversation to a channel the buyer insists on. Most Marketplace
fraud is a variation on "pay you too much, ship before it clears."

## Choosing a channel

A quick decision guide; the per-line detail is in
[product-lines.md](product-lines.md).

- **Handmade, custom, decorative, niche** (plantlets, terrariums, printed/wood décor) → **Etsy**.
- **Commodity with restockable demand, not gated** (much overstock resale) → **Amazon**.
- **Bulky, heavy, fragile, or needs to go fast**; local buyers → **Facebook Marketplace**.
- **Building an owned brand with shipped orders and Instagram reach** → **Facebook/IG Shops**,
  usually alongside Etsy rather than instead of it.

The honest default: **start where the product's shape fits the channel's shape**, prove the
economics on one channel, then expand. Listing everything everywhere on day one multiplies the
listing and photography work and the ways an account can trip, without multiplying sales.

## Cross-listing

Selling the same item on more than one channel is worthwhile for restockable products, with two
rules that prevent the usual disasters:

1. **Price for each channel's fees, not one price everywhere.** A 15% Amazon referral plus FBA
   and a ~10% Etsy take are different economics; a single price is profitable on one and a loss
   on the other. Use the calculator per channel.
2. **Don't oversell your stock.** One physical unit listed on three channels can sell three
   times. For anything not made-to-order, either keep buffer stock, sync inventory (via a
   listing tool), or list one-offs on a single channel. Overselling a live plant you can't
   replace means cancelling on a buyer, which dents metrics on the very channels you're trying
   to grow.

For genuinely one-of-a-kind items (a specific terrarium, a single wood piece), cross-listing
mostly isn't worth the overselling risk — pick the best-fit channel and put the effort into the
listing instead.
