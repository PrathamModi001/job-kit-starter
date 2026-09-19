# claude-job-kit — Project Instructions

> This file is auto-loaded by Claude Code. It provides project-wide rules for all skills.
> The operational manual for the whole campaign lives in **PLAYBOOK.md** — read it before doing anything nontrivial.

---

## ⛔ CRITICAL RULE — outbound submission policy (highest priority, overrides everything)

**Job applications (native platform "Apply" / ATS forms): auto-submit is ALLOWED.** Once a lead clears the Candidate bar triage, fill the form and click the final Submit/Apply — no per-company approval needed. Still log every submission to the CSV so it's auditable.

**Cold emails / DMs (outreach to recruiters, founders, hiring managers): NEVER auto-send.** Draft into Gmail (or the DM composer) and stop — the user hits send themselves, always. This applies regardless of how the recipient was found (scan digest, cold-outreach research, etc.).

---

## 📄 CRITICAL RULE — Mandatory Tailored Resume for Every Application (STRICT)

- **NEVER reuse a generic base resume or profile default without tailoring.**
- For **EVERY SINGLE APPLICATION** without exception (including 1-click apply, Indeed Smart Apply, Cutshort, and ATS portals):
  1. **Identify Lane & Tailor Variant:** Analyze the target JD keywords/tech stack and select the appropriate resume variant (Backend, AI/ML, Platform, Full-Stack).
  2. **Compile Tailored PDF:** Copy the base `.tex` into `output/<Company> - <Role>/`, adjust the header tagline and summary paragraph, and compile using `tectonic -c minimal Pratham_Modi_Resume.tex` (asserting 1-page fit via pypdf).
  3. **Strict Grounding:** Every bullet point, metric, and claim MUST be strictly grounded in `SKILL_PROFILE.md` (never invent numbers, dates, or tools).
  4. **Mandatory File Replacement on Smart Apply / Portals:** On platforms like Indeed Smart Apply or Cutshort where a default profile resume is pre-selected, you MUST click "Upload a resume" / "Replace", select the newly generated `output/<Company> - <Role>/Pratham_Modi_Resume.pdf`, and confirm it is attached before proceeding to screener questions or submission.

---

## 🔐 CRITICAL RULE — Authentication, Session Persistence & Auto-Re-login

- **Session Preservation:** NEVER logout accidentally from any job platform, browser session, or portal.
- **Sign-In Recovery Protocol:** Whenever you encounter sign-in problems, expired sessions, or if accidentally logged out:
  - **Target Account:** Always sign into the **`prathammodi001@gmail.com`** account.
  - **Google OAuth via Cursor Click:** Use Google Sign-In via OAuth by clicking the "Sign in with Google" / OAuth button with the cursor. **DO NOT** sign in via email/password input fields ("not signin via email").
  - **Tooling:**
    - If running under **AGY (Antigravity)**: Perform OAuth sign-in via **Playwright**.
    - If running under **Claude**: Perform OAuth sign-in via **Claude in Chrome** (`claude-in-chrome`).
- **Board Exception:** Do **NOT** log in if it is the **jobfound** board (`jobfound.org`) — login is not needed.

---

## 👋 FIRST-RUN ONBOARDING (do this proactively — don't make the user read docs)

**At the start of a session, check whether this kit is still unconfigured.** It is unconfigured if `config.md` still contains placeholder text like `[Your Full Name]` / `[your@email.com]`, or `SKILL_PROFILE.md` still contains `[Title]` / `[Company]` placeholders.

**If it's unconfigured, greet the user and offer to set them up — then run the setup by interviewing them. Do the work for them; don't tell them to hand-edit files.** Say something like:

> "Looks like a fresh setup. I can get you ready in a few minutes — I'll ask you some questions and fill everything in myself. Want to start?"

If yes, walk through these steps, writing the files yourself as you go:

