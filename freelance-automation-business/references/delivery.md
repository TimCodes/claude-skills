# Delivery Standards & QA

The deliverable is the review. A working script delivered messily reads as amateur work; the
same script with a clean handoff package reads as a $500 job that cost $150. The extra 15
minutes here is the cheapest marketing the business has.

## The handoff package

Every delivery contains:

1. **The code** — one obvious entry point (`python main.py` or a single script), configuration
   at the top of the file or in a `.env.example` / `config` section, no secrets committed.
2. **Pinned dependencies** — `requirements.txt` with versions (or the language's equivalent).
   "Works on my machine" failures are the #1 source of post-delivery friction.
3. **README** — from [assets/delivery-readme-template.md](../assets/delivery-readme-template.md),
   written for a non-developer: what it does, exact setup commands, how to run, what the output
   looks like, common errors in plain English.
4. **Sample output** — the actual result on their data (or sample data), so they see success
   before they run anything.

## Code standards

- Write for the *next* freelancer (or the client's nephew) who opens this file: clear names,
  small functions, comments only where the code can't speak (site quirks, rate limits, "this
  endpoint returns HTML on error instead of a 4xx").
- Fail loudly and helpfully. Every external touchpoint (network, file, credentials) gets an
  error message that tells the client what to check — this converts future support messages
  into self-service.
- Be polite to third parties: honor rate limits, identify with a sane User-Agent, back off on
  errors. Fragile-because-aggressive scrapers boomerang back as unpaid support.
- Don't gold-plate. Deliver what was scoped; put the good ideas ("this could also alert you by
  email") in the delivery message as upsells, not in the code as unpaid features.

## QA checklist — run before anything reaches Review & Send

Report the results with the deliverable; anything not verifiable by you gets flagged for the
human to test.

- [ ] Fresh-environment run: install from the pinned dependency file in a clean venv, run the
      README commands exactly as written. (The README is code — test it.)
- [ ] Ran against real/sample client data; output spot-checked by hand (row counts sane, no
      empty columns, encodings/dates/currency correct).
- [ ] Edge inputs tried: empty input, malformed row, network timeout — script fails with a
      helpful message, not a stack trace.
- [ ] No secrets, personal paths, or leftover debug output in any delivered file.
- [ ] Scope check: every promised deliverable present; nothing significant delivered that
      wasn't scoped.
- [ ] Delivery message drafted: what's included, how to run in one sentence, revision-round
      reminder, and any upsell noted separately.

If any box can't be checked (needs client credentials, client-only environment), state it
explicitly in the Review & Send list: what's untested and exactly what the human or client
must do to verify it.
