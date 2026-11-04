# Daily Scan & Outreach Execution Report — 2026-11-04

## 1. Executive Summary
- **Target Submissions**: `NUM_JOBS = 5` (`Status=Applied` only).
- **Cold Outreach Staged**: 20 new personalized outreach emails created directly as Gmail Drafts with base resume (`Pratham_Modi_Base_Resume.pdf`) attached.
  - 10 Global / HN Startups (November 2026 batch, id: 50338728)
  - 10 High-Growth Indian Tech Companies
  - **All 20 logged to `output/job-search/outreach/startups_outreach.csv` and marked `Status=Sent`** per user instruction for manual review and delivery.
- **Leads Evaluated**: 5 priority leads triaged with custom 1-page resumes compiled, linted, and verified before form handling.
- **Blockers Handled**: 5 leads blocked by bot detection/captchas per rule (*"stop at first captcha/wall, leave tab open, log Blocked, never retry"*).
- **System Sync**: Knowledge graph updated via `graphify update .`, tracker data refreshed (`make_data.py`), and repository committed and synced to remote for seamless home PC access over the next 15 days.

---

## 2. Lead Evaluation & Form Execution Status

| Company | Role | Channel / Platform | Location | Status | Action Taken / Blocker Reason | Resume Path |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **NeoGenCode Technologies** | Full Stack Engineer (Python + React.js) | Cutshort | Indiranagar, Bangalore | **Blocked** | Cloudflare Turnstile captcha challenge triggered during resume file upload. Tab 1 left open per blocker protocol. | `output/NeoGenCode - Full Stack Engineer (Python + React.js)/Pratham_Modi_Resume.pdf` |
| **Fynd** | SDE - 1 Fullstack Developer | Keka | Mumbai | **Blocked** | Keka image captcha wall (`img "Captcha"` + `textbox "Captcha"`) mandatory on submission. Tab 2 left open per blocker protocol. | `output/Fynd - SDE - 1 Fullstack Developer/Pratham_Modi_Resume.pdf` |
| **Viridien** | Machine Learning Engineer | Workday (`cgg.wd103`) | Airoli, Navi Mumbai | **Blocked** | Workday security / bot-detection script automatically terminated session/window on account creation. | `output/Viridien - Machine Learning Engineer/Pratham_Modi_Resume.pdf` |
| **Copeland** | Software Engineer | Workday (`copeland.wd5`) | Pune | **Blocked** | Workday bot defense executed `window.close()` upon automated typing into email field. | `output/Copeland - Software Engineer/Pratham_Modi_Resume.pdf` |
| **Philips** | Software Technologist I | Workday (`philips.wd3`) | Bangalore | **Blocked** | Workday wd3 tenant client-side automated session termination. | `output/Philips - Software Technologist I/Pratham_Modi_Resume.pdf` |

### Scripted Verification Gates Run:
1. `gates.py title "<title>"`: Verified for all evaluated leads (exits 0, CLEAR).
2. `gates.py yoe "<jd.txt>"`: Passed across all targets (Fynd flagged as 2-6 YOE BORDERLINE and noted accordingly).
3. `gates.py lint "<dir>"`: Passed for all 5 tailored resumes (`UNSUPPORTED CLAIM WORDS: none`).
4. `gates.py coverage "<dir>"`: Passed for all 5 tailored resumes.
5. All resumes compiled cleanly to exactly 1 page via `tectonic -c minimal`.

---

## 3. Cold Outreach (20 New Emails Staged in Gmail)

All 20 emails were drafted directly in the authenticated browser session on Gmail with `Pratham_Modi_Base_Resume.pdf` attached, staged in Gmail drafts, and logged to `startups_outreach.csv` with `Status=Sent` for manual verification and transmission.

### A. 10 Global / HN Startups (YC / Tech Startups)
1. **Kanmon** — `mags@kanmonhq.com` (Founder: Mags)
   - *Subject:* Embedded lending APIs & transaction telemetry for Kanmon
   - *Confidence:* Verified | *Tier:* B
2. **NEO Holdings** — `careers@neo.co` (Team)
   - *Subject:* High-throughput exchange backends & Kafka pipelines for NEO Holdings
   - *Confidence:* Verified | *Tier:* B
3. **myDataValue** — `martin@mydatavalue.com` (Founder: Martin)
   - *Subject:* Telemetry analytics pipelines and database indexing for myDataValue
   - *Confidence:* Verified | *Tier:* B
4. **Kraus Hamdani Aerospace** — `software@khaero.com` (Team)
   - *Subject:* Real-time UAV telemetry streaming & distributed backends for KHAero
   - *Confidence:* Verified | *Tier:* B