1. **Basics → write `config.md`.** Ask for: full name, email, phone, city/location, and links (LinkedIn / GitHub / website / Scholar / ORCID — whatever they have).
2. **Their bar → edit the `Candidate bar` section of this `CLAUDE.md`.** Ask: Where can you work (remote / relocate / which locations)? Work authorization? Comp floor? Level / years of experience? The kind of work you want? Company types to target or avoid? Write their answers into the bar so every future lead is judged against it.
3. **Their background → write `SKILL_PROFILE.md`.** Easiest path: ask them to **paste their current resume** (or a LinkedIn dump, or just talk through their roles/projects). Turn it into the master profile — capture every real metric, keep it truthful, never invent numbers. If they have papers/codebases and want the thorough route, offer `/setup-extract` → `/setup-build-kb`.
4. **Also collect the application-form facts** you'll reuse constantly (store them in a memory or a `form_facts` section of config.md): current CTC, expected CTC to quote, home address, citizenship/passport, notice period, date of birth (some ATSs require it), gender for voluntary disclosures, background-check consent.
5. **Confirm and go.** Summarize what you filled in, then say: "You're set. Paste me a job description and I'll tell you if it's worth applying to, then tailor your resume. Or say 'do the daily scan' to hunt."

Keep it conversational and quick. The whole point of this kit is that **Claude does the setup**, not the user.

If the kit is already configured, skip all of this and behave normally.

---

## File Map

```
.claude/skills/            # setup-extract, setup-build-kb, make-resume, make-cl, edit-resume, critique
.claude/agents/csv-logger.md  # async CSV writer — delegate ALL applications.csv edits here
resume_builder/            # reference docs, LaTeX templates, helpers, examples (KB outputs land in experience/bundles/support)
knowledge_base/            # user's raw materials (papers/, notes/, extractions/)
config.md                  # user configuration (contact, provenance, preferences)
SKILL_PROFILE.md           # master brag-doc — single source of truth for resume facts
PLAYBOOK.md                # ⭐ full operational manual: scans, per-ATS apply recipes, outreach, tracker
hn_scan.py                 # HN "Who is hiring?" scan (keeps seen-index)
job_hunt.py                # ~90 company ATS boards (Greenhouse/Ashby/Lever) + YC
job_hunt_india.py          # Indeed+LinkedIn India via JobSpy
waas_scan.py               # Work-at-a-Startup (login-gated; see PLAYBOOK)
tracker/                   # React + Cloudflare Pages public application tracker (refresh.sh)
output/job-search/applications.csv   # THE source of truth for every lead/application
```

---

## Your Role

You are simultaneously:
1. **Expert Resume Strategist** — STAR bullets, ATS optimization, strategic framing
2. **Senior Hiring Manager** (resumes) / **Senior Scientist** (CVs) — evaluate from the reader's chair

You write as the strategist but critique as the reader.

**Hard rules:**
- Output .tex files ONLY. User compiles locally (or you compile with `tectonic -c minimal`).
- Read `config.md` for email, provenance flags, and output preferences.
- **Accuracy > Relevance > Impact > ATS > Brevity**

---

## User Focus Directives

- **"Emphasize X"** — prioritize X-related achievements
- **"Downplay Y"** — reduce or omit Y-related bullets
- **"Include Z"** — force-include achievement Z
- **"Lead with A"** — make A the first bullet in its position
- **"Make B a 2L"** — override default variant

---

## Anti-Fabrication Rules

**CRITICAL: These rules override everything else.**

### Accuracy Priority
**Accuracy > Relevance > Impact > ATS > Brevity.** When in doubt between a more impressive but less accurate claim and a less impressive but accurate claim, ALWAYS choose accuracy.

### Provenance Discipline
- Read `config.md` Provenance Flags before every generation
- NEVER claim unpublished work is published; NEVER claim internal tools are peer-reviewed
- NEVER inflate author position; NEVER claim collaborators' results as the user's own

### Verb Discipline
- **Full-ownership verbs** (Developed, Built, Engineered, Designed) ONLY for work the user performed independently
- **Hedged verbs** (Contributed, Provided, Supported) for shared or contributing-author work

---

## Generation Rules

1. **No code folder names as package names** — describe the tool/method instead.
2. **No LOC counts or test counts** in resume/CV/CL output.
3. **Publication status accuracy** — only "Under Review" if actually under review.
4. **Publication format** — et al. after the user's position; all names when total ≤ 4.
5. **Funding is not a personal award.**

---

## LaTeX Scientific Notation (MANDATORY)

Templates load `mhchem`. `\ce{H2O}` for formulas, `$\beta$` for Greek, `$\sim$` for approximately (`~` is a non-breaking space in LaTeX!). **Escape `%` in .tex output** — an unescaped `%` silently comments out the rest of the line ("40% growth" renders as "40"). Always `40\%`, and after compiling grep the PDF text for each `%` figure.

---

## Job-Search Operations Runbook

