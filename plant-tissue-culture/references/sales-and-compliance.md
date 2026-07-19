# Sales and Compliance

This file covers commercial and regulatory ground. Rules vary enormously by country, state, and
species, and they change. Treat everything here as orientation — what to look into and what
questions to ask — not as legal advice. For anything with real money or real liability attached,
the user should confirm with their state/national agriculture department, and with an attorney
for intellectual property matters. Say so plainly rather than letting confident-sounding
guidance stand in for verification.

Contents:
- [Unit economics](#unit-economics)
- [What to sell, and at what stage](#what-to-sell-and-at-what-stage)
- [Pricing](#pricing)
- [Intellectual property — other people's](#intellectual-property--other-peoples)
- [Intellectual property — yours](#intellectual-property--yours)
- [Licenses and regulatory basics](#licenses-and-regulatory-basics)
- [Moving plants across borders](#moving-plants-across-borders)
- [Shipping](#shipping)
- [Listings, honesty, and customer expectations](#listings-honesty-and-customer-expectations)
- [Scaling](#scaling)

## Unit economics

Most small labs price by looking at competitors and never compute their actual cost. Do the
arithmetic before advising on price.

**Cost per plant** builds up across stages:

- **Consumables** — medium (basal salts, sucrose, agar/gellan, PGRs), vessels and closures,
  gloves, blades, alcohol. Typically small per unit; agar or gellan usually dominates.
- **Labor** — almost always the largest cost, and the one people leave out entirely. A skilled
  technician transfers on the order of 500–1500 explants per day depending on species and shoot
  size. Divide fully-loaded hourly cost by that throughput to get labor per unit per cycle, then
  multiply by the number of cycles a plant passes through.
- **Overhead** — hood, autoclave, culture room electricity (lights run 16 h/day), rent,
  depreciation.
- **Losses** — contamination, off-types, Stage IV mortality. This is where naive costing goes
  most wrong: if 25% of units die in acclimatization, the surviving plants must carry that cost,
  so your real cost per *sellable* plant is roughly cost ÷ 0.75.
- **Time to market** — a plant that takes 18 months from initiation carries 18 months of capital.

The key structural fact: **initiation is expensive and multiplication is cheap.** The first
plant of a genotype may cost hundreds of dollars in labor and failed attempts; the ten-thousandth
costs cents. This is why tissue culture rewards volume and punishes one-off jobs, and why custom
initiation work should be priced as a service with an up-front fee rather than per plant.

## What to sell, and at what stage

| Product | Who buys it | Notes |
|---|---|---|
| **Cultures in flask / multiplication stage** | Other labs, growers with facilities | Highest margin, lowest handling cost, smallest market. You're selling propagation capacity, so IP terms matter enormously |
| **Rooted plantlets in flask** | Hobbyists, collectors, resellers | Popular in the collector market. Ship well, look impressive, and the buyer assumes the Stage IV risk — be clear about that up front |
| **Deflasked, acclimatized plugs** | Nurseries, growers, retail | The large market. You absorb the Stage IV losses, so price accordingly |
| **Finished plants** | Retail, direct-to-consumer | Highest price per unit, longest capital cycle, needs growing space you may not have |
| **Custom initiation / cleanup service** | Breeders, collectors, growers | Price per project, not per plant. Include an explicit failure clause — some material simply will not establish, and the labor is spent either way |
| **Virus indexing and cleanup** | Nurseries, breeders, germplasm collections | Specialized and defensible; requires reliable indexing capability |

Selling **in flask** to hobbyists is attractive because it moves the hardest step onto the buyer,
but it generates support burden and disappointed customers when they lose the whole flask in
acclimatization. If a user goes this route, they should ship acclimatization instructions with
every order and set expectations in the listing. It's both kinder and cheaper than handling the
complaints.

## Pricing

Drivers, in rough order of influence: **scarcity and hype** (dominant in the collector aroid and
rare houseplant market, and volatile), difficulty of propagation, unit cost, time to salable
size, competitor pricing, and whether the plant is protected IP.

Two things to warn users about:

**Hype prices fall, often fast.** The whole point of tissue culture is to convert a scarce plant
into an abundant one — you are personally destroying the scarcity premium you're pricing
against. A genotype that fetches $500 when three people have it fetches $30 once a lab produces
5,000, and the lag between committing to a scale-up and hitting the market is 12–24 months.
Anyone modeling revenue at today's price for a crop landing in 18 months is going to be badly
wrong. Model the price they'll get at delivery, and stress-test at a fraction of today's.

**Don't compete on price against industrial labs** on commodity crops. Labs in low-labor-cost
regions produce standard ornamentals at a per-unit cost a small operation cannot approach. Small
labs win on: rare and difficult genotypes, custom and contract work, proprietary genetics they
own, local relationships and fast turnaround, and quality/cleanliness guarantees.

## Intellectual property — other people's

**This is the single largest legal risk in commercial tissue culture**, because tissue culture is
the most efficient possible way to infringe a plant patent, and because it is trivially provable
after the fact.

Before scaling any named cultivar, check its status:

- **US plant patents** (numbered `PPxxxxx`) cover asexually reproduced plants for 20 years from
  filing. The patent holder's exclusive right specifically includes asexual reproduction —
  which is exactly what micropropagation is. Searchable via the USPTO patent database and Google
  Patents.
- **US utility patents** can also cover plants, traits, and methods, with broader scope.
- **Plant Variety Protection (PVPA)** in the US covers sexually reproduced varieties and tubers.
- **Plant Breeders' Rights / UPOV** systems cover varieties in most other countries; CPVO
  administers EU-wide rights.
- **Trademarked trade names** are a separate layer. A plant can be sold under a trademarked
  marketing name while its cultivar name is unprotected — or the reverse. Using someone's
  trademark to sell your plant is a distinct violation from propagating their patented plant.
- **Licensed cultivars** — many are propagated only under license, often with royalty per unit
  and audit rights.

Practical guidance: **any cultivar with a trademark symbol, a series name, or a recent
introduction date should be assumed protected until verified otherwise.** "I bought the plant so
I can propagate it" is a common and completely wrong belief — buying a plant conveys that plant,
not the right to reproduce it. Say this clearly when it comes up; users get it wrong constantly
and the consequences (damages, destruction orders, injunctions) are severe.

Unprotected: expired patents, species and unnamed selections, heirloom and old cultivars, and
anything the breeder explicitly released. Plenty of viable business exists here.

## Intellectual property — yours

If the user has bred something novel, protection is worth considering *before* they show it to
anyone.

**The timing trap:** in the US, a plant patent must generally be filed within **one year** of
public disclosure or sale — a grace period, but a hard deadline. Many other jurisdictions and
UPOV-based PBR systems have **no grace period at all**, or a much narrower one, so a single
Instagram post or a sale can permanently forfeit protection outside the US.

The practical advice: **talk about protection before publishing photos, sending plants to
influencers, or listing for sale.** This is one of the most common and most expensive unforced
errors in ornamental breeding, and it's completely avoidable.

Requirements generally include distinctness from existing varieties, uniformity, stability across
propagation, and asexual reproduction demonstrated (for US plant patents). The DUS documentation
described in [breeding-and-selection.md](breeding-and-selection.md) is what feeds this.

Alternatives to formal protection: trademark the marketing name (cheaper, indefinite renewal,
protects the brand rather than the genetics), keep the parent lines as a trade secret, or license
exclusively to a single propagator with contractual restrictions. For many small breeders, a
trademark plus a licensing relationship is more practical than a patent.

## Licenses and regulatory basics

Varies by jurisdiction; these are the categories to check:

- **Nursery / plant dealer license** — most US states require one to sell plants, including
  online and including small operations. Typically an annual fee and a periodic inspection.
- **Sales tax registration** for direct retail.
- **Inspection and certification** — some states require nursery stock inspection, and shipping
  to certain states (California, Florida, Arizona, Hawaii, Oregon among the strictest) triggers
  additional requirements or outright prohibitions on some genera.
- **Noxious weed and invasive species lists** — federal and state. Some species can't be shipped
  interstate at all, and lists differ by state, so a legal plant at origin may be prohibited at
  destination.
- **Regulated and controlled plants** — some species (certain psychoactive plants, some
  agricultural hosts under quarantine) carry specific licensing regimes. Where a user's species
  falls into a regulated category, the answer is to point them at the actual licensing authority,
  not to guess at the rules.
- **Waste and chemical handling** — autoclaving culture waste before disposal, and proper
  disposal streams for mutagens and antimitotics. Discussed in
  [breeding-and-selection.md](breeding-and-selection.md).

## Moving plants across borders

- **Import into the US** generally requires a **PPQ 587 import permit** from USDA APHIS, and
  usually a phytosanitary certificate from the exporting country's plant protection organization.
  Some material additionally requires post-entry quarantine.
- **Tissue-cultured plants in sterile media** often move under simpler conditions than soil-grown
  plants, precisely because sterile culture eliminates most pest risk. This is a genuine and
  underused advantage of selling in flask internationally — but it is conditional on meeting the
  specific requirements for that genus and origin, so it must be confirmed per shipment rather
  than assumed.
- **Export from the US** requires a **phytosanitary certificate** issued by APHIS PPQ, plus
  whatever the destination country's import permit demands. The destination's rules govern, and
  they vary widely.
- **CITES** covers all orchids, all cacti, cycads, *Nepenthes*, and others. Appendix I is heavily
  restricted; Appendix II requires export permits. Notably, **artificially propagated specimens
  of certain taxa in sterile flask culture have exemptions** — a significant carve-out for orchid
  labs specifically, but one with precise conditions on labelling and container type that must be
  met exactly.
- **Never ship plants internationally without checking.** Confiscation and destruction at the
  border is the mild outcome; penalties exist for the rest.

Check current requirements at the time of shipping — APHIS and CITES listings change, and a
requirement that was right last year may not be.

## Shipping

- **In flask** — ship the sealed vessel. Robust, but heavy and fragile if glass. Use polycarbonate
  or PP vessels for shipping where possible. Protect from temperature extremes and from light
  (a sealed vessel in a hot delivery vehicle cooks). Include acclimatization instructions.
- **Deflasked plugs** — wrap roots in damp sphagnum or keep in plug trays, bag to hold humidity,
  and ship fast. These plants have almost no reserves.
- **Temperature** — heat packs below ~4 °C, cold packs above ~30 °C, and stop shipping entirely
  during extreme weather. Publish a weather-hold policy so customers aren't surprised.
- **Speed** — 2-day or faster for anything deflasked; avoid shipping so a package sits over a
  weekend.
- **Photograph every package before sealing.** It resolves damage claims, and there will be
  damage claims.
- **A clear live-arrival policy** stated up front prevents most disputes.

## Listings, honesty, and customer expectations

The reputational risks specific to selling tissue-cultured plants:

- **Don't sell mixoploids as tetraploids**, or unverified ploidy as verified. Verify, or say it's
  unverified.
- **Don't sell unstable chimeral variegation as stable.** State honestly that variegation may
  revert and that pattern varies plant to plant — this is inherent to chimeras, not a defect, and
  customers who understand it up front don't file complaints.
- **Don't sell virused plants as variegated.** Selling virused stock is both dishonest and, in
  many jurisdictions, a regulatory violation — and it spreads.
- **Don't imply a chemically-dwarfed plant is a compact cultivar.** The effect wears off in the
  customer's care.
- **Be clear about what stage the buyer receives** and what skill it requires. In-flask plants
  sold to beginners generate losses and bad reviews.
- **State the subculture provenance** for anything sold as true-to-type, and mean it.

The commercial argument, beyond the ethical one: this is a small market with long memories and
active forums. A lab known for accurate descriptions can charge more than one known for
optimistic ones, and reputation compounds faster than inventory does.

## Scaling

Common bottlenecks, in the order labs usually hit them:

1. **Transfer labor** — the binding constraint almost immediately. Every unit passes through a
   hood repeatedly. Addressed by larger vessels, longer cycles, better ergonomics, and eventually
   temporary immersion bioreactors.
2. **Culture room space** — shelf area and the electricity for lighting.
3. **Autoclave throughput** — media prep becomes the constraint before people expect it.
4. **Acclimatization capacity** — greenhouse space and mist capability. Frequently the real
   ceiling, and the one that's slowest and most expensive to expand.
5. **Sales channel** — producing 20,000 plants is much easier than selling 20,000 plants. Secure
   the offtake before scaling production; contract growing for a known buyer is far lower risk
   than speculative production.

Advise users to grow the constraint that's actually binding, and to secure demand before supply.
The characteristic failure of an enthusiastic small lab is a culture room full of plants nobody
ordered, at a price that has fallen since they started.
