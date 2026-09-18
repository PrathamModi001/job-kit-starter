## graphify

This project has a knowledge graph at graphify-out/ with god nodes, community structure, and cross-file relationships.

Rules:
- For codebase questions, first run `graphify query "<question>"` when graphify-out/graph.json exists. Use `graphify path "<A>" "<B>"` for relationships and `graphify explain "<concept>"` for focused concepts. These return a scoped subgraph, usually much smaller than GRAPH_REPORT.md or raw grep output.
- If graphify-out/wiki/index.md exists, use it for broad navigation instead of raw source browsing.
- Read graphify-out/GRAPH_REPORT.md only for broad architecture review or when query/path/explain do not surface enough context.
- After modifying code, run `graphify update .` to keep the graph current (AST-only, no API cost).

## 🔐 Authentication, Session Persistence & Auto-Re-login Rule

- **Session Preservation:** NEVER logout accidentally from any job platform, browser session, or portal.
- **Sign-In Recovery Protocol:** Whenever you encounter sign-in problems, expired sessions, or if accidentally logged out:
  - **Target Account:** Sign into the **`prathammodi001@gmail.com`** account.
  - **Method:** Use **Google Sign-In via OAuth** by clicking the "Sign in with Google" / OAuth button with the cursor. **DO NOT** sign in via email/password input fields ("not signin via email").
  - **Tooling:**
    - If running under **AGY (Antigravity)**: Perform OAuth sign-in via **Playwright**.
    - If running under **Claude**: Perform OAuth sign-in via **Claude in Chrome** (`claude-in-chrome`).
- **Exception:** Do **NOT** log in if it is the **jobfound** board (`jobfound.org`) — login is not needed.

## 🎯 Candidate Bar & Role Focus

- **Target Roles:** Software Developer · Full-Stack Developer · Node.js Backend Developer (plus distributed systems / backend engineering).
- **Frontend Note & Role Exclusions:** Exclude frontend-specific / frontend-only roles (e.g. Frontend Engineer, Front-end Developer, UI Developer, React Developer). Also exclude **Product Engineer II** and **Member of Technical Staff (MTS)** — these do not fall under the 0–3 YOE bracket. Having frontend skills as part of a full-stack or software developer role is fine, but do not focus on or apply to frontend-only jobs.
- **Stack Exclusions:** Hard skip Java, .NET/C#/ASP.NET, C++, and Ruby/Ruby on Rails roles.
- **Level & Comp:** 0–3 YOE, CTC target 18–20 LPA (hard floor 18 LPA). Skip 4+ YOE, Senior/Staff/Principal/Architect/Lead titles, Product Engineer II, and Member of Technical Staff.
- **Locations:** India (Bangalore, Pune, Mumbai, Hyderabad, Gurgaon, Ahmedabad, Chennai) or Remote.

## 📁 Single Source of Truth & Canonical CSV Paths (STRICT)

- **Canonical Applications File:** `job-kit-starter/output/job-search/applications.csv` (the single source of truth tracked in git).
- **Canonical Outreach File:** `job-kit-starter/output/job-search/outreach/startups_outreach.csv` (the single source of truth tracked in git).
- **STRICT RULE:** ALWAYS read from and write ONLY to the existing files under `job-kit-starter/output/job-search/`. NEVER create or write to a secondary or top-level `output/` directory at the repository root. There must always be exactly ONE `applications.csv` and ONE `startups_outreach.csv`.

## 📄 CRITICAL RULE — Mandatory Tailored Resume for Every Application (STRICT)

- **NEVER reuse a generic base resume or profile default without tailoring.**
- For **EVERY SINGLE APPLICATION** without exception (including 1-click apply, Indeed Smart Apply, Cutshort, and ATS portals):
  1. **Identify Lane & Tailor Variant:** Analyze the target JD keywords/tech stack and select the appropriate resume variant (Backend, AI/ML, Platform, Full-Stack).
  2. **Compile Tailored PDF:** Copy the base `.tex` into `output/<Company> - <Role>/`, adjust the header tagline and summary paragraph, and compile using `tectonic -c minimal Pratham_Modi_Resume.tex` (asserting 1-page fit via pypdf).
  3. **Strict Grounding:** Every bullet point, metric, and claim MUST be strictly grounded in `SKILL_PROFILE.md` (never invent numbers, dates, or tools).
  4. **Mandatory File Replacement on Smart Apply / Portals:** On platforms like Indeed Smart Apply or Cutshort where a default profile resume is pre-selected, you MUST click "Upload a resume" / "Replace", select the newly generated `output/<Company> - <Role>/Pratham_Modi_Resume.pdf`, and confirm it is attached before proceeding to screener questions or submission.

