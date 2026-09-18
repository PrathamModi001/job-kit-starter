# Job Hunt Profile & Operations Rule

> **Before running anything in this file**, read `job-kit-starter/CLAUDE.md` and `job-kit-starter/PLAYBOOK.md` in full. This file is a fast-reference summary; those two files hold the complete resume-tailoring pipeline (`resume_builder/` templates, lane bundles, experience files, `SKILL_PROFILE.md`), the per-ATS form-fill recipes (Workday, SuccessFactors, Naukri, Indeed Smart Apply, Wellfound, etc.), and the anti-fabrication rules this workflow depends on. Do not skip them.

## ✅ SUBMISSION RULE — AUTO-SUBMISSION AUTHORIZED FOR QUALIFYING MATCHES
- You ARE explicitly authorized to automatically submit job applications, send outreach, and complete ATS applications on behalf of Pratham Modi when a role clears the Candidate Bar (BULLSEYE or Strong Match).
- For matching roles: automatically tailor the resume, compile the single-page PDF, fill out native/ATS forms (Workday, Greenhouse, Ashby, Lever, Instahyre, Cutshort, Naukri), and click final SUBMIT.
- Log every submitted application immediately to `job-kit-starter/output/job-search/applications.csv` with Status="Applied" and execute `refresh.sh` to update the application tracker.
- If a role is ambiguous, requires subjective essays, or fails the candidate bar, skip or flag for manual review.
- **HARD GATE — resume tailoring is mandatory, not optional:** Never set `Status=Applied` unless a tailored resume PDF actually exists on disk at `output/<Company> - <Role>/Pratham_Modi_Resume.pdf`, built via the full pipeline in PLAYBOOK.md → "Resume variant system" (lane bundle selection → copy-exact bullets from `resume_builder/experience/*.md` → compiled `.tex` → verified 1-page PDF). Never submit with the platform's cached/default resume.

---

## 🎯 Candidate Bar (Pratham Modi)
- **Profile:** B.Tech CSE (GPA 9.20), ~2 YOE (1y 3m full-time at C3iHub, IIT Kanpur + 9m internship).
- **Target Roles:** Software Developer · Full-Stack Developer · Node.js Backend Developer (plus distributed systems / backend engineering).
- **Role Exclusions / Focus Note:** Exclude frontend-specific / frontend-only roles (e.g., Frontend Engineer, Frontend Developer, UI Developer, React Developer). Also exclude **Product Engineer II** and **Member of Technical Staff (MTS)** as they do not fall under 0–3 YOE. Having frontend requirements as part of a Full-Stack or Software Developer role is fine, but do not focus on or apply to frontend-only jobs.
- **Tech Stack:** Node.js, Express, Python, FastAPI, Kafka, Redis, MongoDB, PostgreSQL, AWS, Microservices, Observability (OpenTelemetry/Prometheus/Grafana), React/Next.js, LangGraph/RAG.
- **Stack Exclusions:** Hard skip Java, .NET/C#/ASP.NET, C++, and Ruby/Ruby on Rails roles.
- **Experience Level:** Postings gated at 0–2 YOE or 0–3 YOE. Skip roles requiring 4+ YOE, Senior/Staff/Principal/Architect/Lead titles, Product Engineer II, and Member of Technical Staff.
- **Location Filter:** Koramangala, Bengaluru, India. Open to Bangalore, Pune, Mumbai, Hyderabad, Gurgaon, Ahmedabad, Chennai, or Remote (India/international-friendly). Skip other locations unless remote.
- **Wellfound Location Prompt Policy:** If Wellfound shows *"This job does not support the locations on your profile. Update your location preferences: I am currently in… / I can relocate to… [Location]"*, if the location in the dropdown matches the allowed list above, select **"I can relocate to…"**, confirm, and proceed with the application note. Otherwise, skip.
- **Compensation:** Current CTC: 12 LPA. Target: 18–20 LPA (Floor: 18 LPA). Skip roles under 18 LPA. High-pay override: 25+ LPA is worth surfacing even outside preferred lanes/cities.
- **Company Types:** Product companies, well-funded startups. Skip IT staffing/services firms and unpaid/commission-only roles.

---

## 📋 Application-Form Facts
- **Full Name:** Pratham Modi
- **Email:** prathammodi001@gmail.com | **Phone:** +91-9033393729
- **Address:** 395 5th Avenue, Teachers Colony, Koramangala, Bengaluru
- **Citizenship:** India (Indian passport, no sponsorship required in India)
- **Notice Period:** Immediate
- **DOB:** 23/01/2003 | **Gender:** Male
- **LinkedIn:** https://www.linkedin.com/in/prathammodii001/ | **GitHub:** https://github.com/PrathamModi001

---

## 🌐 Approved Sources (STRICT allowlist — this is the complete list)
- **Scripted:** `job_hunt.py` (~90 ATS boards: Greenhouse/Ashby/Lever/YC), `job_hunt_india.py` (Indeed India only), `hn_scan.py` (HN "Who is hiring?"), `waas_scan.py` (Work-at-a-Startup).
- **Browser (Playwright):** Instahyre, Cutshort, Naukri, jobfound.org, Wellfound.
- **⛔ LinkedIn is NOT an approved source, in any form.** Never open linkedin.com, never scan/search it for leads, never apply through it, even if a company's "Apply" link redirects there — treat a LinkedIn-only apply path as unavailable and skip the lead. This applies to browsing, scripted scanning, and applying alike. (It was previously described as a `job_hunt_india.py` input — that's stale; the script excludes it and always has.)
- Do not add any source outside this list without the user explicitly approving it first.
- Apply the run's `EXCLUDED_PLATFORMS` parameter on top of this allowlist to skip additional sources for that run only.

