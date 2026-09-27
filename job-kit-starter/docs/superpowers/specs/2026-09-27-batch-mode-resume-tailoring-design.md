# Batch Mode: single-path, ATS-first resume tailoring

**Date:** 2026-09-27
**Status:** Approved for planning

## Problem

Two tailoring paths exist today and neither fits the autonomous daily-scan loop:

1. `.claude/skills/make-resume/SKILL.md` (Full/Quick mode) — thorough but expensive:
   mandatory 2-3 web searches, 3 mandatory human STOP gates, full session-file
   re-reads at every phase boundary, and an 8-dimension `critique_framework.md`
   pass (503 lines, 7-element lens + 5 personas + scoring). Fine for 1-3
   high-value applications a day, too expensive to run 5x/day.
2. `.agents/workflows/daily_scan.md` step 5a — what the daily batch actually
   runs: "select lane bundle, pull copy-exact bullets, compile, verify
   1-page." No JD keyword reasoning, no `ai_fingerprint_rules.md` check, no
   critique at all — tailoring with no reasoning about *why* a bullet fits
   *this* JD.

Having two paths also risks the executing LLM picking the wrong one, or
drifting the two out of sync (daily_scan.md re-describes the pipeline inline
instead of invoking the skill).

## Goal

One path only: **Batch Mode**, wired as the sole mode of `/make-resume`,
optimized for **truthful, extreme per-JD ATS keyword coverage** — not
human-narrative polish. ATS scoring is a keyword-coverage problem (does the
JD's vocabulary appear in the resume, verbatim or near-verbatim, in the
right places), not a storytelling problem, so the pipeline should spend its
tokens there and cut everything that optimizes for human narrative instead
(company-culture research, persona reads, lens-building).

**Truthfulness boundary (non-negotiable):** bullets are still copy-exact
from `resume_builder/experience/*.md` — never fabricate what you *did*.
Skills-section entries may include real, listed-but-undemonstrated skills
(existing "Known Gaps" convention). Nothing in this design changes the
anti-fabrication rule; it changes what's expensive vs. cheap around it.

## Non-goals

- Expanding `SKILL_PROFILE.md` with new freelance/hackathon skills — the
  user will do this themselves, ongoing, outside this project.
- Removing the deep-research path entirely — it moves to a legacy reference
  file, still usable on explicit request for a single high-value
  application, just never auto-selected.

## Design

### 1. Legacy archive

Move the current `make-resume/SKILL.md` content (Phase 0-2, Quick Mode,
mandatory STOP gates, web-research requirement) verbatim to
`resume_builder/legacy/make-resume-full-quick.md`. Not wired into any
skill trigger or `user-invocable` frontmatter — reference-only. Add one
line at the top: "Superseded by Batch Mode (`make-resume/SKILL.md`) for the
autonomous daily loop. Use this only if explicitly asked for a deep-research
pass on a single high-value application."

### 2. `make-resume/SKILL.md` rewritten as Batch Mode only

No mode-selection branch (no "Quick:" prefix, no mode ambiguity) — a single
linear pipeline. Steps:

**Step 0 — Load context (no web search).**
Read: the JD, `config.md` (email, provenance flags, Role-Type Decision
Tree), the matching bundle (`bundle_<lane>.md`), all 3 experience files.
Nothing else. Web research is dropped from the default path entirely —
company-culture framing doesn't move ATS score and was the single biggest
token sink in the old path.

**Step 1 — JD keyword table (~10-15 lines output).**
Extract the top 15-20 ATS terms from the JD (tools, frameworks,
methodologies, domain nouns). Tag each Direct / Bridge / Gap against the
experience files + `skills_taxonomy.md`. This is the one reasoning-heavy
step, kept in full — it drives both bullet selection and the ATS gate
(Step 7). Output stays inline/short, not a full requirements table like the
old Phase 0.

**Step 2 — Lane + bullet selection.**
Lane Selection Decision Tree (`achievement_reframing_guide.md`) picks the
lane. Priority Matrix + Step 1's Direct/Bridge tags pick which bullets.
Bullet text is copy-exact from the experience file (unchanged rule).

**Step 3 — Generate Summary / Skills / bullets.**
Apply the five truthful ATS levers:
- Verbatim JD phrasing for genuinely-possessed skills (translate own
  wording to JD's wording, don't invent capability).
- Reorder by relevance — most JD-relevant bullet leads.
- Dense real coverage — every genuinely-possessed JD-relevant skill in
  `SKILL_PROFILE.md` surfaces somewhere (skills line, bullet, or summary).
- Truthful bridging — a real skill used in a different original context
  gets reframed to the JD's language.
- Honest gap acceptance — a truly-missing hard skill lowers the match rate
  for that JD; never invented to close it.

**Step 4 — Char-count gate.** `python3 resume_builder/helpers/char_count.py`
(existing, unchanged).