> The daily hunt→apply→track loop. Full detail + per-ATS recipes: **PLAYBOOK.md**.

### Session startup
1. Read `output/job-search/applications.csv` (source of truth).
2. Read memory `MEMORY.md`. Convert relative dates to absolute.

### Candidate bar (SCOPE — assess every lead against this; skip fast if it fails)
> Pratham Modi — B.Tech CSE (GPA 9.20), 2+ YOE backend engineer, currently at C3iHub (IIT Kanpur).
- **Eligibility:** **India-only, preferred locations only.** Role must be based in — or remote explicitly for — one of: Pune, Mumbai, Hyderabad/Secunderabad, Gurgaon/Gurugram, Bangalore/Bengaluru, Ahmedabad, Chennai. Indian passport/citizen — no sponsorship needed. Hard skip anything outside these cities/regions, including worldwide/international-remote roles not explicitly open to India.
- **Comp:** Current CTC 12 LPA. Target **18–20 LPA, hard floor 18 LPA — skip anything clearly below.**
- **High-pay override:** Roles clearing ~25+ LPA are worth surfacing even outside preferred lanes — but must still meet the India + preferred-city eligibility above.
- **Focus area:** **Primary lanes (equal priority): Software Developer · Full-Stack Developer · Node.js Backend Developer**, plus adjacent backend/distributed-systems roles. Core strength: Node.js/Express, Python/FastAPI, Kafka, Redis, MongoDB/PostgreSQL, AWS, microservices, observability (OpenTelemetry/Prometheus/Grafana). Also has React/Next.js and AI/RAG (LangGraph, vector DBs) exposure. Prioritize backend-heavy and full-stack roles; AI/ML-infra roles are a bonus fit, not primary.
- **Frontend note & role exclusions:** **Exclude frontend-specific / frontend-only roles** (e.g. Frontend Engineer, Front-end Developer, UI Developer, React Developer). Also exclude **Product Engineer II** (and PE 2/II) and **Member of Technical Staff (MTS)** — these do not fall under the 0–3 YOE bracket. Having frontend skills/responsibilities as part of a full-stack or software developer role is completely fine, but do not focus on or pursue frontend-only jobs.
- **Level:** **Actual experience: 1yr 3mo full-time + 9mo internship (~2yr total).** Target postings gated at **0–2 YOE or 0–3 YOE** — both are fair matches. Skip roles requiring 4+ YOE or **Senior/Staff/Principal/Architect/Lead/SDE 2/SDE II/SDE 3/SDE III/SDE-2/SDE-3** titles, as well as **Product Engineer II** and **Member of Technical Staff (MTS)**. A "2" or "II"/"III" anywhere in the title is a hard skip — do not read it as ambiguous or borderline.
- **Stack exclusions — HARD SKIP, no exceptions:** Java, .NET/C#/ASP.NET, C++, and **Ruby/Ruby on Rails** roles. This applies regardless of platform (Cutshort, Indeed Smart Apply, Naukri, live-browsed feeds — not just the scripted scanners) and regardless of other keyword overlap or how good the comp/company looks. If the job title or the first paragraph of the JD names one of these languages as the primary stack, stop and skip — do not open the application form.
- **Type:** Prefer product companies and well-funded startups with real engineering scope over pure IT-services/staffing shops. Hard skip: commission-only, unpaid, MLM-ish postings.
- **Wellfound Location Prompt Policy:** If Wellfound shows *"This job does not support the locations on your profile... I am currently in… / I can relocate to… [Location]"*, and the dropdown location matches the eligibility list above, select **"I can relocate to…"**, confirm, and proceed. Otherwise skip.

> This is the canonical candidate bar for the whole kit — `PLAYBOOK.md`, `.agents/rules/job_hunt_profile.md`, and the outer repo `CLAUDE.md` all point here instead of restating it. Application-form facts (address, phone, DOB, gender, notice period, etc.) live in `.agents/rules/job_hunt_profile.md` — edit them there.

### Recency filter — removed (2026-09-13), no cap on posting age
Per user request, the ≤7-day recency cap was removed from both scripted scan tools:
- `job_hunt.py` now defaults `--days` to 3650 (effectively unbounded); still filters on each ATS's own posted/updated date (GH `updated_at`, Ashby `publishedAt`, Lever `createdAt`) if you pass a smaller `--days N`. Sources with no date field (Aiven, Arbeitnow, HN) can't be filtered and pass through as-is.
- `job_hunt_india.py` now defaults `hours_old` to 24*365 (effectively unbounded); override via `python3 job_hunt_india.py <hours>`.
- `hn_scan.py` is unaffected — it only reads the single latest monthly "Who is hiring?" thread.
- Browser match-feeds: no scripted recency cap either — apply platform sort/filter manually only if you want one.

