# Graph Report - job-kit-starter  (2026-09-13)

## Corpus Check
- 116 files · ~80,202 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 517 nodes · 559 edges · 50 communities (33 shown, 8 thin omitted)
- Extraction: 99% EXTRACTED · 1% INFERRED · 0% AMBIGUOUS · INFERRED: 7 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `3693fcd5`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Critique Framework — Consolidated Multi-Perspective Protocol
- package.json
- claude-job-kit — Project Instructions
- Resume & CV Generation — Reference
- claude-resume-kit
- Achievements
- PlaywrightClient
- /edit-resume
- /make-resume
- job_hunt.py
- Documentation
- char_count.py
- /setup-build-kb
- PLAYBOOK — the full job-search campaign, end to end
- Master Profile (SKILL_PROFILE) — Pratham Modi
- Cover Letter Generation — Reference
- /setup-extract
- Critical Rules — Compact Re-Read
- Shared Operations — All Skills
- /make-cl
- Configuration
- /critique
- Deep Learning-Guided Screening of Thermostable Enzyme Variants for Industrial Biocatalysis
- Configuration
- Bundle: Academia
- job_hunt_india.py
- waas_scan.py
- csv-logger.md
- hn_scan.py
- 👋 Start here
- make_data.py
- Session File Template
- rules/graphify.md
- workflows/graphify.md
- CLAUDE.md
- refresh.sh
- README.md
- test_portal_logins.py
- Job Hunt Profile & Operations Rule
- daily_scan.md
- Authentication & Session Persistence Rule

## God Nodes (most connected - your core abstractions)
1. `PlaywrightClient` - 57 edges
2. `Resume & CV Generation — Reference` - 13 edges
3. `claude-job-kit — Project Instructions` - 12 edges
4. `Critique Framework — Consolidated Multi-Perspective Protocol` - 12 edges
5. `claude-resume-kit` - 11 edges
6. `Master Profile (SKILL_PROFILE) — Pratham Modi` - 11 edges
7. `Cover Letter Generation — Reference` - 11 edges
8. `/make-resume` - 10 edges
9. `Job-Search Operations Runbook` - 10 edges
10. `Shared Operations — All Skills` - 10 edges

## Surprising Connections (you probably didn't know these)
- None detected - all connections are within the same source files.

## Import Cycles
- None detected.

## Communities (50 total, 8 thin omitted)

### Community 0 - "Critique Framework — Consolidated Multi-Perspective Protocol"
Cohesion: 0.06
Nodes (34): 6A. Anti-Pattern Checklist, 6B. Tailoring Signal Checklist, 6C. Context-Specific Checks, 6D. CL ATS Keyword Check, 6E. Structural Checks, 6F. Package Cohesion Check, Assessment Matrix, Build the Lens (+26 more)

### Community 1 - "package.json"
Cohesion: 0.08
Nodes (23): dependencies, react, react-dom, devDependencies, vite, @vitejs/plugin-react, wrangler, name (+15 more)

### Community 2 - "claude-job-kit — Project Instructions"
Cohesion: 0.08
Nodes (24): Accuracy Priority, Anti-Fabrication Rules, Application flow (per lead), Application Tracker, Candidate bar (SCOPE — assess every lead against this; skip fast if it fails), claude-job-kit — Project Instructions, 🔐 CRITICAL RULE — Authentication, Session Persistence & Auto-Re-login, ⛔ CRITICAL RULE — outbound submission policy (highest priority, overrides everything) (+16 more)

### Community 3 - "Resume & CV Generation — Reference"
Cohesion: 0.11
Nodes (18): Bold Width Penalty (COMPILE-VERIFIED), Char Verification Protocol (EVERY written element), Character Limits (HARD STOPS — ZERO TOLERANCE), Content Density Rules, CV (cv.cls), Experience Bullet Writing Protocol (Experience-File-First), Files to Upload (by format), Gap Assessment & Bridge Mappings (+10 more)

### Community 4 - "claude-resume-kit"
Cohesion: 0.06
Nodes (30): 1. Install the prerequisites (one-time), 2. Open the kit in Claude Code, 3. Say hi, 4. Start applying, Quickstart, 1. Clone and configure, 2. Extract your papers, 3. Build your knowledge base (+22 more)

### Community 5 - "Achievements"
Cohesion: 0.10
Nodes (19): Achievements, Achievements, Cross-Position Themes (for cover letters), Cross-Position Themes (for cover letters), Dates: Aug 2018 -- Jul 2023, Dates: Aug 2023 -- Present, L1: ML-Guided Enzyme Stability Screening, L2: Enzyme Solvent Tolerance Prediction (+11 more)

