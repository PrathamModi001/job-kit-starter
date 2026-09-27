# Batch Mode Resume Tailoring — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development
> (recommended) or superpowers:executing-plans to implement this plan task-by-task.
> Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the two existing resume-tailoring paths (expensive Full/Quick
mode, bare-bones `daily_scan.md` step 5a) with a single ATS-first Batch Mode
that's the sole path `/make-resume` and the daily-scan workflow invoke.

**Architecture:** Archive the current deep-research pipeline to a legacy
reference file. Rewrite `make-resume/SKILL.md` as one linear pipeline: JD
keyword extraction → lane/bullet selection → generation → four gates
(char-count, compile, fingerprint, ATS-coverage) → condensed critique → save.
Add a new deterministic `fingerprint_check.py` gate script. Point
`daily_scan.md` step 5a at the skill instead of restating its steps inline.

**Tech Stack:** Markdown skill/workflow files, Python 3 (stdlib `re`,
`argparse` — matches the existing `char_count.py` script, no new
dependencies).

**Spec:** `docs/superpowers/specs/2026-09-27-batch-mode-resume-tailoring-design.md`

## Global Constraints

- Bullets remain copy-exact from `resume_builder/experience/*.md` — never
  fabricate what the candidate did. (Spec: "Truthfulness boundary")
- Batch Mode has no mandatory web search and no mid-run human STOP gates —
  it must run unattended in the autonomous daily loop. (Spec: Step 0, Step 8)
- ATS coverage target is >= 75%; if unreachable truthfully, report the real
  number — never invent a skill to hit it. (Spec: Step 7)
- `fingerprint_check.py` must follow the existing `char_count.py` CLI
  pattern (argparse, single positional file arg, stdlib only, same directory).
- The legacy Full/Quick file must not be wired into any skill trigger or
  `user-invocable` frontmatter — reference-only, never auto-selected.

## Review Focus

- A `.tex` file with zero `\item` bullets (e.g., a malformed/partial compile)
  fed to `fingerprint_check.py` — must not crash, must report cleanly.
  (Task 2 test: `test_run_checks_empty_document`)
