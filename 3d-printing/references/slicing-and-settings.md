# Slicing and Settings

Contents:
- [The settings that actually matter](#the-settings-that-actually-matter)
- [Layer height](#layer-height)
- [Walls, top and bottom](#walls-top-and-bottom)
- [Infill](#infill)
- [Temperature](#temperature)
- [Speed and acceleration](#speed-and-acceleration)
- [Cooling](#cooling)
- [Retraction and stringing](#retraction-and-stringing)
- [First layer and bed adhesion](#first-layer-and-bed-adhesion)
- [Supports](#supports)
- [Seams and surface quality](#seams-and-surface-quality)
- [Calibration order](#calibration-order)
- [Profiles worth keeping](#profiles-worth-keeping)

## The settings that actually matter

Slicers expose hundreds of settings and perhaps a dozen change outcomes. When someone is
lost in a settings menu, pull them back to these: layer height, wall count, infill,
nozzle and bed temperature, print speed, cooling, retraction, and first-layer settings.
Nearly every real problem lives in that list.

The most important framing: **strength comes from walls, not infill.** People reach for
90% infill to make a part strong, which wastes hours and filament for a modest gain. Going
from 2 to 4 walls does far more for stiffness and load capacity than doubling infill,
because the perimeters carry the bending stress. Advise walls first, infill second, and
you'll save people significant time.

## Layer height

Expressed as a fraction of nozzle diameter; the workable range is roughly **25–75% of
nozzle width**. For a 0.4 mm nozzle that's 0.1–0.3 mm.

| Layer height | Trade-off |
|---|---|
| 0.08–0.12 mm | Fine detail, slow. Visible improvement mostly on curved and organic surfaces |
| 0.16–0.20 mm | The sweet spot for most work. 0.2 mm is the sane default |
| 0.24–0.32 mm | Fast and strong (thicker layers bond well), coarse detail |

Two useful counterintuitive points. Thicker layers often produce **stronger** parts,
because each layer's bond area and thermal mass are greater. And layer height barely
affects the quality of *vertical* walls — it changes curves and shallow slopes. Somebody
printing a boxy functional part at 0.1 mm is usually just spending four extra hours for
nothing.

## Walls, top and bottom

- **Walls / perimeters:** 2 for decorative, **3–4 for functional**, 5+ for genuinely
  load-bearing. This is the primary strength lever.
- **Top layers:** enough to total ~0.8–1.0 mm. At 0.2 mm layers that's 4–5. Too few gives
  "pillowing" — visible gaps over infill.
- **Bottom layers:** 3–4 typically.

A quick rule: wall thickness should be a whole multiple of the extrusion width, or the
slicer leaves thin unfilled gaps. With a 0.4 mm nozzle, design walls at 0.8, 1.2, 1.6 mm
rather than 1.0 or 1.5.

## Infill

| Density | Use |
|---|---|
| 0–5% | Display pieces, purely visual |
| 10–15% | The general default. Fine for most parts |
| 20–30% | Functional parts under moderate load |
| 40–60% | Heavily loaded parts — but add walls first |
| 100% | Almost never worth it. Slow, warp-prone, heavy, and rarely stronger than 5 walls + 30% |

Pattern matters less than people think, but broadly: **gyroid** is the good default
(isotropic, fast, no self-intersection, flexible-friendly); **grid/lines** is fastest;
**cubic** is decent 3D strength; **honeycomb** is strong but slow; **lightning** is for
pure display pieces where infill exists only to hold up the top surface.

## Temperature

Start from the spool label, then run a **temp tower** — it's the single highest-value
calibration print. General ranges are in
[processes-and-materials.md](processes-and-materials.md).

Reading the results:

- **Too cold:** poor layer adhesion (part splits along layers), under-extrusion, gaps,
  grinding filament, clogs.
- **Too hot:** stringing, blobs, drooping overhangs, loss of fine detail, glossy or
  "wet" surface, heat creep clogs.

Bed temperature governs adhesion and warping. Too low and parts lift; too high and you get
elephant foot and, with PETG, dangerous over-adhesion to smooth PEI.

## Speed and acceleration

Modern machines with input shaping print far faster than older advice assumes, so avoid
quoting speeds without knowing the machine. Broad guidance:

- **Outer wall speed** matters most for appearance — slowing it to 50–70% of infill speed
  visibly improves surfaces at little time cost. The highest-value speed tweak.
- **First layer** should always be slow — 20–30 mm/s regardless of machine.
- **Small features and overhangs** need slowing so cooling can keep up.
- **TPU** needs 20–35 mm/s; pushing it causes the filament to buckle in the extruder.
- **Bridges** print better slightly slower with full cooling.

The real ceiling is usually **maximum volumetric flow rate** (mm³/s) of the hotend, not the
speed number in the slicer. If a machine under-extrudes only at high speed on solid
layers, that's the flow limit, and no amount of temperature tweaking fixes it — reduce
speed, increase temperature within range, or fit a higher-flow hotend.

## Cooling

Cooling controls the trade between surface quality and layer bonding, and the right answer
is material-dependent:

- **PLA:** 100% fan after the first couple of layers. It practically cannot be over-cooled.
- **PETG:** 30–50%. Too much fan noticeably weakens layer bonds.
- **ABS/ASA:** 0–20%, in an enclosure. Cooling is what makes ABS crack and warp.
- **Nylon/PC:** minimal.
- **TPU:** moderate.

Regardless of material, increase cooling for small layers, overhangs and bridges — most
slicers do this automatically via minimum-layer-time settings.

## Retraction and stringing

Stringing is wispy filament strands between features. Causes, in order of likelihood:

1. **Wet filament.** Check this first — no retraction setting fixes wet PETG.
2. Nozzle too hot.
3. Insufficient retraction distance or speed.
4. Travel moves crossing open space without combing.

Typical retraction: **direct drive 0.5–2 mm**, **Bowden 3–6 mm**, at 25–45 mm/s. Dial it
with a retraction tower. Excessive retraction causes its own problems — grinding, clogs,
and under-extrusion at the start of each new extrusion.

**Pressure advance / linear advance** compensates for pressure lag in the nozzle and
sharply improves corner quality and seam consistency. Worth calibrating on any machine
that supports it; it addresses bulging corners that no speed tuning will fix.

## First layer and bed adhesion

More prints fail here than anywhere else. The first layer should be slightly squished —
adjacent lines touching with no gaps, a smooth surface, no translucent thin spots and no
rippled over-squish.

Fix order when adhesion fails:

1. **Clean the bed.** Warm soapy water, then isopropyl. Fingerprint oil is the number-one
   cause, and wiping with IPA alone smears grease rather than removing it.
2. **Z-offset / first layer height.** Too high is the classic failure; nozzle should be
   close enough to flatten the line.
3. **Bed temperature** — up 5–10 °C.
4. **Slow the first layer** and turn the fan off for it.
5. **Brim** (5–8 mm) for small footprints or tall parts; raft only for badly warping
   materials or damaged beds.
6. **Adhesion aid** — glue stick or hairspray. Note that with PETG on smooth PEI, glue
   stick acts as a *release* agent to stop it bonding too hard, which is the opposite of
   the usual purpose and surprises people.

Surface matters: smooth PEI for PLA and glossy bottoms; textured PEI for PETG and general
use; garolite for nylon; glass with adhesive for ABS.

## Supports

- **Overhangs beyond ~45°** from vertical generally need support; 45° and shallower
  self-supports. Bridges between two anchors print unsupported surprisingly well.
- **Tree/organic supports** use less material, are much easier to remove, and are better
  for organic models. **Normal/grid supports** are better under large flat overhangs.
- **Support Z-distance** is the setting that decides whether supports snap off cleanly or
  weld themselves on. Roughly one layer height for most materials; PETG needs more because
  it bonds to itself aggressively.
- **Support interface layers** give a much better underside finish at the cost of harder
  removal.

The best support strategy is usually **reorienting the part or splitting it** so supports
aren't needed. Supported surfaces always come out worse, so a design or orientation change
beats support tuning. See [design-for-printing.md](design-for-printing.md).

## Seams and surface quality

The Z-seam is the visible scar where each layer starts and stops. Options: **aligned**
(one vertical line — tidy, hideable on a back face), **random** (scattered, no line but
speckled), **sharpest corner** (hides it in geometry — usually the best default), or a
user-painted seam position.

Other surface levers: slow the outer wall, calibrate pressure advance, enable ironing for
flat top surfaces (slow but effective), and check for a worn or partially clogged nozzle
before chasing settings.

## Calibration order

Sequence matters — calibrating flow before the extruder is calibrated just bakes in an
error. Work in this order:

1. **Bed level / mesh and Z-offset** — everything downstream depends on the first layer.
2. **Extruder steps / rotation distance** — command 100 mm, measure what's actually
   extruded, correct.
3. **Flow rate / extrusion multiplier** — print a single-wall cube, measure wall thickness
   with calipers, adjust.
4. **Temperature tower** — per filament, not per printer.
5. **Retraction tower.**
6. **Pressure advance / linear advance.**
7. **Input shaping / resonance compensation**, if supported.
8. **Maximum volumetric flow**, if pushing speed.
9. **Dimensional accuracy** — a calibration cube, adjusting X/Y compensation last, once
   everything upstream is right.

Steps 1–4 get 90% of the benefit. Someone struggling with basic print quality should not
be tuning input shaping.

## Profiles worth keeping

Keep a small number of well-tested profiles rather than tweaking per print. A practical
set: **Draft** (0.28 mm, 2 walls, 10% infill, fast), **Standard** (0.2 mm, 3 walls, 15%),
**Strong** (0.2–0.24 mm, 5 walls, 30%, more cooling restraint), **Fine** (0.12 mm, 3
walls, slow outer wall).

Record what each profile is for and what was calibrated, using
[assets/profile-record-template.md](../assets/profile-record-template.md). A profile whose
provenance is forgotten gets re-tuned from scratch every few months.
