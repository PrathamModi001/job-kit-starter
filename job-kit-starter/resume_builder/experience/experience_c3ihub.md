# Experience: Software Development Engineer — C3iHub, IIT Kanpur

**Dates (FIXED):** Jul 2025 – Present | **Location (FIXED):** Kanpur, India
**Position header rule:** Company line must always read "C3iHub, IIT Kanpur" in full — never abbreviate or drop "IIT Kanpur". It is a credibility signal for Indian recruiters/hiring managers. This is a hard rule from the hiring-manager audit (2026-09-14).

> **Bullet policy:** The bullet text below is COPY-EXACT — the canonical condensed
> rendering, already sized to fit a 2-line resume bullet and already proven to
> compile at 1 page. Do NOT rewrite, rephrase, or regenerate bullet prose.
> The only allowed operations per JD are: (1) SELECT which bullets to include,
> (2) ORDER them, (3) bold the specific tool tokens that match the JD's own
> vocabulary. Never change a number, a tool name, or a verb's ownership level.
> If a bullet must be shortened further to fit, only remove a trailing clause —
> never touch the quantified claim (the number).

---

### C1 — Core LMS backend at scale
**Tags:** node, express, mongodb, redis, socketio, microservices, scale, uptime, backend-core
**Bullet:** Architected core LMS backend serving 50K+ users across microservices using Express.js, MongoDB, Redis, and Socket.IO, sustaining 99.9% uptime at 10,000+ concurrent connections.

### C2 — Cost + latency optimization
**Tags:** aws, s3, mongodb, performance, latency, cost-optimization, indexing, sharding, redis
**Bullet:** Reduced cloud storage costs 60% (~Rs. 4.8L/year) via S3 Object Lock and Glacier; cut MongoDB p99 latency from 450ms to 135ms via compound indexing, sharding, and Redis caching.

### C3 — Event-driven messaging
**Tags:** kafka, bullmq, redis-pubsub, event-driven, messaging, reliability, distributed-systems
**Bullet:** Engineered event-driven notification pipeline handling 75K+ daily events at 99.5% delivery reliability using Kafka, BullMQ, and Redis Pub/Sub with consumer-side deduplication.

### C4 — Observability
**Tags:** opentelemetry, prometheus, grafana, observability, distributed-tracing, sre, incident-response
**Bullet:** Improved incident response time 85% by deploying distributed tracing across 15+ services using OpenTelemetry, Prometheus, and Grafana with defined SLO alerts.

### C5 — National-scale platform + leadership (HIGH-VALUE, currently underused — see audit note)
**Tags:** leadership, platform-ownership, saas, multi-tenant, rbac, scale, product
**Bullet:** Led development of the official IITK hackathon platform onboarding 10K+ participants pan-India; productized into multi-tenant SaaS serving both public and private corporate deployments with RBAC.
**Audit note:** This is the strongest leadership + national-scale + full-ownership signal in the entire profile. It was absent from both resumes actually sent (Wells Fargo, Avoca) per the 2026-09-14 audit. Default to including it for Backend and Full-Stack lanes unless the bundle's Priority Matrix explicitly ranks it below the budget cutoff for a specific JD.

### C6 — Real-time collaborative feature
**Tags:** websocket, django-channels, real-time, concurrency, race-condition-safety
**Bullet (condensed — full version exceeds 2-line budget, condensed here, fact-preserving):** Built real-time collaborative round engine handling 2,000+ concurrent WebSocket sessions via Django Channels and Redis channel groups, with idempotent, race-condition-safe submission sync.
**Full/uncondensed version (source of truth for facts only, do not use verbatim on resume — too long):** Built real-time collaborative round engine handling 2,000+ concurrent WebSocket sessions via Django Channels (ASGI) and Redis channel groups — idempotent submission handling and race-condition-safe team answer sync with timer-enforced auto-submit.