- A bullet whose last word ends in the literal letters "ing" but isn't an
  analysis-style verb (e.g., a proper noun like "Spring") — the check is a
  deterministic suffix match, not NLP, so it will flag these too. This is
  an accepted limitation (spec explicitly calls for a "cheap regex/grep
  pass"), but the test must document the behavior explicitly rather than
  leave it implicit, so a future reader doesn't mistake it for a bug.
  (Task 2 test: `test_ing_ending_suffix_match_is_deterministic_not_nlp`)
- Two bullets that start with the same verb but different capitalization
  ("Built" vs "built") — must still be caught (case-insensitive compare).
  (Task 2 test: `test_consecutive_same_verb_case_insensitive`)
- `daily_scan.md` step 5a pointing at a skill invocation that doesn't exist
  yet mid-implementation — Task 4 is ordered after Task 3 so the skill is
  real before the workflow references it.
- Old Quick-Mode/session-file references left dangling elsewhere (PLAYBOOK.md,
  CLAUDE.md) after the rewrite — Task 5 greps for them explicitly.

---

### Task 1: Archive the Full/Quick pipeline to a legacy reference file

**Files:**
- Create: `resume_builder/legacy/make-resume-full-quick.md`
- Read (source content): `.claude/skills/make-resume/SKILL.md` (current version, before Task 3 rewrites it)

**Interfaces:**
- Produces: a standalone reference doc, not wired into any skill — no other task depends on its internal structure, only on it existing at this path.

- [ ] **Step 1: Copy current SKILL.md content into the legacy file with a superseded-by banner**

Run:
```bash
mkdir -p resume_builder/legacy
cp .claude/skills/make-resume/SKILL.md resume_builder/legacy/make-resume-full-quick.md
```

Then edit `resume_builder/legacy/make-resume-full-quick.md` to remove the
`user-invocable: true` frontmatter (this file must never be auto-triggered)
and insert a banner directly below the frontmatter, before the `# /make-resume`
heading:

```markdown
> **Superseded by Batch Mode** (`.claude/skills/make-resume/SKILL.md`) for
> the autonomous daily loop. Use this file only if explicitly asked for a
> deep-research pass (mandatory web search, 8-dimension critique, mandatory
> human confirmation gates) on a single high-value application.
```

The frontmatter should read:
```markdown
---
description: Legacy deep-research resume pipeline (Full/Quick mode) — superseded by Batch Mode, reference only
---
```

- [ ] **Step 2: Verify the legacy file is inert and complete**

Run:
```bash
grep -c "user-invocable" resume_builder/legacy/make-resume-full-quick.md
grep -c "Superseded by Batch Mode" resume_builder/legacy/make-resume-full-quick.md
diff <(tail -n +5 .claude/skills/make-resume/SKILL.md) <(tail -n +8 resume_builder/legacy/make-resume-full-quick.md)
```
Expected: first grep prints `0` (no `user-invocable` line left), second
prints `1`, third `diff` shows no differences (content preserved verbatim
apart from the banner/frontmatter).

- [ ] **Step 3: Commit**

```bash
git add resume_builder/legacy/make-resume-full-quick.md
git commit -m "Archive Full/Quick resume pipeline as legacy reference doc"
```

---

### Task 2: Write `fingerprint_check.py` gate script with tests

**Files:**
- Create: `resume_builder/helpers/fingerprint_check.py`
- Create: `resume_builder/helpers/test_fingerprint_check.py`
- Read (reused functions): `resume_builder/helpers/char_count.py` (`strip_latex`, `extract_items`, `count_em_dashes` — do not duplicate these, import them)

**Interfaces:**
- Consumes: `char_count.strip_latex(raw: str) -> str`, `char_count.extract_items(text: str) -> list[str]`, `char_count.count_em_dashes(text: str) -> int` (all exist already in `char_count.py`, unchanged).
- Produces (for Task 3's SKILL.md to reference as a CLI gate):
  - CLI: `python3 resume_builder/helpers/fingerprint_check.py <tex_file>` — prints a report, exit code `0` on pass, `1` on any violation.
  - Importable: `run_checks(tex_text: str) -> dict` with keys `banned_words` (list[str]), `em_dash_over_limit` (int, 0 if within limit), `ing_endings` (list[tuple[int, str]]), `consecutive_same_verb` (list[tuple[int, int, str]]).
  - `has_violations(results: dict) -> bool`.

- [ ] **Step 1: Write the test file**

Create `resume_builder/helpers/test_fingerprint_check.py`:

```python
#!/usr/bin/env python3
"""Plain-assert tests for fingerprint_check.py. Run directly: python3 test_fingerprint_check.py"""

import fingerprint_check as fc


def test_banned_word_detected():
    found = fc.check_banned_words("Leveraged Kafka to seamlessly scale the pipeline.")
    assert "leverage" in found or "leveraged" in found, found
    assert "seamlessly" in found, found


def test_no_banned_words_clean_text():
    found = fc.check_banned_words(
        "Architected core LMS backend serving 50K+ users using Express.js, MongoDB, Redis, and Socket.IO."
    )
    assert found == [], found


def test_em_dash_over_limit():
    tex = r"\item Sentence one --- with an em-dash. \item Two --- more --- here."
    assert fc.check_em_dash_count(tex) == 3


def test_em_dash_within_limit():
    tex = r"\item Sentence one --- fine. \item Two --- also fine."
    assert fc.check_em_dash_count(tex) == 0


def test_ing_ending_flagged():
    bullets = ["Reduced latency 60% via caching and reducing"]
    flagged = fc.check_ing_endings(bullets)
    assert flagged == [(1, "Reduced latency 60% via caching and reducing")], flagged


def test_ing_ending_suffix_match_is_deterministic_not_nlp():
    # "Spring" ends in the letters "ing" — the check is a plain suffix
    # match (matches ai_fingerprint_rules.md's "cheap regex/grep pass"
    # intent), so a proper noun like this is flagged too. This is an
    # accepted false-positive tradeoff, not a bug — documented here so a
    # future reader doesn't try to "fix" it into an NLP check.
    bullets = ["Migrated the legacy service to Spring"]
    flagged = fc.check_ing_endings(bullets)
    assert flagged == [(1, bullets[0])], flagged


def test_ing_ending_flagged_on_realistic_bullet():
    # last word is "caching", a real analysis-style "-ing" ending per
    # ai_fingerprint_rules.md — must be flagged.
    bullets = ["Cut MongoDB p99 latency from 450ms to 135ms via compound indexing, sharding, and Redis caching"]
    flagged = fc.check_ing_endings(bullets)
    assert flagged == [(1, bullets[0])], flagged


def test_consecutive_same_verb():
    bullets = ["Built the API gateway", "Built the auth service", "Deployed the pipeline"]
    flagged = fc.check_consecutive_same_verb(bullets)
    assert flagged == [(1, 2, "built")], flagged


def test_consecutive_same_verb_case_insensitive():
    bullets = ["Built the API gateway", "built the auth service"]
    flagged = fc.check_consecutive_same_verb(bullets)
    assert flagged == [(1, 2, "built")], flagged


def test_run_checks_empty_document():
    results = fc.run_checks(r"\begin{itemize} \end{itemize}")
    assert results["banned_words"] == []
    assert results["em_dash_over_limit"] == 0
    assert results["ing_endings"] == []
    assert results["consecutive_same_verb"] == []
    assert fc.has_violations(results) is False


def test_run_checks_clean_document_from_real_bullets():
    tex = r"""
    \item Architected core LMS backend serving 50K+ users across microservices using Express.js, MongoDB, Redis, and Socket.IO, sustaining 99.9% uptime at 10,000+ concurrent connections.
    \item Engineered event-driven notification pipeline handling 75K+ daily events at 99.5% delivery reliability using Kafka, BullMQ, and Redis Pub/Sub with consumer-side deduplication.
    """
    results = fc.run_checks(tex)
    assert fc.has_violations(results) is False, results


def test_run_checks_dirty_document_flags_everything():
    tex = r"""
    \item Leveraged a robust, seamless pipeline for reducing
    \item Built the API gateway
    \item Built the auth service --- fast --- reliable --- scalable
    """
    results = fc.run_checks(tex)
    assert fc.has_violations(results) is True
    assert len(results["banned_words"]) > 0
    assert results["em_dash_over_limit"] > 0
    assert len(results["ing_endings"]) > 0
    assert len(results["consecutive_same_verb"]) > 0


if __name__ == "__main__":
    tests = [v for k, v in list(globals().items()) if k.startswith("test_")]
    failed = 0
    for t in tests:
        try:
            t()
            print(f"PASS {t.__name__}")
        except AssertionError as e:
            failed += 1
            print(f"FAIL {t.__name__}: {e}")
    print(f"\n{len(tests) - failed}/{len(tests)} passed")
    raise SystemExit(1 if failed else 0)
```

- [ ] **Step 2: Run the test file to verify it fails (import error — implementation doesn't exist yet)**

Run: `cd resume_builder/helpers && python3 test_fingerprint_check.py`
Expected: `ModuleNotFoundError: No module named 'fingerprint_check'`

- [ ] **Step 3: Write the implementation**

Create `resume_builder/helpers/fingerprint_check.py`:

```python
#!/usr/bin/env python3
"""
Scan a compiled resume .tex file for AI-fingerprint violations:
Tier-1 banned words, em-dash overuse, "-ing" bullet endings, and
consecutive bullets starting with the same verb.

Ports the checklist in resume_builder/support/ai_fingerprint_rules.md
into a deterministic gate script (no LLM read required).

Usage:
  python3 fingerprint_check.py output/Acme/e2e_acme_resume.tex
"""

import re
import sys
import argparse

from char_count import strip_latex, extract_items, count_em_dashes

BANNED_PHRASES = [
    "delve", "tapestry", "multifaceted", "pivotal", "robust", "seamless",
    "seamlessly", "leverage", "leveraged", "boasts", "showcase", "showcases",
    "fast-paced", "ever-evolving", "cutting-edge", "synergy", "game-changer",
    "unlock", "unlocking", "holistic", "paradigm shift",
]

EM_DASH_LIMIT = 2


def check_banned_words(rendered_text):
    """Return the list of Tier-1 banned phrases found (case-insensitive)."""
    lower = rendered_text.lower()
    return [phrase for phrase in BANNED_PHRASES if phrase in lower]


def check_em_dash_count(raw_tex_text):
    """Return the em-dash count if it exceeds the limit, else 0."""
    count = count_em_dashes(raw_tex_text)
    return count if count > EM_DASH_LIMIT else 0


def check_ing_endings(rendered_bullets):
    """Return (1-based index, bullet text) for bullets whose last word ends in 'ing'."""
    flagged = []
    for i, bullet in enumerate(rendered_bullets, 1):
        words = bullet.strip().rstrip('.').split()
        if words and words[-1].lower().endswith('ing'):
            flagged.append((i, bullet))
    return flagged


def check_consecutive_same_verb(rendered_bullets):
    """Return (i, i+1, verb) for consecutive bullets sharing the same first word."""
    flagged = []
    prev_verb = None
    for i, bullet in enumerate(rendered_bullets, 1):
        words = bullet.strip().split()
        verb = words[0].lower() if words else ''
        if verb and verb == prev_verb:
            flagged.append((i - 1, i, verb))
        prev_verb = verb
    return flagged


def run_checks(tex_text):
    """Run all fingerprint checks against raw .tex text."""
    raw_items = extract_items(tex_text)
    rendered_bullets = [strip_latex(item) for item in raw_items]
    full_rendered = ' '.join(rendered_bullets)

    return {
        'banned_words': check_banned_words(full_rendered),
        'em_dash_over_limit': check_em_dash_count(tex_text),
        'ing_endings': check_ing_endings(rendered_bullets),
        'consecutive_same_verb': check_consecutive_same_verb(rendered_bullets),
    }


def has_violations(results):
    return bool(
        results['banned_words']
        or results['em_dash_over_limit']
        or results['ing_endings']
        or results['consecutive_same_verb']
    )


def format_report(results):
    lines = []
    if results['banned_words']:
        lines.append(f"BANNED WORDS: {', '.join(results['banned_words'])}")
    if results['em_dash_over_limit']:
        lines.append(f"EM-DASH COUNT: {results['em_dash_over_limit']} (limit {EM_DASH_LIMIT})")
    for i, bullet in results['ing_endings']:
        lines.append(f'BULLET {i} ENDS IN "-ing": {bullet}')
    for i, j, verb in results['consecutive_same_verb']:
        lines.append(f'BULLETS {i} & {j} BOTH START WITH "{verb}"')
    return '\n'.join(lines) if lines else 'PASS: no fingerprint violations found.'


def main():
    parser = argparse.ArgumentParser(
        description='Scan a resume .tex file for AI-fingerprint violations')
    parser.add_argument('tex_file', help='.tex file to scan')
    args = parser.parse_args()

    with open(args.tex_file) as f:
        tex_text = f.read()

    results = run_checks(tex_text)
    print(format_report(results))
    sys.exit(1 if has_violations(results) else 0)


if __name__ == '__main__':
    main()
```

- [ ] **Step 4: Run the tests to verify they pass**

Run: `cd resume_builder/helpers && python3 test_fingerprint_check.py`
Expected: `12/12 passed`, exit code `0`.

- [ ] **Step 5: Smoke-test the CLI against a real compiled resume**

Run:
```bash
cd resume_builder/helpers
find ../.. -name "*.tex" -path "*output*" | head -1
```
Then, using whatever path that prints (an existing tailored resume already
in `output/`):
```bash
python3 fingerprint_check.py <that path>
echo "exit code: $?"
```
Expected: prints either `PASS: no fingerprint violations found.` or a
specific violation list, with matching exit code (0 or 1) — confirms the
script runs against real project data, not just synthetic test strings.

- [ ] **Step 6: Commit**

```bash
git add resume_builder/helpers/fingerprint_check.py resume_builder/helpers/test_fingerprint_check.py
git commit -m "Add fingerprint_check.py deterministic AI-fingerprint gate script"
```

---

### Task 3: Rewrite `make-resume/SKILL.md` as Batch Mode only

**Files:**
- Modify: `.claude/skills/make-resume/SKILL.md` (full rewrite)

**Interfaces:**
- Consumes: `resume_builder/helpers/char_count.py` (Task-independent, pre-existing), `resume_builder/helpers/fingerprint_check.py` (from Task 2 — must run after Task 2), `resume_builder/support/achievement_reframing_guide.md`, `resume_builder/bundles/bundle_<lane>.md`, `resume_builder/experience/*.md`, `config.md`.
- Produces: the `/make-resume` skill entry point that Task 4's `daily_scan.md` edit will invoke by name — must remain triggered by `user-invocable: true` and the `/make-resume` name, unchanged from today, so no other file needs to change how it's invoked.

- [ ] **Step 1: Replace the full contents of `.claude/skills/make-resume/SKILL.md`**

```markdown
---
description: Generate a tailored, ATS-optimized resume from a JD (Batch Mode — the sole tailoring path)
user-invocable: true
---

# /make-resume

**User input:** `$ARGUMENTS`

Parse `$ARGUMENTS`:
- File path (e.g., `JDs/*.txt`) → read that file for the JD
- Text after the path starting with "Focus:"/"Emphasize:"/"Downplay:" → focus directive
- Empty → ask the user for the JD
- Inline JD text (no file path) → save to `JDs/temp_<company>.txt`, proceed normally
- `Batch:` prefix is accepted but has no effect — this skill has one mode only. It's kept as a no-op so existing callers (e.g. `daily_scan.md`) that pass it don't need special-casing.

This is **Batch Mode** — the only mode. It's built for the autonomous daily
loop: no mandatory web search, no mid-run human confirmation, optimized for
truthful, extreme per-JD ATS keyword coverage over human-narrative polish.
For a deep-research pass on one high-value application (company-culture
research, 5-persona critique, mandatory confirmation gates), use
`resume_builder/legacy/make-resume-full-quick.md` explicitly — it is never
auto-selected.

---

## Safety Rules (ALWAYS ENFORCED)

**Accuracy > Relevance > Impact > ATS > Brevity**

Read `config.md` Provenance Flags before generating any content. Verify every claim against that table.

- Use the email from `config.md` Personal Info in all outputs
- Resume bullets: ALL variable bullets are 2L (this project is resume-only, no CV — see `config.md` Document Preferences)
- Bullets are COPY-EXACT from `resume_builder/experience/` files, selected via the matching
  `resume_builder/bundles/bundle_<lane>.md` Priority Matrix — see
  `resume_builder/support/achievement_reframing_guide.md` Bullet Generation Policy.
  Do NOT write bullet prose from scratch. Never fabricate what the candidate did.
- Skills-section entries may include real, listed-but-not-yet-demonstrated skills (see
  `achievement_reframing_guide.md` Known Gaps) — truthful knowledge, not project-ownership claims.
- Template: `resume_builder/templates/swe_resume_template.tex` ONLY.
- Run `python3 resume_builder/helpers/char_count.py` after each section — the tool is authoritative.

---

## User Input During Execution

If the user provides feedback, corrections, or suggestions at any point:
1. Acknowledge the input immediately
2. If it affects an already-written section: go back, fix it, re-run char count gate
3. Never restart from scratch — resume from current position

---

## Step 0: Load context (no web search, no session file)

Read, and nothing else:
1. The JD (from `$ARGUMENTS`)
2. `config.md` — Provenance Flags, email, Role-Type Decision Tree
3. `resume_builder/support/achievement_reframing_guide.md` — Lane Selection Decision Tree, Bullet Generation Policy, SWE Resume Budget
4. The matching `resume_builder/bundles/bundle_<lane>.md` (pick lane per the Decision Tree; for hybrid JDs, default to Backend, borrowing at most 1-2 HIGH bullets from a secondary lane per the Decision Tree's rule)
5. All 3 experience files: `resume_builder/experience/experience_c3ihub.md`, `experience_playpower.md`, `experience_projects.md`

Create output folder: `JDs/JD_Acme.txt` → `output/Acme/` (`mkdir -p output/<FolderName>/`).

---

## Step 1: JD keyword table

Extract the top 15-20 ATS terms from the JD (tools, frameworks, methodologies,
domain nouns). Tag each **Direct** (already in the experience files/skills
taxonomy) / **Bridge** (a real skill used in a different original context) /
**Gap** (genuinely absent from `SKILL_PROFILE.md`).

Present as a compact table (not a full requirements doc):

| JD Term | Tag | Source (bullet ID or skills-taxonomy entry) |
|---|---|---|
| [term] | Direct/Bridge/Gap | [C1 / PP4 / "listed skill" / "none"] |

This table drives Step 2 (bullet selection) and Step 5 (ATS gate) — keep it,
don't discard it after this step.

---

## Step 2: Lane + bullet selection

Pick bullets per the bundle's Priority Matrix, weighted toward IDs tagged
Direct/Bridge in Step 1's table. Bullet text is copy-exact from the
experience file — the only edits allowed are trimming a trailing clause to
fit the char budget (never touch a number, tool name, or verb).

Budget (from `achievement_reframing_guide.md` SWE Resume Budget): 4 bullets
Position 1, 3-4 bullets Position 2, 2 projects, 5 skills lines, 3-4 line
summary.

---

## Step 3: Generate Summary / Skills / bullets

Apply these five levers, all truthful:
1. **Verbatim JD phrasing** — for genuinely-possessed skills, use the JD's
   own wording instead of a personal synonym.
2. **Reorder by relevance** — the most JD-relevant bullet leads its position.
3. **Dense real coverage** — every genuinely-possessed, JD-relevant skill in
   `SKILL_PROFILE.md` surfaces somewhere (skills line, bullet, or summary),
   not silently dropped for brevity.
4. **Truthful bridging** — a real skill used in a different original context
   gets reframed into the JD's language (still the same real capability).
5. **Honest gap acceptance** — a truly-missing hard skill lowers the match
   rate for this JD. Never invent it to close the gap.

Tagline and Summary: copy-exact from the bundle, minor trims only. Tool
tokens in the tagline must come from the bundle's Approved Pool.

Save `.tex` to `output/<FolderName>/e2e_<name>_resume.tex`.

---

## Step 4: Char-count and compile gates

```bash
python3 resume_builder/helpers/char_count.py -f resume output/<FolderName>/e2e_<name>_resume.tex
```
No OVER violations. Last line of 2L bullets >= 70% fill. Fix before compiling.

```bash
tectonic -c minimal output/<FolderName>/e2e_<name>_resume.tex
python3 -c "import pypdf; print(len(pypdf.PdfReader('output/<FolderName>/e2e_<name>_resume.pdf').pages))"  # must print 1
```
If FAIL on either gate: fix variable content, recompile, re-run both gates.

---

## Step 5: Fingerprint gate (script, not LLM read)

```bash
python3 resume_builder/helpers/fingerprint_check.py output/<FolderName>/e2e_<name>_resume.tex
```
Exit code 0 = pass. Exit code 1 = violations printed — fix the flagged
bullet(s) and re-run Step 4 and this gate.

---

## Step 6: ATS coverage gate (hard gate)

Compare Step 1's keyword list against the final resume text (verbatim or
clear semantic match). Compute match % = (keywords present) / (keywords
extracted).

- **Target: >= 75%.**
- If under target: check whether an available-but-unused truthful
  bullet/skill (from Step 0's full experience files, not just what Step 2
  picked) would close the gap. If so, swap it in, re-run Steps 4-5, recheck.
- If still under target: accept and report the real number — this is a
  legitimate "borderline fit" signal, not a failure to hide. Never invent a
  skill or claim to hit the number.

---

## Step 7: Condensed critique (~10 lines)

One pass, no personas, no scoring dimensions, no web research:
- Would a human reviewer flag anything obviously wrong (typo, inconsistent
  date, a bullet that reads oddly out of context)?
- Restate the Step 6 ATS match %.

If the user wants the full 5-persona/8-dimension critique for this specific
resume, they can run `/critique` separately — `critique_framework.md` is
unchanged and still available on request.

---

## Step 8: Save output and report

Write `output/<FolderName>/batch_notes.md`:
```markdown
# Batch notes: [Company] [Role]

## JD Keyword Table
[Step 1 table]

## ATS Match Rate
[Step 6 result]: X/Y = Z%

## Condensed Critique
[Step 7 output]
```

Report to the user/caller: resume path, ATS match %, any fingerprint fixes
applied, and the one-line critique verdict. No mid-run STOP — proceed
directly to whatever invoked this skill (e.g., `daily_scan.md`'s next step).
```

- [ ] **Step 2: Verify no orphaned references to the removed Full/Quick structure**

Run:
```bash
grep -n "Quick Mode\|MANDATORY STOP\|Web Search (MANDATORY\|session_<name>.md\|Phase 0\|Phase 1\|Phase 2" .claude/skills/make-resume/SKILL.md
```
Expected: no output (all of these belong to the archived Full/Quick
structure and must not appear in the rewritten file).

Run:
```bash
grep -n "fingerprint_check.py\|char_count.py\|JD keyword table\|ATS coverage gate" .claude/skills/make-resume/SKILL.md
```
Expected: each term found at least once — confirms the new gates are wired in.

- [ ] **Step 3: Commit**

```bash
git add .claude/skills/make-resume/SKILL.md
git commit -m "Rewrite make-resume/SKILL.md as single ATS-first Batch Mode pipeline"
```

---

### Task 4: Point `daily_scan.md` step 5a at the skill

**Files:**
- Modify: `.agents/workflows/daily_scan.md` (step 5a only, lines currently reading the freehand tailoring instructions)

**Interfaces:**
- Consumes: `/make-resume` skill from Task 3 (must exist and work before this task, hence ordered after Task 3).

- [ ] **Step 1: Replace step 5a's freehand instructions with a skill invocation**

In `.agents/workflows/daily_scan.md`, replace this text (currently step 5a):

```
   a. Build the tailored resume per PLAYBOOK.md → "Resume variant system": select the lane bundle (`resume_builder/bundles/bundle_<lane>.md`), pull copy-exact bullets from `resume_builder/experience/*.md`, compile `resume_builder/templates/swe_resume_template.tex` with `tectonic -c minimal`, verify 1-page via pypdf. Save to `output/<Company> - <Role>/Pratham_Modi_Resume.pdf`.
```

with:

```
   a. Run `/make-resume <JD path or text>` — this is Batch Mode (`.claude/skills/make-resume/SKILL.md`), the sole tailoring path: JD keyword extraction, lane/bullet selection, generation, char-count/compile/fingerprint/ATS-coverage gates, condensed critique. Do not restate its internal steps here; the skill is the single source of truth. It saves the compiled PDF to `output/<Company>/e2e_<name>_resume.pdf` and a `batch_notes.md` with the ATS match rate — rename/copy the PDF to `output/<Company> - <Role>/Pratham_Modi_Resume.pdf` for the apply step below.
```

- [ ] **Step 2: Verify the edit**

Run:
```bash
grep -n "make-resume\|Resume variant system" .agents/workflows/daily_scan.md
```
Expected: step 5a now references `/make-resume` and no longer restates
"select the lane bundle... pull copy-exact bullets... compile...".

- [ ] **Step 3: Commit**

```bash
git add .agents/workflows/daily_scan.md
git commit -m "Point daily_scan.md step 5a at make-resume Batch Mode instead of inline instructions"
```

---

### Task 5: Cross-file consistency check and end-to-end validation

**Files:**
- Read only: `PLAYBOOK.md`, `CLAUDE.md`, `.claude/skills/make-resume/SKILL.md`, `resume_builder/legacy/make-resume-full-quick.md`
- No files modified unless Step 1 finds a dangling reference, in which case fix it in place.

**Interfaces:** None — this task validates the output of Tasks 1-4, no new interfaces produced.

- [ ] **Step 1: Grep for dangling references to the removed mode structure**

Run:
```bash
grep -rn "Quick Mode\|Quick:" PLAYBOOK.md CLAUDE.md .agents/workflows/daily_scan.md .claude/skills/make-resume/SKILL.md
```
Expected: any hits are either in `resume_builder/legacy/make-resume-full-quick.md`
(fine, it's the archived reference) or absent. If a hit shows up in
`PLAYBOOK.md`/`CLAUDE.md` pointing at the old mode as if it's still live,
edit that line to reference Batch Mode instead, then re-run the grep to confirm.

- [ ] **Step 2: Run the full gate chain against a real JD end-to-end**

Pick any JD file already present under `JDs/` (or a fresh one), then walk
Batch Mode manually to confirm the pipeline as written actually produces a
compiling, gate-passing resume:

```bash
python3 resume_builder/helpers/char_count.py -f resume output/<FolderName>/e2e_<name>_resume.tex
tectonic -c minimal output/<FolderName>/e2e_<name>_resume.tex
python3 -c "import pypdf; print(len(pypdf.PdfReader('output/<FolderName>/e2e_<name>_resume.pdf').pages))"
python3 resume_builder/helpers/fingerprint_check.py output/<FolderName>/e2e_<name>_resume.tex
```
Expected: char-count gate shows no OVER violations, page count prints `1`,
fingerprint check exits 0 (or any flagged violations get fixed and re-run
until it does).

- [ ] **Step 3: Commit any fixes from Step 1**

```bash
git add -A
git commit -m "Fix dangling Quick-Mode references found during Batch Mode rollout validation"
```
(Skip this commit entirely if Step 1 found nothing to fix.)