### Community 7 - "/edit-resume"
Cohesion: 0.12
Nodes (15): Cover Letter Verification Gates (if CL was edited), /edit-resume, FIXED Sections — Refuse if Asked to Edit, >>>>>> MANDATORY STOP <<<<<<, >>>>>> MANDATORY STOP — DO NOT PROCEED <<<<<<, Phase 1: Load Context, Phase 2: Diagnose & Plan Edits, Phase 3: Load Reference Files (only confirmed edits) (+7 more)

### Community 8 - "/make-resume"
Cohesion: 0.12
Nodes (16): Budget Gate (AFTER user confirms bullet plan, BEFORE Phase 2), CHAR COUNT GATE (per position), COMPILE GATE, End of /make-resume, /make-resume, >>>>>> MANDATORY STOP <<<<<<, >>>>>> MANDATORY STOP — DO NOT PROCEED <<<<<<, >>>>>> MANDATORY STOP — DO NOT PROCEED <<<<<< (+8 more)

### Community 9 - "job_hunt.py"
Cohesion: 0.23
Nodes (17): fetch_aiven(), fetch_arbeitnow(), fetch_ashby(), fetch_gh(), fetch_hn(), fetch_lever(), get(), loc_tag() (+9 more)

### Community 10 - "Documentation"
Cohesion: 0.12
Nodes (17): Architecture, Concepts, Customization, Documentation, Everything in `config.md` (edit directly), Experience Files, FAQ, Key Design Decisions (+9 more)

### Community 11 - "char_count.py"
Cohesion: 0.20
Nodes (14): classify_bullet(), count_bold_chars(), count_em_dashes(), extract_items(), format_one(), main(), Format analysis for a single bullet., Extract \\item lines from .tex source. (+6 more)

### Community 12 - "/setup-build-kb"
Cohesion: 0.13
Nodes (14): Final: Status Report, KB Build Status, >>>>>> MANDATORY STOP <<<<<<, >>>>>> MANDATORY STOP — DO NOT PROCEED <<<<<<, >>>>>> MANDATORY STOP — DO NOT PROCEED <<<<<<, Phase 1: Build Experience Files, Phase 2: Build Skills Taxonomy, Phase 3: Build Publication Metadata (+6 more)

### Community 13 - "PLAYBOOK — the full job-search campaign, end to end"
Cohesion: 0.14
Nodes (13): After every apply batch, ATS recipes (every quirk here was hit in production), Phase 0 — Setup (first session), Phase 1 — Platform profiles (do these early; they compound), Phase 2 — Daily scan (say "do the daily scan"), Phase 3 — Applying (auto-submit allowed once a lead clears the bar; see CLAUDE.md top rule), Phase 4 — Cold email outreach (startups without open roles), Phase 5 — X/Twitter cold DMs (+5 more)

### Community 14 - "Master Profile (SKILL_PROFILE) — Pratham Modi"
Cohesion: 0.14
Nodes (13): Achievements / Awards, Certifications, Education, Experience, Load-Bearing Facts (pin the current numbers here; grep for stale copies before every send), Log (append new wins here, fold up later), Master Profile (SKILL_PROFILE) — Pratham Modi, Projects (+5 more)

### Community 15 - "Cover Letter Generation — Reference"
Cohesion: 0.17
Nodes (11): ACADEMIC Cover Letter (350-450 postdoc, 450-650 faculty; 4 paragraphs), CL Anti-Patterns, CL Format Rules, CL Hook Verification (MANDATORY), Cover Letter Generation — Reference, INDUSTRY Cover Letter (250-300 words, 3 paragraphs), Institution Type Detection, Jargon Calibration (+3 more)

### Community 16 - "/setup-extract"
Cohesion: 0.18
Nodes (10): Batch Mode, >>>>>> MANDATORY STOP <<<<<<, >>>>>> MANDATORY STOP — DO NOT PROCEED <<<<<<, Phase 1: Read & Understand the Paper, Phase 2: Clarify User's Role, Phase 3: Write Extraction, Phase 4: Update Inventory, Phase 5: Next Steps (+2 more)

### Community 17 - "Critical Rules — Compact Re-Read"
Cohesion: 0.18
Nodes (10): Bold Width Penalty, Budget Reminder, Character Limits, Critical Rules — Compact Re-Read, FIXED Sections — NEVER Modify, KB Corrections, LaTeX Notation Quick-Ref, Orphan Rule (+2 more)

### Community 18 - "Shared Operations — All Skills"
Cohesion: 0.18
Nodes (10): Char Count Enforcement, Finalization (after /critique approval), Folder Creation (Phase 0 of /make-resume), Fresh Session Startup, Progress Commentary, Session End Protocol, Session File Derivation (for /make-cl, /critique, and /edit-resume), Session File System (+2 more)

### Community 19 - "/make-cl"
Cohesion: 0.20
Nodes (9): CL Hook Verification Gate (MANDATORY before presenting to user), /make-cl, >>>>>> MANDATORY STOP — DO NOT PROCEED <<<<<<, Phase 1: Load Context, Phase 2: Generate Cover Letter, Phase 3: Compile & Verify, Safety Rules (ALWAYS ENFORCED), Startup (+1 more)

