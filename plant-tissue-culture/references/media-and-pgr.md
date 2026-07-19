# Media and Plant Growth Regulators

Contents:
- [Choosing a base medium](#choosing-a-base-medium)
- [The standard MS recipe](#the-standard-ms-recipe)
- [Carbon, gelling agent, and pH](#carbon-gelling-agent-and-pH)
- [Plant growth regulators](#plant-growth-regulators)
- [Auxin:cytokinin ratio — the master dial](#auxincytokinin-ratio--the-master-dial)
- [Stage-by-stage PGR starting points](#stage-by-stage-pgr-starting-points)
- [Additives](#additives)
- [Stock solutions and sterilization](#stock-solutions-and-sterilization)
- [Common formulation mistakes](#common-formulation-mistakes)

## Choosing a base medium

The base medium supplies macro- and micronutrients, and the main axis of difference is nitrogen
level and form. Woody and ericaceous plants are damaged by MS-level ammonium; herbaceous plants
generally thrive on it.

| Medium | Full name | Best for | Notes |
|---|---|---|---|
| **MS** | Murashige & Skoog 1962 | Most herbaceous species, aroids, orchids in later stages, the default | Very high total N (~60 mM). Half-strength MS (½MS) is the workhorse for rooting and for sensitive species |
| **WPM** | Lloyd & McCown Woody Plant Medium | Woody ornamentals, *Rhododendron*, *Vaccinium*, many trees | ~¼ the nitrate of MS, lower ammonium, higher sulfate |
| **DKW** | Driver & Kuniyuki Walnut | *Juglans*, *Malus*, *Prunus*, many temperate woody crops | Higher Ca and Cu than MS; often outperforms WPM on fruit/nut trees |
| **B5** | Gamborg B5 | Legumes, protoplast and suspension culture | Much lower ammonium than MS, higher thiamine |
| **Knudson C / Vacin & Went** | — | Orchid seed and protocorm culture | Low salt; usually run with organic supplements |
| **SH** | Schenk & Hildebrandt | Monocots, some callus work | — |

Practical rule when you don't know: **herbaceous → MS; woody → WPM or DKW; sensitive or
browning-prone → ½MS.** If a species browns or shows tip necrosis on full MS, drop to ½MS
macronutrients while keeping full-strength vitamins and iron before you change anything else.

Buy premixed powder ("MS with vitamins") rather than weighing 20 salts. The premix at
**4.3–4.4 g/L** gives full-strength MS.

## The standard MS recipe

Per litre, full-strength, for a general Stage II multiplication medium:

```
MS basal salts with vitamins   4.4 g
Sucrose                        30 g
Myo-inositol                   100 mg   (already in most "with vitamins" premixes — check)
PGRs                           per stage, see below
pH adjusted to                 5.7–5.8   (before adding agar, before autoclaving)
Agar                           7 g       (or gellan gum 2.5 g)
Autoclave                      121 °C, 15 psi, 20 min for 1 L
```

Autoclave time scales with vessel volume, not total volume — 20 min suits flasks up to ~1 L;
larger single vessels need longer to reach core temperature. Over-autoclaving caramelizes
sucrose (medium darkens, pH drops) and degrades some vitamins.

## Carbon, gelling agent, and pH

**Sucrose** at 20–30 g/L is standard. Cultures in vitro are largely heterotrophic — the low CO₂
and low light in a sealed vessel means they can't photosynthesize their way to a carbon balance.
Raise to 40–60 g/L for storage organ induction (microtubers, bulblets) or osmotic stress
protocols; drop to 10–20 g/L in late Stage III to push photoautotrophy before acclimatization.

**Gelling agent:**
- **Agar** 6–8 g/L. Cheap, forgiving. Below ~6 g/L the medium gets soft and hyperhydricity risk
  rises sharply; above ~9 g/L water availability drops and growth slows.
- **Gellan gum** (Phytagel, Gelrite) 2–3 g/L. Clear, so you see contamination and roots earlier,
  and it's cheaper per litre. But it's associated with more hyperhydricity, and it needs
  divalent cations to set properly.
- **Liquid + support** (filter paper bridge, rockwool, or agitated) gives faster uptake and
  faster growth, at higher hyperhydricity risk. Temporary immersion systems (RITA, SETIS) are
  the industrial answer — best growth rates, lowest hyperhydricity, highest capital cost.

**pH 5.7–5.8** before autoclaving, adjusted with 0.1 N KOH or HCl. This matters more than people
think: agar won't gel reliably below ~4.8, iron availability collapses above ~6.5, and
autoclaving typically drops pH 0.3–0.5 units on its own. Adjust before adding the gelling agent
and before autoclaving, and check the pH meter's calibration monthly — a drifting meter silently
ruins every batch downstream.

## Plant growth regulators

### Cytokinins — drive shoot multiplication

| PGR | Typical range | Character |
|---|---|---|
| **BAP / BA** (6-benzylaminopurine) | 0.5–3 mg/L | The default. Cheap, effective, well-documented. Downside: at higher doses causes hyperhydricity and can carry over, inhibiting later rooting |
| **Kinetin** | 0.5–5 mg/L | Milder than BAP. Useful when BAP causes distortion |
| **2iP** | 1–15 mg/L | Weak; needed at high doses. Preferred for some woody species and *Rhododendron* |
| **TDZ** (thidiazuron) | 0.01–1 mg/L | *Extremely* potent — a phenylurea, not a purine. Excellent for recalcitrant woody species and adventitious regeneration. Notorious for causing fasciation, stunted rosettes, and rooting inhibition; almost always needs a TDZ-free transfer before Stage III |
| **meta-Topolin (mT)** | 0.5–5 mg/L | An aromatic cytokinin. Costs more, but markedly reduces hyperhydricity and the rooting inhibition BAP causes. Worth trialling when a BAP line roots poorly |

Note the order-of-magnitude gap: **TDZ is dosed 10–100× lower than BAP.** Mixing these up is one
of the most common and most destructive formulation errors.

### Auxins — drive roots, callus, and elongation

| PGR | Typical range | Character |
|---|---|---|
| **IBA** (indole-3-butyric acid) | 0.1–3 mg/L | The rooting standard. More stable in medium than IAA |
| **NAA** (1-naphthaleneacetic acid) | 0.01–2 mg/L | Potent and stable. Above ~0.5 mg/L tends to produce a callus plug at the shoot base, which impedes acclimatization — keep it low for rooting |
| **IAA** (indole-3-acetic acid) | 0.1–10 mg/L | Natural auxin; degrades under light and during autoclave, so effective dose is unreliable. Filter-sterilize if using |
| **2,4-D** | 0.5–5 mg/L | Callus and somatic embryogenesis only. Strongly mutagenic in effect — drives somaclonal variation. Never use it in a line intended to stay true-to-type |

### Others

- **GA₃** (gibberellic acid) 0.1–2 mg/L — internode elongation for rosetted or stunted cultures,
  and dormancy breaking. Filter-sterilize; it's heat-labile. Overuse gives spindly, weak shoots
  that root badly.
- **ABA** 0.1–5 mg/L — embryo maturation, somatic embryo quality, and cold/desiccation hardening
  before storage.
- **Anti-gibberellins** (paclobutrazol, ancymidol) — used deliberately to induce compact habit;
  see the dwarfing section of [breeding-and-selection.md](breeding-and-selection.md).

## Auxin:cytokinin ratio — the master dial

Skoog and Miller's finding still runs the whole field. Absolute concentrations matter, but the
*ratio* determines what organ forms:

| Ratio | Result |
|---|---|
| High cytokinin : low auxin | Shoot proliferation (Stage II) |
| Roughly balanced | Undifferentiated callus |
| Low cytokinin : high auxin | Root initiation (Stage III), or somatic embryogenesis with 2,4-D |
| Both near zero | Elongation without multiplication; a useful "rest" medium |

When a culture does the wrong thing, move the ratio before you move anything else. Too much
callus at the base means the auxin is too high for a multiplication medium. A dense rosette that
won't elongate means cytokinin is too high — cut it, or add a low-PGR pass.

## Stage-by-stage PGR starting points

These are starting points for an unknown herbaceous species. Expect to titrate, and change one
variable at a time.

**Stage I — establishment.** MS or ½MS, low or no PGR, often with 0.5–1 mg/L BAP to nudge the
axillary bud. Add antioxidants if the species browns (below). Keep the first 5–7 days dim or
dark to reduce phenolic oxidation.

**Stage II — multiplication.** MS + BAP 1–2 mg/L, optionally NAA 0.05–0.2 mg/L. Subculture every
4–6 weeks. If multiplication rate is under ~2×, raise cytokinin one step; if shoots are glassy
or fasciated, lower it.

**Stage III — rooting.** ½MS + IBA 0.5–1 mg/L, sucrose reduced to 15–20 g/L, no cytokinin. Many
species root better with a **pulse**: 24–72 h on high auxin (or a 1–5 minute dip in 500–1000
mg/L IBA), then transfer to PGR-free medium. The pulse avoids the basal callus that continuous
auxin produces. Activated charcoal 1–2 g/L helps by scavenging residual cytokinin.

**Stage IV — acclimatization.** No medium. See [stages-and-protocols.md](stages-and-protocols.md).

## Additives

- **Activated charcoal** 0.5–3 g/L — adsorbs phenolics and residual PGRs, darkens the medium
  (useful for root culture). Caveat: it adsorbs PGRs *non-selectively*, so any PGR in a charcoal
  medium is at an unknown effective dose. Don't combine charcoal with a PGR you're titrating.
- **PVP / PVPP** 0.5–3 g/L, or **ascorbic acid + citric acid** 50–150 mg/L each — antioxidants
  for browning-prone species. Filter-sterilize the acids.
- **PPM** (Plant Preservative Mixture) 0.5–2 mL/L — a biocide, heat-stable, added pre-autoclave.
  Genuinely useful for suppressing low-level contamination during establishment. It is *not* a
  substitute for aseptic technique, and above ~2 mL/L it inhibits rooting and germination. Using
  PPM routinely to mask sloppy technique produces a lab full of latent endophytes that erupt
  later — treat a rising PPM dependence as a technique alarm.
- **Antibiotics** (cefotaxime, timentin) — for known bacterial endophytes and *Agrobacterium*
  cleanup only. They suppress rather than cure, are phytotoxic at higher doses, and select for
  resistance. Prefer discarding the line and re-initiating from clean material.
- **Coconut water** 10–15% v/v, banana homogenate, potato extract — undefined organics that
  genuinely improve orchid and some monocot cultures. Their downside is batch-to-batch
  variability, so avoid them in experiments where you need reproducibility.
- **Silver nitrate / STS** 1–10 mg/L — ethylene inhibitor; helps in sealed vessels where
  ethylene accumulates and causes leaf abscission or stunting.

## Stock solutions and sterilization

PGRs are used in milligram quantities per litre, which you cannot weigh accurately. Make stocks.

**Standard approach:** 1 mg/mL (= 1000 ppm) stock. Dissolve 100 mg in a minimum of solvent, then
bring to 100 mL with distilled water. At that concentration, **1 mL of stock per litre of medium
= 1 mg/L in the final medium**, which makes the arithmetic trivial and hard to get wrong.

**Solvents** — most PGRs won't dissolve in water directly:
- Auxins (IAA, IBA, NAA, 2,4-D): a few drops of 1 N NaOH, or warm ethanol
- Cytokinins (BAP, kinetin, 2iP): a few drops of 1 N HCl or NaOH, warming gently
- TDZ: DMSO or dilute NaOH
- GA₃: ethanol

Store stocks at 4 °C in amber bottles. Label with compound, concentration, solvent, and date.
Discard auxin and GA₃ stocks after ~1 month, cytokinins after ~3; a degraded stock reads as a
mysterious protocol failure.

**Heat stability:** BAP, kinetin, 2iP, NAA, IBA, and 2,4-D autoclave fine. **GA₃, zeatin, ABA,
IAA, and most antibiotics and vitamins are heat-labile** — filter-sterilize through 0.22 µm and
add to molten medium that has cooled to ~50 °C (hand-warm, not hot).

Use `scripts/media_calc.py` for the recipe arithmetic rather than doing it in prose.

## Common formulation mistakes

- **Confusing TDZ with BAP dosing** — a 100× overdose; produces fasciated, unrootable rosettes.
- **Adjusting pH after adding agar** — the reading is unreliable in a slurry, and you can't
  correct it once gelled.
- **Autoclaving heat-labile PGRs** — GA₃ loses most activity; the experiment silently has no
  treatment.
- **Charcoal plus a titrated PGR** — the dose-response curve becomes meaningless.
- **Changing two variables between batches** — when it works, you don't know why, and you can't
  reproduce it. One variable per batch, always.
- **Not recording the lot number of the basal salt premix** — batch differences in micronutrients
  are real and account for a surprising number of "everything suddenly stopped working" cases.
