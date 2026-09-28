# Job Hunt Profile & Operations Rule

> **Before running anything in this file**, read `job-kit-starter/CLAUDE.md` and `job-kit-starter/PLAYBOOK.md` in full. This file is a fast-reference summary; those two files hold the complete resume-tailoring pipeline (`resume_builder/` templates, lane bundles, experience files, `SKILL_PROFILE.md`), the per-ATS form-fill recipes (Workday, SuccessFactors, Naukri, Indeed Smart Apply, Wellfound, etc.), and the anti-fabrication rules this workflow depends on. Do not skip them.

## ✅ SUBMISSION RULE — job applications auto-submit; cold outreach never does
Canonical source: `job-kit-starter/CLAUDE.md` → "outbound submission policy" and "Mandatory Tailored Resume" rules. Read those in full before triaging or applying — do not rely on a stale summary here. One reminder specific to this file: if a role is ambiguous, requires subjective essays, or fails the candidate bar, skip or flag for manual review rather than guessing.

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
- **Website:** https://prathammodi001.github.io/prathammodi/ | **X/Twitter:** https://x.com/PrathamModii

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
- **Step-by-step scan/rank/apply procedure (sources, recency window, `NUM_JOBS`/Smart-Apply-lane accounting, mechanical exclusion check, execution steps, report format):** canonical source is `.agents/workflows/daily_scan.md` — read it in full, do not rely on a stale summary here. This file only adds the "Approved Sources" allowlist above, which `daily_scan.md` points back to.

---

## 📧 Cold Outreach Operations
Canonical procedure: `job-kit-starter/PLAYBOOK.md` → "Phase 4 — Cold email outreach" (tiers, template, deliverability) and `.agents/rules/regression_checklist.md` → "Cold outreach" (mandatory pre-send gate). Read both in full — do not rely on a stale summary here. One fact worth restating because it's easy to get wrong from memory: **always attach the base resume, exact path `job-kit-starter/output/Pratham_Modi_Base_Resume.pdf`** — never a per-company tailored variant for outreach, and never left unattached (Gmail's URL-compose pattern can't carry an attachment — use the Gmail connector's `create_draft` with the PDF base64-encoded into `attachments`).

---

## 🚧 Blocker Handling (fully autonomous — no user check-ins mid-run)
Canonical source: `.agents/workflows/daily_scan.md` step 5g. Read it in full before handling any blocker — do not rely on a stale summary here.

---

## 🔐 Authentication & Session Persistence Rule
Canonical source: `job-kit-starter/CLAUDE.md` → "Authentication, Session Persistence & Auto-Re-login". Read it in full before handling any sign-in issue — do not rely on a stale summary here.
