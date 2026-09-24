# Job Hunt Profile & Operations Rule

> **Before running anything in this file**, read `job-kit-starter/CLAUDE.md` and `job-kit-starter/PLAYBOOK.md` in full. This file is a fast-reference summary; those two files hold the complete resume-tailoring pipeline (`resume_builder/` templates, lane bundles, experience files, `SKILL_PROFILE.md`), the per-ATS form-fill recipes (Workday, SuccessFactors, Naukri, Indeed Smart Apply, Wellfound, etc.), and the anti-fabrication rules this workflow depends on. Do not skip them.

## ✅ SUBMISSION RULE — job applications auto-submit; cold outreach never does
- **Job applications:** you ARE explicitly authorized to automatically submit and complete ATS applications on behalf of Pratham Modi when a role clears the Candidate Bar (BULLSEYE or Strong Match). Automatically tailor the resume, compile the single-page PDF, fill out native/ATS forms (Workday, Greenhouse, Ashby, Lever, Instahyre, Cutshort, Naukri), and click final SUBMIT.
- **Cold outreach (email/DM):** NEVER auto-send — draft-only, always. See "📧 Cold Outreach Operations" below.
- Log every submitted application immediately to `job-kit-starter/output/job-search/applications.csv` with Status="Applied" and execute `refresh.sh` to update the application tracker.
- If a role is ambiguous, requires subjective essays, or fails the candidate bar, skip or flag for manual review.
- **HARD GATE — resume tailoring is mandatory, not optional:** Never set `Status=Applied` unless a tailored resume PDF actually exists on disk at `output/<Company> - <Role>/Pratham_Modi_Resume.pdf`, built via the full pipeline in PLAYBOOK.md → "Resume variant system" (lane bundle selection → copy-exact bullets from `resume_builder/experience/*.md` → compiled `.tex` → verified 1-page PDF). Never submit with the platform's cached/default resume.

---

## 🎯 Candidate Bar (Pratham Modi)
Canonical source: `job-kit-starter/CLAUDE.md` → "Candidate bar" (under "Job-Search Operations Runbook"). Read it in full before triaging any lead — do not rely on a stale summary here.

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
- **Browser (Playwright):** Instahyre, Cutshort, Naukri, jobfound.org, Wellfound, **LinkedIn**.
- **LinkedIn is now an approved browser source** (exclusion lifted by user request 2026-09-20). Browse/scan LinkedIn jobs and apply via native/company "Apply" links normally, subject to the Candidate Bar and the mechanical exclusion check like every other source. **LinkedIn Easy Apply is a separate, uncapped lane — same treatment as Indeed Smart Apply below:** do it for every qualifying LinkedIn lead regardless of `NUM_JOBS` usage, it does not count against `NUM_JOBS`, but it still must clear the Candidate Bar and exclusion checklist first.
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
  4. Platform browser feeds via Playwright: Instahyre (`candidate/opportunities/?matching=true`), Cutshort matches page, Naukri (`jobAge=7` for past 7 days backend/full-stack engineer roles in Bengaluru/remote), and LinkedIn jobs search (Bengaluru/remote, backend/full-stack, past week).
  5. Skip any source/platform listed in the run's `EXCLUDED_PLATFORMS` parameter entirely.
