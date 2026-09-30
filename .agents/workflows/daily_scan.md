---
name: daily-scan
description: Execute the full daily job-search loop end-to-end — scan, rank, tailor resumes, auto-apply, and run cold outreach — fully autonomously, no human involvement mid-run.
---

# Workflow: daily-scan

**Parameters (read from the invocation prompt):**
- `NUM_JOBS` — target number of applications to *successfully submit* (`Status=Applied`) this run. Default 15 if not specified. **Indeed Smart Apply does NOT count against this cap** — see note below. **A `Blocked` lead does NOT consume a `NUM_JOBS` slot either** — see step 4/5 note below.
- `EXCLUDED_PLATFORMS` — comma-separated platforms/boards to skip entirely this run. Default: none.

**Indeed Smart Apply — separate, uncapped lane:** Smart Apply is a one-click resubmission flow (no fresh form fill), so it must still be done for every qualifying Indeed lead found in the scan, but it is tracked with its own count and never eats into `NUM_JOBS`. `NUM_JOBS` is reserved for the harder, form-fill applications (Workday, Greenhouse, Cutshort native modals, WaaS, custom portals, etc.) that actually take meaningful tailoring/fill effort. Still apply the Candidate Bar and mandatory-tailored-resume gate to every Smart Apply submission — being uncapped is not a license to skip fit-screening.

**LinkedIn — exclusion lifted (2026-09-20), treated like Indeed Smart Apply:** LinkedIn is now an approved source for browsing/scanning and applying. LinkedIn Easy Apply is a one-click flow like Smart Apply — same separate, uncapped lane, does not count against `NUM_JOBS`, but every LinkedIn lead (Easy Apply or native) still must clear the Candidate Bar and the mechanical exclusion check in step 5 before applying.

**Before step 1:** read `job-kit-starter/CLAUDE.md` and `job-kit-starter/PLAYBOOK.md` in full, `.agents/rules/job_hunt_profile.md` for the candidate bar, form facts, and submission/outreach rules, and **`.agents/rules/regression_checklist.md`** — every mechanical check in it is mandatory, not advisory, and applies regardless of which lane/tier you're in. CLAUDE.md and PLAYBOOK.md hold the complete resume-tailoring pipeline (`resume_builder/`), the per-ATS form-fill recipes, and the anti-fabrication rules this workflow depends on — do not skip them.

1. **Deduplication Check**:
   - Run `python3 job-kit-starter/check_applied_companies.py job-kit-starter/output/job-search/applications.csv`
     and use its output (one company per line) to skip already-touched companies —
     do not read the full `applications.csv` into context for this check.

2. **Execute Scan Scripts** — only the sources listed in `job_hunt_profile.md` → "Approved Sources" (skip any also matching `EXCLUDED_PLATFORMS`):
   - Run `python job-kit-starter/job_hunt.py` to pull top ATS openings (Ashby, Greenhouse, Lever, YC).
   - Run `python job-kit-starter/job_hunt_india.py` to aggregate fresh Indeed India postings (this script itself only covers Indeed; LinkedIn leads come from the browser feed in step 3, not this script).
   - Run `python job-kit-starter/hn_scan.py` for direct founder/engineering posts.

3. **Check Portal Feeds** — only the sources listed in `job_hunt_profile.md` → "Approved Sources" (skip any also matching `EXCLUDED_PLATFORMS`):
   - If Playwright browser/extension is active, inspect new matches from the past week on Instahyre (`/candidate/opportunities/?matching=true`), Cutshort (`/profile/all-jobs`), Naukri (`jobAge=7` for last 7 days backend/full-stack roles in Bengaluru/remote), jobfound.org, Wellfound, and LinkedIn jobs search (Bengaluru/remote, backend/full-stack, past week).
   - **LinkedIn is an approved source (exclusion lifted 2026-09-20)** — browse/scan/apply normally, Easy Apply counted in its own separate uncapped lane like Indeed Smart Apply (see param note above).
   - **Authentication:** canonical source is `job-kit-starter/CLAUDE.md` → "Authentication, Session Persistence & Auto-Re-login" (Google OAuth cursor-click re-login; jobfound.org exception) — follow it in full, do not rely on a stale summary here.

