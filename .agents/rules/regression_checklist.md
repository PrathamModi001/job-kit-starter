# Regression Checklist (canonical — every fixed issue lives here, permanently)

> Purpose: a prose fix in one file (a template, a prompt) gets forgotten or
> only applies to the lane it was written for. This file is the single place
> every "this went wrong once, never let it happen again" fix accumulates as
> a **mechanical, boolean check** — not prose to remember, a box to tick.
>
> **Referenced from:** `job-kit-starter/CLAUDE.md` (outbound submission policy),
> `job-kit-starter/PLAYBOOK.md` Phase 4 (cold outreach), `.agents/workflows/daily_scan.md`.
> Any agent running the daily loop or cold outreach MUST run the applicable
> section below before marking work done / logging a CSV row. When you fix a
> new recurring issue, add it here — do not just patch the one file where it
> happened.

---

## Cold outreach (Tier A + Tier B) — run before marking any draft done

- [ ] **Attachment actually present.** After calling `create_draft`, call `get_draft`
  (or equivalent) on the returned draft ID and confirm the `attachments` array is
  non-empty with filename `Pratham_Modi_Base_Resume.pdf`. Do not trust the
  `create_draft` call succeeding as proof the file attached.
  *(Fixed 2026-09-27 — 10 Tier A drafts were logged as "Resume Attached" in
  `startups_outreach.csv` and the run summary, but none of the 10 Gmail drafts
  actually had an attachment when inspected directly.)*
- [ ] **Grep the drafted body** against `resume_builder/support/ai_fingerprint_rules.md`
  Tier-1 banned words — zero hits.
- [ ] **Structural-diversity check across the batch**, not just literal-string dedup.
  Compare this email's skeleton against the last 2-3 sent in the same batch:
  opener style, number of bullets, closer phrasing, subject. If the shape is
  identical and only the company noun/metric changed, rewrite — that reads as
  templated even when no two bodies are byte-identical.
  *(Fixed 2026-09-27 — all 10 "Tier A bespoke" emails in one run shared the
  identical skeleton: generic-flattery opener → 3 metric bullets → "Attached
  is my 1-page base resume and GitHub" → "Would love to discuss X at
  [Company]!" → same sign-off, just nouns swapped. Same underlying issue as
  the 2026-09-20 fix below, recurring in a lane that didn't reference the fix.)*
- [ ] **No fixed/reused closer or subject line within a batch** — see
  `output/job-search/outreach/tier_b_template.md` Closer/Subject rotation rules.
  This applies to Tier A too, not just Tier B.
  *(Fixed 2026-09-20 — hardcoded closer "Attached my tailored 1-page resume
  and pinned GitHub" was templated/AI-sounding; replaced with a rotation rule.
  This is the original fix that the 2026-09-27 regression above slipped past —
  it only lived in `tier_b_template.md`, which Tier A generation never reads.)*
- [ ] **Concrete ask, not vague flattery-close.** The email should name what
  you're looking for or propose a specific next step, not just "would love to
  discuss X."

## Applications (auto-apply loop)

- [ ] **Every touched lead gets a CSV row** — Applied, Skipped, or Blocked —
  even if the application was abandoned mid-form due to a bug/quirk and you
  pivoted to another lead. No touched lead should be untracked.
  *(Fixed 2026-09-27 — a Cardboard/Ashby application was filled out, hit a
  form-validation bug, and was abandoned for another lead; it was never
  logged anywhere in `applications.csv`, leaving no record of a possibly
  half-submitted form.)*
- [ ] **Log the actual per-job posting URL**, not a generic feed/search URL
  (e.g. Instahyre's `/candidate/opportunities/?matching=true`). If you can't
  find the specific posting URL, that's a signal you didn't read the individual
  JD closely enough before applying — go back and get it.
  *(Fixed 2026-09-27 — 3 of 5 Instahyre "Applied" rows in one run logged the
  generic matching-feed URL instead of the specific job posting.)*
- [ ] **Personal-info fields come only from `config.md` canonical facts** —
  never invent a plausible-looking URL/handle for a missing field.
  *(Fixed 2026-09-24 — Website/X-Twitter fields were "none"/missing in
  `config.md`, so the agent fabricated URLs during autonomous form-fill.)*
- [ ] **Titles containing "Founding"/"Founder [Role]"** are a soft-skip signal
  for a 0-3 YOE candidate even though they don't match the literal
  SDE-2/MTS/"II" hard-skip regex — flag for a second look rather than
  auto-applying.
  *(Flagged 2026-09-27 — "Founding Platform Engineer" cleared the mechanical
  title check but is the kind of role the Candidate Bar's spirit, not its
  literal regex, is meant to catch.)*
- [ ] **AI/ML-labeled roles stay a bonus lane, not primary.** Cap them to
  roughly 1 of every 5 application slots in a run — the Candidate Bar says
  "bonus fit, not primary," and it's easy for a matching feed's own ranking
  to quietly skew a whole batch toward them.
  *(Flagged 2026-09-27 — 2 of 5 slots in one run went to AI-labeled roles.)*

---

## How to add a new entry

1. State the rule as a checkbox someone can mechanically verify (not "be more
   careful" — "grep for X" / "check field Y is non-empty").
2. Add a one-line **why**, dated, describing the concrete incident.
3. If the old fix lived in a lane-specific file (a template, one workflow step),
   note that here explicitly so the next reader knows *why* it didn't generalize.
