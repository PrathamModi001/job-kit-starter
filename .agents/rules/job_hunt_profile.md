# Job Hunt Profile & Operations Rule

## ✅ SUBMISSION RULE — AUTO-SUBMISSION AUTHORIZED FOR QUALIFYING MATCHES
- You ARE explicitly authorized to automatically submit job applications, send outreach, and complete ATS applications on behalf of Pratham Modi when a role clears the Candidate Bar (BULLSEYE or Strong Match).
- For matching roles: automatically tailor the resume, compile the single-page PDF, fill out native/ATS forms (Workday, Greenhouse, Ashby, Lever, Instahyre, Cutshort, Naukri), and click final SUBMIT.
- Log every submitted application immediately to `job-kit-starter/output/job-search/applications.csv` with Status="Applied" and execute `refresh.sh` to update the application tracker.
- If a role is ambiguous, requires subjective essays, or fails the candidate bar, skip or flag for manual review.

---

## 🎯 Candidate Bar (Pratham Modi)
- **Profile:** B.Tech CSE (GPA 9.20), ~2 YOE (1y 3m full-time at C3iHub, IIT Kanpur + 9m internship).
- **Target Roles:** Software Developer · Full-Stack Developer · Node.js Backend Developer (plus distributed systems / backend engineering).
- **Role Exclusions / Focus Note:** Exclude frontend-specific / frontend-only roles (e.g., Frontend Engineer, Frontend Developer, UI Developer, React Developer). Also exclude **Product Engineer II** and **Member of Technical Staff (MTS)** as they do not fall under 0–3 YOE. Having frontend requirements as part of a Full-Stack or Software Developer role is fine, but do not focus on or apply to frontend-only jobs.
- **Tech Stack:** Node.js, Express, Python, FastAPI, Kafka, Redis, MongoDB, PostgreSQL, AWS, Microservices, Observability (OpenTelemetry/Prometheus/Grafana), React/Next.js, LangGraph/RAG.
- **Stack Exclusions:** Hard skip Java, .NET/C#/ASP.NET, C++, and Ruby/Ruby on Rails roles.
- **Experience Level:** Postings gated at 0–2 YOE or 0–3 YOE. Skip roles requiring 4+ YOE, Senior/Staff/Principal/Architect/Lead titles, Product Engineer II, and Member of Technical Staff.
- **Location Filter:** Koramangala, Bengaluru, India. Open to Bangalore, Pune, Mumbai, Hyderabad, Gurgaon, Ahmedabad, Chennai, or Remote (India/international-friendly). Skip other locations unless remote.
- **Wellfound Location Prompt Policy:** If Wellfound shows *"This job does not support the locations on your profile. Update your location preferences: I am currently in… / I can relocate to… [Location]"*, if the location in the dropdown matches the allowed list above, select **"I can relocate to…"**, confirm, and proceed with the application note. Otherwise, skip.
- **Compensation:** Current CTC: 12 LPA. Target: 18–20 LPA (Floor: 18 LPA). Skip roles under 18 LPA. High-pay override: 25+ LPA is worth surfacing even outside preferred lanes/cities.
- **Company Types:** Product companies, well-funded startups. Skip IT staffing/services firms and unpaid/commission-only roles.

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

## ⚡ Daily Scan Operations
- **Single Sources of Truth (STRICT):**
  - Applications: `job-kit-starter/output/job-search/applications.csv`
  - Founder Cold Outreach: `job-kit-starter/output/job-search/outreach/startups_outreach.csv`
  - **Rule:** These files tracked in git are the ONLY authorized CSV targets. NEVER create or write to a root-level `output/` folder.
- **Daily Scans (Window: Past 7 Days / Last Week):**
  1. `python job-kit-starter/job_hunt.py` (~90 curated ATS boards -> `output/job-search/digest.md`)
  2. `python job-kit-starter/job_hunt_india.py` (Indeed + LinkedIn India -> `output/job-search/digest_india.md`)
  3. `python job-kit-starter/hn_scan.py` (HN hiring -> excludes already-applied)
  4. Platform browser feeds via Playwright: Instahyre (`candidate/opportunities/?matching=true`), Cutshort matches page, and Naukri (`jobAge=7` for past 7 days backend/full-stack engineer roles in Bengaluru/remote).
- **Execution & Auto-Submit:**
  - Triage each lead against the Candidate Bar.
  - For each qualifying BULLSEYE/Strong Match lead:
    1. Tailor single-page resume `.tex`, compile with `tectonic -c minimal`, verify 1-page PDF.
    2. Fill application fields via Playwright and submit.
    3. Append entry to `job-kit-starter/output/job-search/applications.csv` using Python's `csv` module.
    4. Run `job-kit-starter/tracker/refresh.sh` (or update tracker data).
- **Report Summary:** Present a structured report of applied roles, submitted timestamps, links, and skipped noise with reasons.

---

## 🔐 Authentication & Session Persistence Rule
- **Never Logout Accidentally:** Do NOT ever log out accidentally from any platform, session, or browser.
- **Sign-In Recovery Protocol:** Whenever encountering sign-in problems, expired sessions, or an accidental logout:
  - **Target Account:** Sign into the **`prathammodi001@gmail.com`** account.
  - **Google OAuth via Cursor Click:** Use Google Sign-In via OAuth by clicking the "Sign in with Google" / OAuth button with the cursor. **DO NOT** sign in by typing credentials into email/password fields ("not signin via email").
  - **Tooling:**
    - When running under **AGY (Antigravity)**: Perform OAuth sign-in via **Playwright**.
    - When running under **Claude**: Perform OAuth sign-in via **Claude in Chrome** (`claude-in-chrome`).
- **Board Exception:** Do **NOT** log in if it is the **jobfound** board (`jobfound.org`) — login is not needed.
