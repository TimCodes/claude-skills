# Monitoring and Troubleshooting

Contents:
- [The culture log](#the-culture-log)
- [Metrics that matter](#metrics-that-matter)
- [Identifying contamination](#identifying-contamination)
- [Responding to contamination](#responding-to-contamination)
- [Physiological disorders](#physiological-disorders)
- [Diagnostic flow](#diagnostic-flow)
- [Routine lab monitoring](#routine-lab-monitoring)

## The culture log

Everything else here depends on records existing. A lab without a log can only react to
disasters; a lab with one sees them forming.

The schema `scripts/culture_metrics.py` expects, matching
[assets/culture-log-template.csv](../assets/culture-log-template.csv):

| Column | Meaning |
|---|---|
| `batch_id` | Unique batch identifier, e.g. `MON-ALB-2026-03-A` |
| `date` | ISO date of the transfer or observation (`YYYY-MM-DD`) |
| `genotype` | Species + cultivar/clone. The unit selection actually operates on |
| `stage` | `0`, `I`, `II`, `III`, `IV` |
| `subculture_no` | Cycles since initiation from the mother plant. **The single most important column** |
| `vessels_in` | Vessels started this cycle |
| `explants_in` | Explants/shoots plated |
| `vessels_clean` | Vessels still uncontaminated at assessment |
| `explants_out` | Viable shoots harvested at the end of the cycle |
| `contaminated_bacterial` / `contaminated_fungal` / `contaminated_other` | Loss counts by cause |
| `off_type` | Shoots culled for reversion, variegation drift, or abnormality |
| `medium_id` | Reference to a formulation record — links outcomes back to recipes |
| `operator` | Who did the work. Not for blame; contamination clustering by operator is a real and fixable signal |
| `notes` | Free text |

Two habits make the log worth keeping. Record **failures with the same care as successes** — a
log containing only good batches can't explain anything. And record **what changed** — new
premix lot, new autoclave cycle, new person, different vessel closure. Causes are almost always
found in the change list, not in the outcome column.

## Metrics that matter

Run `python scripts/culture_metrics.py logs/cultures.csv` for these.

**Contamination rate** = contaminated vessels ÷ vessels started. Track it *separately by stage*,
because the meaning is completely different. Stage I contamination reflects the source plant and
sterilization; Stage II contamination reflects the hood, the autoclave, and technique. Rough
benchmarks: Stage I 10–40% depending on material (field-collected woody at the top); Stage II
should sit **below 2–3%**. Stage II above 5% means something is broken — find it rather than
absorbing it, because it compounds.

**Multiplication rate** = `explants_out ÷ explants_in` per cycle. The economic engine. Track per
genotype; a lab-wide average hides the lines that are actually losing money.

**Cycle time** — days between subcultures. Multiplication rate per *unit time* is what matters
commercially, not rate per cycle. A 2.5× rate in 4 weeks beats a 3.5× rate in 8.

**Off-type rate** — the honest measure of trueness-to-type and of chimeral drift. Rising
off-type rate with subculture number is the signal to restart the line from mother stock.

**Subculture number distribution** — how much of the inventory sits near the ceiling. A line
approaching subculture 10–12 needs a restart planned *before* it's needed, since re-initiation
takes months.

**Stage IV survival** = plants established ÷ plants deflasked. The number that converts lab
output into sellable product, and often the least measured.

Plot these over time. Trends matter more than levels: a contamination rate rising from 1% to 4%
over six weeks is a failing autoclave or filter announcing itself, and it's invisible if you
only ever look at this month's number.

## Identifying contamination

| Appearance | Likely cause | Timing | Notes |
|---|---|---|---|
| Cloudy or milky halo diffusing through medium around the explant; slimy; sometimes sour smell | **Bacteria** | Fast, 2–5 days | The most common Stage I loss |
| Fuzzy aerial mycelium, white/green/black/pink, spreading across the surface | **Fungus (mold)** | 3–10 days | Often airborne — check hood and closures |
| Small raised creamy or pink glistening colonies, well-defined edges, doesn't spread far | **Yeast** | 3–7 days | Frequently from the operator or the air |
| Cloudiness appearing only after 2–6 weeks, or only after the first subculture | **Endophytic bacteria** | Late, recurrent | Lives inside the tissue. Surface sterilization cannot reach it |
| Contamination at the medium surface across a whole batch, all vessels | **Autoclave or media failure** | Uniform | Check autoclave with indicator strips before anything else |
| Contamination clustered by shelf or by day | **Room, hood, or operator** | Clustered | The clustering pattern is the diagnosis |
| Tiny moving specks; fine webbing; irregular tissue damage | **Mites or thrips** | Any | Mites carry fungal spores between vessels and can move through poor closures. Escalating, cross-contaminating problem |

The **pattern of losses across vessels** is more diagnostic than the appearance in any one
vessel. Uniform across a whole batch points at the autoclave or the medium; scattered randomly
points at technique; clustered by explant source points at the mother plant; late and recurring
points at endophytes.

## Responding to contamination

1. **Remove the vessel from the culture room without opening it.** Do not open it in the hood —
   sporulating fungi will seed the whole room from a single opened jar.
2. **Autoclave before disposal.** Non-negotiable for both biosecurity and, in many jurisdictions,
   waste regulations.
3. **Record it** — batch, date, stage, type, operator. A loss you don't log teaches nothing.
4. **Look for the pattern** before changing anything. Single random vessel: technique, accept it.
   Whole batch: autoclave or medium. Cluster: room or operator or shelf.
5. **Only attempt rescue for irreplaceable genetics.** Excise the cleanest apical tip, re-sterilize
   lightly, and plate into fresh medium with PPM — modest odds, and worth it only when the
   genotype can't be re-obtained. Otherwise, discard and re-initiate; a rescued line often carries
   a latent endophyte that resurfaces months later, having contaminated everything it sat near.

Chronically high contamination is a **systems** problem, not a bad-luck problem. Audit in this
order, cheapest and most likely first: autoclave performance with indicator strips (fails
quietly and gradually), HEPA filter age and hood airflow, media pH and sterilization protocol,
vessel closure integrity, operator technique, then mother plant health.

## Physiological disorders

These aren't contamination and won't respond to cleaner technique.

### Hyperhydricity (vitrification)

Glassy, water-soaked, translucent, brittle shoots — thickened and often curled leaves, poor wax
and stomatal development. They can't be rooted or acclimatized successfully.

Causes, roughly in order of frequency: **too much cytokinin**; **poor gas exchange in sealed
vessels** (accumulated ethylene and saturated humidity); gelling agent too low (soft medium);
high ammonium nitrogen; liquid medium without support; high relative humidity in the vessel.

Fixes: lower cytokinin, or switch BAP → meta-topolin; **use vented closures or gas-permeable
membranes** (usually the highest-leverage single change); raise agar to 8–9 g/L; lower ammonium
by moving toward WPM or reducing NH₄NO₃; drop temperature slightly.

Mildly affected shoots sometimes recover on a low-PGR, well-ventilated, higher-agar medium over
1–2 subcultures. Severely affected ones don't — cull them rather than spending cycles.

### Phenolic browning

The medium and the cut surface darken, and the explant declines. Wounded tissue releases
phenolics that oxidize into toxic quinones. Predominantly a Stage I problem, and worst in woody
species, high-tannin species, and mature tissue.

Fixes: transfer to fresh medium frequently (every 2–3 days initially — laborious but effective);
add antioxidants (PVP 0.5–3 g/L, or ascorbic + citric acid 50–150 mg/L each, filter-sterilized);
add activated charcoal 1–2 g/L; hold the first 3–7 days in darkness; use younger explants; cut
under sterile water or antioxidant solution; and use ½MS rather than full strength.

### Tip necrosis / shoot tip dieback

Apical meristem blackens and dies while lower tissue looks fine. Usually **calcium deficiency**
— calcium is phloem-immobile and doesn't reach the apex when transpiration is near zero in a
saturated vessel. Also associated with boron deficiency and high cytokinin.

Fixes: raise calcium (add CaCl₂, or move to DKW which is calcium-rich), improve gas exchange to
restore some transpiration, lower cytokinin, check that pH hasn't drifted high enough to
precipitate calcium out.

### Callus at the shoot base

Auxin too high in a multiplication medium, or continuous rather than pulsed auxin in Stage III.
Matters because roots arising from callus often lack vascular continuity with the shoot — they
look fine and then fail on deflasking. Lower the auxin, or switch to a pulse. Excise the callus
before Stage IV.

### Rosetting / failure to elongate

Cytokinin too high, TDZ carryover, or ethylene accumulation. Give a PGR-free elongation pass,
add GA₃ 0.1–0.5 mg/L (filter-sterilized), improve gas exchange, and consider silver nitrate if
ethylene is implicated.

### Leaf yellowing / chlorosis

Medium exhaustion (subculture overdue), iron unavailability from pH drift, or light too high for
the stage. Check the days since transfer first — it's usually just time.

### Slow or no growth

Check in this order: subculture overdue; PGR stock degraded or wrongly made (a stale GA₃ or
auxin stock is a classic silent failure); temperature or photoperiod drift in the room; medium
pH wrong; genotype simply recalcitrant. Rule out the boring causes before redesigning a
protocol.

## Diagnostic flow

When the user reports a problem, work in this order:

1. **What stage and how many days since transfer?** Same symptom, different meaning per stage.
2. **How many vessels, and what's the pattern?** Uniform, random, or clustered — this
   distinguishes systemic from technique from source-plant causes.
3. **What changed since the last batch that worked?** New premix lot, new bleach bottle, new
   operator, different closure, autoclave serviced. Solves more cases than any other question.
4. **Is it contamination or physiology?** Cloudy/fuzzy/slimy = biological. Glassy/brown/necrotic
   = physiological. They call for entirely different responses and are often confused.
5. **Full formulation and environment** — only now is the recipe worth interrogating.
6. **Give one change and a checkpoint.** Name what to change, which direction, and when they'll
   know. Multiple simultaneous changes destroy the information the batch would have produced.

## Routine lab monitoring

A weekly rhythm that catches problems while they're cheap:

- **Daily** — walk the culture room and pull contaminated vessels promptly. A missed fungal jar
  seeds its shelf.
- **Weekly** — log contamination counts by stage; check room temperature and photoperiod against
  set point; check that transfers are on schedule.
- **Per subculture** — record multiplication rate, off-type culls, and increment the subculture
  number on every label.
- **Monthly** — autoclave indicator strip test; pH meter calibration; review contamination and
  multiplication trends against previous months; review which lines are approaching their
  subculture ceiling.
- **Quarterly** — HEPA filter check and hood airflow test; mother stock health and virus
  indexing; verify that a restart plan exists for every line nearing its ceiling.

The quarterly items are the ones that get skipped and the ones that cause the expensive
failures, because their consequences arrive months after the neglect.
