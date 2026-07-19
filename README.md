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
| [discretionary-trading-assistant](discretionary-trading-assistant/SKILL.md) | Analyst co-pilot for discretionary trading across futures, stocks, forex, and crypto — setup analysis, chart-screenshot reading, risk-based sizing, and trade journaling via MCP servers (broker, exchange, news, RAG store). |
| [plant-tissue-culture](plant-tissue-culture/SKILL.md) | Lab partner for micropropagation — media and PGR formulation, stage-by-stage protocols, breeding and selection for unique traits (chimeral variegation, polyploidy, dwarfing), contamination and culture-log monitoring, experiment design, and the commercial/IP side of selling plantlets. Bundles a media calculator and a culture-metrics script. |
| [freelance-automation-business](freelance-automation-business/SKILL.md) | Operator co-pilot for a solo Upwork/Fiverr automation & scripting business — browser-driven job scouting, job scoring, proposal drafting, client-message drafts, delivery packaging with QA, and a daily operating loop that batches everything into one human Review & Send hour. |
