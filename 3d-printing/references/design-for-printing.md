# Design for Printing

Contents:
- [Orientation is the first decision](#orientation-is-the-first-decision)
- [Anisotropy and where parts break](#anisotropy-and-where-parts-break)
- [Overhangs and self-supporting geometry](#overhangs-and-self-supporting-geometry)
- [Tolerances and fits](#tolerances-and-fits)
- [Holes](#holes)
- [Threads and fasteners](#threads-and-fasteners)
- [Snap fits and living hinges](#snap-fits-and-living-hinges)
- [Wall thickness and features](#wall-thickness-and-features)
- [Splitting and joining parts](#splitting-and-joining-parts)
- [Shrinkage and warping](#shrinkage-and-warping)
- [File formats](#file-formats)
- [A design review checklist](#a-design-review-checklist)

## Orientation is the first decision

Before any setting, decide how the part sits on the plate. Orientation determines strength
direction, surface finish, support requirements, print time, and dimensional accuracy —
more than any slicer setting will.

The four competing goals, which rarely agree:

1. **Put layer lines perpendicular to the main load** so stress isn't pulling layers apart.
2. **Minimise overhangs** needing support.
3. **Put the best surface where it shows** — top surfaces and outer walls look best,
   supported undersides look worst.
4. **Keep the footprint stable and tall thin sections short**, to avoid tipping and
   wobble artefacts.

When these conflict, **strength wins for functional parts and appearance wins for
decorative ones.** Say which you're optimising for, because the answers genuinely differ.

## Anisotropy and where parts break

An FDM part is a stack of welded layers. Bonds between layers are weaker than the plastic
itself — typically **30–50% weaker in Z than in XY**, varying with material, temperature
and cooling.

The practical consequence: **a printed part breaks along a layer line, almost always.** So
the design question is always "which way will the layers run, and does my load pull them
apart?"

Worked example — a bracket, an L-shape carrying a load on the horizontal arm:

- Printed flat on the plate, layers run horizontally, and the bending stress at the inside
  corner pulls directly across a layer bond. It snaps at the corner under modest load.
- Printed standing on the L's back face, layers run vertically through the corner and the
  stress runs *along* layers rather than across them. Same geometry, same material, several
  times stronger.

That reorientation is free. It's the highest-value advice in the whole skill for anyone
making functional parts, and most people never hear it.

Also worth knowing: **add a fillet at every inside corner.** Sharp internal corners are
stress concentrators, and a 2–3 mm fillet often doubles the load a bracket takes. This is
ordinary mechanical design, but printed parts make it especially cheap to add.

For genuinely isotropic strength, the answer is SLS or a different manufacturing process,
not better FDM settings.

## Overhangs and self-supporting geometry

The **45° rule**: overhangs up to 45° from vertical print unsupported because each layer
is half-supported by the one beneath. Beyond that, droop begins; beyond ~60° it usually
fails without support.

Designing around it:

- **Chamfer instead of overhang.** A 45° chamfer under a boss or ledge self-supports; a
  90° ledge needs support.
- **Teardrop horizontal holes.** A round horizontal hole has a 90° overhang at its top and
  sags. Adding a small point at the top makes it self-supporting — standard practice in
  printed parts.
- **Bridge rather than support.** Flat spans between two anchors print well up to 50 mm or
  so with good cooling; bridges are usually better than supported overhangs.
- **Split the part** at the problem plane and glue or fasten it.

## Tolerances and fits

Typical FDM dimensional accuracy is around **±0.2 mm** on a well-calibrated machine, and
the error is not symmetric — extrusion width, elephant foot and shrinkage all bias
dimensions. External features print slightly oversize, internal features slightly
undersize.

Practical clearances for mating printed parts, as a starting point to be verified on the
specific machine:

| Fit | Clearance (per side) |
|---|---|
| Press / interference | 0.0–0.05 mm |
| Snug — assembles with force, no play | 0.10–0.15 mm |
| Sliding — moves freely | 0.20–0.30 mm |
| Loose / hinge pin | 0.35–0.50 mm |

These vary by machine, material and speed, so anyone doing repeated assembly work should
**print a tolerance test** — a small part with a graduated series of clearances — once per
material, and then design to their measured numbers. It takes twenty minutes and saves
endless reprints.

## Holes

Printed holes come out **undersize**, for two compounding reasons: the slicer approximates
a circle with straight segments that fall inside the true circle, and extruded plastic
pulls inward slightly as it cools. A 5 mm designed hole typically measures 4.7–4.9 mm.

Options:

- **Oversize the hole in CAD** by 0.2–0.4 mm on diameter. Simplest.
- **Drill or ream** after printing where precision matters. Most reliable, and the right
  answer for bearing seats and dowel fits.
- **Use horizontal hole compensation** in the slicer if available.

For a vertical hole that must fit an M3 screw, design ~3.2–3.4 mm rather than 3.0 mm.

## Threads and fasteners

Options for threads in printed parts, best first:

1. **Heat-set threaded inserts.** Brass inserts pressed in with a soldering iron. Strong,
   reusable, and the correct answer for anything assembled more than once. Design the boss
   hole to the insert manufacturer's spec.
2. **Captive nuts.** A hexagonal pocket holding a standard nut. Cheap and strong; design a
   0.2 mm clearance and add a chamfered lead-in.
3. **Self-tapping screws into a plain hole.** Fine for light-duty and single assembly;
   strips readily on repeat use.
4. **Printed threads.** Workable at coarse pitches and larger diameters (M8+, or custom
   coarse profiles). Fine threads (M3) print poorly. Print them vertically where possible
   and expect to chase them with a tap.

Printed threads under real load are usually a mistake; heat-set inserts cost pennies and
solve the problem properly.

## Snap fits and living hinges

**Snap fits** work well printed, provided the cantilever is oriented so bending doesn't
pull layers apart — a snap arm printed flat, bending across layer lines, will snap off on
first use. Print the arm so its bending stress runs along layers. Taper the beam toward
the tip for even stress distribution, and use PETG or nylon rather than PLA, which is too
brittle to flex repeatedly.

**Living hinges** need a material with high fatigue resistance — **polypropylene or nylon**
are the real answers; PETG manages limited cycles; PLA cracks almost immediately. Print
them so the hinge flexes along layers, keep the thin section around 0.3–0.6 mm, and expect
to flex the hinge many times immediately after printing to align the polymer, as with
injection-moulded hinges.

## Wall thickness and features

- **Minimum wall:** ~2× extrusion width. With a 0.4 mm nozzle that's ~0.8 mm; below this
  the slicer may drop the feature entirely.
- **Design walls in multiples of extrusion width** (0.8, 1.2, 1.6 mm) so the slicer fills
  them cleanly without thin gaps.
- **Minimum embossed/engraved detail:** ~0.4 mm wide and 0.4 mm deep to show reliably.
- **Text:** at least 3–4 mm tall, embossed rather than engraved where possible; engraved
  fine text fills in.
- **Avoid tall thin towers** — they wobble and ring. Add a support structure or reorient.

## Splitting and joining parts

Splitting a model is often the right answer, not a compromise. Reasons: eliminating
supports entirely, fitting the build plate, orienting each piece for strength, printing
sections in different colours, and reducing the cost of a failure.

Alignment features make reassembly clean — printed dowel pins and sockets, or a
tongue-and-groove joint, with the clearances above. Joining: cyanoacrylate for PLA and
PETG, acetone welding for ABS, friction welding, or mechanical fasteners for anything that
must come apart.

## Shrinkage and warping

Thermoplastics shrink as they cool, and unevenly — the bottom is held by the bed while
upper layers pull inward, which lifts corners. Approximate shrinkage: **PLA ~0.3%, PETG
~0.4%, ABS/ASA ~0.7–0.8%, PC ~0.7%, nylon ~1%+.**

For large or precision parts this is real: a 200 mm ABS part can come out ~1.5 mm short.
Either compensate in CAD or apply a slicer shrinkage factor.

Reducing warping: enclosure and higher ambient temperature (the real fix for ABS), brim or
raft, generous fillets on bottom corners (sharp corners lift first), reduced cooling for
warp-prone materials, and avoiding large flat bottom surfaces where practical.

## File formats

- **STL** — universal, but a triangle mesh with no units, no curves and no metadata.
  Rounded features are faceted at whatever resolution was exported. Fine for distribution,
  poor for editing.
- **3MF** — the better modern choice. Carries units, colours, materials and often slicer
  settings. Prefer it when the toolchain supports it.
- **STEP** — parametric solid geometry. The right format for engineering exchange and for
  anything that may need editing later.
- **OBJ** — mesh with colour/texture; used for multi-colour and artistic models.

When exporting STL, **raise the export resolution** — the default in many CAD packages
visibly facets curved surfaces, and it's a common cause of "why does my cylinder look
polygonal".

## A design review checklist

When reviewing someone's part before printing:

1. What load does it carry, and in which direction relative to the layers?
2. Are there sharp internal corners that should be filleted?
3. What's the print orientation, and does it need supports? Can a chamfer or a split
   remove them?
4. Are horizontal holes teardropped?
5. Are mating clearances specified, and verified on this machine and material?
6. Are threads handled with inserts or captive nuts rather than printed fine threads?
7. Are walls a multiple of extrusion width, and above the minimum?
8. Is the material right for the service temperature and UV exposure?
9. For large parts, is shrinkage compensated?
10. Is there a large flat bottom that will warp, or a tall thin section that will wobble?
