# Research Methods

Contents:
- [Finding prior work](#finding-prior-work)
- [Reading a tissue culture paper critically](#reading-a-tissue-culture-paper-critically)
- [Designing an experiment](#designing-an-experiment)
- [Response variables](#response-variables)
- [Sample size and replication](#sample-size-and-replication)
- [Analysis](#analysis)
- [Recording and reproducibility](#recording-and-reproducibility)
- [Writing it up](#writing-it-up)

## Finding prior work

Always search before designing. Micropropagation literature is enormous — well over a century of
work across thousands of species — and someone has usually published something on your genus.
Even a mediocre paper on a congener beats reasoning from first principles.

Where to look, roughly in order of yield:

- **Google Scholar** — broadest coverage, and the "cited by" trail is the fastest way to find
  what came after a foundational paper.
- **PubMed / PMC** — good coverage of *Plant Cell, Tissue and Organ Culture* (PCTOC), the field's
  central journal, and *In Vitro Cellular & Developmental Biology – Plant*.
- **Review articles first.** A 2015 review of *Rhododendron* micropropagation saves you fifty
  primary papers and tells you which ones matter.
- **Society for In Vitro Biology**, IAPB, and regional horticultural society proceedings.
- **Theses and dissertations** — often contain the failed treatments that journal papers omit,
  which is exactly the information you need.
- **Extension publications** from land-grant universities — practical, production-oriented, and
  written for people who actually have to make it work.
- **Commercial lab catalogues** (PhytoTech, Caisson, Duchefa) — their premix listings implicitly
  document which media are standard for which crops.

Search strategy: try `micropropagation <genus>`, `in vitro regeneration <genus>`, `<genus>
tissue culture`, and `axillary shoot proliferation <genus>`. If the species yields nothing,
climb the taxonomy — genus, then tribe, then family. Also search the species' *commercial*
name; ornamental work is often published under trade names.

Use WebSearch and WebFetch when available. Report what you found and what you didn't — "no
published protocol for this species; the closest is X on a congener" is a genuinely useful
result and sets expectations honestly.

## Reading a tissue culture paper critically

Quality in this literature is uneven. Weight a paper by:

- **Is the genotype specified?** "*Rosa* sp." is nearly useless; cultivar-level response
  variation is large.
- **Is the explant type and its source described?** Explant type determines regeneration
  pathway, which determines whether the result transfers to your situation at all.
- **Is n stated, with replication and a control?** A great many papers report a single flask.
- **Are the statistics appropriate?** Percentage data analyzed by ANOVA without transformation
  is a common error. Fisher's LSD without correction over many comparisons inflates
  significance.
- **Is the medium fully specified** — base, strength, sucrose, gelling agent and concentration,
  pH, PGRs with units, and vessel type and closure? Missing gas exchange information is very
  common and it's a major variable.
- **Do they report acclimatization survival?** Papers ending at "100% rooting in vitro" have not
  demonstrated a working protocol. Stage IV is where protocols die.
- **Is the reported optimum at the edge of the range tested?** If the best result is at the
  highest BAP level tried, the real optimum is probably outside their range and their conclusion
  is an artefact of the design.

Treat a published protocol as a well-informed prior, not a result. Your water, your premix lot,
your vessels, and your genotype all differ.

## Designing an experiment

**Ask one question at a time, but test it across levels.** The most common amateur design —
"I'll try this new medium and see" — produces an uninterpretable result, because the new medium
differs in several ways at once.

**Factorial designs** are the workhorse. Testing cytokinin at 4 levels × auxin at 3 levels = 12
treatment combinations, which reveals the *interaction* — and in tissue culture the interaction
is usually the whole story, since it's the ratio that determines organogenesis. A one-factor-at-
a-time approach systematically misses this.

**Always include a control.** Usually PGR-free medium, or your current standard protocol. Without
it you can't tell whether the treatment helped or the batch was just good.

**Randomize and block.** Position in a culture room is not neutral — light and temperature vary
by shelf and by distance from the door. Randomize vessel placement, or block by shelf and treat
shelf as a factor. Systematic placement by treatment turns a shelf gradient into a fake
treatment effect, and this is a genuinely common error.

**Blind the scoring** where the response variable is subjective (vigor ratings, variegation
quality). Knowing which flask got the good treatment biases scoring more than people expect.

**Run a pilot** before a large factorial, especially for anything toxic or destructive. A small
kill curve or range-finding run costs one batch and prevents a full experiment landing entirely
outside the responsive range.

## Response variables

Choose these before you start, and define them operationally so scoring is repeatable:

- **Establishment rate** — % explants clean and viable at day 30
- **Contamination rate** — by type
- **Multiplication rate** — shoots ≥ some defined length per explant per cycle. Define the length
  threshold in advance; "usable shoot" drifts otherwise
- **Shoot length** — mean, and note the distribution; a mean hides a bimodal response
- **Rooting percentage**, root number, root length
- **Hyperhydricity incidence** — % shoots showing glassiness, scored against a written rubric
- **Off-type / variant frequency**
- **Stage IV survival at 4 weeks** — the one that actually matters commercially

Record **quality as well as quantity**. A treatment giving 8 shoots per explant that are all
hyperhydric is worse than one giving 3 that root cleanly, and a design that only counts shoots
will pick the wrong winner.

## Sample size and replication

**Replication** means independent experimental units — separate vessels, not multiple shoots in
one vessel. Shoots sharing a vessel share its medium, its closure, and its contamination fate,
so they are pseudoreplicates. Analyzing them as independent inflates n and manufactures
significance. Use vessel as the experimental unit, or handle it with a mixed model treating
vessel as a random effect.

Practical minimums: **at least 10 vessels per treatment** for a screening experiment, 20–30 for
anything you'll publish or bet money on. For rare events (mutation screening, polyploid
recovery), you need hundreds to thousands, which is why those programs are designed around
cheap mass screening.

**Repeat the whole experiment** at least once, at a different time. Batch effects in tissue
culture are large — a different premix lot or season shifts everything. A result that doesn't
replicate across runs isn't a result, and this is the single best defense against fooling
yourself.

## Analysis

- **Percentage and proportion data** (contamination, rooting, survival) violate ANOVA
  assumptions. Use logistic regression / a GLM with binomial family, or apply an
  arcsine-square-root or logit transformation. Analyzing raw percentages is the most common
  statistical error in this literature.
- **Count data** (shoots per explant, roots per shoot) — Poisson or negative binomial GLM.
  Negative binomial when variance exceeds the mean, which is usual.
- **Continuous data** (lengths, weights) — ANOVA, after checking normality and equal variance.
- **Multiple comparisons** — with many treatments, use Tukey HSD or Dunnett (when comparing all
  treatments against one control) rather than unadjusted pairwise t-tests.
- **Report effect sizes and confidence intervals**, not just p-values. "Significantly higher"
  matters much less than "2.1 shoots higher, 95% CI 1.4–2.8" when you're deciding whether a
  protocol change pays for itself.

Python with `pandas` + `statsmodels` (or R) handles all of this. Offer to write the analysis
script rather than reasoning about statistics in prose — and plot the data before testing it. A
scatter or box plot per treatment reveals bimodality, outliers, and shelf gradients that no
summary statistic will show you.

## Recording and reproducibility

A year later you will not remember which flask was which. Record, at minimum:

- Full medium formulation, including basal salt **lot number** and gelling agent brand
- PGR stock preparation dates and solvents
- Autoclave cycle and the load size
- Explant source: mother plant ID, tissue type, position on the plant, date and time collected
- Culture room conditions and shelf position
- Every date of transfer and observation
- Photographs, with a scale reference and consistent lighting, at every scoring point

Use [assets/protocol-template.md](../assets/protocol-template.md) for protocols and the culture
log schema in [monitoring-and-troubleshooting.md](monitoring-and-troubleshooting.md) for batches.

**Photograph more than feels necessary.** Photographs are the only record that can answer a
question you didn't know you'd have — and in ornamental breeding they're also dated evidence of
when a phenotype first appeared, which matters for protection claims.

## Writing it up

For a journal, a horticultural society, or just a lab report someone else will read, the
standard structure works because readers expect it:

- **Materials and methods** in enough detail to reproduce — this is where most papers fail, and
  where yours can be genuinely more useful than the ones you had to read.
- **Report failed treatments.** They carry as much information as successes and are almost never
  published, which is why everyone repeats the same dead ends.
- **State the genotype and the conditions** so readers can judge transferability.
- **Don't over-claim.** "100% rooting" without acclimatization data is not a working protocol,
  and readers who try it will find out.
