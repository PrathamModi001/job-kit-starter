# Master Profile (SKILL_PROFILE) — Pratham Modi

> The "brag doc" — single source of truth for every fact about the career.
> Every tailored resume is generated FROM this file.
>
> Rules:
> - **Real numbers only.** Anything inflated here becomes an inflated resume.
> - **Append as you go** — add wins to the Log, fold up later.

---

## Summary
Backend-focused software engineer with 2+ years in production. Led backend development of an
LMS platform serving 50K+ users at C3iHub (IIT Kanpur), spanning event-driven microservices,
distributed tracing, and cloud infrastructure. Strong in Node.js, Python, Kafka, Redis, and AWS.
Experienced owning systems end-to-end across backend, DevOps, and AI integration.
Target lanes (equal priority): **Software Developer · Full-Stack Developer · Node.js Backend Developer** and adjacent backend/distributed-systems roles.

## Experience

### Software Development Engineer — C3iHub, IIT Kanpur · Jul 2025 – Present · Kanpur, India
- Architected core LMS backend serving 50K+ users across microservices for auth, notifications, and content delivery using Express.js, MongoDB, Redis, and Socket.IO, achieving 99.9% uptime at 10,000+ concurrent connections.
- Reduced cloud storage costs 60% (~Rs. 4.8L/year) via S3 Object Lock, Glacier Instant Retrieval, and a 2-tier S3 backup strategy; cut MongoDB p99 latency from 450ms → 135ms through compound indexing, horizontal sharding, and Redis caching.
- Engineered event-driven notification pipeline handling 75K+ daily events at 99.5% delivery reliability using Kafka, BullMQ, and Redis Pub/Sub — guaranteed at-least-once delivery with consumer-side deduplication.
- Improved incident response time 85% by deploying distributed tracing across 15+ services using OpenTelemetry, Prometheus, and Grafana; defined alerting SLOs across cross-functional teams.
- Led development of the official IITK hackathon platform onboarding 10K+ participants pan-India; productized into multi-tenant SaaS serving both public and private corporate deployments with RBAC.
- Built real-time collaborative round engine handling 2,000+ concurrent WebSocket sessions via Django Channels (ASGI) and Redis channel groups — idempotent submission handling and race-condition-safe team answer sync with timer-enforced auto-submit.

### Software Development Engineer — Playpower Labs · Nov 2024 – Jun 2025 · Remote
- Developed AI tutoring platform using Next.js with SSR/ISR and React Server Components alongside FastAPI microservices, supporting 500+ concurrent WebSocket sessions with sub-100ms response times.
- Increased user session depth by 35% by integrating ChromaDB vector search over 10K+ documents via a RAG pipeline, achieving sub-200ms retrieval latency at p95.
- Cut document retrieval latency by 47% (340ms to 180ms) with a PDF ingestion pipeline using 512-token chunking, OpenAI text-embedding-3-small, and HNSW-indexed ChromaDB.
- Reduced release cycle time by 65% by implementing blue-green CI/CD on AWS with GitHub Actions and automated rollback triggers for zero-downtime deployments.

## Projects

- **Autonomous Invoice Processing Platform** — Kafka, Redis Streams, FastAPI, PostgreSQL. Hackathon Winner. Event-driven platform automating invoice intake across 3 channels (Gmail API, WhatsApp Business API, Google Drive) with automated validation, deduplication, full audit trail. Fault-tolerant microservices with consumer groups, dead-letter queues, exponential backoff retry, RBAC-based human review workflow. GitHub: PrathamModi001/apex-invoice-processing
- **DeployMind: AI-Powered GitOps Platform** — Python, FastAPI, CrewAI, Redis, Docker, Kubernetes. Personal project. GitOps platform automating deployments from GitHub to EC2 and Kubernetes (EKS/GKE) via a 3-agent AI pipeline (security audit, build, deploy) using CrewAI, with conditional rollback on security gate failure. Rolling, Canary (graduated traffic shifting with auto-rollback), and Blue-Green deployment strategies with Redis-backed queue, distributed locking, 200+ unit/integration/E2E tests. GitHub: PrathamModi001/DeployMind
- **Mnemoniq: Multi-Tier Memory AI Agent** — FastAPI, LangGraph, PostgreSQL, Qdrant, Redis. Personal project. Three-tier memory system (working, episodic, knowledge graph) for a conversational AI agent orchestrated via a LangGraph multi-agent pipeline, cutting injected context tokens 38% versus naive full-history buffering. Qdrant/ChromaDB vector retrieval combined with NetworkX knowledge-graph traversal (Hebbian edge reinforcement, GraphRAG/HippoRAG-style scoring) behind a FastAPI + SSE backend with PostgreSQL and Redis-backed sessions; validated with a RAGAS-inspired eval harness across relevance, faithfulness, token efficiency. GitHub: PrathamModi001/Mnemoniq

