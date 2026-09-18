# AI Fingerprint Rules

> Referenced by `make-resume` Phase 2 and `critique_framework.md` Part 6G.
> Purpose: avoid resume text that reads as LLM-generated to a human reviewer
> or an LLM-based screening tool — not an ATS keyword issue, a "does this
> sound like a real engineer wrote it" issue.

## Banned words / phrases (Tier 1 — hard fail if present)

delve, tapestry, multifaceted, pivotal, robust (as a filler adjective), seamless,
seamlessly, leverage/leveraged (as a verb for "used"), boasts, showcase(s),
in today's fast-paced/ever-evolving, cutting-edge (as filler), synergy,
game-changer, unlock/unlocking potential, holistic, paradigm shift.

## Structural rules

1. **No "-ing" analysis endings** on bullets (e.g., "...advancing the field",
   "...contributing to scalability"). End bullets on a concrete result or metric.
2. **Em-dash cap:** max 2 per document. This project's bullets use "--" (en-dash)
   for ranges already — do not introduce additional em-dashes during editing.
3. **No uniform sentence length.** If every bullet is within 5 characters of
   the same length, that's a generation artifact — natural variation is fine
   as long as each bullet stays within its char budget.
4. **No generic cover-letter openers** ("I am writing to express my interest...").
5. **Every bullet must contain a real number or a named tool** (already true for
   this profile's bullets) — a bullet with neither reads as vague/generated filler.

## Post-generation scan checklist

- [ ] Grep the compiled `.tex`/PDF text for every Tier 1 word above — zero hits.
- [ ] Count em-dashes — flag if > 2.
- [ ] Read every bullet ending — flag any "-ing" analysis closer.
- [ ] Confirm no two consecutive bullets start with the same verb.
