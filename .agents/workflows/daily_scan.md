---
name: daily-scan
description: Execute the full daily job-search loop end-to-end — scan, rank, tailor resumes, auto-apply, and run cold outreach — fully autonomously, no human involvement mid-run.
---

# Workflow: daily-scan

**Indeed is DISABLED (2026-10-07) — overrides every Indeed mention below.** Do not run `job_hunt_india.py`, do not scan or apply on Indeed (Smart Apply included); treat it as part of `EXCLUDED_PLATFORMS` always. Reason: the 2026-10-07 run spent ~110M of 165M tokens on Indeed (7 reCAPTCHA blocks, ~27M per successful application vs ~7M elsewhere). Re-enable only on explicit user request.

**Parameters (read from the invocation prompt):**
- `NUM_JOBS` — target number of applications to *successfully submit* (`Status=Applied`) this run. Default 15 if not specified. **Indeed Smart Apply does NOT count against this cap** — see note below. **A `Blocked` lead does NOT consume a `NUM_JOBS` slot either** — see step 4/5 note below.
- `EXCLUDED_PLATFORMS` — comma-separated platforms/boards to skip entirely this run. Default: none.

**Indeed Smart Apply — separate, uncapped lane:** Smart Apply is a one-click resubmission flow (no fresh form fill), so it must still be done for every qualifying Indeed lead found in the scan, but it is tracked with its own count and never eats into `NUM_JOBS`. `NUM_JOBS` is reserved for the harder, form-fill applications (Workday, Greenhouse, Cutshort native modals, WaaS, custom portals, etc.) that actually take meaningful tailoring/fill effort. Still apply the Candidate Bar and mandatory-tailored-resume gate to every Smart Apply submission — being uncapped is not a license to skip fit-screening.

**LinkedIn — exclusion lifted (2026-09-20), treated like Indeed Smart Apply:** LinkedIn is now an approved source for browsing/scanning and applying. LinkedIn Easy Apply is a one-click flow like Smart Apply — same separate, uncapped lane, does not count against `NUM_JOBS`, but every LinkedIn lead (Easy Apply or native) still must clear the Candidate Bar and the mechanical exclusion check in step 5 before applying.

**Before step 1 (orchestrator only — subagents get `subagent_prompt.py` output instead):** read `job-kit-starter/CLAUDE.md` and `job-kit-starter/PLAYBOOK.md` in full, and `.agents/rules/job_hunt_profile.md` for the candidate bar, form facts, and submission/outreach rules. CLAUDE.md and PLAYBOOK.md hold the complete resume-tailoring pipeline (`resume_builder/`), the per-ATS form-fill recipes, and the anti-fabrication rules this workflow depends on — do not skip them.

1. **Deduplication Check**:
   - Check `job-kit-starter/output/job-search/applications.csv` for companies already applied to or closed.

2. **Execute Scan Scripts** — only the sources listed in `job_hunt_profile.md` → "Approved Sources" (skip any also matching `EXCLUDED_PLATFORMS`):
   - Run `python job-kit-starter/job_hunt.py` to pull top ATS openings (Ashby, Greenhouse, Lever, YC).
   - Run `python job-kit-starter/job_hunt_india.py` to aggregate fresh Indeed India postings (this script itself only covers Indeed; LinkedIn leads come from the browser feed in step 3, not this script).
   - Run `python job-kit-starter/hn_scan.py` for direct founder/engineering posts.

