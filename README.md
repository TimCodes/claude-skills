# claude-skills

Personal library of Claude Code skills. This directory is loaded directly by Claude Code as
`~/.claude/skills/`, so every skill folder here is available automatically in every project.

## Structure

Each skill is a self-contained top-level folder:

```
<skill-name>/
├── SKILL.md            required — frontmatter (name, description) + instructions
├── references/         optional — docs loaded into context on demand
├── assets/              optional — templates/files used in output
└── evals/evals.json    optional — test prompts for the skill-creator eval loop
```

Add a new skill by creating a new top-level folder following this layout — no other wiring is
needed for Claude Code to discover it.

## Skills

| Skill | Purpose |
|---|---|
| [marketplace-selling](marketplace-selling/SKILL.md) | Operations partner for a multi-channel maker + resale business on Etsy, Amazon, and Facebook — channel choice and fee maths, listing SEO, cross-channel pricing, fulfilment and returns, account health, and overstock sourcing. Covers five product lines (plants, 3D prints, terrariums, woodworking, resold overstock) and hands off product-making detail to the plant-tissue-culture and 3d-printing skills. Bundles a channel-margin/pricing calculator and a sales-metrics script. |
| [3d-printing](3d-printing/SKILL.md) | Shop partner for 3D printing — process and material selection, slicer profiles and calibration, design-for-printing (orientation, anisotropy, tolerances, fits), failure diagnosis and machine maintenance, print testing and experiment design, and honest costing/pricing/licensing for selling prints. Bundles a quote calculator and a print-log metrics script. |
| [discretionary-trading-assistant](discretionary-trading-assistant/SKILL.md) | Analyst co-pilot for discretionary trading across futures, stocks, forex, and crypto — setup analysis, chart-screenshot reading, risk-based sizing, and trade journaling via MCP servers (broker, exchange, news, RAG store). |
| [plant-tissue-culture](plant-tissue-culture/SKILL.md) | Lab partner for micropropagation — media and PGR formulation, stage-by-stage protocols, breeding and selection for unique traits (chimeral variegation, polyploidy, dwarfing), contamination and culture-log monitoring, experiment design, and the commercial/IP side of selling plantlets. Bundles a media calculator and a culture-metrics script. |
| [freelance-automation-business](freelance-automation-business/SKILL.md) | Operator co-pilot for a solo Upwork/Fiverr automation & scripting business — browser-driven job scouting, job scoring, proposal drafting, client-message drafts, delivery packaging with QA, and a daily operating loop that batches everything into one human Review & Send hour. |
