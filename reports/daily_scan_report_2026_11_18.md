# Daily Scan & Outreach Execution Report — 2026-11-18

## 1. Executive Summary
- **Target Submissions**: `NUM_JOBS = 5` (`Status=Applied` strictly satisfied).
- **Applications Successfully Submitted (`Status=Applied`)**: **5**
  1. **Springboard**: Product Engineer (Full Stack, IC) - India (`https://wellfound.com/jobs/4982389-product-engineer-full-stack-ic-india`)
  2. **Isomorph AI**: Founding Engineer, Platform Capabilities (`https://wellfound.com/jobs/5081936-founding-engineer-platform-capabilities`)
  3. **Tonbo Imaging Pvt.Ltd**: System Software Engineer (`https://wellfound.com/jobs/4632634-system-software-engineer`)
  4. **Tonbo Imaging Pvt.Ltd**: Software Development Engineer in Test ( SDET ) (`https://wellfound.com/jobs/4634106-software-development-engineer-in-test-sdet`)
  5. **Isomorph AI**: Founding Engineer, Finance Agents and Apps (`https://wellfound.com/jobs/5081935-founding-engineer-finance-agents-and-apps`)
- **Skipped Leads (Gate-Filtered)**: **4**
  - **MaxHome.ai**: Full-stack engineer (`SKIP 4+ years`)
  - **Fuze**: Software Engineer (`SKIP 4+ years`)
  - **Archetype Solutions Software**: Full Stack Engineer - Python (`SKIP 4-6 years`)
  - **Finthos**: Full-Stack Engineer — Finthos (`SKIP 4+ years`)
- **Blocked Leads**: **0** (No bot detection/captcha interruptions required opening holding tabs).
- **Cold Outreach Sent**: **20** new emails (10 Global/HN Who is Hiring + 10 High-Growth Indian Tech Startups) dispatched by user with base resume `job-kit-starter/output/Pratham_Modi_Base_Resume.pdf` attached, 0 duplicates, reconciled in `output/job-search/outreach/startups_outreach.csv` under `Status=Sent`.
- **Tracker & Knowledge Graph Sync**:
  - `make_data.py`: Processed 454 application rows -> `tracker/src/data.json`
  - `npm run build`: Vite production build passed cleanly.
  - `graphify update .`: AST-only code graph updated with 0 cost.

---

## 2. Applied Roles Detail (`NUM_JOBS = 5`)

All applied positions passed:
- `gates.py title "<title>"` -> `CLEAR`
- Live JD verbatim fetch (>=2 KB)
- `gates.py yoe output/<dir>/jd.txt` -> `OK`
- Single-page LaTeX compilation via `tectonic`, verified `pages == 1` via `pypdf`
- `gates.py lint "<dir>"` -> `PASSED` (0 unsupported claim words)
- `gates.py coverage "<dir>"` -> `PASSED` (100% coverage of extracted technical keywords)
- `gates.py form "<exact values typed>"` -> `OK` (0 divergences)

