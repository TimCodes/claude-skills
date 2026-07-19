# Troubleshooting and Maintenance

Contents:
- [Diagnostic flow](#diagnostic-flow)
- [The print log](#the-print-log)
- [Metrics that matter](#metrics-that-matter)
- [FDM defect catalogue](#fdm-defect-catalogue)
- [Resin defect catalogue](#resin-defect-catalogue)
- [Clogs](#clogs)
- [Maintenance schedule](#maintenance-schedule)
- [Consumable lifespans](#consumable-lifespans)

## Diagnostic flow

Work in this order. It front-loads the cheap, high-probability causes and avoids sending
people into settings menus for a mechanical fault.

1. **When did it fail — first layer, a specific height, or throughout?** First-layer
   failures are adhesion or Z-offset. Failures at a consistent height point to a mechanical
   obstruction, a thermal event, or a model feature. Failures throughout are settings,
   material or hardware.
2. **Did this exact file and profile ever print correctly?** If yes, it's a change —
   filament, nozzle wear, firmware, ambient temperature, mechanical drift. If no, it's the
   profile or the model.
3. **What changed?** New spool, new nozzle, slicer update, firmware update, the shop got
   cold, the printer was moved.
4. **Is the filament dry?** For PETG, nylon, TPU or any spool open more than a few weeks
   with diffuse symptoms, this is the highest-probability single cause.
5. **Mechanical check** — belt tension, loose grub screws on pulleys, nozzle tightness,
   wobble in the gantry, debris on rails. Two minutes, rules out a whole class of problems.
6. **Only now, settings.** And change one at a time, testing with the smallest print that
   isolates the variable rather than the real part.

## The print log

A log turns a farm from reactive to predictable, and it's what the metrics script reads.
Schema, matching [assets/print-log-template.csv](../assets/print-log-template.csv):

| Column | Meaning |
|---|---|
| `job_id` | Unique job identifier |
| `date` | ISO date (`YYYY-MM-DD`) |
| `printer` | Machine ID. Failure clustering by machine is the fastest route to a hardware fault |
| `material` | PLA / PETG / ABS / ASA / TPU / PA-CF / resin |
| `filament_g` | Grams consumed, including purge and supports |
| `print_hours` | Machine hours for the job |
| `status` | `success`, `failed`, or `aborted` |
| `failure_cause` | Free text or a controlled vocabulary — see the catalogue below |
| `parts` | Number of good parts produced |
| `post_hours` | Post-processing labour. **The most commonly omitted cost** |
| `profile` | Slicer profile used — links outcomes back to settings |
| `nozzle` | Size and type (e.g. `0.4 hardened`) |
| `notes` | Free text |

The habits that make it worth keeping: log **failures with the same care as successes**,
and record **what changed**. A log of only successful prints can't diagnose anything.

## Metrics that matter

Run `python scripts/print_metrics.py logs/prints.csv`.

**Success rate**, overall and by printer, material and profile. A well-run FDM setup
should sit **above 90%**; below ~80% something is systematically wrong. Track it by
machine — a single bad printer dragging the average is invisible in the aggregate and
obvious when split out.

**Failure cause distribution.** The point isn't the total, it's which cause dominates.
Adhesion failures point at bed prep and first layer; clogs at moisture, nozzle wear or
temperature; layer shifts at belts and mechanics.

**Material consumed per good part**, including failed prints. This is the true material
cost, and it's meaningfully higher than the slicer's estimate.

**Machine utilisation** — printing hours as a fraction of available hours. For anyone
selling, this decides whether capacity or demand is the constraint, and therefore whether
buying another printer helps at all.

**Cost per good part** — the number that makes pricing honest. See
[selling-and-licensing.md](selling-and-licensing.md).

Watch **trends, not levels**. A success rate drifting from 95% to 85% over a month is a
nozzle wearing out or a belt loosening, announcing itself early.

## FDM defect catalogue

| Symptom | Likely causes, most likely first |
|---|---|
| **Nothing sticks / part comes loose** | Dirty bed (fingerprint oil — wash with soap and water, not just IPA); Z-offset too high; bed too cold; no brim on a small footprint; warped bed needing a mesh |
| **Warping, corners lifting** | No enclosure on ABS/ASA; bed too cool; draught from a window or AC; sharp bottom corners; too much cooling |
| **Stringing / wisps** | **Wet filament**; nozzle too hot; retraction too low; travel crossing open space |
| **Poor layer adhesion, splits along layers** | Nozzle too cold; too much cooling; layer height too large for nozzle; printing too fast; wet filament |
| **Under-extrusion, gaps, thin lines** | Partial clog; wet filament; worn nozzle (especially after abrasives); flow rate low; extruder tension; exceeding max volumetric flow at speed |
| **Over-extrusion, blobby, dimensions oversize** | Flow rate too high; extruder steps uncalibrated; nozzle too hot |
| **Layer shift** | Loose belt; loose pulley grub screw; nozzle collided with a curled part; acceleration too high; stepper driver overheating |
| **Elephant foot (bulged first layers)** | Z-offset too low; bed too hot; no elephant-foot compensation |
| **Pillowing / holes in top surface** | Too few top layers; infill too sparse to support them; insufficient cooling |
| **Zits, blobs on the surface** | Retraction/coasting tuning; Z-seam placement; pressure advance uncalibrated |
| **Ringing / ghosting (echoes after corners)** | Acceleration/jerk too high; loose belts; printer not rigid or sitting on a flexible table; input shaping uncalibrated |
| **Z-banding (regular horizontal bands)** | Bent lead screw; binding on Z; inconsistent layer heights; temperature oscillation |
| **Spaghetti** | An earlier failure — part detached, or a clog mid-print. Diagnose the underlying cause, not the spaghetti |
| **Cracking in tall ABS parts** | No enclosure; draughts; cooling too high; layer bonding too weak |
| **Curled overhangs** | Insufficient cooling; nozzle too hot; overhang beyond 45° with no support |
| **Nozzle dragging through the print** | Over-extrusion; curled edges; Z-offset too low; needs Z-hop |

## Resin defect catalogue

| Symptom | Likely causes |
|---|---|
| **Nothing on the plate, prints stuck to FEP** | Under-exposed bottom layers; too few bottom layers; plate not levelled; plate not clean |
| **Layer separation / delamination** | Peel forces too high — reduce cross-section by angling the part; lift speed too fast; suction from an unvented hollow; FEP too tight or cloudy |
| **Loss of fine detail, holes filled in** | Over-exposure. Reduce exposure time |
| **Soft, sticky or undersized parts** | Under-exposure; resin too cold (most resins want ~25 °C); resin expired or poorly mixed |
| **Elephant foot** | Bottom exposure too long; too many bottom layers; no lift/chamfer on the raft |
| **Supports snap off mid-print** | Support tips too small; under-exposure; part angled poorly; insufficient support density on islands |
| **Brittle, yellowed parts** | Over-cured after washing; UV exposure over time; inherent to most standard resins |
| **Cracks appearing days later** | Trapped uncured resin inside a hollow with no drain holes |

## Clogs

Clogs are common enough to warrant their own approach. Types:

- **Partial clog** — intermittent under-extrusion, clicking. Usually debris or burnt
  residue. Try a cold pull (heat, then cool to ~90 °C for PLA and pull the filament out
  with the residue attached), repeated until it comes out clean.
- **Full clog** — nothing extrudes. Cold pull, then a nozzle cleaning needle, then replace
  the nozzle. Nozzles are cheap; a long fight with a clogged one rarely pays.
- **Heat creep** — filament softens too far up the heatbreak and jams. Symptoms: works
  initially then clogs partway into long prints, or after retractions. Causes: hotend fan
  failing or blocked (check it first), ambient too hot, too much retraction, printing too
  slowly at high temperature.
- **PTFE degradation** — in all-metal-adjacent hotends with a PTFE liner, printing above
  ~250 °C degrades the liner, causing clogs and releasing fumes. If someone is printing
  nylon or PC, confirm they have a genuinely all-metal hotend.

Prevention: dry filament, correct temperature, a clean nozzle, a working hotend fan, and
not letting filament run out mid-print.

## Maintenance schedule

Skipped maintenance shows up as mysterious quality problems weeks later.

**Weekly (or every ~50 print hours)**
- Wash the build plate with soap and water
- Visually check belt tension — should be taut, a low note when plucked
- Check the nozzle for oozing residue and clean while warm
- Clear debris from rails and the gantry

**Monthly (or ~200 hours)**
- Check and re-tension belts properly
- Check all pulley grub screws — a loose one causes intermittent layer shifts that look
  like a firmware problem
- Lubricate linear rails/rods with the correct lubricant (PTFE-based or manufacturer-spec;
  not WD-40)
- Check lead screws, clean and re-grease
- Check the hotend fan and part cooling fan actually spin
- Verify bed mesh / re-level
- Inspect the PTFE tube for wear at the hotend end

**Quarterly (or ~600 hours)**
- Replace the nozzle as a matter of course, sooner with abrasives
- Check extruder gears for wear and clear filament dust
- Check wiring, particularly the cable chain to the hotend, for chafing
- Inspect the heater cartridge and thermistor wiring for damage
- Resin: replace FEP/nFEP film; check the LCD for dead pixels

**As needed**
- Replace the build surface when adhesion degrades despite cleaning
- Replace PTFE tubing when the end deforms
- Recalibrate fully after any hardware change

## Consumable lifespans

Rough guidance; abrasive materials shorten all of these dramatically.

| Item | Typical life |
|---|---|
| Brass nozzle, non-abrasive | 300–800 print hours |
| Brass nozzle, abrasive filament | **10–50 hours** — often a single spool |
| Hardened steel nozzle, abrasive | 500–1500 hours |
| PTFE tube in hotend | 300–600 hours, less at high temperature |
| Build surface (PEI sheet) | 1–3 years with care; sooner if gouged |
| Resin FEP film | 20–60 prints, or immediately on any visible cloudiness or dent |
| Resin LCD | 500–2000 hours |
| Belts | 1–3 years |

A worn nozzle is the most under-diagnosed hardware fault in FDM. It degrades gradually, so
quality drifts down slowly enough that people adapt to it and blame their settings. If
someone has printed abrasives at all and is chasing diffuse quality problems, replacing the
nozzle costs a few pounds and eliminates the variable.
