# Achievement Reframing Guide (SWE Edition)

> Replaces the academic-CV "write bullets FRESH per JD" protocol in
> `resume_reference.md` for this project. For a 2-job, 2-year backend-engineer
> profile, fresh-writing bullets per JD is a hallucination risk, not a benefit —
> the facts are few and precise enough that SELECTION + REORDERING covers all
> genuine JD tailoring. This file is the override; if `resume_reference.md`
> or `make-resume/SKILL.md` conflicts with this file on bullet-writing policy,
> **this file wins for this project.**

---

## Hiring-Manager Audit Findings (2026-09-14) — why these rules exist

Read against 83 real applications and 2 actually-tailored resumes (Wells Fargo,
Avoca). Findings, and the rule each one produced:

1. **C5 (IITK hackathon platform — leadership, 10K+ users, multi-tenant SaaS,
   RBAC) was never used.** It's the strongest differentiation signal in the
   profile and reads as a distinct achievement from the day-to-day backend
   bullets (scale infra vs. platform leadership).
   → **Rule:** C5 defaults to HIGH priority for Backend and Full-Stack lanes.
   Dropping it requires a stated reason in the session file.

2. **Lane-bleed:** an AI-lane tagline/bullet-mix reused for a backend-titled
   JD reads as "AI engineer, not backend engineer" to a backend hiring manager.
   → **Rule:** cap AI/RAG-specific bullets (PP2, PP3) at 1 total for the
   Backend and Full-Stack lanes (`bundle_backend.md`, `bundle_fullstack.md`).
   The tagline's FIRST tool must match the lane, never Python/LangChain for a
   backend/full-stack lane.

3. **TypeScript claimed in Skills, never demonstrated.** A recruiter/ATS keyword
   hit with no supporting bullet doesn't survive a human second look.
   → **Rule:** see Known Gaps below. Never write a bullet claiming TypeScript
   ownership without user confirmation.

4. **IIT Kanpur affiliation is a real credibility signal for Indian recruiters**
   and was intact in existing resumes — keep enforcing it.
   → **Rule:** `experience_c3ihub.md` — company line always "C3iHub, IIT Kanpur" in full.

---

## Bullet Generation Policy (overrides resume_reference.md for this project)

1. Bullets come ONLY from `resume_builder/experience/*.md`, by ID. Copy the
   canonical bullet text verbatim.
2. The only edits allowed to bullet text: trimming a trailing clause to fit
   the 2-line char budget (see `resume_builder/reference/resume_reference.md`
   Character Limits — targets still apply even though the section-by-section
   spec for publications/CV does not). Never touch a number, a tool name, or
   swap a verb to a stronger/weaker ownership level.
3. Where an experience file offers lane variants (e.g. PP1 Variant A/B), pick
   exactly one per the matching bundle — never blend.
4. Tagline and Summary: copy-exact from the matching `bundle_<lane>.md`, minor
   trims only, same rule as bullets.
5. Tool tokens inserted into the tagline MUST come from the bundle's "Approved
   pool" list, which itself only contains tools already in `SKILL_PROFILE.md`.
   Never insert a tool because the JD mentions it if it isn't already a real,
   listed skill.

**If none of the above produces a strong enough match** (e.g. a JD requires a
tool/technology genuinely absent from `SKILL_PROFILE.md`), that is a Gap, not
a reframing problem. Log it plainly in the session file — do not bridge it by
inventing a bullet.

---

## Lane Selection Decision Tree

| If JD title/body says... | Lane | Bundle file |
|---|---|---|
| Backend Engineer, Node.js Developer, Distributed Systems, Platform Engineer, SDE (backend-heavy) | Backend | `resume_builder/bundles/bundle_backend.md` |
| Full-Stack Developer, Software Developer with both frontend (React/Next.js) and backend listed | Full-Stack | `resume_builder/bundles/bundle_fullstack.md` |
| AI Engineer, ML Engineer, LLM/Agent/RAG-focused role | AI (bonus fit only — confirm it still passes the candidate bar in `config.md`) | `resume_builder/bundles/bundle_ai.md` |
| Ambiguous / hybrid JD | Default to Backend lane (primary target per `config.md`), then check if 2+ Full-Stack-lane signals (React/Next.js explicitly required) push it to Full-Stack instead | — |

---

## SWE Resume Budget (overrides `resume_reference.md` Quick Budget Card for this project)

`resume_reference.md`'s Budget Card (20 variable bullets, Content Density "~6 bullets for
1-page") is calibrated for `resume.cls`'s academic layout — it does not match
`swe_resume_template.tex`'s denser, simpler layout. Use these empirically-validated
numbers instead (matches the actually-compiled, 1-page Wells Fargo resume):

- **4 bullets** for Position 1 (most recent), **3-4 bullets** for Position 2 = 7-8 total
- **2 projects**, 1 line each
- **5 Technical Skills lines** (one per group)
- **Summary:** 3-4 lines
- If this overflows 1 page after compile: trim a Position-2 bullet to 3, or drop to 1 project — never shrink font/margins (those are FIXED in the template).

## Known Gaps (truthful — do not paper over)

- **TypeScript:** listed skill, not demonstrated in any bullet. See
  `resume_builder/support/skills_taxonomy.md` for the exact bridge language rule.
- **GraphQL, Terraform:** listed skills, not demonstrated in any bullet. Same
  treatment — list only, never claim project-level ownership in a bullet.
- **No dedicated frontend-only project** in the portfolio (see `bundle_fullstack.md`).
  For heavily frontend-weighted Full-Stack JDs, this is a real ceiling on how
  strong the Full-Stack resume can be — do not fabricate a project to close it.
