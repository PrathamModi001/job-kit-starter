# Apply-loop token optimization: per-job isolation + deterministic tailoring

## Problem

The daily apply loop (`.agents/workflows/daily_scan.md`) runs all `NUM_JOBS`
(default 15) applications inside one flat conversation. Two consequences:

1. **Token bloat.** Each job's resume tailoring (`/make-resume` Batch Mode)
   reads ~8 files (~20k tokens) cold, and Playwright form-filling can add
   more on top. Across 15 jobs this compounds to 300k+ tokens in a single
   context, with no isolation between jobs.
2. **Late-run quality decay.** As context grows, the model is more likely to
   mis-recall personal-info facts (name, phone, CTC, notice period) when
   filling forms for job #8+, or to lose track of the mechanical
   exclusion/candidate-bar rules established at the top of the run.

Separately, `daily_scan.md` step 5 currently tailors a resume (5a) *before*
running the mechanical exclusion / screener check (5b2), even though the
check's own text says "before opening the application form" — this wastes a
full tailoring pass on jobs that get skipped anyway (e.g. a JD that turns
out to require 4+ YOE or Java, only discovered on the application form
itself).

## Goals

- **Every application gets a resume tailored specifically to that job's JD,
  with the highest truthful ATS keyword match rate achievable.** No
  generic/cached/reused resume, ever — this is a hard invariant, not a
  preference.
- Cut the per-job token cost of resume tailoring by having a deterministic
  script own keyword extraction and bullet/tagline/skills selection, with
  the LLM reviewing and polishing that draft rather than reading all
  candidate material cold.
- Isolate each job's context (tailoring reasoning, Playwright traces, form
  fills) inside its own subagent, so the orchestrator's context — and thus
  the risk of personal-info hallucination from context decay — stays flat
  regardless of `NUM_JOBS`.
- Stop wasting tailoring effort on jobs that fail the mechanical exclusion
  check or an early screener signal.
- Reduce incidental token waste: full-CSV reads for dedup, `browser_snapshot`
  calls for element discovery.

## Non-goals

- Not replacing the existing quality gates (`char_count.py`,
  `fingerprint_check.py`, 1-page compile check, ATS-coverage ≥75% floor,
  condensed critique) — every one of them still runs, per job, no exceptions.
- Not touching cold-outreach (Phase 4/5/6) — explicitly out of scope per the
  user's original request.
- Not building a new orchestration framework — uses Claude Code's existing
  Task/Agent tool (the same primitive `.claude/agents/csv-logger.md`
  already uses), not a bespoke subagent system.
- Not changing the `NUM_JOBS` semantics, Indeed Smart Apply / LinkedIn Easy
  Apply uncapped-lane behavior, or the Candidate Bar itself.

## Design

### 1. `resume_builder/helpers/tailor_resume.py` (new, deterministic)

CLI: `python3 tailor_resume.py --jd <path> --lane <backend|ai|fullstack|auto>`

Given a JD, this script:

1. **Lane selection** (if `--lane auto`): keyword-match the JD against each
   bundle's "Use for JDs titled..." line; default to Backend on ties, per
   the existing Decision Tree in `achievement_reframing_guide.md`.
2. **Keyword extraction**: tokenize the JD, match against (a) each bundle's
   Approved Tool Pool, (b) `skills_taxonomy.md` entries, (c) tokens that
   appear verbatim inside any experience-file bullet. Tag each matched term
   Direct (in experience files/skills taxonomy) / Bridge (present in
   skills taxonomy but not yet demonstrated) / Gap (absent).
3. **Bullet selection**: score every bullet ID in the lane's Priority Matrix
   by JD-keyword overlap with that bullet's literal text. Start from the
   matrix's default HIGH/MEDIUM/LOW ranking and default caps (e.g. the
   backend lane's "max 1 of {PP2, PP3}" rule), then **greedily try
   alternate truthful swaps within the same rank tier if a swap raises
   keyword coverage** — this is the "maximize ATS" behavior the user asked
   for, not just picking the static default order.
4. **Tagline assembly**: pick the 4 approved-pool tools that appear in the
   JD, in JD order, falling back to the bundle's default priority list to
   fill remaining slots — mechanical, matches the bundle rule exactly.
5. **Output**: writes a draft `output/<Company>/e2e_<name>_resume.tex`
   (from the template, with bullets/tagline/skills substituted in) plus
   `output/<Company>/keyword_table.json` (the Direct/Bridge/Gap table and
   the computed coverage %). Runtime target: under a few seconds, 0 LLM
   tokens.

This script **never reads or copies a previous output folder** — every
invocation regenerates from the bundle + experience files + this JD only.
There is no code path that can produce a reused resume.

### 2. `make-resume/SKILL.md` changes (Batch Mode)

Step 0 changes from "read all 3 experience files + full bundle + skills
taxonomy cold" to:

