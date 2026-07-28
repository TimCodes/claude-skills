# Selling and Licensing

This is practical guidance for a hobbyist-to-small-seller operating in normal territory —
selling your own designs and appropriately-licensed models through ordinary channels. It's
written to help you move confidently, not to make you nervous. Two things genuinely warrant
care because they carry real cost: a model's licence (a CC-NC model can't be sold, full
stop) and safety-critical parts (don't sell anything where failure hurts someone). Those
aside, price the work, read the licence, and get on with it. Rules vary by country and
change, so for a specific high-stakes question the actual licence text or marketplace terms
are the authority — but most of the time this section is all you need.

Contents:
- [Costing a print honestly](#costing-a-print-honestly)
- [The costs people forget](#the-costs-people-forget)
- [Pricing](#pricing)
- [Licensing — other people's models](#licensing--other-peoples-models)
- [Licensing — your own models](#licensing--your-own-models)
- [What not to print for sale](#what-not-to-print-for-sale)
- [Where to sell](#where-to-sell)
- [Client work](#client-work)
- [Scaling a print farm](#scaling-a-print-farm)

## Costing a print honestly

Most people cost a print as "grams × filament price" and are then puzzled that the
business doesn't work. Use `scripts/print_cost.py`, which builds the full stack:

- **Material** — grams × (spool price ÷ spool grams). Include purge, prime lines and
  supports; the slicer estimate usually understates real consumption.
- **Machine time** — print hours × machine hourly rate, where the rate is
  (printer cost ÷ expected life hours) + maintenance provision. A £400 printer over
  ~4000 usable hours is ~£0.10/hour of depreciation, plus consumables.
- **Power** — print hours × average watts × electricity price. A typical FDM printer
  averages 100–150 W (heated bed dominating), a resin printer 50–100 W. Usually small, but
  real at farm scale.
- **Consumables** — nozzles, build surfaces, FEP film, IPA, gloves, desiccant, glue.
- **Labour** — setup, plate prep, support removal, sanding, gluing, painting, packing.
  **Usually the largest cost for anything not shipped raw off the plate.**
- **Failure uplift** — divide the whole cost by (1 − failure rate). At a 10% failure rate,
  the good parts must carry the cost of the bad ones, so true cost is ~11% higher than
  nominal.
- **Post-sale costs** — packaging, shipping, marketplace fees (Etsy's various fees
  typically total ~10%+), payment processing, returns and reprints.

Only after all of that does a margin get applied.

## The costs people forget

In rough order of how often they're omitted and how much they matter:

1. **Labour.** A print that takes 30 minutes of support removal and sanding has more labour
   cost than material cost, and often more than machine cost. Track `post_hours` in the
   print log so this is measured rather than guessed.
2. **Failure rate.** Nobody's success rate is 100%, and failures consume material, machine
   hours and often the deadline.
3. **Design and setup time.** For custom work, CAD and slicing time is real work. Charge it
   as a one-off setup fee rather than burying it in per-unit price — otherwise a repeat
   order is priced as if the design were free, which is fine, and a one-off order is priced
   as if the design were free, which is a loss.
4. **Machine depreciation.** Printers wear out. A farm that doesn't reserve for replacement
   is consuming capital and calling it profit.
5. **Marketplace and payment fees.** ~10–15% off the top on most platforms.
6. **Your own time on customer service, listings and photography.** For a small shop this
   can exceed print time.

## Pricing

Two approaches, both worth doing:

**Cost-plus** — true cost × margin. Establishes the floor below which you're losing money.
For made-to-order printing, a 2–3× multiplier on true cost is a common starting point.

**Value-based** — what the item is worth to the buyer. A custom jig that saves a machine
shop an hour a day is worth far more than its material cost, and pricing it at cost-plus
leaves most of the value on the table. This is where the actual money is for functional and
custom work.

Realities worth stating plainly to anyone starting out:

- **Competing on price for generic models is a losing game.** Articulated dragons and
  common Thingiverse models are printed by thousands of people with cheaper electricity
  and more machines. The margin is near zero and falling.
- **The money is in what isn't commoditised**: custom and bespoke work, functional parts
  for local businesses, replacement parts that aren't otherwise available, your own
  original designs, prototyping services, and finishing quality others won't do.
- **Charge for the design, not just the plastic.** Selling print time as a commodity puts
  you in a race against people who value their own time at zero.
- **Minimum order value.** A £4 item with 20 minutes of handling and packing is a loss
  regardless of the material maths.

## Licensing — other people's models

**This is the most commonly and expensively misunderstood area in the hobby.** Downloading
a model does not grant the right to sell prints of it. The licence the designer attached
governs, and it's usually stated on the model page.

Creative Commons variants, which cover most free models:

| Licence | Can you sell prints? |
|---|---|
| **CC0** / public domain | Yes, no conditions |
| **CC-BY** | Yes, with attribution to the designer |
| **CC-BY-SA** | Yes, with attribution; derivatives must carry the same licence |
| **CC-BY-ND** | Prints generally yes with attribution, but **no modified versions** |
| **CC-BY-NC** | **No — non-commercial only.** No selling prints, at all |
| **CC-BY-NC-SA / NC-ND** | **No commercial use** |

The **NC** clause is the one that catches people. A large share of popular free models are
NC-licensed, and selling prints of them is a licence breach — designers do notice, do
issue takedowns, and marketplaces do act on reports.

Also relevant:

- **Marketplace-specific terms.** MakerWorld, Printables, Cults3D and Thingiverse each
  have their own terms layered on top, and some designers sell explicit **commercial
  licences** separately — often inexpensive and the clean way to sell someone's model
  legitimately. When in doubt, buy the commercial licence or ask the designer; most
  respond, and written permission resolves it.
- **Patents** can cover functional designs independent of any model licence.
- **Trademarks and copyright in characters.** Printing and selling fan art of
  copyrighted or trademarked characters is infringement regardless of who modelled it, and
  regardless of whether the STL was free. Rights holders do enforce.
- **"For personal use" purchases.** Buying an STL usually licenses you to print it, not to
  sell prints. Check the specific terms.

The practical rule: **before selling prints of anything you didn't design, read the actual
licence on the model page.** If it says NC, the answer is no unless you buy a commercial
licence.

## Licensing — your own models

If the user designs their own, they choose the terms:

- **Sell the STL/3MF** on Cults3D, MyMiniFactory, Patreon, or their own storefront.
- **Sell prints** and keep the files private.
- **Release free under CC-BY-NC**, keeping commercial rights to sell separately — a common
  and effective model that builds an audience while protecting income.
- **MakerWorld/Printables reward schemes** pay for downloads and prints, which can be
  meaningful for popular designs.

Keep the source CAD (STEP or native), not just exported meshes. A mesh is very hard to
edit properly, and losing the parametric source means every revision is a rebuild.

Watermarking and file protection are largely ineffective — anything downloadable gets
shared. Business models that assume otherwise tend to disappoint.

## What not to print for sale

- **Firearms and firearm components.** Heavily regulated and often outright criminal to
  manufacture or distribute depending on jurisdiction; this is not an area to improvise in.
- **Copyrighted or trademarked characters and brands.** Fan art sells until the rights
  holder notices.
- **Anything load-bearing where failure hurts someone** — climbing hardware, tow points,
  child car-seat parts, structural or safety-critical components. Printed parts have
  scatter, hidden defects and anisotropy. Say this clearly when it comes up, because the
  liability is real and so is the risk.
- **Medical or dental devices** — regulated, and requiring biocompatible certified
  materials and process validation.
- **Food-contact items** are fine to make and sell — just do them properly, because one
  thing here is genuinely counterintuitive: **"food-safe filament" does not make a food-safe
  part.** The gap is the layer crevices, which harbour bacteria and can't be reliably
  cleaned, plus the nozzle (brass leaches lead — use stainless) and any pigment. The recipe
  that works: an appropriate material, a smooth or sealed surface, and a food-safe epoxy or
  resin coating over the print. For repeated-use items that's the way; for one-off or dry
  contact (a cookie cutter, a dry-goods scoop) a well-printed part is usually fine as-is.
- **Toys for young children**, without checking toy-safety rules (CPSIA in the US, EN 71 in
  the EU) — small parts, choking hazards and chemical testing all apply.

## Where to sell

| Channel | Notes |
|---|---|
| **Etsy** | Largest craft marketplace; fees ~10%+ total; saturated for generic prints, good for customised and personalised items |
| **eBay/Amazon** | Higher volume, thinner margins, more commoditised |
| **Own storefront** (Shopify, etc.) | Best margins, but you supply all the traffic |
| **Local businesses** | Often the best margins available — replacement parts, jigs, signage, prototypes. Underexploited because it requires talking to people |
| **Craft fairs / markets** | Good for finished decorative goods; immediate feedback on what sells |
| **Design marketplaces** (Cults3D, MyMiniFactory) | Selling files rather than prints — no per-unit cost, scales without machine time |
| **Patreon / membership** | Recurring income from a design catalogue; requires consistent output |
| **Print services** (Craftcloud, Shapeways, Xometry as a supplier) | Fills machine time without marketing effort, at low margin |

## Client work

For bespoke jobs, quote properly using
[assets/job-quote-template.md](../assets/job-quote-template.md). The things to nail down in
writing before starting:

- **Material and its limitations**, stated explicitly — especially service temperature and
  UV, so a PLA part isn't expected to live on a dashboard.
- **Tolerances achievable**, so ±0.2 mm isn't assumed to be ±0.02 mm.
- **Cosmetic expectations** — layer lines are inherent; if they expect injection-moulded
  smoothness, that's finishing work and must be priced.
- **A separate setup/design fee** from the per-unit price.
- **Revision limits** — how many design iterations are included.
- **Lead time with a failure buffer.** Prints fail; a quoted deadline with no slack will
  eventually be missed.
- **Explicit exclusion of safety-critical use.**

For repeat commercial clients, a printed sample before the full run costs little and
prevents the expensive misunderstanding.

## Scaling a print farm

Bottlenecks, in the order most operations hit them:

1. **Post-processing labour.** Almost always the real ceiling. Machines run unattended;
   humans remove supports. Design parts to need less finishing before buying more printers.
2. **Demand.** Producing parts is far easier than selling them. Secure the orders before
   the capacity.
3. **Machine attention** — plate changes, failures, maintenance. Automation (auto-ejection,
   remote monitoring) helps only after post-processing is solved.
4. **Space and power.** Printers need ventilation, stable temperature, and circuit capacity.
5. **Capital.** More machines mean more depreciation and maintenance, so utilisation has to
   be genuinely high before another printer pays.

Grow the binding constraint. The characteristic failure is buying a fifth printer while
drowning in support removal and short of orders — which adds cost and capacity that can't
be converted into revenue.
