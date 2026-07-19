# Processes and Materials

Contents:
- [Choosing a process](#choosing-a-process)
- [FDM filaments](#fdm-filaments)
- [Picking a filament by requirement](#picking-a-filament-by-requirement)
- [Moisture](#moisture)
- [Abrasive filaments and nozzles](#abrasive-filaments-and-nozzles)
- [Resin](#resin)
- [Health and safety](#health-and-safety)

## Choosing a process

| Process | Resolution | Strength | Best for | Watch out for |
|---|---|---|---|---|
| **FDM / FFF** | 0.1–0.3 mm layers, ~0.4 mm feature floor | Good in XY, weak in Z | Functional parts, brackets, enclosures, jigs, most of everything | Anisotropy, visible layer lines, overhangs need support |
| **MSLA / SLA resin** | 0.02–0.05 mm layers, ~0.05 mm features | Usually brittle; tough resins exist | Miniatures, jewellery masters, dental, fine detail, smooth surfaces | Messy post-processing, resin is a sensitiser, most resins are UV-degraded and creep under load |
| **SLS (nylon powder)** | ~0.1 mm | Near-isotropic, genuinely strong | Functional end-use parts, complex geometry, living hinges | Industrial cost, grainy surface, powder handling |
| **MJF** | ~0.08 mm | Near-isotropic | Production runs of functional parts | Service-bureau only for most people |
| **DMLS / SLM metal** | ~0.05 mm | Metal | Aerospace, tooling, medical | Very expensive; effectively a bureau service |

For nearly everyone, the real choice is **FDM vs. resin**, and it's decided by what the
part is for. Functional and load-bearing → FDM. Fine detail where it just has to look
right → resin. People routinely choose resin for its resolution and then discover the part
is brittle, creeps under sustained load, and yellows in sunlight.

## FDM filaments

Temperatures are typical starting ranges. Brands vary meaningfully — always check the
spool label first, and run a temp tower if the surface quality or layer bonding is off.

| Material | Nozzle °C | Bed °C | Enclosure | Notes |
|---|---|---|---|---|
| **PLA** | 190–220 | 50–60 | No | Easiest to print, stiff, good detail, cheap. **Softens around 55–60 °C** — fails in cars, in sunlight, near heat. Not for functional outdoor or under-load parts |
| **PLA+ / tough PLA** | 200–230 | 55–65 | No | Less brittle than PLA, same heat limit |
| **PETG** | 230–250 | 70–85 | Helpful | The functional default. Tough, some flex, chemically resistant, ~75 °C service. Strings readily; **bonds aggressively to smooth PEI** — use a release agent or a textured plate or you'll tear the sheet |
| **ABS** | 240–260 | 100–110 | **Yes** | Heat resistant (~95 °C), machinable, acetone-smoothable. Warps and cracks badly without an enclosure. Emits styrene — ventilate |
| **ASA** | 240–265 | 100–110 | **Yes** | ABS with genuine UV stability. The right pick for outdoor parts |
| **TPU (flexible)** | 210–235 | 40–60 | No | Print **slow** (20–35 mm/s) with minimal retraction. Direct drive strongly preferred; Bowden setups struggle. Shore 95A is manageable, 85A is difficult |
| **Nylon / PA** | 250–280 | 70–100 | Yes | Tough, abrasion resistant, low friction — excellent for gears and living hinges. **Extremely hygroscopic**; must be dried and often printed from a dry box |
| **PC (polycarbonate)** | 260–310 | 100–120 | **Yes** | Very strong and heat resistant (~110 °C+). Warps hard, needs high temps many hotends can't reach |
| **PA-CF / PET-CF / CF blends** | Base + 10–20 | Base | Per base | Stiffer, dimensionally stable, matte finish. **Abrasive — hardened nozzle required.** Carbon fill raises stiffness but usually *lowers* impact toughness |
| **PVA / BVOH** | 190–220 | 60 | — | Water-soluble support for dual-material. Very hygroscopic and expensive |
| **HIPS** | 230–245 | 100–110 | Yes | Limonene-soluble support for ABS |

## Picking a filament by requirement

The question to ask isn't "which is best" but "what does it have to survive":

- **Just has to look good indoors** → PLA. Cheapest, easiest, best detail.
- **Functional, indoors, moderate load** → PETG. The right default for most functional parts.
- **Hot car, near an engine, in direct sun** → ASA, ABS, or PC. Never PLA — this is the
  single most common material mistake, and the part sags rather than snapping, so people
  don't recognise the cause.
- **Outdoors long-term** → ASA. UV stability is the deciding property; ABS chalks and
  embrittles.
- **Flexible, gasket, phone case, tyre** → TPU, chosen by Shore hardness.
- **Gears, hinges, wear surfaces** → Nylon or PA-CF.
- **Stiff and dimensionally stable, low warp** → a CF-filled blend.
- **Food contact** → see the food-safety discussion in
  [selling-and-licensing.md](selling-and-licensing.md). The short version is that FDM
  parts are a poor choice and "food-safe filament" alone does not make a food-safe part.

## Moisture

Filament absorbs atmospheric water, and wet filament is one of the highest-yield
diagnoses in the whole hobby because its symptoms mimic everything else: popping or
crackling sounds during extrusion, steam wisps at the nozzle, stringing that retraction
tuning won't fix, rough or foggy surfaces, weak brittle layers, and inconsistent
extrusion.

Hygroscopic ranking, worst first: **PVA > Nylon > TPU > PETG > ABS/ASA > PLA.** Nylon can
noticeably degrade in a single humid day on the shelf.

Drying: a filament dryer or a low oven, roughly **PLA 45–50 °C, PETG/TPU 55–65 °C, ABS/ASA
65–75 °C, Nylon 70–80 °C, for 4–12 hours.** Never exceed the material's glass transition —
PLA above ~55 °C will fuse the spool into a solid brick. Store dried spools with fresh
desiccant in sealed containers, or print directly from a dry box for nylon.

When symptoms are diffuse and the spool has been open for weeks, dry it before changing
anything else in the profile. It's cheap and it eliminates a confounding variable.

## Abrasive filaments and nozzles

Anything filled with carbon fibre, glass fibre, metal, wood or glow powder will destroy a
standard brass nozzle — sometimes within a single spool. A worn nozzle's orifice widens
and rounds, producing under-extrusion, poor dimensional accuracy, and blobby detail that
reads as a settings problem.

Use **hardened steel, ruby-tipped, or tungsten carbide** for abrasives. The trade-off:
hardened steel conducts heat less well than brass, so run 5–10 °C hotter to compensate.

Nozzle diameter is an underused lever. **0.4 mm** is the default; **0.6 mm** prints
roughly twice as fast with slightly coarser detail and is the better choice for most
functional parts; **0.2 mm** is for fine detail and is slow and clog-prone; **0.8 mm+** is
for fast, chunky, strong parts.

## Resin

MSLA settings are resin- and printer-specific, and the manufacturer's profile is a much
better starting point than any general table.

The variables that matter: **exposure time per layer** (the master setting — dialled in
with a validation print such as a Cones of Calibration or XP2 test), bottom layer count
and bottom exposure, lift speed and distance, and light-off delay.

- **Under-exposed** → parts miss detail, come out soft or undersized, supports snap off,
  islands fail.
- **Over-exposed** → detail fills in and bloats, holes shrink or close, parts stick to the
  FEP and cause layer separation.

Workflow specifics people get wrong:

- **Hollow parts need drain holes** — at least two, 3 mm+. A sealed hollow part traps
  resin and forms a suction cup against the FEP, which tears film and rips parts off
  supports. Trapped uncured resin also leaks later and cracks the part.
- **Orient at an angle**, typically 20–45°, to reduce cross-sectional area per layer. It
  lowers peel forces dramatically and moves support scars onto non-visible surfaces.
- **Wash then cure, in that order.** IPA wash 5–10 min, dry thoroughly, then UV cure.
  Curing before washing locks residue onto the surface permanently.
- **Don't over-cure** — excessive cure time makes parts brittle and can yellow them.
- Resin parts **creep under sustained load** and degrade in UV. They're display and
  detail parts, not structural ones, whatever the "tough resin" marketing says.

## Health and safety

Give this alongside the technical answer rather than instead of it.

**Resin.** Uncured resin is a skin and respiratory **sensitiser** — the danger isn't a
one-time burn, it's that sensitisation is cumulative and permanent, so people develop a
lifelong allergic reaction after months of casual contact. Nitrile gloves every time
(latex is permeable to it), eye protection, ventilation. IPA is flammable and needs
sensible storage. Cure all waste resin, contaminated paper towels, and rinse water under
UV before disposal — liquid resin is aquatic-toxic and must never go down a drain.

**FDM emissions.** All FDM printing emits ultrafine particles; ABS, ASA and nylon also
emit VOCs (styrene from ABS notably). PLA and PETG are the mildest. Print in a ventilated
space, or use an enclosure with a HEPA + activated carbon filter. A printer running ABS in
an unventilated bedroom is a genuinely bad idea.

**Fire.** Hotends and heated beds are ignition sources, and prints run unattended for many
hours. Confirm firmware thermal runaway protection is enabled, keep the machine off
carpet and away from anything flammable, and put a smoke alarm in the room. For a print
farm, this moves from sensible to mandatory.

**Mechanical.** Powered printers have unguarded moving parts and heaters at 250 °C+.
Obvious, and still where most minor injuries come from.