1. Run `tailor_resume.py` for this JD.
2. Read only: the generated draft `.tex`, `keyword_table.json`, and the
   bundle's "Bullet Generation Policy" / lever rules (not the full
   experience files) — unless the script's coverage % is below target, in
   which case fall back to reading the relevant full experience file to
   find a better truthful swap the script's overlap heuristic missed.

Steps 3 (apply the 5 levers as a *review* pass over the draft, not
from-scratch generation), 4 (char-count/compile), 5 (fingerprint), 6 (ATS
coverage — recheck the script's computed number against the final text),
7 (critique), 8 (report) are unchanged in substance — same gates, same
pass/fail behavior, just operating on a script-provided draft instead of a
blank page. This preserves the review step that catches cases a keyword
heuristic can't judge (truthful bridging, honest gap acceptance).

### 3. `daily_scan.md` restructuring

**3a. Gate reorder (step 5).** New order per lead:
1. Mechanical exclusion check (title/stack string match) — unchanged logic,
   just moved first.
2. Fetch the JD and, where visible without a full form-fill (JD text,
   ATS API response, or the first form page), check for an explicit hard
   screener disqualifier (e.g. "4+ years required", visa sponsorship
   required) — skip immediately if found, logging `Status=Skipped`.
3. Only then: tailor (`/make-resume`, now backed by `tailor_resume.py`),
   fill, submit.

**3b. Per-job subagent dispatch.** For each of the top `NUM_JOBS` shortlisted
leads (plus each qualifying Indeed Smart Apply / LinkedIn Easy Apply lead),
the orchestrator dispatches one Task/Agent-tool subagent instead of running
step 5 inline. Payload passed to the subagent (kept deliberately small):

```
Company, Role, Job URL, JD text or fetch instructions,
output folder path (output/<Company> - <Role>/),
path to .agents/rules/job_hunt_profile.md (canonical form facts —
  read fresh inside the subagent, not pasted into the payload),
today's date (subagent has no clock)
```

The subagent runs steps 3a.2–3a.3 above end-to-end (screener check →
tailor → fill → submit → csv-logger delegation) and returns exactly one
line to the orchestrator:

```
<Status> | <Company> | <Role> | <Resume path or "-"> | <Req ID or reason>
```

The orchestrator's job is only to track the queue (`Pending/Applied/
Blocked/Skipped` per lead) from these one-line returns and decide whether
to pull another lead to fill a `NUM_JOBS` slot — it never holds tailoring
reasoning, browser traces, or compile output in its own context. This is
the direct fix for late-run hallucination: personal-info form-filling
always happens inside a subagent that just freshly read
`job_hunt_profile.md`, never from a conversation that has drifted across
7+ prior jobs.

Sourcing (`job_hunt.py`/`job_hunt_india.py`/`hn_scan.py`) and cold outreach
(Phase 4+) stay inline in the orchestrator — they're already 0-LLM scripts
or explicitly out of scope.

### 4. Playwright evaluate-only rule

Add a short rule (in `PLAYBOOK.md`, near the existing ATS recipes) stating:
element discovery/interaction during form-filling uses `browser_evaluate`
with targeted DOM queries (the pattern every existing ATS recipe already
uses) or `browser_click`/`browser_fill_form` with known selectors —
`browser_snapshot` (full accessibility-tree dump) is reserved for cases
where the agent is genuinely stuck and has no other way to locate an
element. This codifies existing practice rather than changing it, so a
future session doesn't regress into snapshot-heavy debugging.

### 5. CSV dedup check

Step 1 of `daily_scan.md` ("check applications.csv for companies already
applied to") changes from "read the file" to a small helper/one-liner
(`python3 -c "..."` or a tiny script) that greps company names out of the
CSV and returns just the list — not the full 52KB/142-row file — into
context.

## Testing / validation

- `tailor_resume.py`: unit tests against 2-3 sample JDs per lane, asserting
  (a) tagline tools all come from the approved pool, (b) bullet selection
  respects existing cap rules (e.g. backend lane's PP2/PP3 cap), (c)
  coverage % calculation matches a hand-computed value.
- End-to-end: run `/make-resume` on a real JD before/after, diff the
  resulting `.tex` and ATS coverage % — coverage should be equal or higher,
  never lower, and all existing gates (char-count, compile, fingerprint)
  must still pass.
- `daily_scan.md`: dry-run a single lead through the new subagent dispatch
  path, confirm the one-line return format and that `applications.csv` gets
  exactly one correct row via `csv-logger`.
- Confirm the reordered gate actually skips a known-excluded JD (e.g. a
  Java-titled role) before any `.tex` file is written.

## Rollout

Implemented on branch `apply-loop-token-optimization` (off
`batch-mode-merge-and-cleanup`). No changes to `NUM_JOBS` defaults, the
Candidate Bar, or cold-outreach behavior. Existing single-shot `/make-resume`
invocation (outside `daily_scan.md`) continues to work unchanged, just
faster.