### Community 20 - "Configuration"
Cohesion: 0.20
Nodes (9): Configuration, Document Preferences, FIXED Sections, KB Corrections Log, Output Rules, Personal Info, Provenance Flags, Role-Type Decision Tree (+1 more)

### Community 21 - "/critique"
Cohesion: 0.25
Nodes (7): /critique, >>>>>> MANDATORY STOP <<<<<<, Protocol, Safety Rules, Startup, User Input During Execution, When user approves / says "looks good" / finalizes:

### Community 22 - "Deep Learning-Guided Screening of Thermostable Enzyme Variants for Industrial Biocatalysis"
Cohesion: 0.25
Nodes (7): Collaboration & Scope, Deep Learning-Guided Screening of Thermostable Enzyme Variants for Industrial Biocatalysis, Key Results (with numbers), Metadata, Methods & Tools, Provenance, Resume Bullet Seeds

### Community 23 - "Configuration"
Cohesion: 0.25
Nodes (7): Application-Form Facts (reused constantly — collect once during onboarding), Configuration, Document Preferences, Personal Info, Preferred Job Platforms, Provenance Flags, Target Roles & Preferences

### Community 24 - "Bundle: Academia"
Cohesion: 0.29
Nodes (6): Bundle: Academia, S1: Role Profile, S2: Summary Guide, S3: Achievement Reframing Map, S4: Skills Guide, S5: Cover Letter Guide

### Community 25 - "job_hunt_india.py"
Cohesion: 0.53
Nodes (5): already_applied_companies(), load_seen(), main(), India-aggregator job scan (complements job_hunt.py, which only hits company ATS…, score()

### Community 26 - "waas_scan.py"
Cohesion: 0.53
Nodes (5): eligible(), load(), main(), parse_k(), Work-at-a-Startup (YC) triage + index. WaaS is login-gated with no public API,…

### Community 27 - "csv-logger.md"
Cohesion: 0.40
Nodes (4): Dates, Hard rules, Operations you support, Output

### Community 29 - "👋 Start here"
Cohesion: 0.40
Nodes (4): How to start (2 minutes), 👋 Start here, Two rules that keep this safe and honest, What you need installed

### Community 30 - "make_data.py"
Cohesion: 0.60
Nodes (4): derive(), domain_name(), main(), Convert output/job-search/applications.csv into tracker/src/data.json…

### Community 31 - "Session File Template"
Cohesion: 0.50
Nodes (3): Context Efficiency Notes, Session File Template, Template

### Community 34 - "CLAUDE.md"
Cohesion: 0.40
Nodes (4): 🔐 Authentication, Session Persistence & Auto-Re-login Rule, 🎯 Candidate Bar & Role Focus, graphify, 📁 Single Source of Truth & Canonical CSV Paths (STRICT)

### Community 41 - "Job Hunt Profile & Operations Rule"
Cohesion: 0.29
Nodes (6): 📋 Application-Form Facts, 🔐 Authentication & Session Persistence Rule, 🎯 Candidate Bar (Pratham Modi), ⚡ Daily Scan Operations, Job Hunt Profile & Operations Rule, ✅ SUBMISSION RULE — AUTO-SUBMISSION AUTHORIZED FOR QUALIFYING MATCHES

### Community 43 - "Authentication & Session Persistence Rule"
Cohesion: 0.40
Nodes (4): Authentication & Session Persistence Rule, 🚫 Board Exception (jobfound), ⛔ Never Logout Accidentally, 🔐 Sign-In & Recovery Protocol

## Knowledge Gaps
- **282 isolated node(s):** `name`, `private`, `version`, `type`, `dev` (+277 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 337 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **8 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Documentation` connect `Documentation` to `claude-resume-kit`?**
  _High betweenness centrality (0.005) - this node is a cross-community bridge._
- **What connects `name`, `private`, `version` to the rest of the system?**
  _282 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Critique Framework — Consolidated Multi-Perspective Protocol` be split into smaller, more focused modules?**
  _Cohesion score 0.05714285714285714 - nodes in this community are weakly interconnected._
- **Should `package.json` be split into smaller, more focused modules?**
  _Cohesion score 0.08262108262108261 - nodes in this community are weakly interconnected._
- **Should `claude-job-kit — Project Instructions` be split into smaller, more focused modules?**
  _Cohesion score 0.08 - nodes in this community are weakly interconnected._
- **Should `Resume & CV Generation — Reference` be split into smaller, more focused modules?**
  _Cohesion score 0.10526315789473684 - nodes in this community are weakly interconnected._
- **Should `claude-resume-kit` be split into smaller, more focused modules?**
  _Cohesion score 0.058823529411764705 - nodes in this community are weakly interconnected._