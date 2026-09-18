---
name: daily-scan
description: Execute the full daily job-search loop end-to-end — scan, rank, tailor resumes, auto-apply, and run cold outreach — fully autonomously, no human involvement mid-run.
---

# Workflow: daily-scan

**Parameters (read from the invocation prompt):**
- `NUM_JOBS` — max jobs to apply to this run. Default 15 if not specified.
- `EXCLUDED_PLATFORMS` — comma-separated platforms/boards to skip entirely this run. Default: none.

**Before step 1:** read `job-kit-starter/CLAUDE.md` and `job-kit-starter/PLAYBOOK.md` in full, and `.agents/rules/job_hunt_profile.md` for the candidate bar, form facts, and submission/outreach rules. CLAUDE.md and PLAYBOOK.md hold the complete resume-tailoring pipeline (`resume_builder/`), the per-ATS form-fill recipes, and the anti-fabrication rules this workflow depends on — do not skip them.

1. **Deduplication Check**:
   - Check `job-kit-starter/output/job-search/applications.csv` for companies already applied to or closed.

2. **Execute Scan Scripts** — only the sources listed in `job_hunt_profile.md` → "Approved Sources" (skip any also matching `EXCLUDED_PLATFORMS`):
   - Run `python job-kit-starter/job_hunt.py` to pull top ATS openings (Ashby, Greenhouse, Lever, YC).
   - Run `python job-kit-starter/job_hunt_india.py` to aggregate fresh Indeed India postings (LinkedIn excluded — do not add it).
   - Run `python job-kit-starter/hn_scan.py` for direct founder/engineering posts.

3. **Check Portal Feeds** — only the sources listed in `job_hunt_profile.md` → "Approved Sources" (skip any also matching `EXCLUDED_PLATFORMS`):
   - If Playwright browser/extension is active, inspect new matches from the past week on Instahyre (`/candidate/opportunities/?matching=true`), Cutshort (`/profile/all-jobs`), Naukri (`jobAge=7` for last 7 days backend/full-stack roles in Bengaluru/remote), jobfound.org, and Wellfound.
   - **⛔ Never open, scan, or apply via linkedin.com, in any form** — it is explicitly not on the Approved Sources list, even if a company's apply link redirects there; skip that lead instead.
   - **Authentication Rule:** Never logout accidentally. If sign-in issues occur on any portal, Google sign-in into `prathammodi001@gmail.com` by clicking the Google OAuth button with the cursor (do NOT sign in via email). Use Playwright.
   - **Jobfound Exception:** Do NOT log in on `jobfound.org` (no login needed).

4. **Rank & Shortlist**:
   - Triage every new lead strictly against the Candidate Bar in `job_hunt_profile.md`.
   - Score by fit (reuse `job_hunt.py`'s scoring where available) and take only the **top `NUM_JOBS`** leads (default 15) — never apply to more than this in one run.
   - Log a one-line fit reason for every lead considered, including ones cut for being outside the top `NUM_JOBS`.

5. **Apply — Tailor + Submit**, for each of the top `NUM_JOBS` leads:
   a. Build the tailored resume per PLAYBOOK.md → "Resume variant system": select the lane bundle (`resume_builder/bundles/bundle_<lane>.md`), pull copy-exact bullets from `resume_builder/experience/*.md`, compile `resume_builder/templates/swe_resume_template.tex` with `tectonic -c minimal`, verify 1-page via pypdf. Save to `output/<Company> - <Role>/Pratham_Modi_Resume.pdf`.
   b. **HARD GATE:** do not proceed to Submit unless that PDF exists on disk. Never submit with a generic/default/cached resume.
   c. Fill the ATS form using the platform-specific recipe in PLAYBOOK.md → "ATS recipes" (Workday, SuccessFactors, Naukri, Indeed Smart Apply, Wellfound, Phenom, Freshteam, custom forms, etc.). Always replace any pre-selected default resume with the tailored PDF. Save any account credentials / TOTP secrets created during signup to `output/<Company> - <Role>/account_credentials.txt`.
   d. Click final Submit.
   e. **On any blocker** (image/grid captcha, Cloudflare "Additional Verification Required" wall, an unresolvable required field): do not close the tab, do not pause, do not hand off. Leave that application exactly where it got stuck in its own browser tab, log `Status=Blocked` in `applications.csv` with the specific reason, and move on to the next lead in a new tab. The user finishes blocked ones manually later.
   f. Log the result (Applied / Blocked / Skipped) to `applications.csv` via the Python `csv` module and run `job-kit-starter/tracker/refresh.sh`.

6. **Cold Outreach**:
   - Run per `job_hunt_profile.md` → "Cold Outreach Operations": target ~50 sends/day (5 Tier A bespoke + 45 Tier B templated-with-slots, per PLAYBOOK.md Phase 4 and `output/job-search/outreach/tier_b_template.md`).
   - Source leads from HN (`hn_scan.py` email extraction), funding-news/YC-batch research, `waas_scan.py`, and founder posts — mix sources, don't pull all leads from one channel.
   - Every email needs a `Confidence` tag (Verified/Pattern-guessed) and a plausibility check before sending — see the HARD rule in `job_hunt_profile.md`.
   - Send directly (auto-send is authorized for outreach, no draft-staging step). Log every send to `startups_outreach.csv` (Company, Founder, Email, Confidence, Role Pitch, Subject, Status, Sent Date, Notes, Source, Tier).

7. **Report Summary**:
   - Present a structured report: applied roles (with resume path + req ID), blocked leads (with reason + tab left open), skipped noise (with reasons), and cold outreach sent (count by tier + source).