**Step 5 — Compile + page gate.** `tectonic -c minimal` + pypdf page-count
check (existing, unchanged).

**Step 6 — Fingerprint gate (new script, see below).**
`python3 resume_builder/helpers/fingerprint_check.py <file>` — pass/fail,
zero LLM reasoning. Replaces the old LLM read-and-eyeball of
`ai_fingerprint_rules.md`.

**Step 7 — ATS coverage gate (new, hard gate).**
Diff Step 1's keyword list against the final resume text (verbatim or
semantic match). Compute match %. Target **>= 75%**.
- If under target: check whether an available-but-unused truthful
  bullet/skill would close the gap; if so, swap it in and recheck.
- If still under target after that check: accept the real number and
  report it plainly — this is a legitimate "borderline fit" signal for
  `daily_scan.md`'s ranking step, not a failure to paper over.
- Never invent a skill or claim to hit the number.

**Step 8 — Condensed critique (~10 lines).**
One pass: "would a human reviewer flag anything obviously wrong" (typos,
inconsistent dates, a bullet that reads oddly out of context) + restate the
Step 7 ATS %. No five-persona sweep, no 8-dimension scoring, no
lens-building, no web research. `critique_framework.md` itself is untouched
and still available for explicit `/critique` calls outside the batch loop.

**Step 9 — Save output.**
Compiled PDF to `output/<Company>/Pratham_Modi_Resume.pdf` (unchanged
naming). Plus one short plain-text note (`output/<Company>/batch_notes.md`):
JD keyword table, final ATS %, any fingerprint fixes applied. No full
session-file scaffolding (`session_file_template.md`'s 8-section format is
part of the legacy path now). No mid-run STOP — this path is for the
autonomous loop.

### 3. `resume_builder/helpers/fingerprint_check.py` (new script)

Modeled on the existing `char_count.py` CLI pattern (reads a `.tex` or
compiled PDF text, prints pass/fail + violations, matches the project's
existing gate-script conventions). Checks, all regex/mechanical — ported
directly from `ai_fingerprint_rules.md`:

- Tier-1 banned word/phrase list (delve, tapestry, multifaceted, pivotal,
  robust-as-filler, seamless(ly), leverage/leveraged-as-verb, boasts,
  showcase(s), "fast-paced/ever-evolving", cutting-edge-as-filler, synergy,
  game-changer, unlock(ing) potential, holistic, paradigm shift) — zero
  hits required.
- Em-dash count — flag if > 2.
- "-ing" analysis-ending scan on bullet lines (regex on line endings before
  the bullet-terminating char).
- Consecutive-bullet same-starting-verb check.

Exit non-zero with a violation list on any failure, matching `char_count.py`'s
existing gate convention so `daily_scan.md` and Batch Mode treat it the same
way as the char-count/compile gates.

### 4. `daily_scan.md` step 5a

Replace the current freehand instruction:

> Build the tailored resume per PLAYBOOK.md → "Resume variant system":
> select the lane bundle..., pull copy-exact bullets..., compile..., verify
> 1-page...

with a direct invocation of the skill:

> Run `/make-resume Batch: <JD path or text>` — this is Batch Mode
> (`make-resume/SKILL.md`), the sole tailoring path. Do not restate its
> steps here; the skill is the single source of truth.

This removes the drift risk between what daily_scan.md describes and what
the skill actually does.

## What's explicitly cut vs. kept

| Old (Full/Quick) | Batch Mode |
|---|---|
| 2-3 mandatory web searches | none |
| 3 mandatory human STOP gates | none (autonomous loop) |
| Full session file, 8 sections, re-read every phase | one short plain-text note |
| `critique_framework.md` full pass (lens + 5 personas + 8-dim scoring) | 10-line condensed pass (human-flag + ATS %) |
| `ai_fingerprint_rules.md` read by LLM each time | `fingerprint_check.py` script gate |
| No ATS-coverage measurement at all (old daily_scan path) | ATS keyword table (Step 1) + hard coverage gate (Step 7), >=75% target |
| Bullet copy-exact, no fabrication | unchanged |
| Char-count / page-fill / compile gates | unchanged (already script-driven) |

## Testing / validation

- Run Batch Mode end-to-end against 2-3 real JDs already in
  `output/job-search/applications.csv`, compare resulting ATS % and
  resume quality against the existing compiled resumes for those same
  companies (Full/Quick-generated).
- Run `fingerprint_check.py` against a handful of already-compiled resumes
  to confirm it flags the same issues the LLM-eyeball process caught
  historically (spot-check against `ai_fingerprint_rules.md`'s own
  checklist).
- Confirm `daily_scan.md`'s step 5a invocation actually triggers
  `make-resume/SKILL.md` correctly (no orphaned Quick-mode references
  left elsewhere in PLAYBOOK.md or CLAUDE.md that could cause an executing
  LLM to look for the old mode).
