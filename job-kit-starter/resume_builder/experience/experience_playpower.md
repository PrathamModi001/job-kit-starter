# Experience: Software Development Engineer — Playpower Labs

**Dates (FIXED):** Nov 2024 – Jun 2025 | **Location (FIXED):** Remote

> **Bullet policy:** same COPY-EXACT rule as `experience_c3ihub.md`. PP1 has two
> approved variants — pick the one matching the lane, never blend or rewrite them.

---

### PP1 — AI tutoring platform (two lane variants — pick ONE per bundle)
**Tags:** nextjs, fastapi, websocket, ssr, react-server-components, ai-product, full-stack

**Variant A — Backend/AI lane (leads with backend, omits frontend framework detail):**
Developed AI tutoring platform using FastAPI microservices and Next.js, supporting 500+ concurrent WebSocket sessions with sub-100ms response times.

**Variant B — Full-Stack lane (leads with frontend architecture — use this when JD is frontend/full-stack heavy):**
Built AI tutoring platform using Next.js (SSR/ISR, React Server Components) and FastAPI microservices, supporting 500+ concurrent WebSocket sessions at sub-100ms response times.

### PP2 — RAG retrieval (AI lane only — cap at 1 AI-specific bullet total for Backend/Full-Stack lanes)
**Tags:** rag, chromadb, vector-search, ai, retrieval
**Bullet:** Integrated ChromaDB vector search over 10K+ documents via a RAG pipeline, increasing user session depth 35% with sub-200ms retrieval latency at p95.

### PP3 — Ingestion pipeline (AI lane only)
**Tags:** rag, embeddings, chromadb, pdf-ingestion, ai
**Bullet:** Cut document retrieval latency by 47% (340ms to 180ms) via a PDF ingestion pipeline using 512-token chunking, OpenAI embeddings, and HNSW-indexed ChromaDB.

### PP4 — CI/CD (usable in every lane — strong DevOps signal)
**Tags:** cicd, aws, github-actions, devops, deployment, reliability
**Bullet:** Reduced release cycle time by 65% by implementing blue-green CI/CD on AWS with GitHub Actions and automated rollback triggers for zero-downtime deployments.

---

## Known truthful gap — DO NOT paper over

**TypeScript** is listed in `SKILL_PROFILE.md` Skills but is not directly demonstrated by any bullet above (Next.js/React work here is not confirmed to be TypeScript specifically). If a JD hard-requires TypeScript:
- Do NOT add a bullet claiming "built with TypeScript" — this would be fabrication.
- Acceptable bridge language in Skills section only: keep "TypeScript" listed as a language skill (already true per SKILL_PROFILE.md), but do not claim project-level TypeScript ownership in prose.
- If the user confirms Playpower or C3iHub frontend work was actually done in TypeScript, update this file and `SKILL_PROFILE.md` first, then this gap note becomes obsolete — verify before removing.