| # | Company | Role | Req ID / Job URL | Platform | Tailored 1-Page Resume Path | Tool Calls | Notes |
|---|---------|------|------------------|----------|-----------------------------|------------|-------|
| 1 | **Springboard** | Product Engineer (Full Stack, IC) - India | `4982389` ([Link](https://wellfound.com/jobs/4982389-product-engineer-full-stack-ic-india)) | Wellfound | `output/Springboard - Product Engineer (Full Stack, IC)/Pratham_Modi_Resume.pdf` | 41 | Budget violation noted (exceeded 40-call budget by 1). Native 1-click modal with tailored pitch note. |
| 2 | **Isomorph AI** | Founding Engineer, Platform Capabilities | `5081936` ([Link](https://wellfound.com/jobs/5081936-founding-engineer-platform-capabilities)) | Wellfound | `output/Isomorph AI - Founding Engineer, Platform Capabilities/Pratham_Modi_Resume.pdf` | 24 | Wellfound Native Apply (Undo timer active). Tailored pitch note on distributed microservices & agentic workflows. |
| 3 | **Tonbo Imaging Pvt.Ltd** | System Software Engineer | `4632634` ([Link](https://wellfound.com/jobs/4632634-system-software-engineer)) | Wellfound | `output/Tonbo Imaging - System Software Engineer/Pratham_Modi_Resume.pdf` | 29 | Wellfound Native Apply (Undo timer active). Tailored pitch note on C/C++, low-level streaming & C3iHub reliability. |
| 4 | **Tonbo Imaging Pvt.Ltd** | Software Development Engineer in Test ( SDET ) | `4634106` ([Link](https://wellfound.com/jobs/4634106-software-development-engineer-in-test-sdet)) | Wellfound | `output/Tonbo Imaging - SDET/Pratham_Modi_Resume.pdf` | 22 | Wellfound Native Apply (Undo timer active). Tailored pitch note on SDET test automation, 200+ test suites & CI/CD. |
| 5 | **Isomorph AI** | Founding Engineer, Finance Agents and Apps | `5081935` ([Link](https://wellfound.com/jobs/5081935-founding-engineer-finance-agents-and-apps)) | Wellfound | `output/Isomorph AI - Founding Engineer, Finance Agents and Apps/Pratham_Modi_Resume.pdf` | 23 | Wellfound Native Apply (Undo timer active). Tailored pitch note on autonomous finance agents & invoice platform. |

---

## 3. Skipped Leads (Gated Out)

| Company | Role | URL | Reason / Matched Term |
|---|---|---|---|
| **MaxHome.ai** | Full-stack engineer | `https://wellfound.com/jobs/3049915-full-stack-engineer` | `gates.py yoe` exited 1 (`SKIP 4+ years`) |
| **Fuze** | Software Engineer | `https://wellfound.com/jobs/2448180-software-engineer` | `gates.py yoe` exited 1 (`SKIP 4+ years`) |
| **Archetype Solutions Software** | Full Stack Engineer - Python | `https://wellfound.com/jobs/4791207-full-stack-engineer-python` | `gates.py yoe` exited 1 (`SKIP 4-6 years`) |
| **Finthos** | Full-Stack Engineer — Finthos | `https://wellfound.com/jobs/5081922-full-stack-engineer-finthos-ai-native-fintech-startup` | `gates.py yoe` exited 1 (`SKIP 4+ years`) |

---

## 4. Cold Outreach (20 New Emails Dispatched & Reconciled)

All 20 outreach records were prepared using the Tier B template (`output/job-search/outreach/tier_b_template.md`), validated for 0 duplicates against 804 existing entries in `startups_outreach.csv`, staged with base resume `job-kit-starter/output/Pratham_Modi_Base_Resume.pdf` attached, dispatched by user, and reconciled in `output/job-search/outreach/startups_outreach.csv` under status `Sent`.

### A. 10 Global / HN Who is Hiring Startups
1. **Strobe Power** — `keeley@strobepower.com` (Founder: Keeley) | **Confidence:** Verified | **Tier:** B
   - *Subject:* Backend systems for Strobe Power's energy infrastructure
2. **Quaisr** — `careers@quaisr.com` (Team) | **Confidence:** Verified | **Tier:** B
   - *Subject:* Platform engineering for Quaisr simulation workflows
3. **Talonic** — `jobs@talonic.ai` (Team) | **Confidence:** Verified | **Tier:** B
   - *Subject:* AI systems & backend pipelines for Talonic
4. **Aeqium** — `careers@aeqium.com` (Team) | **Confidence:** Verified | **Tier:** B
   - *Subject:* Data workflows & platform backend for Aeqium
5. **River** — `tarek@rivergtm.com` (Founder: Tarek) | **Confidence:** Verified | **Tier:** B
   - *Subject:* AI automation & backend architecture for River
6. **Pingintel** — `jobs@pingintel.com` (Team) | **Confidence:** Verified | **Tier:** B
   - *Subject:* High-throughput data ingestion for Pingintel
7. **Phonely** — `recruiting@phonely.ai` (Team) | **Confidence:** Verified | **Tier:** B
   - *Subject:* Low-latency streaming & agent backend for Phonely
8. **Phaselaw** — `hn@phase.law` (Team) | **Confidence:** Verified | **Tier:** B
   - *Subject:* Reliable document extraction & LLM pipelines for Phaselaw
9. **Pantograph** — `hiring@pantograph.com` (Team) | **Confidence:** Verified | **Tier:** B
   - *Subject:* Scalable systems & backend services for Pantograph
10. **Hotwash** — `hiring@hotwash.com` (Team) | **Confidence:** Verified | **Tier:** B
    - *Subject:* Founding backend & infrastructure execution for Hotwash

### B. 10 Indian Tech Startups (Direct Verified Founders)
11. **Kuku FM** — `bisu@kukufm.com` (Founder: Lal Chand Bisu) | **Confidence:** Verified | **Tier:** B
    - *Subject:* High-throughput audio streaming & event backend for Kuku FM
12. **Teachmint** — `mihir@teachmint.com` (Founder: Mihir Gupta) | **Confidence:** Verified | **Tier:** B
    - *Subject:* Low-latency classroom systems & backend reliability for Teachmint
13. **Hoppscotch** — `liyas@hoppscotch.io` (Founder: Liyas Thomas) | **Confidence:** Verified | **Tier:** B
    - *Subject:* Core platform performance & API ecosystem for Hoppscotch
14. **Pushowl** — `shashank@pushowl.com` (Founder: Shashank Kumar) | **Confidence:** Verified | **Tier:** B
    - *Subject:* Real-time dispatch pipelines & delivery backend for Pushowl
15. **Leap Scholar** — `vaibhav@leapscholar.com` (Founder: Vaibhav Singh) | **Confidence:** Verified | **Tier:** B
    - *Subject:* Distributed services & application processing for Leap Scholar
16. **Miko** — `sneh@miko.ai` (Founder: Sneh Vaswani) | **Confidence:** Verified | **Tier:** B
    - *Subject:* Low-latency conversational AI & backend scale for Miko
17. **BukuWarung** — `chinmay@bukuwarung.com` (Founder: Chinmay Chauhan) | **Confidence:** Verified | **Tier:** B
    - *Subject:* Financial transaction throughput & ledger backend for BukuWarung
18. **Bijak** — `nukul@bijak.in` (Founder: Nukul Upadhye) | **Confidence:** Verified | **Tier:** B
    - *Subject:* Real-time pricing & transaction architecture for Bijak
19. **Stellapps** — `ranjith@stellapps.com` (Founder: Ranjith Mukundan) | **Confidence:** Verified | **Tier:** B
    - *Subject:* IoT data ingestion & distributed telemetry for Stellapps
20. **Flobiz** — `rahul@flobiz.in` (Founder: Rahul Raj) | **Confidence:** Verified | **Tier:** B
    - *Subject:* Scalable ledger services & backend performance for FloBiz

---

## 5. Token Usage & Subagent Audit

### Real Token Usage (Extracted from Session Transcript Logs)
- **Input Tokens**: `2,559,909`
- **Output Tokens**: `193,532`
- **Cache Read Tokens**: `60,694,516`
- **Grand Total Tokens**: `63,447,957`

### Subagents Tool-Call Audit (Budget = 40 tool calls max per subagent)
| Subagent | Role | Tool Calls | Budget Status |
|---|---|---|---|
| `ec48bf27` | Lead Subagent - Springboard | 41 | **Violation** (+1 call over 40-call budget, noted in CSV) |
| `abd0cf0d` | Lead Subagent - MaxHome.ai | 9 | Passed |
| `80696012` | Lead Subagent - Fuze | 8 | Passed |
| `fe91cbb7` | Lead Subagent - Archetype | 23 | Passed |
| `093b1c82` | Lead Subagent - Isomorph AI (Platform) | 24 | Passed |
| `a37be0ac` | Lead Subagent - Tonbo System | 29 | Passed |
| `4fb554eb` | Lead Subagent - Tonbo SDET | 22 | Passed |
| `365d3c43` | Lead Subagent - Isomorph Finance | 23 | Passed |

---

## 6. Discrepancies vs. Spec
- **Outreach count vs target**: 20 staged / 20 target (**0 discrepancy**).
- **Applied count vs target**: 5 applied / 5 target (**0 discrepancy**).
- **Budget violation**: Lead 1 (Springboard) used 41 tool calls (+1 over 40-call budget) due to initial Playwright element query retries; all subsequent subagents finished in 8 to 29 tool calls.
- **Tracker Deploy**: Vite build & `make_data.py` succeeded (454 rows synced). Wrangler pages deploy prompted for interactive OAuth in background; process cleanly stopped so local artifacts remain ready for deployment with existing tokens.
