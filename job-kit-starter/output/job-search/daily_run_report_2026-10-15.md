# Daily Job Search & Cold Outreach Run Report
**Date:** 2026-10-15
**Run Mode:** Fully Autonomous Scan, Apply & Outreach via Playwright
**Orchestrator:** Antigravity Agent

---

## 1. Executive Summary

- **Jobs Applied:** 5 applied (qualifying bar strictly enforced; 0 placeholder slots).
- **Cold Outreach:** 20 new emails drafted and sent to uncontacted companies with tailored hooks and base resume attached (`Pratham_Modi_Resume.pdf`).
- **Repetition Check:** 0 duplicates; all 20 target companies checked against all 345 historical rows in `startups_outreach.csv`.
- **ATS Form Validation:** Verified via `gates.py form` for every submission.
- **Tracker & Knowledge Graph:** Synced across `applications.csv`, `startups_outreach.csv`, `data.json`, and `graphify`.

---

## 2. Jobs Applied (NUM_JOBS = 5)

| # | Company | Role | Location | Channel | Comp | Resume Variant | Status |
|---|---|---|---|---|---|---|---|
| 1 | **Sarvam AI** | Agent Engineer | India, Bengaluru | Ashby ATS | 18–25 LPA | Tailored AI/Agent Resume | **Applied** |
| 2 | **Kalydo** | Founding Full Stack Engineer | India, Bengaluru | Cutshort ATS | 18–22 LPA | Tailored Full Stack Resume | **Applied** |
| 3 | **Valiance Solutions** | Software Engineer | India, Remote | Wellfound | 18–20 LPA | Tailored Backend Resume | **Applied** |
| 4 | **Webbtreejobs** | Fullstack Developer | Mumbai, India | Webbtree ATS | 18–20 LPA | Tailored Full Stack Resume | **Applied** |
| 5 | **Nvidia** | System Software Engineer (JR2025205) | Bengaluru, India | Workday ATS | 20–25 LPA | Tailored Systems/Infra Resume | **Applied** |

### Audit Trail of Form Values
- **Candidate:** Pratham Modi
- **Email:** `prathammodi001@gmail.com`
- **Phone:** `+91-9033393729`
- **Notice Period:** Immediate
- **Current CTC:** 12 LPA | **Expected CTC:** 18–20 LPA (minimum 18 LPA)
- **Citizenship:** India (No sponsorship required)

---

## 3. Cold Outreach Sent (20 Companies)

All 20 emails were drafted in Gmail (`prathammodi001@gmail.com`), verified for attachment upload (`Pratham_Modi_Resume.pdf`), and sent via Playwright automation.

| # | Company | Recipient Email | Contact / Role | Subject Line | Status |
|---|---|---|---|---|---|
| 1 | **GovStar** | `nicholas.hanson@govstar.us` | Nicholas Hanson | *Scalable procurement backends & APIs for GovStar — quick note* | **Sent** |
| 2 | **Irash Tech** | `hello@irashtech.com` | Founding Team | *Full-stack AI automation & async pipelines for Irash Tech — quick note* | **Sent** |
| 3 | **Sendery** | `jobs@sendery.co` | Nikos Caroyannis | *Reliable API infrastructure & distributed sync for Sendery — quick note* | **Sent** |
| 4 | **Komodo Health** | `kaushal.parikh@komodohealth.com` | Kaushal Parikh | *Healthcare AI pipelines & high-throughput backends for Komodo Health — quick note* | **Sent** |
| 5 | **Willow Education** | `careers@willowed.org` | Hiring Team | *High-reliability EdTech platforms for Willow Education — quick note* | **Sent** |
| 6 | **neoshare** | `product-jobs@neoshare.com` | Engineering Team | *Fintech AI workflows & robust microservices for neoshare — quick note* | **Sent** |
| 7 | **Estuary** | `careers@estuary.dev` | Engineering Hiring | *Real-time CDC capture pipelines & streaming infrastructure for Estuary — quick note* | **Sent** |
| 8 | **Silkline** | `hn@silkline.ai` | Hiring Team | *Scalable AI agent infrastructure for Silkline — quick note* | **Sent** |
| 9 | **Steg.AI** | `careers@steg.ai` | Raj Kataria | *High-throughput AI watermarking pipelines for Steg.AI — quick note* | **Sent** |
| 10 | **Quill** | `rishi@quill.co` | Rishi | *Real-time collaboration backends for Quill — quick note* | **Sent** |
| 11 | **Pango** | `steve@pango.ai` | Steve | *Autonomous agent infrastructure for Pango — quick note* | **Sent** |
| 12 | **Catalyst Wayfare AI** | `hn@cwai.co` | Hiring Team | *Scalable agent execution runtimes for Catalyst Wayfare AI — quick note* | **Sent** |
| 13 | **Biobase** | `jobs@biobase.ai` | Hiring Team | *Scalable life-sciences data platforms for Biobase — quick note* | **Sent** |
| 14 | **Lucia** | `emily.thompson@luciaprotocol.com` | Emily Thompson | *High-throughput protocol backends & MLOps for Lucia — quick note* | **Sent** |
| 15 | **Noricum** | `michael@noricum.io` | Michael | *High-reliability payment ledgers for Noricum — quick note* | **Sent** |
| 16 | **Senzing** | `enghiring@senzing.com` | Sam | *High-performance entity resolution platforms for Senzing — quick note* | **Sent** |
| 17 | **Privy.pro** | `careers@privy.pro` | Scott Fahl | *Scalable real estate analytics platforms for Privy.pro — quick note* | **Sent** |
| 18 | **SKIES** | `julius@skieslearn.com` | Julius Su | *Mission-critical assistive communication backends for SKIES — quick note* | **Sent** |
| 19 | **Cascade Space** | `careers@cascade.space` | Arlen | *Ground-segment infrastructure & telemetry backends for Cascade Space — quick note* | **Sent** |
| 20 | **Tecuity** | `hr@tecuity.com` | Melissa Thomas | *Scalable regulatory filing backends for Tecuity — quick note* | **Sent** |

---

## 4. Reconciliation & System Invariants

- **`applications.csv`:** Updated to 241 total application records.
- **`startups_outreach.csv`:** Updated to 365 total outreach records.
- **`data.json`:** Regenerated via `tracker/make_data.py` with 241 rows for public Cloudflare Pages tracking.
- **`graphify`:** Complete knowledge graph AST update run (11,242 nodes, 29,967 edges, 410 communities).
