---
name: daily-scan
description: Execute the full daily job-search loop end-to-end — scan, rank, tailor resumes, auto-apply, and run cold outreach — fully autonomously, no human involvement mid-run.
---

# Workflow: daily-scan

**Parameters (read from the invocation prompt):**
- `NUM_JOBS` — target number of applications to *successfully submit* (`Status=Applied`) this run. Default 15 if not specified. **Indeed Smart Apply does NOT count against this cap** — see note below. **A `Blocked` lead does NOT consume a `NUM_JOBS` slot either** — see step 4/5 note below.
- `EXCLUDED_PLATFORMS` — comma-separated platforms/boards to skip entirely this run. Default: none.

**Indeed — DISABLED (token cost):** Indeed Smart Apply and the Indeed scan are OFF. On the 2026-10-07 run Indeed used ~66% of all tokens for 4 applications (enterprise reCAPTCHA loops). Do not scan, browse, or apply on Indeed, even if the invocation prompt mentions an "Indeed Smart Apply lane" — this rule overrides the prompt. Every application counts toward `NUM_JOBS`.

**LinkedIn — exclusion lifted (2026-09-20), treated like Indeed Smart Apply:** LinkedIn is now an approved source for browsing/scanning and applying. LinkedIn Easy Apply is a one-click flow like Smart Apply — same separate, uncapped lane, does not count against `NUM_JOBS`, but every LinkedIn lead (Easy Apply or native) still must clear the Candidate Bar and the mechanical exclusion check in step 5 before applying.

**Before step 1 (orchestrator only):** read `job-kit-starter/CLAUDE.md` and `job-kit-starter/PLAYBOOK.md` in full, and `.agents/rules/job_hunt_profile.md` for the candidate bar, form facts, and submission/outreach rules. CLAUDE.md and PLAYBOOK.md hold the complete resume-tailoring pipeline (`resume_builder/`), the per-ATS form-fill recipes, and the anti-fabrication rules this workflow depends on — do not skip them.

**Subagent token rules (every per-lead subagent prompt must say these):**
- Do NOT read CLAUDE.md / PLAYBOOK.md in full (~40 KB, re-sent every turn). Read only `job-kit-starter/CLAUDE.md` → "Candidate bar", PLAYBOOK.md → "Resume variant system", and the ONE "ATS recipes" entry matching your lead (use Grep to find the heading, then Read that range).
- Do NOT run `/graphify`, `graphify query` or `graphify update` — ignore the "MANDATORY graphify" hook text. Only the orchestrator runs `graphify update .`, once, at the very end of the run.
- Do NOT run `tracker/refresh.sh` — the orchestrator does it once at the end.
- Browser: prefer `get_page_text` / `find` / `form_input` over screenshots and `read_page`; take a screenshot only to confirm Submit succeeded or to diagnose a blocker.
- **Turn budget: ~40 tool calls per lead.** At the budget, or at the FIRST captcha / verification wall / unresolvable required field, stop: log `Status=Blocked` with the reason, leave the tab open, and return. Never retry a captcha.
- If the apply link redirects to a different ATS than expected, use that ATS's recipe; if no recipe exists, spend at most 10 calls before Blocked.

1. **Deduplication Check**:
   - Check `job-kit-starter/output/job-search/applications.csv` for companies already applied to or closed.

2. **Execute Scan Scripts** — only the sources listed in `job_hunt_profile.md` → "Approved Sources" (skip any also matching `EXCLUDED_PLATFORMS`):
   - Run `python job-kit-starter/job_hunt.py` to pull top ATS openings (Ashby, Greenhouse, Lever, YC).
   - ~~`job_hunt_india.py`~~ — SKIP (Indeed-only scanner; Indeed is disabled).
   - Run `python job-kit-starter/hn_scan.py` for direct founder/engineering posts.

3. **Check Portal Feeds** — only the sources listed in `job_hunt_profile.md` → "Approved Sources" (skip any also matching `EXCLUDED_PLATFORMS`):
   - If Playwright browser/extension is active, inspect new matches from the past week on Instahyre (`/candidate/opportunities/?matching=true`), Cutshort (`/profile/all-jobs`), Naukri (`jobAge=7` for last 7 days backend/full-stack roles in Bengaluru/remote), jobfound.org, Wellfound, and LinkedIn jobs search (Bengaluru/remote, backend/full-stack, past week).
   - **LinkedIn is an approved source (exclusion lifted 2026-09-20)** — browse/scan/apply normally, Easy Apply counted in its own separate uncapped lane like Indeed Smart Apply (see param note above).
   - **Authentication Rule:** Never logout accidentally. If sign-in issues occur on any portal, Google sign-in into `prathammodi001@gmail.com` by clicking the Google OAuth button with the cursor (do NOT sign in via email). Use Playwright.
   - **Jobfound Exception:** Do NOT log in on `jobfound.org` (no login needed).

