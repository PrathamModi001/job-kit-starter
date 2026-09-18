# Bundle: Backend / Node.js / Distributed Systems Lane

Use for JDs titled: Backend Engineer, Node.js Developer, Distributed Systems Engineer,
Platform Engineer, SDE (backend-heavy), Software Developer where the JD body is
backend/infra-heavy with little/no frontend requirement.

---

## 1. Tagline Formula

`Software Engineer | Backend & Distributed Systems | [Tool1], [Tool2], [Tool3], [Tool4]`

Tool1-4 selection rule: pick the 4 tools from this APPROVED POOL that appear in the
JD text, in the order they appear in the JD. If fewer than 4 JD tools match the pool,
fill remaining slots in this default priority order: Node.js, Kafka, Redis, AWS, PostgreSQL.

**Approved pool (from SKILL_PROFILE.md — never add a tool not in this list):**
Node.js, Express.js, Kafka, Redis, MongoDB, PostgreSQL, AWS, Docker, Kubernetes,
Microservices, WebSocket, OpenTelemetry.

---

## 2. Summary (copy-exact, minor trims only)

Backend-focused software engineer with 2+ years in production. Led backend development of an event-driven LMS platform serving 50K+ users at C3iHub (IIT Kanpur), spanning microservices, distributed tracing, and cloud infrastructure. Strong in Node.js, Kafka, Redis, and AWS, with a track record of cutting latency and infrastructure cost while scaling systems to 10,000+ concurrent connections.

---

## 3. Experience Priority Matrix

### C3iHub, IIT Kanpur (pick 4 of 6 — see rationale)
| Rank | ID | Achievement | Priority |
|---|---|---|---|
| 1 | C1 | Core LMS backend at scale | HIGH |
| 2 | C3 | Event-driven Kafka pipeline | HIGH |
| 3 | C4 | Observability / incident response | HIGH |
| 4 | C5 | National-scale platform + leadership | HIGH |
| 5 | C2 | Cost + latency optimization | MEDIUM — swap in for C4 if JD emphasizes AWS cost/perf over observability tooling |
| — | C6 | Real-time WebSocket feature | LOW — omit for this lane; Django Channels reads as tangential to a Node-centric backend story |

**Rationale (hiring-manager audit, 2026-09-14):** C5 was missing from every resume sent so far despite being the strongest leadership+scale signal in the profile. It is HIGH by default for this lane — do not drop it without a specific reason logged in the session file.

### Playpower Labs (pick 3-4 of 4)
| Rank | ID | Achievement | Priority |
|---|---|---|---|
| 1 | PP4 | CI/CD / release engineering | HIGH |
| 2 | PP1 (Variant A) | AI tutoring platform, backend framing | MEDIUM |
| 3 | PP2 | RAG retrieval | LOW — cap: at most 1 AI-specific bullet (PP2 or PP3, not both) for this lane |
| — | PP3 | Ingestion pipeline | LOW — mutually exclusive with PP2, see cap above |

**Cap rule:** Never include more than 1 of {PP2, PP3} in a Backend-lane resume. Two AI/RAG bullets on a backend-titled application reads as unfocused to the hiring manager (audit finding).

### Projects (pick 2 of 3)
| Rank | ID | Priority |
|---|---|---|
| 1 | PJ1 (Invoice Processing) | HIGH |
| 2 | PJ2 (DeployMind) | HIGH |
| 3 | PJ3 (Mnemoniq) | LOW — omit unless JD explicitly values AI/agent systems as a plus |

---

## 4. Skills Group Order

1. Backend (Node.js, Express.js, FastAPI, WebSocket, REST APIs)
2. Databases (PostgreSQL, MongoDB, Redis, DynamoDB)
3. Messaging (Kafka, BullMQ, Redis Streams, Event-Driven Architecture)
4. Cloud, DevOps & Observability
5. Architecture (Microservices, Distributed Systems, System Design)

Bold only the tokens that literally appear in the JD text.
