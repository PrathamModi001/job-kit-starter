# Configuration

> Claude fills this in during first-run onboarding. Every skill reads this file.

---

## Personal Info

- **Name:** Pratham Modi
- **Degree suffix:** (none)
- **Email:** prathammodi001@gmail.com
- **Phone:** +91-9033393729
- **Location:** Koramangala, Bengaluru, India
- **LinkedIn:** https://www.linkedin.com/in/prathammodii001/
- **GitHub:** https://github.com/PrathamModi001
- **Website:** none
- **Google Scholar:** none
- **ORCID:** none

---

## Preferred Job Platforms
> Sessions persist in browser cookies/profile. NEVER logout accidentally. If sign-in problems or accidental logouts occur, re-authenticate into **prathammodi001@gmail.com** via Google OAuth by clicking the "Sign in with Google" button with the cursor (do NOT sign in via email/password input fields). Use Playwright if running in AGY, or Claude in Chrome (claude-in-chrome) if running in Claude.
- Wellfound
- Instahyre
- Cutshort
- Indeed
- Jobfound — always use this exact filter URL: `https://jobfound.org/?page=0&loc=India&sal=10-20+LPA%2C20-30+LPA&exp=0-1+yr%2C1-3+yrs&work=remote%2Chybrid%2Consite&type=Full-time` (Note: Do NOT login to jobfound board; login is not needed)
- Naukri (Premium subscription — prioritize for profile optimization, better recruiter visibility)

**LinkedIn is excluded as a job-search source by request — never scan/search it for leads.**

---

## Target Roles & Preferences

- **Primary Lanes:** Software Developer · Full-Stack Developer · Node.js Backend Developer (plus distributed systems).
- **Frontend Note & Exclusions:** Exclude frontend-specific / frontend-only roles (e.g., pure Frontend Engineer, UI Developer, React Developer). It is fine if frontend skills are needed as part of a Full-Stack or Software Developer role, but do not focus on frontend-only jobs.
- **Role Exclusions (Experience mismatch):** Exclude **Product Engineer II** (and PE 2) and **Member of Technical Staff (MTS)** — these do not fall under the 0–3 YOE bracket.
- **Stack Exclusions:** Java, .NET/C#, C++, Ruby/Ruby on Rails.
- **Target Locations (Eligible Cities):** Bengaluru (Bangalore), Pune, Mumbai, Hyderabad (Secunderabad), Gurgaon (Gurugram), Ahmedabad, Chennai, or Remote (India).
- **Wellfound Location Prompt Policy:** When Wellfound shows *"This job does not support the locations on your profile. Update your location preferences: I am currently in… / I can relocate to… [Location]"*, if the location shown/dropdown matches our Target Locations list above, click **"I can relocate to…"**, select the matching location, update/confirm, and proceed with the application note. Otherwise, skip the role.

---

## Application-Form Facts (reused constantly — collect once during onboarding)

- **Current CTC / salary:** 12 LPA
- **Expected CTC we quote on forms:** 18–20 LPA (floor 18 LPA, target 20 LPA)
- **Home address (for ATS forms):** 395 5th Avenue, Teachers Colony, Koramangala, Bengaluru
- **Citizenship / passport:** India (Indian passport)
- **Needs sponsorship in home country:** no
- **Notice period:** Immediate
- **Date of birth:** 23/01/2003
- **Gender (voluntary-disclosure forms):** Male
- **Background checks:** OK
- **Email signature for outreach:** Best, / Pratham Modi / prathammodi001@gmail.com

---

## Document Preferences

- **Resume pages:** 1
- **CV pages:** n/a (industry-only)
- **Resume bullet variant:** 2L default
- **Skills config (resume):** matches base LaTeX resume grouping (Languages / Backend / Frontend / Databases / Messaging / AI-ML / Cloud-DevOps-Observability / Architecture)
- **Immigration line:** no
- **Template:** `resume_builder/templates/swe_resume_template.tex` — THE only template for this project. Do NOT use `resume_template.tex`, `resume.cls`, `cv_template.tex`, or `cv.cls` — those are unmodified academic-CV scaffolding from the original kit (publications section, mhchem, protein-engineering example) and do not apply here.
- **`resume_builder/templates/base_resume_reference.tex`** — a REFERENCE-ONLY copy of the actual, real, previously-used base resume (not a template to compile from or edit). It exists purely as ground truth for facts/wording if a KB file (`experience/*.md`) ever looks incomplete. All its bullet content is already reflected in `resume_builder/experience/*.md` — do not copy from this file directly, copy from the experience files.
- **Bullet generation policy:** COPY-EXACT, not fresh-write. See `resume_builder/support/achievement_reframing_guide.md` — Bullet Generation Policy. This overrides the "write bullets FRESH per JD" instruction in `resume_reference.md`, which was written for an academic CV/paper-extraction workflow that doesn't apply to this 2-job profile.

---

## Role Types → Bundle Mapping

> Read by `/make-resume` Phase 0 to pick the matching bundle. See
> `resume_builder/support/achievement_reframing_guide.md` — Lane Selection
> Decision Tree — for the full JD-to-lane matching rules.

| Role Type | Bundle File |
|---|---|
| Backend / Node.js / Distributed Systems (primary lane) | `resume_builder/bundles/bundle_backend.md` |
| Full-Stack (primary lane) | `resume_builder/bundles/bundle_fullstack.md` |
| AI / Agentic Systems (bonus fit, not primary) | `resume_builder/bundles/bundle_ai.md` |

**FIXED sections** (never regenerated per JD — copy verbatim from `swe_resume_template.tex` FIXED markers): Header (name/email/phone/GitHub/LinkedIn), Education, position company/title/dates lines.

---

## Provenance Flags

> Anything here constrains what resumes may claim. Fill honestly.

- **Publications actually under review:** none. Published: paper at INDIACom 2024 (IEEE Xplore: https://ieeexplore.ieee.org/document/10498330/) — title/author-position not yet confirmed, see SKILL_PROFILE.md Publications.
- **Internal tools (NOT peer-reviewed / NOT public):** C3iHub LMS platform, IITK hackathon platform, Playpower AI tutoring platform — employer-owned production systems, not public/open-source.
- **Shared/team work (use hedged verbs):** none flagged yet — confirm if any C3iHub/Playpower work was team-shared vs. solely owned before claiming full-ownership verbs.