## Education
- B.Tech, Computer Science and Engineering — Pandit Deendayal Energy University (2021–2025), GPA 9.20/10

## Skills (grouped)
- **Languages:** Python, JavaScript, TypeScript, Java, C++, SQL
- **Backend:** Node.js, Express.js, FastAPI, Socket.IO, RESTful APIs, WebSocket, GraphQL, Nginx
- **Frontend:** Next.js, React, Tailwind CSS
- **Databases:** PostgreSQL, MongoDB, Redis, DynamoDB
- **Messaging:** Kafka, BullMQ, Redis Streams, Redis Pub/Sub, Event-Driven Architecture
- **AI/ML:** Multi-Agent Systems (CrewAI, LangGraph), RAG Pipelines, Vector Databases (ChromaDB, Qdrant), Knowledge Graphs (NetworkX), LLM Integration
- **Cloud, DevOps & Observability:** AWS (EC2, S3, Lambda, EKS, IAM, ECR), Docker, Kubernetes, Terraform, GitHub Actions, CI/CD, OpenTelemetry, Prometheus, Grafana, Distributed Tracing
- **Architecture:** Microservices, Distributed Systems, System Design, Scalable Backend, High-Throughput Systems

## Achievements / Awards
- Hackathon Winner — Autonomous Invoice Processing Platform

## Publications
- Paper published at the 11th International Conference on Computing for Sustainable Global Development (INDIACom), 2024. IEEE Xplore: https://ieeexplore.ieee.org/document/10498330/
  - NEEDS CONFIRMATION: exact paper title, author order/position, co-authors — get from user before citing on any resume/CL.

## Certifications
[none on file yet — add if any]

## Load-Bearing Facts (pin the current numbers here; grep for stale copies before every send)
- GPA = 9.20/10 (Pandit Deendayal Energy University, B.Tech CSE)
- C3iHub LMS: 50K+ users, 99.9% uptime, 10,000+ concurrent connections
- C3iHub storage cost cut 60% (~Rs. 4.8L/year); MongoDB p99 450ms → 135ms
- C3iHub notification pipeline: 75K+ daily events, 99.5% delivery reliability
- C3iHub observability: incident response time down 85%, tracing across 15+ services
- C3iHub hackathon platform: 10K+ participants pan-India
- C3iHub collaborative engine: 2,000+ concurrent WebSocket sessions
- Playpower AI tutor: 500+ concurrent WebSocket sessions, sub-100ms responses
- Playpower RAG: session depth +35%, 10K+ documents, sub-200ms p95 retrieval
- Playpower ingestion: retrieval latency 340ms → 180ms (-47%)
- Playpower CI/CD: release cycle time -65%, blue-green zero-downtime
- Mnemoniq: context tokens -38% vs. naive full-history buffering
- DeployMind: 200+ unit/integration/E2E tests
- GitHub URL = https://github.com/PrathamModi001
- BASE resume source: user-provided LaTeX (Roboto font, single-column, sections: Summary/Experience/Projects/Technical Skills/Education) — port into resume_builder/templates/ as the FIXED base before first /make-resume run.

## Log (append new wins here, fold up later)
- 2026-09-09 Profile created from user-supplied LaTeX resume.