3. **Check Portal Feeds** — only the sources listed in `job_hunt_profile.md` → "Approved Sources" (skip any also matching `EXCLUDED_PLATFORMS`):
   - If Playwright browser/extension is active, inspect new matches from the past week on Instahyre (`/candidate/opportunities/?matching=true`), Cutshort (`/profile/all-jobs`), Naukri (`jobAge=7` for last 7 days backend/full-stack roles in Bengaluru/remote), jobfound.org, Wellfound, and LinkedIn jobs search (Bengaluru/remote, backend/full-stack, past week).
   - **LinkedIn is an approved source (exclusion lifted 2026-09-20)** — browse/scan/apply normally, Easy Apply counted in its own separate uncapped lane like Indeed Smart Apply (see param note above).
   - **Authentication Rule:** Never logout accidentally. If sign-in issues occur on any portal, Google sign-in into `prathammodi001@gmail.com` by clicking the Google OAuth button with the cursor (do NOT sign in via email). Use Playwright.
   - **Jobfound Exception:** Do NOT log in on `jobfound.org` (no login needed).

4. **Rank & Shortlist**:
   - **Scripted first (no LLM turns):** after step 2, run `python job-kit-starter/shortlist.py <NUM_JOBS*3>` — it parses the digests, applies the gates (title hard-skips, approved cities, already-applied dedup) and prints the ranked list. Only browse portal feeds (step 3) to top up if this is short.
   - **Dispatch each lead with a small prompt:** `python job-kit-starter/subagent_prompt.py "<Company - Role>" "<apply URL>"` prints a ~7 KB prompt (bar + form facts + only the matching ATS recipe + gate commands). Pass its output as the subagent prompt — do NOT tell subagents to read CLAUDE.md/PLAYBOOK.md in full (44 KB re-read every turn was the biggest token cost). Subagents skip graphify and tracker refresh; the orchestrator does both once at the end.
   - Triage every new lead strictly against the Candidate Bar in `job_hunt_profile.md`.
   - Score by fit (reuse `job_hunt.py`'s scoring where available) and take only the **top `NUM_JOBS`** leads (default 15) as the initial shortlist. Indeed Smart Apply leads are ranked and shortlisted the same way but sit in their own separate, uncapped bucket (see param note above) — don't let them consume `NUM_JOBS` slots.
   - Log a one-line fit reason for every lead considered, including ones cut for being outside the top `NUM_JOBS`.
   - **`NUM_JOBS` counts `Status=Applied` only, not attempts.** If a shortlisted lead ends up `Blocked` (step 5e), that slot is still open — pull the next-best qualifying lead from the ranked list (or re-scan for more if the list is exhausted) and keep going until `NUM_JOBS` leads are actually `Applied`, or there are genuinely no more qualifying leads left from this run's sources. Do not stop early and report a `NUM_JOBS=5` run as complete with e.g. 3 Applied + 2 Blocked — that under-delivers the target.

5. **Apply — Tailor + Submit**, for each of the top `NUM_JOBS` leads (plus all qualifying Indeed Smart Apply leads, tracked separately — see param note above):
   a. Build the tailored resume per PLAYBOOK.md → "Resume variant system": select the lane bundle (`resume_builder/bundles/bundle_<lane>.md`), pull copy-exact bullets from `resume_builder/experience/*.md`, compile `resume_builder/templates/swe_resume_template.tex` with `tectonic -c minimal`, verify 1-page via pypdf. Save to `output/<Company> - <Role>/Pratham_Modi_Resume.pdf`.
   a2. Before Submit run `python job-kit-starter/gates.py lint "<Company - Role>"` and `... coverage "<Company - Role>"` (writes `keyword_table.json`); add any `missing_but_in_profile` skills (e.g. Prompt Engineering, LLM Evaluation, AWS) and recompile. After filling the form run `... gates.py form "<Personal Info Filled>"` — must print OK (notice=Immediate, expected CTC ≥18).
   b. **HARD GATE:** do not proceed to Submit unless that PDF exists on disk. Never submit with a generic/default/cached resume.
   b2. **HARD GATE — mechanical exclusion check, run this for EVERY lead regardless of source (scripted, Cutshort, Naukri, Instahyre, Wellfound, live-browsed Indeed — the `-50` code-level skip in `job_hunt.py`/`job_hunt_india.py` only covers the two scripted scanners, so this step is the only gate for everything else):** before opening the application form, literally quote the job title and re-check it word-by-word against this list — Java, .NET/C#/ASP.NET, C++, Ruby/Ruby on Rails, Senior, Staff, Principal, Architect, Lead, SDE 2/II, SDE 3/III, SDE-2, SDE-3, Product Engineer II/PE 2, Member of Technical Staff/MTS, **customer, client, mobile, React Native** (title, or JD primary focus). Run `python job-kit-starter/gates.py title "<title>"` and `python job-kit-starter/gates.py yoe output/<dir>/jd.txt` (hard 4+ YOE = skip) — scripted, so no judgment call. Any match anywhere in the title or the JD's stated primary stack → do not open the form, log `Status=Skipped` with the matched term as the reason, move to the next lead. This is a literal string check, not a judgment call — do not rationalize a match as "close enough to acceptable."
   c. Fill the ATS form using the platform-specific recipe in PLAYBOOK.md → "ATS recipes" (Workday, SuccessFactors, Naukri, Indeed Smart Apply, Wellfound, Phenom, Freshteam, custom forms, etc.). Always replace any pre-selected default resume with the tailored PDF. Save any account credentials / TOTP secrets created during signup to `output/<Company> - <Role>/account_credentials.txt`.
   d. Click final Submit.
   e0. **Platform circuit-breaker:** if 2 leads on the same platform/ATS hit a captcha or verification wall in this run, stop dispatching leads for that platform for the rest of the run (a run of captchas means the session is flagged) and pull leads from other sources. Subagents are turn-capped (10 turns after a blocker, 40 total without a submit) via `subagent_prompt.py`.
   e. **On any blocker** (image/grid captcha, Cloudflare "Additional Verification Required" wall, an unresolvable required field): do not close the tab, do not pause, do not hand off. Leave that application exactly where it got stuck in its own browser tab, log `Status=Blocked` in `applications.csv` with the specific reason, and move on to the next lead in a new tab. The user finishes blocked ones manually later. **This does not fill a `NUM_JOBS` slot** — pull another qualifying lead to replace it (see step 4's `NUM_JOBS` note).
   f. Log the result (Applied / Blocked / Skipped) to `applications.csv` via the Python `csv` module and run `job-kit-starter/tracker/refresh.sh`.

6. **Cold Outreach**:
   - Run per `job_hunt_profile.md` → "Cold Outreach Operations": target ~50 drafts/day (5 Tier A bespoke + 45 Tier B templated-with-slots, per PLAYBOOK.md Phase 4 and `output/job-search/outreach/tier_b_template.md`).
   - Source leads from HN (`hn_scan.py` email extraction), funding-news/YC-batch research, `waas_scan.py`, and founder posts — mix sources, don't pull all leads from one channel.
   - Every email needs a `Confidence` tag (Verified/Pattern-guessed) and a plausibility check before drafting — see the HARD rule in `job_hunt_profile.md`.
   - **NEVER auto-send** — draft into Gmail only (via the connector or the Gmail URL draft pattern in PLAYBOOK.md Phase 4), the user hits send themselves. Log every draft to `startups_outreach.csv` (Company, Founder, Email, Confidence, Role Pitch, Subject, Status, Sent Date, Notes, Source, Tier).

**Subagent note (token saver):** when a lead is dispatched to its own subagent, the subagent does **not** need to run `/graphify` or `graphify query` — the workflow only touches `output/<dir>/`, `config.md`, `SKILL_PROFILE.md`, `resume_builder/` and the CSV, none of which need graph orientation. Only the main orchestrator runs `graphify update .` once at the end. (This overrides the PreToolUse "MANDATORY graphify" hook text for subagents; tell each subagent in its prompt.)

7. **Report Summary**:
   - Present a structured report: applied roles (with resume path + req ID), blocked leads (with reason + tab left open), skipped noise (with reasons), and cold outreach sent (count by tier + source).
