---
name: daily-scan
description: Execute the daily multi-channel job scan and triage matches against Pratham Modi's candidate bar
---

# Workflow: daily-scan

1. **Deduplication Check**:
   - Check `job-kit-starter/output/job-search/applications.csv` for companies already applied to or closed.

2. **Execute Scan Scripts**:
   - Run `python job-kit-starter/job_hunt.py` to pull top ATS openings (Ashby, Greenhouse, Lever, YC).
   - Run `python job-kit-starter/job_hunt_india.py` to aggregate fresh LinkedIn & Indeed India postings.
   - Run `python job-kit-starter/hn_scan.py` for direct founder/engineering posts.

3. **Check Portal Feeds**:
   - If Playwright browser/extension is active, inspect new matches from the past week on Instahyre (`/candidate/opportunities/?matching=true`), Cutshort (`/profile/all-jobs`), and Naukri (`jobAge=7` for last 7 days backend/full-stack roles in Bengaluru/remote).
   - **Authentication Rule:** Never logout accidentally. If sign-in issues occur on any portal, Google sign-in into `prathammodi001@gmail.com` by clicking the Google OAuth button with the cursor (do NOT sign in via email). Use Playwright (AGY) or Claude in Chrome (Claude).
   - **Jobfound Exception:** Do NOT log in on `jobfound.org` (no login needed).

4. **Triage & Auto-Apply**:
   - Filter strictly against the Candidate Bar: 0–3 YOE, Backend/Full-Stack, 18+ LPA, Bengaluru/Pune/Mumbai/Hyderabad/Gurgaon/Ahmedabad/Remote. Skip frontend-only / frontend-specific roles (frontend as part of full-stack is fine, but do not focus on frontend-only jobs).
   - For all qualifying BULLSEYE / Strong Match roles:
     - Generate customized 1-page resume `.tex`, compile with `tectonic -c minimal`.
     - Autofill application fields and auto-submit via Playwright.
     - Record application in `job-kit-starter/output/job-search/applications.csv` and trigger `refresh.sh`.
   - Present a full summary report of applied jobs and skipped noise with reasons.
