# Proposal Writing

Clients skim 20–50 proposals. The winner is almost always the one that proves it read the
posting and reduces the client's perceived risk. Length: 120–200 words. Never send boilerplate
— a template the client can smell is worse than a short honest note.

## Structure (in this order)

1. **First line = their problem, specifically.** Reference a concrete detail from the posting
   (the site being scraped, the column names, the error). This one line beats credentials.
2. **The plan in 2–3 steps.** Show you already know how to solve it. Name the approach/tools
   plainly ("requests + BeautifulSoup; Playwright only if the site needs JS").
3. **One relevant proof point.** A similar past job, or — if the profile is new — offer a
   small verifiable slice: "I'll deliver the first 50 rows extracted before you pay anything
   beyond the milestone." Never invent history.
4. **Price, delivery date, what's included.** Fixed price, calendar date, "includes one
   revision round and a README so your team can run it."
5. **One smart question.** A question only someone who understood the job would ask. It starts
   the conversation, which is the real goal of the proposal.

## Tone rules

- Write like a competent human, not a marketer. No "I am thrilled", no "esteemed client",
  no wall of skills.
- Confidence without guarantees: "this is a 1–2 day job" ✓, "guaranteed to never break" ✗.
- Match the client's register — terse posting, terse proposal.

## Example

**Posting:** "Our Python script that pulls listings from a real-estate site stopped working
last week. Need it fixed fast. Budget $150."

**Proposal:**

> Your scraper most likely broke because the site changed its HTML or added bot detection last
> week — I fix this exact failure regularly.
>
> Plan: (1) run your script against the live site and pinpoint what changed, (2) update the
> selectors or switch that section to their underlying JSON endpoint, which survives redesigns,
> (3) add a clear error message so future breakage tells you what happened instead of failing
> silently.
>
> Recent similar work: repaired a product-listing scraper broken by a Cloudflare update,
> delivered in 36 hours.
>
> $140 fixed, delivered within 2 days of getting the script. Includes one revision round and a
> short README. One question: do you need the fix only, or also a heads-up mechanism (e.g.,
> email alert) for the next time the site changes?

## New-profile angle

With zero reviews, sell the two things reviews normally prove: **verifiable competence** (offer
a milestone structure where they see working output before most of the money moves) and
**introductory pricing** (say explicitly it's temporary while building marketplace history —
this reframes cheap as strategic, not desperate).