## ⚡ Daily Scan Operations
- **Single Sources of Truth (STRICT):**
  - Applications: `job-kit-starter/output/job-search/applications.csv`
  - Founder Cold Outreach: `job-kit-starter/output/job-search/outreach/startups_outreach.csv`
  - **Rule:** These files tracked in git are the ONLY authorized CSV targets. NEVER create or write to a root-level `output/` folder.
- **Daily Scans (Window: Past 7 Days / Last Week)** — only the sources in "Approved Sources" above:
  1. `python job-kit-starter/job_hunt.py` -> `output/job-search/digest.md`
  2. `python job-kit-starter/job_hunt_india.py` (Indeed India — LinkedIn excluded) -> `output/job-search/digest_india.md`
  3. `python job-kit-starter/hn_scan.py` (excludes already-applied)
  4. Platform browser feeds via Playwright: Instahyre (`candidate/opportunities/?matching=true`), Cutshort matches page, and Naukri (`jobAge=7` for past 7 days backend/full-stack engineer roles in Bengaluru/remote).
  5. Skip any source/platform listed in the run's `EXCLUDED_PLATFORMS` parameter entirely.
- **Rank & Cap:** Triage every new lead against the Candidate Bar, score by fit (reuse `job_hunt.py`'s scoring), and take only the **top `NUM_JOBS`** leads (default 15, or whatever number is given at run time) — never apply to more than this in a single run. Log a one-line fit reason for every lead considered (applied, skipped, or blocked).
- **Execution & Auto-Submit:**
  - For each of the top `NUM_JOBS` leads:
    1. Tailor the resume via the full pipeline in PLAYBOOK.md → "Resume variant system" (never a bare/generic `.tex`), compile with `tectonic -c minimal`, verify 1-page PDF.
    2. Fill application fields via Playwright using the platform-specific recipe in PLAYBOOK.md → "ATS recipes"; replace any pre-selected default resume with the tailored PDF; submit.
    3. Append entry to `job-kit-starter/output/job-search/applications.csv` using Python's `csv` module.
    4. Run `job-kit-starter/tracker/refresh.sh` (or update tracker data).
- **Report Summary:** Present a structured report of applied roles, submitted timestamps, links, blocked leads, and skipped noise with reasons.

---

## 📧 Cold Outreach Operations
- Two tiers, run together, targeting **~50 sends/day total** (default split: 5 Tier A bespoke + 45 Tier B templated-with-slots — see PLAYBOOK.md → "Phase 4 — Cold email outreach" and `output/job-search/outreach/tier_b_template.md` for the exact skeleton, subject-line rotation, and pre-approved metric pool).
- Auto-send is authorized for outreach — no draft-staging step required. But every recipient email must carry a `Confidence` tag (`Verified` or `Pattern-guessed`) in `startups_outreach.csv`, and must clear a plausibility check (team/about page, GitHub commit author, LinkedIn/X bio, or an email-prospecting connector) before sending. Never send to a bare guessed address with no corroboration — a bounced or misdirected send is a reputational cost with no upside.
- Log every send to `job-kit-starter/output/job-search/outreach/startups_outreach.csv` (columns: Company, Founder, Email, Confidence, Role Pitch, Subject, Status, Sent Date, Notes, Source, Tier).
- Deliverability rules from `tier_b_template.md` still apply even though sends are direct, not drafts: no two bodies byte-identical in a batch, rotate subject lines, plain text only (no images/tracking links), mix lead sources (HN, funding news, WaaS, founder posts) rather than pulling all leads from one channel.

---

## 🚧 Blocker Handling (fully autonomous — no user check-ins mid-run)
- On a captcha image/grid challenge, a Cloudflare "Additional Verification Required" wall, or a required field you cannot resolve: **do not close the tab, and do not pause/hand off for input.** Leave that application exactly where it got stuck in its own tab, log the lead as `Status=Blocked` in `applications.csv` with the specific reason, and continue to the next lead in a new tab. The user will finish blocked ones manually later — never abandon a blocked tab by closing it.
- Before clicking final Submit on any ATS form, enumerate all fields still showing an unanswered/required state (e.g. `button[id*=Questionnaire]` still "Select One") — a lack of a visible error does not mean the form is complete.

---

## 🔐 Authentication & Session Persistence Rule
- **Never Logout Accidentally:** Do NOT ever log out accidentally from any platform, session, or browser.
- **Sign-In Recovery Protocol:** Whenever encountering sign-in problems, expired sessions, or an accidental logout:
  - **Target Account:** Sign into the **`prathammodi001@gmail.com`** account.
  - **Google OAuth via Cursor Click:** Use Google Sign-In via OAuth by clicking the "Sign in with Google" / OAuth button with the cursor. **DO NOT** sign in by typing credentials into email/password fields ("not signin via email").
  - **Tooling:**
    - When running under **AGY (Antigravity)**: Perform OAuth sign-in via **Playwright**.
    - When running under **Claude**: Perform OAuth sign-in via **Claude in Chrome** (`claude-in-chrome`).
- **Board Exception:** Do **NOT** log in if it is the **jobfound** board (`jobfound.org`) — login is not needed.
