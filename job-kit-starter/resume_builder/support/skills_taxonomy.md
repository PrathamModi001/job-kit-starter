# Skills Taxonomy

> Single source of truth for what skills exist. Copied directly from
> `SKILL_PROFILE.md` Skills section — never add a skill here that isn't
> already listed there. Group ORDER is chosen per-lane by the bundle file;
> this file only defines group CONTENTS.

- **Languages:** Python, JavaScript, TypeScript, Java, C++, SQL
- **Backend:** Node.js, Express.js, FastAPI, Socket.IO, RESTful APIs, WebSocket, GraphQL, Nginx
- **Frontend:** Next.js, React, Tailwind CSS
- **Databases:** PostgreSQL, MongoDB, Redis, DynamoDB
- **Messaging:** Kafka, BullMQ, Redis Streams, Redis Pub/Sub, Event-Driven Architecture
- **AI/ML:** Multi-Agent Systems (CrewAI, LangGraph), RAG Pipelines, Vector Databases (ChromaDB, Qdrant), Knowledge Graphs (NetworkX), LLM Integration
- **Cloud, DevOps & Observability:** AWS (EC2, S3, Lambda, EKS, IAM, ECR), Docker, Kubernetes, Terraform, GitHub Actions, CI/CD, OpenTelemetry, Prometheus, Grafana, Distributed Tracing
- **Architecture:** Microservices, Distributed Systems, System Design, Scalable Backend, High-Throughput Systems

## Bolding rule

Bold a skill token in the Technical Skills section ONLY if it appears (verbatim or as an
obvious synonym, e.g. "Postgres" = PostgreSQL) in the current JD text. Never bold based
on how important the skill is to the candidate — bold is a JD-match signal, not a
self-assessment.

## Demonstrated vs. listed-only skills

Every skill above except the following is backed by at least one bullet in
`resume_builder/experience/`. Flagged skills are listed-only (true skills the
candidate has, but not shown in a resume bullet):

- **TypeScript** — see `achievement_reframing_guide.md` Known Gaps. Do not claim
  project ownership in prose; keep it in the skills list only, or bridge honestly.
- **GraphQL** — same treatment: list only, no bullet currently demonstrates it.
- **Terraform** — list only.