5. **Lyra Space** — `tanmayi@lyraspace.co` (Founder: Tanmayi)
   - *Subject:* Ground station telemetry ingestion & microservices for Lyra Space
   - *Confidence:* Verified | *Tier:* B
6. **Stream** — `pauli.ojala@getstream.io` (Founder/Team: Pauli)
   - *Subject:* High-concurrency WebSocket backends and event pipelines for Stream
   - *Confidence:* Verified | *Tier:* B
7. **Stratirus** — `hiring@stratirus.com` (Team)
   - *Subject:* 10 min re: Stratirus backend & distributed infra hiring
   - *Confidence:* Verified | *Tier:* B
8. **Voluntas** — `jobs@voluntas.io` (Team)
   - *Subject:* Async data pipelines & database query optimization for Voluntas
   - *Confidence:* Verified | *Tier:* B
9. **Mesmer** — `hiring@mesmer.co` (Team)
   - *Subject:* Agentic test pipelines & async microservices for Mesmer
   - *Confidence:* Verified | *Tier:* B
10. **Helmsted AI** — `careers@helmsted.ai` (Team)
    - *Subject:* Low-latency retrieval & agentic orchestration for Helmsted AI
    - *Confidence:* Verified | *Tier:* B

### B. 10 High-Growth Indian Tech Companies
11. **Navi Technologies** — `sachin@navi.com` (Founder: Sachin Bansal)
    - *Subject:* High-throughput transaction pipelines & Kafka microservices for Navi
    - *Confidence:* Pattern-guessed | *Tier:* B
12. **DronaHQ** — `divyesh@dronahq.com` (Founder: Divyesh Patel)
    - *Subject:* High-concurrency API runtimes and WebSocket sync for DronaHQ
    - *Confidence:* Pattern-guessed | *Tier:* B
13. **Segwise** — `bipin@segwise.ai` (Founder: Bipin Baburaj)
    - *Subject:* Distributed tracing & telemetry ingestion engines for Segwise
    - *Confidence:* Pattern-guessed | *Tier:* B
14. **CogniSwitch** — `ritesh@cogniswitch.ai` (Founder: Ritesh Mukherjee)
    - *Subject:* Knowledge graph ingestion and sub-200ms vector retrieval for CogniSwitch
    - *Confidence:* Pattern-guessed | *Tier:* B
15. **Aikenist** — `ashwin@aikenist.com` (Founder: Ashwin Roy)
    - *Subject:* High-throughput async pipelines and image ingestion for Aikenist
    - *Confidence:* Pattern-guessed | *Tier:* B
16. **FreightFox** — `nitish@freightfox.ai` (Founder: Nitish Rai)
    - *Subject:* Real-time dispatch telemetry and event-driven backends for FreightFox
    - *Confidence:* Pattern-guessed | *Tier:* B
17. **KredX** — `manish@kredx.com` (Founder: Manish Kumar)
    - *Subject:* High-volume transaction processing and event streaming for KredX
    - *Confidence:* Pattern-guessed | *Tier:* B
18. **Riskcovry** — `suvendu@riskcovry.com` (Founder: Suvendu Prusty)
    - *Subject:* Embedded insurance API engines and microservices for Riskcovry
    - *Confidence:* Pattern-guessed | *Tier:* B
19. **Onsurity** — `yogesh@onsurity.com` (Founder: Yogesh Agarwal)
    - *Subject:* Microservice scalability and event processing for Onsurity
    - *Confidence:* Pattern-guessed | *Tier:* B
20. **M2P Fintech** — `madhu@m2pfintech.com` (Founder: Madhusudanan R)
    - *Subject:* High-throughput transaction switches and Kafka backends for M2P Fintech
    - *Confidence:* Pattern-guessed | *Tier:* B

---

## 4. Token & Resource Usage Accounting

*Figures extracted directly from session trajectory logs (`transcript.jsonl`):*
- **Orchestrator Execution**:
  - Input Tokens: 1,650,787
  - Output Tokens: 127,455
  - Cache Read Tokens: 56,871,639
  - Trajectory Steps: 950
- **Subagents (`Lead 1 Applicant`)**:
  - Input Tokens: 301,655
  - Output Tokens: 34,922
  - Cache Read Tokens: 1,355,508
- **Combined Total Session Usage**:
  - **Total Input Tokens**: 1,952,442
  - **Total Output Tokens**: 162,377
  - **Total Cache Read Tokens**: 58,227,147
