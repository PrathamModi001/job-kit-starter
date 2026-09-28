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

## Step 0: Run the deterministic tailoring pass

```bash
python3 resume_builder/helpers/tailor_resume.py --jd <JD file path> --company "<Company>" --out-dir output/<FolderName>
```

This writes a draft `output/<FolderName>/e2e_<name>_resume.tex` and
`output/<FolderName>/keyword_table.json` with 0 LLM tokens — bullet/tagline/skills
selection already applied per the matching lane's bundle rules.

Then read, and nothing else:
1. `output/<FolderName>/e2e_<name>_resume.tex` (the draft)
2. `output/<FolderName>/keyword_table.json` (Direct/Bridge keyword table + coverage %)
3. `resume_builder/support/achievement_reframing_guide.md` — Bullet Generation Policy
   and the five tailoring levers (needed for Step 3's review pass)
4. `resume_builder/support/skills_taxonomy.md` — the source the resume
   template's Skills section is built from (needed to fill in the draft's
   empty skill-lists in Step 3)
5. `SKILL_PROFILE.md` — grounds Step 1's Gap-tag review ("genuinely absent
   from `SKILL_PROFILE.md`") and Step 3 lever 3's "every genuinely-possessed,
   JD-relevant skill" enumeration in an actual file, not model recall

**Fallback (only if `keyword_table.json`'s `coverage_pct` is below 75%):** read the
relevant `resume_builder/experience/experience_*.md` file in full to look for a
truthful bullet swap the script's tag-overlap heuristic missed, per Step 6.

Create output folder: `JDs/JD_Acme.txt` → `output/Acme/` (`mkdir -p output/<FolderName>/`) — the script's `--out-dir` already does this, so this is a no-op if the script ran first.

---

## Step 1: Review the JD keyword table

`keyword_table.json` already has the Direct/Bridge keyword table and computed
coverage %. Present it as the compact table (same format as before). If a term looks
mis-tagged (e.g. a Gap the script missed, or a Bridge term that's actually a hard Gap
given `SKILL_PROFILE.md`), correct it here — this is the review checkpoint, not a
blind pass-through.

| JD Term | Tag | Source (bullet ID or skills-taxonomy entry) |
|---|---|---|
| [term] | Direct/Bridge/Gap | [C1 / PP4 / "listed skill" / "none"] |

This table drives Step 2 (bullet selection) and Step 6 (ATS gate) — keep it,
don't discard it after this step.

---

## Step 2: Review the script's bullet selection

The draft `.tex` already has bullets selected by `tailor_resume.py` (cap rules and
Priority Matrix ranks already respected). Sanity-check: does each selected bullet
genuinely fit this JD better than an unselected one in the same slot? If the script's
coverage % is below 75%, consult the fallback experience-file read from Step 0 and
swap in a stronger truthful bullet for the weakest-fitting slot — copy-exact only, same
rule as always.

Budget (from `achievement_reframing_guide.md` SWE Resume Budget): 4 bullets
Position 1, 3-4 bullets Position 2, 2 projects, 5 skills lines, 3-4 line
summary.

---

## Step 3: Generate Summary / Skills / bullets

This step reviews and polishes the script's draft — it is not a from-scratch
generation. Apply these five levers as edits to what's already in the draft:
1. **Verbatim JD phrasing** — for genuinely-possessed skills, use the JD's
   own wording instead of a personal synonym. This applies only to bullet
   phrasing and skills-line wording — the Tagline and Summary stay
   copy-exact from the bundle (see below) and are not touched by this
   lever.
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

Skills section: the draft's skills groups already have group *names and
order* filled in but empty skill-lists — fill each group's comma-separated
skills from `skills_taxonomy.md`, bolding only tokens that appear in the JD.

Save edits in place to `output/<FolderName>/e2e_<name>_resume.tex` (the
draft `tailor_resume.py` wrote in Step 0).

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
Exit code 0 = pass. Exit code 1 = violations printed. The remedy for a
flagged bullet is **swap, never rewrite**: pick a different copy-exact
bullet for that slot from the same lane's bundle Priority Matrix (Step 2)
that doesn't trip the check, then re-run Step 4 and this gate. Do NOT trim
or rewrite the flagged bullet's tool-token/trailing content to dodge the
gate — that violates the copy-exact rule (e.g. `experience_c3ihub.md`'s
canonical C2 bullet ends "...and Redis caching," which trips the "-ing"
check every time it's used; "Redis caching" is a real tool token and may
not be trimmed or reworded to pass). If no truthful alternate bullet is
available for that slot, this is a known, accepted limitation — treat the
gate as advisory for that specific bullet only, and say so explicitly in
the Step 8 report (never silently ignore the violation).

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
