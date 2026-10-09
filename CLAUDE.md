## graphify

This project has a knowledge graph at graphify-out/ with god nodes, community structure, and cross-file relationships.

Rules:
- For codebase questions, first run `graphify query "<question>"` when graphify-out/graph.json exists. Use `graphify path "<A>" "<B>"` for relationships and `graphify explain "<concept>"` for focused concepts. These return a scoped subgraph, usually much smaller than GRAPH_REPORT.md or raw grep output.
- If graphify-out/wiki/index.md exists, use it for broad navigation instead of raw source browsing.
- Read graphify-out/GRAPH_REPORT.md only for broad architecture review or when query/path/explain do not surface enough context.
- After modifying code, run `graphify update .` to keep the graph current (AST-only, no API cost).

## 🔐 Authentication & 🎯 Candidate Bar — canonical source

Full detail for both lives in `job-kit-starter/CLAUDE.md` (Authentication rule near the top; Candidate Bar under "Job-Search Operations Runbook"). Read that file in full before running anything job-search-related — do not rely on a stale copy. Quick gist for orientation only: Bengaluru/India-based product/startup roles (Software Developer · Full-Stack · Node.js Backend, 0–3 YOE, 18–20 LPA floor); never log into LinkedIn; re-auth via Google OAuth cursor-click into `prathammodi001@gmail.com` (jobfound.org excepted, no login needed there).

## 📁 Single Source of Truth & Canonical CSV Paths (STRICT)

- **Canonical Applications File:** `job-kit-starter/output/job-search/applications.csv` (the single source of truth tracked in git).
- **Canonical Outreach File:** `job-kit-starter/output/job-search/outreach/startups_outreach.csv` (the single source of truth tracked in git).
- **STRICT RULE:** ALWAYS read from and write ONLY to the existing files under `job-kit-starter/output/job-search/`. NEVER create or write to a secondary or top-level `output/` directory at the repository root. There must always be exactly ONE `applications.csv` and ONE `startups_outreach.csv`.

## 📄 CRITICAL RULE — Mandatory Tailored Resume for Every Application (STRICT)

**NEVER reuse a generic/cached resume for any application — no exceptions.** Full pipeline (lane selection, copy-exact bullets, compile + 1-page verification, mandatory upload-replace on Smart Apply/Cutshort/portals): see `job-kit-starter/CLAUDE.md` → "Mandatory Tailored Resume" and `job-kit-starter/PLAYBOOK.md` → "Resume variant system".

