# Testing and Research

Contents:
- [Calibration prints vs. experiments](#calibration-prints-vs-experiments)
- [The standard calibration prints](#the-standard-calibration-prints)
- [Designing a real experiment](#designing-a-real-experiment)
- [Confounds specific to printing](#confounds-specific-to-printing)
- [Mechanical testing](#mechanical-testing)
- [Measuring properly](#measuring-properly)
- [Analysis](#analysis)
- [Finding prior work](#finding-prior-work)
- [Recording results](#recording-results)

## Calibration prints vs. experiments

Two different activities that get conflated.

**Calibration** finds the right value of a setting for a known-good outcome — a temp tower
tells you which temperature gives the best surface and bonding. The answer is read off by
eye, and that's fine, because the effect sizes are large and obvious.

**Experiments** answer a question where the effect is smaller than the noise of a single
print: does 4 walls at 20% infill beat 3 walls at 40%? Does printing at 0.28 mm really
produce stronger parts? Here a single print of each proves nothing, because print-to-print
variation is substantial. You need replication and measurement.

Most people run experiments as if they were calibrations — one print each, eyeball the
result, conclude confidently — and reach wrong conclusions. When someone asks a
comparative question about strength or accuracy, the honest answer usually starts with
"that needs more than one print of each."

## The standard calibration prints

| Print | Answers | Read it by |
|---|---|---|
| **Temperature tower** | Best nozzle temp for this filament | Surface quality, stringing between segments, and snapping each segment to compare layer bonding |
| **Retraction tower** | Retraction distance/speed | Stringing between towers |
| **Calibration cube (20 mm)** | Dimensional accuracy | Calipers on X, Y, Z. Check all three; Z errors mean something different from XY errors |
| **Single-wall cube** | Flow rate / extrusion multiplier | Caliper the wall; compare to expected extrusion width |
| **Overhang test** | Where overhangs start failing on this machine | Visual, per angle step |
| **Bridging test** | Bridge quality and max span | Visual sag |
| **Tolerance/fit test** | Real clearances for this machine and material | Which pin actually slides |
| **Max volumetric flow test** | Hotend flow ceiling | Where extrusion starts falling behind |
| **Benchy** | General health check, several issues at once | Comparison to known-good; useful as a regression test, poor as a first diagnostic |

Two notes. Print a **tolerance test once per material** — it converts guessed clearances
into measured ones and pays for itself immediately for anyone designing assemblies. And
use Benchy as a *regression* test after changing something, not as a starting diagnostic;
it exercises too many variables at once to isolate a cause.

## Designing a real experiment

1. **State the question and the response variable up front.** "Is it stronger" is not
   measurable; "what load does it carry before fracture, in three-point bending" is.
2. **Change one factor at a time, or run a proper factorial.** Testing wall count × infill
   at 3 × 3 = 9 combinations reveals whether they interact — and for strength they do,
   because walls and infill contribute differently under different loads. One-factor-at-a-
   time misses that.
3. **Include a control** — the current profile, so the comparison is against practice
   rather than an abstraction.
4. **Replicate.** At least **5 specimens per condition** for mechanical testing, more if
   variance is high. A single specimen tells you almost nothing; printed-part strength has
   substantial scatter because failure initiates at random defects.
5. **Randomise plate position** (see below).
6. **Pre-register the decision rule.** Decide before printing what result would change your
   profile. Otherwise the result gets rationalised either way.

## Confounds specific to printing

These quietly ruin comparisons, and most are invisible unless you know to control them:

- **Plate position.** Parts at the edges of a bed print differently from the centre —
  cooling airflow, bed temperature uniformity and Z-height all vary. If all condition-A
  specimens sit on the left and condition-B on the right, you've measured position, not
  treatment. **Randomise or alternate positions across the plate.**
- **Printing conditions together vs. separately.** Printing all specimens on one plate
  means they share the same ambient conditions but also means each layer's cooling time
  depends on the other parts. Printing separately changes layer times. Neither is wrong;
  be consistent and say which you did.
- **Spool and batch.** Colour and batch change mechanical properties measurably — pigment
  affects crystallinity in PLA. Use one spool for a whole comparison where possible, and
  record the spool.
- **Moisture drift.** A spool absorbs water across a multi-day experiment. Dry it first
  and keep it in a dry box, or you're measuring humidity.
- **Ambient temperature.** A garage in winter versus a warm afternoon changes warping and
  layer bonding. Record it.
- **Nozzle wear across a long test.** If the experiment spans hundreds of hours with an
  abrasive, the nozzle at the end isn't the nozzle at the start.

## Mechanical testing

Real standards exist and are worth following loosely even without a lab:

- **Tensile:** ASTM D638 (Type IV specimens are the practical choice) or ISO 527.
- **Flexural / three-point bend:** ASTM D790. Much easier to rig at home and often more
  relevant to how printed parts actually fail.
- **Impact:** ASTM D256 (Izod). Hard to do informally.

A workable home setup: three-point bending with a printed jig, a hanging bucket, and water
added until fracture, weighing the bucket. Crude but genuinely comparative if the geometry
and span are held constant. A luggage scale or a cheap load cell improves it.

What to hold constant so results mean something: specimen geometry, span, loading rate
(add water at a consistent pace — loading rate genuinely affects results in polymers),
temperature, and time since printing. **Print orientation must be recorded**, since it
dominates everything else.

Report the **mean and the spread**, not the single best result. Printed-part strength has
a long lower tail, and for design purposes the low values matter more than the mean.

## Measuring properly

- **Calipers**: measure the same feature three times and average; digital calipers are
  repeatable to ~0.02 mm but user technique is worse than that. Measure away from the
  seam and the elephant foot.
- **Mass**: a 0.01 g scale is the cheapest way to compare actual material use against the
  slicer's estimate — useful for costing.
- **Don't measure dimensions on the first layer** — elephant foot biases it.
- **Let parts cool fully** before measuring; a warm PLA part is still shrinking.

## Analysis

- **Comparing two conditions:** a t-test if the data are roughly normal, otherwise
  Mann-Whitney. With n=5 per group, only large effects will be detectable — say so rather
  than reporting a null as "no difference".
- **More than two conditions:** ANOVA followed by Tukey, or the factorial equivalent.
- **Failure/success counts:** proportions with confidence intervals. With 20 prints and 2
  failures, the 95% interval on the failure rate runs roughly 1–32% — far wider than
  people assume, which is why one bad week doesn't prove a machine is broken.
- **Always plot before testing.** A scatter of specimen strength by plate position will
  reveal a position confound that no summary statistic shows.
- **Report effect sizes**, not just significance. "8% stronger" is decision-relevant;
  "p < 0.05" alone isn't, especially when the cost is 40% more print time.

Offer to write the analysis in Python (`pandas`, `scipy`, `statsmodels`) rather than
reasoning about statistics in prose.

## Finding prior work

Search before running a long experiment — many of these questions have been answered
carefully.

- **CNC Kitchen** (Stefan Hermann) — the reference source for systematic mechanical testing
  of printing variables, with published methodology.
- **Peer-reviewed additive manufacturing literature** via Google Scholar — search
  "FDM tensile strength layer height", "raster angle mechanical properties", and similar.
  Substantial academic work exists on process parameters vs. mechanical properties.
- **Manufacturer technical data sheets** — for glass transition, service temperature and
  recommended settings. Always prefer the actual TDS over forum numbers.
- **Slicer documentation** (PrusaSlicer, OrcaSlicer) — genuinely good explanations of what
  settings do.
- **Printer and material community forums** — useful for machine-specific quirks, weak on
  quantitative claims. Treat specific numbers as hypotheses.

Report what you found and what you didn't. "No systematic data on this specific
comparison; here's the closest study and how it differs" is an honest and useful answer.

## Recording results

Record enough that a result is interpretable later: material, brand, colour and spool;
whether it was dried and when; printer and nozzle (size, type, approximate hours);
complete profile settings or the exported profile file; plate position; ambient
temperature; date; and specimen geometry and orientation.

Use [assets/profile-record-template.md](../assets/profile-record-template.md) for
profiles, and photograph fracture surfaces — how a part broke (along a layer, through the
wall, at a stress concentration) usually explains the number better than the number does.