4. **Rank & Shortlist**:
   - Triage every new lead strictly against the Candidate Bar in `job_hunt_profile.md`.
   - Score by fit (reuse `job_hunt.py`'s scoring where available) and take only the **top `NUM_JOBS`** leads (default 15) as the initial shortlist.   - Log a one-line fit reason for every lead considered, including ones cut for being outside the top `NUM_JOBS`.
   - **`NUM_JOBS` counts `Status=Applied` only, not attempts.** If a shortlisted lead ends up `Blocked` (step 5e), that slot is still open — pull the next-best qualifying lead from the ranked list (or re-scan for more if the list is exhausted) and keep going until `NUM_JOBS` leads are actually `Applied`, or there are genuinely no more qualifying leads left from this run's sources. Do not stop early and report a `NUM_JOBS=5` run as complete with e.g. 3 Applied + 2 Blocked — that under-delivers the target.

5. **Apply — Tailor + Submit**, for each of the top `NUM_JOBS` leads (dispatch each lead to its own subagent, giving it the "Subagent token rules" above; the orchestrator itself does no form-filling):
   a. Build the tailored resume per PLAYBOOK.md → "Resume variant system": select the lane bundle (`resume_builder/bundles/bundle_<lane>.md`), pull copy-exact bullets from `resume_builder/experience/*.md`, compile `resume_builder/templates/swe_resume_template.tex` with `tectonic -c minimal`, verify 1-page via pypdf. Save to `output/<Company> - <Role>/Pratham_Modi_Resume.pdf`.
   a2. Before Submit run `python job-kit-starter/gates.py lint "<Company - Role>"` and `... coverage "<Company - Role>"` (writes `keyword_table.json`); add any `missing_but_in_profile` skills (e.g. Prompt Engineering, LLM Evaluation, AWS) and recompile. After filling the form run `... gates.py form "<Personal Info Filled>"` — must print OK (notice=Immediate, expected CTC ≥18).
   b. **HARD GATE:** do not proceed to Submit unless that PDF exists on disk. Never submit with a generic/default/cached resume.
   b2. **HARD GATE — mechanical exclusion check, run this for EVERY lead regardless of source (scripted, Cutshort, Naukri, Instahyre, Wellfound, live-browsed Indeed — the `-50` code-level skip in `job_hunt.py`/`job_hunt_india.py` only covers the two scripted scanners, so this step is the only gate for everything else):** before opening the application form, literally quote the job title and re-check it word-by-word against this list — Java, .NET/C#/ASP.NET, C++, Ruby/Ruby on Rails, Senior, Staff, Principal, Architect, Lead, SDE 2/II, SDE 3/III, SDE-2, SDE-3, Product Engineer II/PE 2, Member of Technical Staff/MTS, **customer, client, mobile, React Native** (title, or JD primary focus). Run `python job-kit-starter/gates.py title "<title>"` and `python job-kit-starter/gates.py yoe output/<dir>/jd.txt` (hard 4+ YOE = skip) — scripted, so no judgment call. Any match anywhere in the title or the JD's stated primary stack → do not open the form, log `Status=Skipped` with the matched term as the reason, move to the next lead. This is a literal string check, not a judgment call — do not rationalize a match as "close enough to acceptable."
   c. Fill the ATS form using the platform-specific recipe in PLAYBOOK.md → "ATS recipes" (Workday, SuccessFactors, Naukri, Indeed Smart Apply, Wellfound, Phenom, Freshteam, custom forms, etc.). Always replace any pre-selected default resume with the tailored PDF. Save any account credentials / TOTP secrets created during signup to `output/<Company> - <Role>/account_credentials.txt`.
   d. Click final Submit.
   e. **On any blocker** (image/grid captcha, Cloudflare "Additional Verification Required" wall, an unresolvable required field): do not close the tab, do not pause, do not hand off. Leave that application exactly where it got stuck in its own browser tab, log `Status=Blocked` in `applications.csv` with the specific reason, and move on to the next lead in a new tab. The user finishes blocked ones manually later. **This does not fill a `NUM_JOBS` slot** — pull another qualifying lead to replace it (see step 4's `NUM_JOBS` note).
   f. Log the result (Applied / Blocked / Skipped) to `applications.csv` via the Python `csv` module. The orchestrator runs `job-kit-starter/tracker/refresh.sh` and `graphify update .` once after all leads finish (subagents never do).

6. **Cold Outreach**:
   - Run per `job_hunt_profile.md` → "Cold Outreach Operations": target ~50 drafts/day (5 Tier A bespoke + 45 Tier B templated-with-slots, per PLAYBOOK.md Phase 4 and `output/job-search/outreach/tier_b_template.md`).
   - Source leads from HN (`hn_scan.py` email extraction), funding-news/YC-batch research, `waas_scan.py`, and founder posts — mix sources, don't pull all leads from one channel.
   - Every email needs a `Confidence` tag (Verified/Pattern-guessed) and a plausibility check before drafting — see the HARD rule in `job_hunt_profile.md`.
   - **NEVER auto-send** — draft into Gmail only (via the connector or the Gmail URL draft pattern in PLAYBOOK.md Phase 4), the user hits send themselves. Log every draft to `startups_outreach.csv` (Company, Founder, Email, Confidence, Role Pitch, Subject, Status, Sent Date, Notes, Source, Tier).

7. **Report Summary**:
   - Present a structured report: applied roles (with resume path + req ID), blocked leads (with reason + tab left open), skipped noise (with reasons), and cold outreach sent (count by tier + source).