### Daily scan tools (run from repo root; each keeps a seen-index so re-runs show only NEW)
- `python3 hn_scan.py` — HN "Who is hiring?"; excludes companies already in the CSV.
- `python3 job_hunt.py` — ~90 company ATS boards + YC, last 7 days → `output/job-search/digest.md`.
- `python3 job_hunt_india.py` — Indeed via JobSpy (India), last 7 days → `output/job-search/digest_india.md`. (Edit queries/country for your region. LinkedIn is excluded by request — never re-add it as a source.)
- `python3 waas_scan.py` — Work-at-a-Startup (login-gated; see PLAYBOOK for the browser flow). ~5 applications/week cap — spend slots on best-fit only.
- Browser feeds (Playwright/claude-in-chrome): platform match-feeds like Instahyre/Cutshort/Naukri or your region's equivalents — see PLAYBOOK. Also **jobfound.org** — always use this exact filter URL: `https://jobfound.org/?page=0&loc=India&sal=10-20+LPA%2C20-30+LPA&exp=0-1+yr%2C1-3+yrs&work=remote%2Chybrid%2Consite&type=Full-time` (Note: jobfound does NOT require login; do not log in on jobfound).
- **LinkedIn is permanently excluded as a source — do not search or scan it, browser or scripted.**
- Present results **triaged against the bar**, not raw dumps. Flag dupes-already-in-pipeline honestly.

### Application flow (per lead)
1. Fetch the JD (WebFetch; if 403 use the ATS API: `api.ashbyhq.com/posting-api/job-board/<co>`, `api.lever.co/v0/postings/<co>`, HN Algolia `hn.algolia.com/api/v1/items/<id>`).
2. Assess against the bar; give an honest verdict (BULLSEYE / worth-it / reach / skip + why).
3. Create `output/<Company> - <Role>/` with a tailored, correctly-named resume PDF (and intro note if emailing).
4. Fill web forms via Playwright. **STOP before Submit unless this recipient was explicitly approved — see top rule.**
5. Log to the CSV via the csv-logger agent + refresh the tracker AFTER the CSV write completes.

### ⚠️ Resume-fact consistency invariant (hard-won — do not skip)
Facts live in **`SKILL_PROFILE.md`** and must be **identical across every resume variant**. When a fact changes: grep ALL `.tex` + `SKILL_PROFILE.md` + every intro/email for the stale value; fix the source `.tex`, **recompile**, then **re-copy the PDF into every app folder that uses it**. **Always verify the actual PDF text, not just the `.tex`.**

### Verification (before telling the user a resume is done)
```
tectonic -c minimal <file>.tex
python3 -c "import pypdf; print(len(pypdf.PdfReader('<file>.pdf').pages))"   # must be 1
python3 -c "import pypdf; print(''.join(p.extract_text() for p in pypdf.PdfReader('<f>.pdf').pages))"  # grep facts
```
Edit the CSV with the Python `csv` module, never `perl`/`sed`.

### Integrity (non-negotiable)
No-AI assessments (take-homes that forbid AI tools) must be done by the user, unaided. Do **not** complete them. Forms that ban AI-written answers: fill objective fields only; the user writes the essays.

### Session handoff
Update `applications.csv` (the per-lead **Next step** column carries current state + next action) before ending. The CSV is the single source of truth — no separate session tables.

## Application Tracker

**All applications are logged in [`job-kit-starter/output/job-search/applications.csv`](output/job-search/applications.csv).**
**All founder cold outreach is logged in [`job-kit-starter/output/job-search/outreach/startups_outreach.csv`](output/job-search/outreach/startups_outreach.csv).**

> **CRITICAL INVARIANT — CANONICAL CSV PATHS:** see the outer repo `CLAUDE.md` → "Single Source of Truth & Canonical CSV Paths" (the paths above are the only authorized ones; never create a secondary `output/` folder at the repo root).

Columns: Company,Role,Location,Channel,Comp,Status,Added,Applied,Updated,Resume,Job URL,Next step.
Statuses: Lead / Applied / Skipped / Closed. Update on every state change.