- **Rank & Cap:** Triage every new lead against the Candidate Bar, score by fit (reuse `job_hunt.py`'s scoring), and take only the **top `NUM_JOBS`** leads (default 15, or whatever number is given at run time) — never *complete* more than this many in a single run. Log a one-line fit reason for every lead considered (applied, skipped, or blocked).
- **NUM_JOBS counts `Status=Applied` only — a `Blocked` lead does NOT consume a slot.** `NUM_JOBS` is a target for successfully *submitted* applications, not attempted ones. If a qualifying lead gets blocked (captcha, verification wall, unresolvable field), log it `Status=Blocked` per the Blocker Handling policy below, but pull the next-best qualifying lead to fill that slot instead — keep going until `NUM_JOBS` leads are actually `Applied` (or the qualifying pool for this run's sources is exhausted, whichever comes first). A run that ends with 3 Applied + 2 Blocked when `NUM_JOBS=5` has NOT met the target — it should have kept pulling more leads until 5 were actually submitted.
- **Indeed Smart Apply — separate, uncapped lane:** Smart Apply is a one-click resubmission (no fresh form fill), so it does NOT count against `NUM_JOBS` — do it for every qualifying Indeed lead regardless of how many `NUM_JOBS` slots are already used. `NUM_JOBS` is reserved for form-fill applications that take real tailoring/fill effort (Workday, Greenhouse, Cutshort native, WaaS, custom portals). Smart Apply submissions still must clear the Candidate Bar and the mandatory tailored-resume gate below.
- **Execution & Auto-Submit:**
  - For each of the top `NUM_JOBS` leads:
    1. Tailor the resume via the full pipeline in PLAYBOOK.md → "Resume variant system" (never a bare/generic `.tex`), compile with `tectonic -c minimal`, verify 1-page PDF.
    1b. **HARD GATE — mechanical exclusion check, every lead, every source (not just scripted ones — the code-level `-50` skip in `job_hunt.py`/`job_hunt_india.py` doesn't cover Cutshort/Naukri/Instahyre/Wellfound/live-browsed Indeed):** quote the job title back and check it literally against: Java, .NET/C#/ASP.NET, C++, Ruby/Ruby on Rails, Senior, Staff, Principal, Architect, Lead, SDE 2/II, SDE 3/III, Product Engineer II/PE 2, Member of Technical Staff/MTS. Any match → skip, log `Status=Skipped` with the matched term, do not open the application form. Treat this as a literal string check, not a fit judgment.
    2. Fill application fields via Playwright using the platform-specific recipe in PLAYBOOK.md → "ATS recipes"; replace any pre-selected default resume with the tailored PDF; submit. While filling each personal-info field, note down the exact value you typed/selected — do not paraphrase or infer it afterward from memory.
    3. Append entry to `job-kit-starter/output/job-search/applications.csv` using Python's `csv` module, including the `Personal Info Filled` column: the exact `key=value; key=value` pairs actually entered into that form's personal-info fields (per csv-logger.md). This must reflect what was actually typed on the page, not a copy of the canonical "Application-Form Facts" list above — if a value diverges from that canonical list for any reason, log it as-typed and flag it in `Next step` so it surfaces on audit.
    4. Run `job-kit-starter/tracker/refresh.sh` (or update tracker data).
- **Report Summary:** Present a structured report of applied roles, submitted timestamps, links, blocked leads, and skipped noise with reasons.

---

## 📧 Cold Outreach Operations
- **NEVER auto-send.** Cold emails/DMs are draft-only, always — same rule as CLAUDE.md's outbound submission policy. Draft into Gmail (or the DM composer) and stop; the user hits send themselves. This applies regardless of how the recipient was found (scan digest, cold-outreach research, etc.).
- **Always attach the base resume — exact path: `job-kit-starter/output/Pratham_Modi_Base_Resume.pdf`.** Cold outreach is a general pitch, not tied to a specific JD, so it always uses this one file — never a per-company tailored variant, never left unattached. Since Gmail's URL-compose pattern (`fs=1&tf=cm&to=...`) cannot carry an attachment, draft cold outreach emails via the Gmail connector's `create_draft` (base64-encode this exact PDF into `attachments`), not the URL pattern.
- Two tiers, run together, targeting **~50 drafts/day total** (default split: 5 Tier A bespoke + 45 Tier B templated-with-slots — see PLAYBOOK.md → "Phase 4 — Cold email outreach" and `output/job-search/outreach/tier_b_template.md` for the exact skeleton, subject-line rotation, and pre-approved metric pool).
- Every recipient email must carry a `Confidence` tag (`Verified` or `Pattern-guessed`) in `startups_outreach.csv`, and must clear a plausibility check (team/about page, GitHub commit author, LinkedIn/X bio, or an email-prospecting connector) before drafting. Never draft to a bare guessed address with no corroboration — a bounced or misdirected send is a reputational cost with no upside.
- Log every draft to `job-kit-starter/output/job-search/outreach/startups_outreach.csv` (columns: Company, Founder, Email, Confidence, Role Pitch, Subject, Status, Sent Date, Notes, Source, Tier).
- Deliverability rules from `tier_b_template.md` still apply: no two bodies byte-identical in a batch, rotate subject lines, plain text only (no images/tracking links), mix lead sources (HN, funding news, WaaS, founder posts) rather than pulling all leads from one channel.

---

## 🚧 Blocker Handling (fully autonomous — no user check-ins mid-run)
- On a captcha image/grid challenge, a Cloudflare "Additional Verification Required" wall, or a required field you cannot resolve: **do not close the tab, and do not pause/hand off for input.** Leave that application exactly where it got stuck in its own tab, log the lead as `Status=Blocked` in `applications.csv` with the specific reason, and continue to the next lead in a new tab. The user will finish blocked ones manually later — never abandon a blocked tab by closing it.
- Before clicking final Submit on any ATS form, enumerate all fields still showing an unanswered/required state (e.g. `button[id*=Questionnaire]` still "Select One") — a lack of a visible error does not mean the form is complete.

---

## 🔐 Authentication & Session Persistence Rule
Canonical source: `job-kit-starter/CLAUDE.md` → "Authentication, Session Persistence & Auto-Re-login". Read it in full before handling any sign-in issue — do not rely on a stale summary here.
