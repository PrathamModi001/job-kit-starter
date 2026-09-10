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

4. **Triage & Auto-Apply**:
   - Filter strictly against the Candidate Bar: 0–3 YOE, Backend/Full-Stack, 18+ LPA, Bengaluru/Pune/Mumbai/Hyderabad/Gurgaon/Ahmedabad/Remote.
   - For all qualifying BULLSEYE / Strong Match roles:
     - Generate customized 1-page resume `.tex`, compile with `tectonic -c minimal`.
     - Autofill application fields and auto-submit via Playwright.
     - Record application in `job-kit-starter/output/job-search/applications.csv` and trigger `refresh.sh`.
   - Present a full summary report of applied jobs and skipped noise with reasons.