4. **Rank & Shortlist**:
   - Triage every new lead strictly against the Candidate Bar in `job_hunt_profile.md`.
   - Score by fit (reuse `job_hunt.py`'s scoring where available) and take only the **top `NUM_JOBS`** leads (default 15) as the initial shortlist. Indeed Smart Apply leads are ranked and shortlisted the same way but sit in their own separate, uncapped bucket (see param note above) — don't let them consume `NUM_JOBS` slots.
   - Log a one-line fit reason for every lead considered, including ones cut for being outside the top `NUM_JOBS`.
   - **`NUM_JOBS` counts `Status=Applied` only, not attempts.** If a shortlisted lead ends up `Blocked` (step 5h), that slot is still open — pull the next-best qualifying lead from the ranked list (or re-scan for more if the list is exhausted) and keep going until `NUM_JOBS` leads are actually `Applied`, or there are genuinely no more qualifying leads left from this run's sources. Do not stop early and report a `NUM_JOBS=5` run as complete with e.g. 3 Applied + 2 Blocked — that under-delivers the target. Track this from each subagent's one-line return in step 5, not from re-reading `applications.csv`.

5. **Apply — Screen, then Tailor + Submit**, for each of the top `NUM_JOBS` leads (plus
   all qualifying Indeed Smart Apply / LinkedIn Easy Apply leads, tracked separately —
   see param note above). **Dispatch each lead to its own subagent** (see step 5's
   subagent contract below) running the sequence:

   **Dispatch mode — one subagent at a time, never concurrent:** the orchestrator
   dispatches exactly one lead's subagent, waits for its one-line return (Applied /
   Blocked / Skipped), logs it (step i below), and only then dispatches the next lead's
   subagent. Do not fan out multiple subagents in parallel. This is a hard rule, not an
   optimization to skip under time pressure — the browser session (Playwright MCP /
   Chrome Extension CDP bridge) is a single shared resource; concurrent subagents
   compete for the same tab/CDP connection and cause disconnects and lost form state.
   Running subagents sequentially still gets the isolation benefit that matters (each
   lead's personal-info form-filling starts from a fresh, undrifted read of
   `job_hunt_profile.md` instead of an increasingly-long single session) without the
   concurrency hazard.

   **"Shared browser tab" is not a valid reason to skip dispatch.** Each subagent
   opens its own new tab (`tabs_create_mcp` / Playwright `browser_tabs` new) for its
   lead and closes it (or leaves it open per 5h on a blocker) before returning — it
   never reuses a tab another subagent or the orchestrator is holding open. Since
   dispatch is strictly sequential, no two subagents ever touch the CDP connection at
   the same instant regardless of tab count. If you find yourself about to run every
   lead in the main session instead of dispatching, that reasoning is invalid — the
   concurrency/collision risk it's protecting against does not exist under sequential
   dispatch with per-subagent tabs. Dispatch anyway.

   **This is mechanically checked, not self-reported.** Before writing step 7's
   report, run `python3 job-kit-starter/verify_subagent_dispatch.py --date <today>`.
   It reads the raw Antigravity transcript log and counts actual `invoke_subagent`
   tool calls against the leads logged to `applications.csv` for that date — it does
   not trust narration about what happened. Paste its output into the report. A run
   where this script exits non-zero (dispatch count < lead count) must say so plainly
   in the Execution-architecture disclosure — do not omit or soften a FAIL result.

   a. **HARD GATE — mechanical exclusion check, run first, before any tailoring:**
      literally quote the job title and re-check it word-by-word against this list —
      Java, .NET/C#/ASP.NET, C++, Ruby/Ruby on Rails, Senior, Staff, Principal,
      Architect, Lead, SDE 2/II, SDE 3/III, SDE-2, SDE-3, Product Engineer II/PE 2,
      Member of Technical Staff/MTS. Any match anywhere in the title or the JD's
      stated primary stack → do not open the form, log `Status=Skipped` with the
      matched term as the reason, return that status to the orchestrator, done — no
      resume is ever built for this lead.
   b. **Screener check, before tailoring:** from the JD text (or the first form page,
      if reachable without a full fill), check for an explicit hard screener
      disqualifier (e.g. "4+ years required", visa sponsorship required, a
      language/stack requirement missed by 5a's string check). If found, log
      `Status=Skipped` with the reason, return, done.
   c. **Save the JD verbatim before tailoring:** write the complete JD exactly as
      fetched — every requirement/responsibility line, in full — to
      `output/<Company> - <Role>/jd.txt` (the existing convention), prefixed with the
      job posting URL and the date fetched as a header. If the raw page was fetched as
      HTML, also keep `jd.html` alongside it. **A condensed paraphrase or bullet-point
      summary written from memory does NOT satisfy this step** — this is the permanent
      record for later audits (Skipped/exclusion-check decisions included, whenever a
      JD was fetched far enough to make that call), and audits must be able to trust
      it as identical to the live posting at fetch time, since postings get taken down
      or edited later.
   d. **Only now, tailor:** run `/make-resume <JD path or text>` (Batch Mode, now
      backed by `tailor_resume.py` — see `.claude/skills/make-resume/SKILL.md`). It
      saves the compiled PDF to `output/<Company>/e2e_<name>_resume.pdf` and a
      `batch_notes.md` with the ATS match rate — rename/copy the PDF to
      `output/<Company> - <Role>/Pratham_Modi_Resume.pdf` for the apply step.
   e. **HARD GATE:** do not proceed to Submit unless that PDF exists on disk. Never
      submit with a generic/default/cached resume.
   f. Fill the ATS form using the platform-specific recipe in PLAYBOOK.md → "ATS
      recipes". Always replace any pre-selected default resume with the tailored PDF.
      Save any account credentials / TOTP secrets created during signup to
      `output/<Company> - <Role>/account_credentials.txt`. Element discovery follows
      the Playwright evaluate-only rule in PLAYBOOK.md — do not call `browser_snapshot`
      for this.
   g. Click final Submit.
   h. **On any blocker** (image/grid captcha, Cloudflare "Additional Verification
      Required" wall, an unresolvable required field): do not close the tab, do not
      pause. Leave that application exactly where it got stuck in its own browser tab,
      log `Status=Blocked` with the specific reason, return that status. The user
      finishes blocked ones manually later. **This does not fill a `NUM_JOBS` slot** —
      the orchestrator pulls another qualifying lead to replace it.

   The subagent's job ends at 5h — it never touches `applications.csv` itself.
   **Step i (CSV logging) is the orchestrator's job, not the subagent's:** as each
   subagent returns its one-line result, the orchestrator — one lead at a time, in the
   order results arrive, never in parallel — logs that result (Applied / Blocked /
   Skipped, with the actual per-job posting URL, not a generic feed/search URL, and for
   `Applied` rows the subagent's returned `Personal Info Filled` string passed through
   verbatim — never rewritten or filled in by the orchestrator) to `applications.csv`
   via the csv-logger agent, then runs
   `job-kit-starter/tracker/refresh.sh`, before processing the next returned result.
   This keeps all writes to the single-source-of-truth CSV serialized through one
   writer even when multiple per-lead subagents are in flight at once.

   **Subagent dispatch contract:** the orchestrator dispatches one subagent per lead
   with this payload — Company, Role, Job URL, JD text (or fetch instructions),
   output folder path (`output/<Company> - <Role>/`), the paths
   `.agents/workflows/daily_scan.md` (steps 5a-5h), `.agents/rules/job_hunt_profile.md`
   (canonical form facts), `.claude/skills/make-resume/SKILL.md`, and `PLAYBOOK.md`
   → "ATS recipes" (the subagent reads these itself — never paste their contents into
   the payload), and today's date (the subagent has no clock). The subagent runs 5a-5h
   above and returns exactly one line:
   `<Status> | <Company> | <Role> | <Resume path or "-"> | <Req ID or reason> |
   <Personal Info Filled or "-">`. The 6th field is required whenever `Status=Applied`
   — the subagent's own verbatim record of the personal-info values it actually typed
   into the form (`key=value; key=value`, same format the csv-logger agent expects for
   this column), since it's the only party that ever saw the filled form; the
   orchestrator must never reconstruct or blank this field itself. The orchestrator's
   context holds only these one-line returns plus the queue state
   (Pending/Applied/Blocked/Skipped per lead) — it never holds tailoring reasoning,
   browser traces, or compile output. This isolation is deliberate: it's what keeps
   personal-info form-filling accurate at job #10 the same as job #1, since each
   subagent starts from a fresh read of `job_hunt_profile.md` rather than a
   conversation that's drifted across many prior jobs.

6. **Cold Outreach**:
   - Run per `job_hunt_profile.md` → "Cold Outreach Operations": target ~50 drafts/day (5 Tier A bespoke + 45 Tier B templated-with-slots, per PLAYBOOK.md Phase 4 and `output/job-search/outreach/tier_b_template.md`).
   - Source leads from HN (`hn_scan.py` email extraction), funding-news/YC-batch research, `waas_scan.py`, and founder posts — mix sources, don't pull all leads from one channel.
   - Every email needs a `Confidence` tag (Verified/Pattern-guessed) and a plausibility check before drafting — see the HARD rule in `job_hunt_profile.md`.
   - **NEVER auto-send** — draft into Gmail only (via the connector or the Gmail URL draft pattern in PLAYBOOK.md Phase 4), the user hits send themselves. Log every draft to `startups_outreach.csv` (Company, Founder, Email, Confidence, Role Pitch, Subject, Status, Sent Date, Notes, Source, Tier).
   - **Before logging any draft as done**, run `.agents/rules/regression_checklist.md` → "Cold outreach" section in full — this includes calling `get_draft` back to confirm the attachment actually landed (don't trust `create_draft` succeeding) and checking this email's structure against the last few in the batch, not just against a banned-word list.

7. **Report Summary**:
   - Present a structured report: applied roles (with resume path + req ID), blocked leads (with reason + tab left open), skipped noise (with reasons), and cold outreach sent (count by tier + source).
   - **Execution-architecture disclosure (mandatory, every run) — verified, not narrated:**
     include the full stdout of `verify_subagent_dispatch.py` from step 5 above, plus a
     per-lead table with one row per lead logged today and a Y/N column for "subagent
     dispatched" — sourced from the script's `invoke_subagent` count, not from memory of
     what you intended to do. If the script's exit code is non-zero, state the FAIL
     result plainly and give the concrete technical reason dispatch was skipped for
     those leads — a claimed reason must be consistent with the "shared browser tab"
     rule above (i.e. it can't just re-assert the collision risk the sequential-dispatch
     design already rules out).
   - **Token usage disclosure (mandatory, every run):** report total tokens consumed by
     this run, broken down by phase (scan/rank, per-lead apply — per subagent if
     subagents were used, cold outreach, reporting). Source this from the actual
     `gen_metadata` records in the run's own conversation SQLite database(s) under
     `~/.gemini/antigravity-cli/conversations/`, or from whatever real usage/billing
     metadata the runtime exposes — never estimate from memory of turn count or
     approximate context size. If only an estimate is possible, say so explicitly and
     give the method; do not present an estimate as a measured total.
