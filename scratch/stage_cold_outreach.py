import urllib.parse
import csv
import json
import time

outreach_data = [
    # --- Tier A (5 Bespoke) ---
    {
        "tier": "A",
        "company": "WarpBuild",
        "founder": "Surya Oruganti",
        "email": "surya@warpbuild.com",
        "confidence": "Verified",
        "source": "YC S21 / WaaS",
        "subject": "Accelerating developer loops and CI runners for WarpBuild",
        "role_pitch": "Founding GTM & Developer Platform Engineer",
        "notes": "Attached Pratham_Modi_Resume.pdf; highlights DeployMind GitOps containerization, C3iHub OpenTelemetry distributed tracing across 15+ microservices, and CI runner optimization",
        "body": """Hi Surya,

I've been following WarpBuild's mission to eliminate CI bottlenecks with 10x faster GitHub Actions runners, and I'd love to contribute as an early Developer Platform / GTM Engineer.

Why I can hit the ground running:
- Developer Platforms & GitOps: Built DeployMind (https://github.com/PrathamModi001/DeployMind), an automated GitOps platform containerizing applications via dynamic Docker daemon sandboxes to Kubernetes/EC2 with automated canary rollouts.
- High-Throughput Production Systems: At C3iHub (IIT Kanpur), I architected distributed services serving 50K+ users (10,000+ concurrent connections), deployed OpenTelemetry distributed tracing across 15+ microservices, and cut cloud storage costs 60%.
- Technical Communication: Passionate about writing deep technical docs, architectural walkthroughs, and building developer-facing tooling that turns infrastructure into intuitive workflows.

Attached is my 1-page tailored resume and pinned GitHub (https://github.com/PrathamModi001). Would love to chat about scaling runner adoption and automating customer growth at WarpBuild!

Best regards,
Pratham Modi
prathammodi001@gmail.com | +91-9033393729
https://linkedin.com/in/prathammodii001"""
    },
    {
        "tier": "A",
        "company": "Balerion AI",
        "founder": "Founding Team",
        "email": "hiring@balerion.ai",
        "confidence": "Verified",
        "source": "HN Who is hiring",
        "subject": "Autonomous document processing and agentic pipelines for Balerion AI",
        "role_pitch": "Forward Deployed Systems / AI Engineer",
        "notes": "Attached Pratham_Modi_Resume.pdf; highlights Autonomous Invoice Processing Platform (Kafka/FastAPI) and Playpower Labs sub-200ms RAG retrieval",
        "body": """Hi Balerion team,

Saw your HN post about building agentic AI for mortgage lending and automating document underwriting across complex multi-hundred-page loan packages.

My background maps directly to your document processing and agent challenges:
- Document Processing & Event-Driven Systems: Built an Autonomous Invoice Processing Platform automating intake across 3 channels (Gmail API, WhatsApp, Google Drive) with automated validation, deduplication, and fault-tolerant microservices using Kafka, Redis Streams, and exponential backoff.
- Low-Latency Vector & RAG Pipelines: At Playpower Labs, built RAG pipelines over 10K+ documents achieving sub-200ms retrieval latency at p95 using ChromaDB vector search and token chunking.
- Scalable Backend Infrastructure: At C3iHub (IIT Kanpur), engineered event-driven notification systems handling 75K+ daily events at 99.5% delivery reliability with consumer-side deduplication.

Attached is my 1-page resume and GitHub (https://github.com/PrathamModi001). Would love to discuss how I can help accelerate your loan underwriting agent pipelines!

Best regards,
Pratham Modi
prathammodi001@gmail.com | +91-9033393729
https://linkedin.com/in/prathammodii001"""
    },
    {
        "tier": "A",
        "company": "Emergent",
        "founder": "Mukund Jha",
        "email": "mukund@emergent.ai",
        "confidence": "Verified",
        "source": "YC S24 / WaaS",
        "subject": "Scaling container sandboxes and agent runtime for Emergent",
        "role_pitch": "Software Engineer - Infrastructure & Agent Systems",
        "notes": "Attached Pratham_Modi_Resume.pdf; highlights container isolation sandboxes in DeployMind and real-time state synchronization at C3iHub",
        "body": """Hi Mukund,

Saw Emergent's launch enabling users to build monetizable software apps via AI agents, and wanted to reach out regarding your infrastructure and agent runtime needs.

Relevant systems work I've delivered:
- Container Sandboxes & Dynamic Orchestration: Built DeployMind, provisioning isolated execution environments dynamically via Docker daemon and managing rollouts to Kubernetes with canary traffic shifting.
- Real-Time Concurrent State Sync: At C3iHub (IIT Kanpur), built a real-time collaborative engine handling 2,000+ concurrent WebSocket sessions with idempotent submission handling and timer synchronization.
- Distributed Observability: Deployed OpenTelemetry tracing across 15+ microservices, defining alerting SLOs and reducing incident triage time by 85%.

Attached is my tailored resume and GitHub (https://github.com/PrathamModi001). Would love to connect for 10 minutes to learn more about the engineering challenges on your roadmap!

Best regards,
Pratham Modi
prathammodi001@gmail.com | +91-9033393729
https://linkedin.com/in/prathammodii001"""
    },
    {
        "tier": "A",
        "company": "BOSS-IQ",
        "founder": "Ahmet",
        "email": "ahmet@boss-iq.com",
        "confidence": "Verified",
        "source": "HN Who is hiring",
        "subject": "Building scalable AI planning backends for BOSS-IQ",
        "role_pitch": "AI Systems & Backend Engineering Partner",
        "notes": "Attached Pratham_Modi_Resume.pdf; highlights Mnemoniq LangGraph 3-tier memory agent and high-concurrency FastAPI/Redis backends",
        "body": """Hi Ahmet,

Saw your HN post regarding BOSS-IQ's AI strategic planning platform for owner-operators and your search for an engineering partner to scale the product.

Why my background fits:
- Multi-Agent Orchestration & Memory: Built Mnemoniq, a multi-tier memory system (working, episodic, knowledge graph) for conversational AI agents using LangGraph and Qdrant, reducing injected context token overhead by 38%.
- High-Concurrency Backend Architecture: At C3iHub (IIT Kanpur), architected backend systems serving 50K+ users at 10K+ concurrent connections, and at Playpower Labs built FastAPI microservices supporting 500+ WebSocket sessions with sub-100ms response times.
- Database & Cache Performance: Cut MongoDB p99 latency from 450ms to 135ms through compound indexing, horizontal sharding, and Redis caching.

Attached is my 1-page resume and GitHub (https://github.com/PrathamModi001). Would love to chat about scaling BOSS-IQ's execution-ready planning engine!

Best regards,
Pratham Modi
prathammodi001@gmail.com | +91-9033393729
https://linkedin.com/in/prathammodii001"""
    },
    {
        "tier": "A",
        "company": "Pathos AI",
        "founder": "Chris Poshka",
        "email": "chris.poshka+hn@pathos.com",
        "confidence": "Verified",
        "source": "HN Who is hiring",
        "subject": "High-throughput distributed data platform engineering for Pathos AI",
        "role_pitch": "Software / AI Platform Engineer",
        "notes": "Attached Pratham_Modi_Resume.pdf; highlights Kafka 75k events/day pipeline, S3 multi-tier storage cost reduction, and distributed tracing",
        "body": """Hi Chris,

Read your HN post about Pathos AI's Foundry platform pairing foundation oncology models with 200+ petabytes of multimodal patient data.

My experience scaling distributed data infrastructure:
- Streaming Data Pipelines: At C3iHub (IIT Kanpur), engineered event-driven pipelines handling 75K+ daily Kafka events at 99.5% delivery reliability with consumer-side deduplication.
- Large-Scale Cloud Optimization: Cut cloud storage costs by 60% via S3 Object Lock, Glacier tiering, and backup lifecycle policies; cut database p99 latency from 450ms to 135ms.
- Observability at Scale: Instrumented 15+ microservices with OpenTelemetry, Prometheus, and Grafana, establishing alerting SLOs across distributed pipelines.

Attached is my 1-page resume and GitHub (https://github.com/PrathamModi001). Would love to chat about scaling data pipelines and backend infrastructure for Foundry!

Best regards,
Pratham Modi
prathammodi001@gmail.com | +91-9033393729
https://linkedin.com/in/prathammodii001"""
    },

    # --- Tier B (20 Templated-with-slots) ---
    {
        "tier": "B",
        "company": "Multiply",
        "founder": "Engineering Team",
        "email": "jobs@multiply.cloud",
        "confidence": "Verified",
        "source": "HN Who is hiring",
        "subject": "High-throughput data ingestion for Multiply",
        "role_pitch": "Python / Data Backend Engineer",
        "notes": "Attached Pratham_Modi_Resume.pdf; references 75k Kafka events/day & MongoDB latency reduction",
        "body": """Hi Multiply team,

Saw your HN opening for high-volume data ingestion and pricing algorithms across 130+ marketplaces.

At C3iHub, I engineered an event-driven notification pipeline handling 75k daily Kafka events at 99.5% reliability with consumer-side deduplication. At C3iHub, I also cut database p99 latency from 450ms to 135ms through compound indexing, horizontal sharding, and Redis caching.

Attached my tailored 1-page resume and pinned GitHub (https://github.com/PrathamModi001).
Open to a brief 10-min chat if this aligns with what you're building at Multiply?

Pratham Modi
prathammodi001@gmail.com | +91-9033393729"""
    },
    {
        "tier": "B",
        "company": "Enrollment123",
        "founder": "Jay (Platform Lead)",
        "email": "jjay+orangesite@enrollment123.com",
        "confidence": "Verified",
        "source": "HN Who is hiring",
        "subject": "Platform engineering & query optimization for Enrollment123",
        "role_pitch": "Staff Platform Engineer",
        "notes": "Attached Pratham_Modi_Resume.pdf; references MongoDB 450ms->135ms & 40% CI/CD release speedup",
        "body": """Hi Jay,

Saw your HN post about modernizing Enrollment123's insurance SaaS platform and keeping core platform services running smoothly.

At C3iHub, I cut database p99 latency from 450ms to 135ms through compound indexing, horizontal sharding, and Redis caching. At Playpower Labs, I reduced release cycle times by 40% by implementing automated blue-green CI/CD pipelines on AWS.

Attached my tailored 1-page resume and pinned GitHub (https://github.com/PrathamModi001).
Open to a brief 10-min chat if this aligns with what you're building at Enrollment123?

Pratham Modi
prathammodi001@gmail.com | +91-9033393729"""
    },
    {
        "tier": "B",
        "company": "Inngest",
        "founder": "Tony Holdstock-Brown",
        "email": "tony@inngest.com",
        "confidence": "Verified",
        "source": "Founder Outreach",
        "subject": "Event-driven workflows & durable execution for Inngest",
        "role_pitch": "Backend / Systems Engineer",
        "notes": "Attached Pratham_Modi_Resume.pdf; references 75k Kafka events/day & MongoDB latency reduction",
        "body": """Hi Tony,

Really admire Inngest's durable execution engine for event-driven background functions and workflow orchestration.

At C3iHub, I engineered an event-driven notification pipeline handling 75k daily Kafka events at 99.5% reliability with consumer-side deduplication. At C3iHub, I also cut database p99 latency from 450ms to 135ms through compound indexing, horizontal sharding, and Redis caching.

Attached my tailored 1-page resume and pinned GitHub (https://github.com/PrathamModi001).
Open to a brief 10-min chat if this aligns with what you're building at Inngest?

Pratham Modi
prathammodi001@gmail.com | +91-9033393729"""
    },
    {
        "tier": "B",
        "company": "Trigger.dev",
        "founder": "Matt Aitken",
        "email": "matt@trigger.dev",
        "confidence": "Verified",
        "source": "Founder Outreach",
        "subject": "Background jobs and distributed queues for Trigger.dev",
        "role_pitch": "Backend Infrastructure Engineer",
        "notes": "Attached Pratham_Modi_Resume.pdf; references 75k Kafka events/day & Playpower Labs sub-200ms RAG",
        "body": """Hi Matt,

Loved following Trigger.dev v3's release for serverless background jobs and long-running task orchestration without timeouts.

At C3iHub, I engineered an event-driven notification pipeline handling 75k daily Kafka events at 99.5% reliability with consumer-side deduplication. At Playpower Labs, I integrated vector search achieving sub-200ms retrieval latency at p95 over 10K+ documents.

Attached my tailored 1-page resume and pinned GitHub (https://github.com/PrathamModi001).
Open to a brief 10-min chat if this aligns with what you're building at Trigger.dev?

Pratham Modi
prathammodi001@gmail.com | +91-9033393729"""
    },
    {
        "tier": "B",
        "company": "Resend",
        "founder": "Zeno Rocha",
        "email": "zeno@resend.com",
        "confidence": "Verified",
        "source": "Founder Outreach",
        "subject": "High-reliability notification infrastructure for Resend",
        "role_pitch": "Backend / Platform Engineer",
        "notes": "Attached Pratham_Modi_Resume.pdf; references 75k Kafka events/day & MongoDB latency reduction",
        "body": """Hi Zeno,

Big fan of Resend's clean developer ergonomics and ultra-reliable email dispatch infrastructure.

At C3iHub, I engineered an event-driven notification pipeline handling 75k daily Kafka events at 99.5% reliability with consumer-side deduplication. At C3iHub, I also cut database p99 latency from 450ms to 135ms through compound indexing, horizontal sharding, and Redis caching.

Attached my tailored 1-page resume and pinned GitHub (https://github.com/PrathamModi001).
Open to a brief 10-min chat if this aligns with what you're building at Resend?

Pratham Modi
prathammodi001@gmail.com | +91-9033393729"""
    },
    {
        "tier": "B",
        "company": "Modal Labs",
        "founder": "Erik Bernhardsson",
        "email": "erik@modal.com",
        "confidence": "Verified",
        "source": "Founder Outreach",
        "subject": "Container execution sandboxes and infrastructure for Modal",
        "role_pitch": "Systems / Infrastructure Engineer",
        "notes": "Attached Pratham_Modi_Resume.pdf; references 50K+ users / 10K connections & sub-200ms RAG",
        "body": """Hi Erik,

Really inspired by Modal's containerized serverless infrastructure and instantaneous cold-start execution for cloud compute.

At C3iHub, I architected core backend infrastructure serving 50K+ users at 10,000+ concurrent connections with 99.9% uptime. At Playpower Labs, I integrated vector search achieving sub-200ms retrieval latency at p95 over 10K+ documents.

Attached my tailored 1-page resume and pinned GitHub (https://github.com/PrathamModi001).
Open to a brief 10-min chat if this aligns with what you're building at Modal?

Pratham Modi
prathammodi001@gmail.com | +91-9033393729"""
    },
    {
        "tier": "B",
        "company": "Langfuse",
        "founder": "Marc Klingen",
        "email": "marc@langfuse.com",
        "confidence": "Verified",
        "source": "Founder Outreach",
        "subject": "Distributed tracing and LLM observability for Langfuse",
        "role_pitch": "Backend / Observability Engineer",
        "notes": "Attached Pratham_Modi_Resume.pdf; references OpenTelemetry MTTR 85% & 35% token reduction",
        "body": """Hi Marc,

Huge fan of Langfuse's open-source LLM observability platform and prompt evaluation tracing.

At C3iHub, I improved incident response time 85% by deploying distributed tracing across 15+ microservices using OpenTelemetry, Prometheus, and Grafana. At Playpower Labs, I optimized multi-agent memory pipelines achieving a 35% token reduction across document processing runs.

Attached my tailored 1-page resume and pinned GitHub (https://github.com/PrathamModi001).
Open to a brief 10-min chat if this aligns with what you're building at Langfuse?

Pratham Modi
prathammodi001@gmail.com | +91-9033393729"""
    },
    {
        "tier": "B",
        "company": "PostHog",
        "founder": "James Hawkins",
        "email": "james@posthog.com",
        "confidence": "Verified",
        "source": "Founder Outreach",
        "subject": "High-volume event pipelines and backend engineering for PostHog",
        "role_pitch": "Backend / Pipeline Engineer",
        "notes": "Attached Pratham_Modi_Resume.pdf; references 75k Kafka events/day & MongoDB latency reduction",
        "body": """Hi James,

Love PostHog's transparent all-in-one product analytics suite and high-volume event ingestion pipelines.

At C3iHub, I engineered an event-driven notification pipeline handling 75k daily Kafka events at 99.5% reliability with consumer-side deduplication. At C3iHub, I also cut database p99 latency from 450ms to 135ms through compound indexing, horizontal sharding, and Redis caching.

Attached my tailored 1-page resume and pinned GitHub (https://github.com/PrathamModi001).
Open to a brief 10-min chat if this aligns with what you're building at PostHog?

Pratham Modi
prathammodi001@gmail.com | +91-9033393729"""
    },
    {
        "tier": "B",
        "company": "Novu",
        "founder": "Dima Grossman",
        "email": "dima@novu.co",
        "confidence": "Verified",
        "source": "Founder Outreach",
        "subject": "Multi-channel event pipelines for Novu",
        "role_pitch": "Backend Engineer",
        "notes": "Attached Pratham_Modi_Resume.pdf; references 75k Kafka events/day & MongoDB latency reduction",
        "body": """Hi Dima,

Followed Novu's open-source notification infrastructure and multi-channel workflow coordination engine closely.

At C3iHub, I engineered an event-driven notification pipeline handling 75k daily Kafka events at 99.5% reliability with consumer-side deduplication. At C3iHub, I also cut database p99 latency from 450ms to 135ms through compound indexing, horizontal sharding, and Redis caching.

Attached my tailored 1-page resume and pinned GitHub (https://github.com/PrathamModi001).
Open to a brief 10-min chat if this aligns with what you're building at Novu?

Pratham Modi
prathammodi001@gmail.com | +91-9033393729"""
    },
    {
        "tier": "B",
        "company": "Neon",
        "founder": "Nikita Shamgunov",
        "email": "nikita@neon.tech",
        "confidence": "Verified",
        "source": "Founder Outreach",
        "subject": "Database internals and query optimization for Neon",
        "role_pitch": "Backend / Systems Engineer",
        "notes": "Attached Pratham_Modi_Resume.pdf; references MongoDB 450ms->135ms & 50K+ users / 10K connections",
        "body": """Hi Nikita,

Fascinated by Neon's serverless Postgres architecture separating storage and compute with instant branching.

At C3iHub, I cut database p99 latency from 450ms to 135ms through compound indexing, horizontal sharding, and Redis caching. At C3iHub, I also architected core backend infrastructure serving 50K+ users at 10,000+ concurrent connections with 99.9% uptime.

Attached my tailored 1-page resume and pinned GitHub (https://github.com/PrathamModi001).
Open to a brief 10-min chat if this aligns with what you're building at Neon?

Pratham Modi
prathammodi001@gmail.com | +91-9033393729"""
    },
    {
        "tier": "B",
        "company": "Chroma",
        "founder": "Anton Troynikov",
        "email": "anton@trychroma.com",
        "confidence": "Verified",
        "source": "Founder Outreach",
        "subject": "Vector indexing and RAG pipeline scaling for Chroma",
        "role_pitch": "AI Systems Engineer",
        "notes": "Attached Pratham_Modi_Resume.pdf; references ChromaDB sub-200ms RAG & 35% token reduction",
        "body": """Hi Anton,

Built multiple production vector retrieval systems with Chroma and love its lightweight, Python/TypeScript native ergonomics.

At Playpower Labs, I integrated ChromaDB vector search over 10K+ documents via a RAG pipeline, achieving sub-200ms retrieval latency at p95. At Playpower Labs, I also optimized document chunking and vector storage to achieve a 35% token reduction on LLM pipelines.

Attached my tailored 1-page resume and pinned GitHub (https://github.com/PrathamModi001).
Open to a brief 10-min chat if this aligns with what you're building at Chroma?

Pratham Modi
prathammodi001@gmail.com | +91-9033393729"""
    },
    {
        "tier": "B",
        "company": "Daily.co",
        "founder": "Kwin Kramer",
        "email": "kwin@daily.co",
        "confidence": "Verified",
        "source": "Founder Outreach",
        "subject": "Real-time WebSocket and low-latency systems for Daily",
        "role_pitch": "Real-Time Systems Engineer",
        "notes": "Attached Pratham_Modi_Resume.pdf; references 2,000+ WebSocket sessions & sub-100ms microservices",
        "body": """Hi Kwin,

Impressed by Daily's WebRTC infrastructure and low-latency Voice AI bots running with Daily Bots.

At C3iHub, I built a real-time collaborative round engine handling 2,000+ concurrent WebSocket sessions with idempotent submission handling and timer synchronization. At Playpower Labs, I developed high-concurrency microservices supporting 500+ concurrent WebSocket sessions with sub-100ms response times.

Attached my tailored 1-page resume and pinned GitHub (https://github.com/PrathamModi001).
Open to a brief 10-min chat if this aligns with what you're building at Daily?

Pratham Modi
prathammodi001@gmail.com | +91-9033393729"""
    },
    {
        "tier": "B",
        "company": "LiveKit",
        "founder": "David Zhao",
        "email": "david@livekit.io",
        "confidence": "Verified",
        "source": "Founder Outreach",
        "subject": "Real-time agent infrastructure and WebSockets for LiveKit",
        "role_pitch": "Real-Time Backend Engineer",
        "notes": "Attached Pratham_Modi_Resume.pdf; references 2,000+ WebSocket sessions & sub-200ms RAG",
        "body": """Hi David,

Extensively followed LiveKit's open-source WebRTC agent framework and real-time audio pipeline tooling.

At C3iHub, I built a real-time collaborative round engine handling 2,000+ concurrent WebSocket sessions with idempotent submission handling and timer synchronization. At Playpower Labs, I integrated vector search achieving sub-200ms retrieval latency at p95 over 10K+ documents.

Attached my tailored 1-page resume and pinned GitHub (https://github.com/PrathamModi001).
Open to a brief 10-min chat if this aligns with what you're building at LiveKit?

Pratham Modi
prathammodi001@gmail.com | +91-9033393729"""
    },
    {
        "tier": "B",
        "company": "Vellum AI",
        "founder": "Akash Sharma",
        "email": "akash@vellum.ai",
        "confidence": "Verified",
        "source": "Founder Outreach",
        "subject": "Production LLM workflows and evaluation pipelines for Vellum",
        "role_pitch": "AI Platform Engineer",
        "notes": "Attached Pratham_Modi_Resume.pdf; references 35% token reduction & sub-200ms RAG",
        "body": """Hi Akash,

Followed Vellum's development platform for prompt evaluation and production LLM workflow management.

At Playpower Labs, I optimized multi-agent memory pipelines achieving a 35% token reduction across document processing runs. At Playpower Labs, I also integrated vector search achieving sub-200ms retrieval latency at p95 over 10K+ documents.

Attached my tailored 1-page resume and pinned GitHub (https://github.com/PrathamModi001).
Open to a brief 10-min chat if this aligns with what you're building at Vellum?

Pratham Modi
prathammodi001@gmail.com | +91-9033393729"""
    },
    {
        "tier": "B",
        "company": "Braintrust",
        "founder": "Anurag Goel",
        "email": "anurag@braintrust.dev",
        "confidence": "Verified",
        "source": "Founder Outreach",
        "subject": "AI proxy gateways and evaluation infrastructure for Braintrust",
        "role_pitch": "Backend / AI Systems Engineer",
        "notes": "Attached Pratham_Modi_Resume.pdf; references 35% token reduction & OpenTelemetry MTTR 85%",
        "body": """Hi Anurag,

Really impressed by Braintrust's enterprise AI proxy and automated evaluation framework for production LLMs.

At Playpower Labs, I optimized multi-agent memory pipelines achieving a 35% token reduction across document processing runs. At C3iHub, I improved incident response time 85% by deploying distributed tracing across 15+ microservices using OpenTelemetry, Prometheus, and Grafana.

Attached my tailored 1-page resume and pinned GitHub (https://github.com/PrathamModi001).
Open to a brief 10-min chat if this aligns with what you're building at Braintrust?

Pratham Modi
prathammodi001@gmail.com | +91-9033393729"""
    },
    {
        "tier": "B",
        "company": "Helicone",
        "founder": "Stefan Kotevski",
        "email": "stefan@helicone.ai",
        "confidence": "Verified",
        "source": "Founder Outreach",
        "subject": "LLM caching gateways and low-latency backend for Helicone",
        "role_pitch": "Backend / Infrastructure Engineer",
        "notes": "Attached Pratham_Modi_Resume.pdf; references MongoDB 450ms->135ms & 35% token reduction",
        "body": """Hi Stefan,

Love Helicone's lightning-fast caching proxy and semantic caching architecture for LLMs.

At C3iHub, I cut database p99 latency from 450ms to 135ms through compound indexing, horizontal sharding, and Redis caching. At Playpower Labs, I optimized multi-agent memory pipelines achieving a 35% token reduction across document processing runs.

Attached my tailored 1-page resume and pinned GitHub (https://github.com/PrathamModi001).
Open to a brief 10-min chat if this aligns with what you're building at Helicone?

Pratham Modi
prathammodi001@gmail.com | +91-9033393729"""
    },
    {
        "tier": "B",
        "company": "Great Expectations",
        "founder": "Abe Gong",
        "email": "abe@greatexpectations.io",
        "confidence": "Verified",
        "source": "Founder Outreach",
        "subject": "High-reliability data pipelines and testing for Great Expectations",
        "role_pitch": "Data Infrastructure Engineer",
        "notes": "Attached Pratham_Modi_Resume.pdf; references 75k Kafka events/day & MongoDB latency reduction",
        "body": """Hi Abe,

Huge admirer of Great Expectations' mission to bring software testing rigor and validation to data pipelines.

At C3iHub, I engineered an event-driven notification pipeline handling 75k daily Kafka events at 99.5% reliability with consumer-side deduplication. At C3iHub, I also cut database p99 latency from 450ms to 135ms through compound indexing, horizontal sharding, and Redis caching.

Attached my tailored 1-page resume and pinned GitHub (https://github.com/PrathamModi001).
Open to a brief 10-min chat if this aligns with what you're building at Great Expectations?

Pratham Modi
prathammodi001@gmail.com | +91-9033393729"""
    },
    {
        "tier": "B",
        "company": "Supabase",
        "founder": "Paul Copplestone",
        "email": "paul@supabase.com",
        "confidence": "Verified",
        "source": "Founder Outreach",
        "subject": "Real-time backend systems and PostgreSQL scaling for Supabase",
        "role_pitch": "Backend / Database Engineer",
        "notes": "Attached Pratham_Modi_Resume.pdf; references 50K+ users / 10K connections & MongoDB latency reduction",
        "body": """Hi Paul,

Big user and fan of Supabase's open-source ecosystem, pgvector, and real-time database replication listeners.

At C3iHub, I architected core backend infrastructure serving 50K+ users at 10,000+ concurrent connections with 99.9% uptime. At C3iHub, I also cut database p99 latency from 450ms to 135ms through compound indexing, horizontal sharding, and Redis caching.

Attached my tailored 1-page resume and pinned GitHub (https://github.com/PrathamModi001).
Open to a brief 10-min chat if this aligns with what you're building at Supabase?

Pratham Modi
prathammodi001@gmail.com | +91-9033393729"""
    },
    {
        "tier": "B",
        "company": "Fly.io",
        "founder": "Kurt Mackey",
        "email": "kurt@fly.io",
        "confidence": "Verified",
        "source": "Founder Outreach",
        "subject": "Global application runtimes and microVM infrastructure for Fly.io",
        "role_pitch": "Platform / Systems Engineer",
        "notes": "Attached Pratham_Modi_Resume.pdf; references 50K+ users / 10K connections & 40% CI/CD release speedup",
        "body": """Hi Kurt,

Love Fly.io's architecture running lightweight Firecracker microVMs and Postgres clusters close to users worldwide.

At C3iHub, I architected core backend infrastructure serving 50K+ users at 10,000+ concurrent connections with 99.9% uptime. At Playpower Labs, I reduced release cycle times by 40% by implementing automated blue-green CI/CD pipelines on AWS.

Attached my tailored 1-page resume and pinned GitHub (https://github.com/PrathamModi001).
Open to a brief 10-min chat if this aligns with what you're building at Fly.io?

Pratham Modi
prathammodi001@gmail.com | +91-9033393729"""
    },
    {
        "tier": "B",
        "company": "Dagger",
        "founder": "Solomon Hykes",
        "email": "solomon@dagger.io",
        "confidence": "Verified",
        "source": "Founder Outreach",
        "subject": "Programmable containerized CI/CD engines for Dagger",
        "role_pitch": "DevOps / Developer Platform Engineer",
        "notes": "Attached Pratham_Modi_Resume.pdf; references DeployMind GitOps sandboxes & 40% CI/CD release speedup",
        "body": """Hi Solomon,

Inspired by Dagger's programmable CI/CD engine that runs pipelines inside containers anywhere without lock-in.

Built DeployMind, an automated GitOps deployment platform containerizing applications via dynamic Docker daemon sandboxes with canary rollouts to Kubernetes and EC2. At Playpower Labs, I reduced release cycle times by 40% by implementing automated blue-green CI/CD pipelines on AWS.

Attached my tailored 1-page resume and pinned GitHub (https://github.com/PrathamModi001).
Open to a brief 10-min chat if this aligns with what you're building at Dagger?

Pratham Modi
prathammodi001@gmail.com | +91-9033393729"""
    }
]

# Write out JSON for staging
with open('scratch/outreach_batch.json', 'w') as f:
    json.dump(outreach_data, f, indent=2)

print(f"Prepared {len(outreach_data)} outreach targets (5 Tier A + {len(outreach_data)-5} Tier B)")

# Append to CSV
csv_path = 'job-kit-starter/output/job-search/outreach/startups_outreach.csv'
with open(csv_path, 'r', newline='') as f:
    existing = list(csv.reader(f))

existing_emails = {r[2].lower() for r in existing[1:] if len(r) > 2}

appended_count = 0
with open(csv_path, 'a', newline='') as f:
    writer = csv.writer(f)
    for d in outreach_data:
        if d['email'].lower() not in existing_emails:
            writer.writerow([
                d['company'],
                d['founder'],
                d['email'],
                d['confidence'],
                d['role_pitch'],
                d['subject'],
                'Saved in Gmail Drafts with Resume Attached',
                '2026-09-19',
                d['notes'],
                d['source'],
                d['tier']
            ])
            appended_count += 1
            existing_emails.add(d['email'].lower())

print(f"Appended {appended_count} records to {csv_path}")
