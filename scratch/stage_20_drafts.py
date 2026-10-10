import json, base64, csv
from pathlib import Path

# Load Base Resume as base64
resume_path = Path("job-kit-starter/output/Pratham_Modi_Base_Resume.pdf")
b64_resume = base64.b64encode(resume_path.read_bytes()).decode("utf-8")

targets = [
    # --- 10 Global / HN / YC Startups ---
    {
        "Tier": "B",
        "Company": "Propel Labs",
        "Founder": "Lisa",
        "Email": "lisa@propellabs.ai",
        "Confidence": "Verified",
        "Source": "HN (id: 49922569)",
        "Role Pitch": "Full-Stack & Systems Quality Engineer",
        "Subject": "Backend & delivery systems for Propel Labs — quick note from an engineer",
        "Notes": "Attached Pratham_Modi_Base_Resume.pdf; highlights C3iHub 450ms->135ms DB query latency and 75k daily Kafka events",
        "Body": """Hi Lisa,

Saw Propel Labs' focus on high-reliability full-stack systems and engineering delivery on HN.

At C3iHub (IIT Kanpur), I cut MongoDB p99 latency from 450ms to 135ms and engineered a notification engine handling 75k daily Kafka events at 99.5% reliability. At Playpower Labs, I developed microservices supporting 500+ concurrent WebSocket sessions with sub-100ms response times.

Resume's attached — github.com/PrathamModi001 if you want to poke around the code. Open to chatting if there's a fit.

Pratham"""
    },
    {
        "Tier": "B",
        "Company": "KSC Trading",
        "Founder": "Hiring Team",
        "Email": "hiring@ksctrading.com",
        "Confidence": "Verified",
        "Source": "HN (id: 49922569)",
        "Role Pitch": "Backend Software Engineer (High-Throughput Systems)",
        "Subject": "High-throughput backend pipelines for KSC Trading",
        "Notes": "Attached Pratham_Modi_Base_Resume.pdf; highlights C3iHub 75k daily Kafka events and 450ms->135ms latency reduction",
        "Body": """Hi Team,

Noticed KSC Trading is scaling low-latency backend infrastructure for distributed trading systems.

At C3iHub (IIT Kanpur), I engineered an event-driven engine handling 75k daily Kafka events at 99.5% delivery reliability and cut database p99 latency from 450ms to 135ms via compound indexing and Redis caching. At Playpower Labs, I built high-concurrency microservices maintaining sub-100ms response times.

Sending my resume along — happy to jump on a quick call if useful.

Pratham"""
    },
    {
        "Tier": "B",
        "Company": "ICEYE",
        "Founder": "WB",
        "Email": "wb@iceye.com",
        "Confidence": "Verified",
        "Source": "HN (id: 49922569)",
        "Role Pitch": "Platform & Observability Engineer",
        "Subject": "Distributed observability and platform systems for ICEYE",
        "Notes": "Attached Pratham_Modi_Base_Resume.pdf; highlights C3iHub OpenTelemetry tracing across 15+ services and 85% MTTR drop",
        "Body": """Hi WB,

Saw ICEYE's opening for platform and observability engineering supporting satellite data pipelines.

At C3iHub (IIT Kanpur), I deployed distributed tracing across 15+ services using OpenTelemetry, Prometheus, and Grafana, improving incident response time by 85%. At Playpower Labs, I implemented blue-green CI/CD on AWS with GitHub Actions, reducing release cycle time by 65%.

Resume attached — github.com/PrathamModi001 for code and architecture. Worth a quick chat about ICEYE?

Pratham"""
    },
    {
        "Tier": "A",
        "Company": "Modal Labs",
        "Founder": "Erik Bernhardsson",
        "Email": "erik@modal.com",
        "Confidence": "Pattern-guessed",
        "Source": "Founder Outreach",
        "Role Pitch": "Container Sandboxes & Cloud Runtime Engineer",
        "Subject": "Container sandboxing and cold-start execution for Modal",
        "Notes": "Attached Pratham_Modi_Base_Resume.pdf; highlights DeployMind container sandboxes and C3iHub high-concurrency microservices",
        "Body": """Hi Erik,

Modal's instant cloud execution and container virtualization speed has redefined serverless computing.

At C3iHub (IIT Kanpur), I architected microservices serving 50K+ users at 10,000+ concurrent connections with 99.9% uptime. On personal projects, I built DeployMind, orchestrating container sandboxes with real-time log streaming and canary traffic shifting.

Resume's attached — github.com/PrathamModi001. Would love to chat about scaling cloud execution environments at Modal!

Pratham"""
    },
    {
        "Tier": "A",
        "Company": "Fireworks AI",
        "Founder": "Lin Qiao",
        "Email": "lin@fireworks.ai",
        "Confidence": "Pattern-guessed",
        "Source": "Founder Outreach",
        "Role Pitch": "Inference Gateway & High-Throughput API Engineer",
        "Subject": "High-throughput inference streaming and API gateways for Fireworks AI",
        "Notes": "Attached Pratham_Modi_Base_Resume.pdf; highlights Playpower Labs sub-200ms RAG pipelines and C3iHub 75k Kafka events/day",
        "Body": """Hi Lin,

Fireworks AI's ultra-low latency model serving and compound AI systems set the standard for inference speed.

At Playpower Labs, I integrated ChromaDB vector retrieval cutting query latency to sub-200ms at p95 and reduced LLM token overhead by 35%. At C3iHub (IIT Kanpur), I engineered event-driven pipelines handling 75k daily Kafka events at 99.5% reliability.

Sending my resume along — would be great to connect on low-latency gateway scaling at Fireworks AI.

Pratham"""
    },
    {
        "Tier": "A",
        "Company": "Together AI",
        "Founder": "Vipul Ved Prakash",
        "Email": "vipul@together.ai",
        "Confidence": "Pattern-guessed",
        "Source": "Founder Outreach",
        "Role Pitch": "Distributed Systems & Inference Platform Engineer",
        "Subject": "Distributed pipeline scaling and platform engineering for Together AI",
        "Notes": "Attached Pratham_Modi_Base_Resume.pdf; highlights C3iHub 99.9% uptime at 10k connections and OpenTelemetry tracing",
        "Body": """Hi Vipul,

Together AI's distributed training clusters and ultra-fast inference engine are driving the open-source model movement forward.

At C3iHub (IIT Kanpur), I architected distributed microservices maintaining 99.9% uptime across 10,000+ concurrent connections and cut incident resolution by 85% using OpenTelemetry distributed tracing. At Playpower Labs, I built sub-200ms retrieval pipelines for production AI workflows.

Resume attached — github.com/PrathamModi001. Open to chatting if there's a strong fit on the systems side.

Pratham"""
    },
    {
        "Tier": "A",
        "Company": "LangChain",
        "Founder": "Harrison Chase",
        "Email": "harrison@langchain.dev",
        "Confidence": "Pattern-guessed",
        "Source": "Founder Outreach",
        "Role Pitch": "Agent Runtime & LangGraph Systems Engineer",
        "Subject": "Multi-agent runtime execution and memory state machines for LangGraph",
        "Notes": "Attached Pratham_Modi_Base_Resume.pdf; highlights Mnemoniq LangGraph 3-tier memory agent and sub-100ms microservices",
        "Body": """Hi Harrison,

LangGraph's stateful orchestration and cyclic graph paradigm have become the core backbone of agent architecture.

I built Mnemoniq (github.com/PrathamModi001/Mnemoniq), an autonomous agent memory system with a 3-tier architecture (working, episodic, knowledge graph) orchestrated via LangGraph, cutting token overhead by 38% behind a FastAPI backend. At C3iHub, I scaled event pipelines handling 75k daily Kafka events.

Attached my base resume — would love to jump on a quick call about agent runtime state systems!

Pratham"""
    },
    {
        "Tier": "A",
        "Company": "Unstructured",
        "Founder": "Brian Raymond",
        "Email": "brian@unstructured.io",
        "Confidence": "Pattern-guessed",
        "Source": "Founder Outreach",
        "Role Pitch": "Ingestion Pipeline & Document Processing Engineer",
        "Subject": "High-throughput document extraction and chunking pipelines for Unstructured",
        "Notes": "Attached Pratham_Modi_Base_Resume.pdf; highlights Playpower Labs 47% document parsing speedup and Kafka pipelines",
        "Body": """Hi Brian,

Unstructured is the foundational layer transforming raw enterprise documents into LLM-ready inputs.

At Playpower Labs, I built an automated PDF ingestion pipeline with 512-token chunking and vector indexing, cutting document retrieval latency by 47% (340ms to 180ms). At C3iHub, I engineered event-driven pipelines handling 75k daily Kafka events with zero data loss.

Resume's attached — github.com/PrathamModi001. Open to chatting about high-volume ingestion architecture.

Pratham"""
    },
    {
        "Tier": "A",
        "Company": "Pinecone",
        "Founder": "Edo Liberty",
        "Email": "edo@pinecone.io",
        "Confidence": "Pattern-guessed",
        "Source": "Founder Outreach",
        "Role Pitch": "Distributed Indexing & Vector Search Platform Engineer",
        "Subject": "High-throughput indexing and distributed database systems for Pinecone",
        "Notes": "Attached Pratham_Modi_Base_Resume.pdf; highlights Playpower Labs sub-200ms vector search and C3iHub database latency drop",
        "Body": """Hi Edo,

Pinecone's serverless vector database architecture and index scaling have set the industry gold standard.

At Playpower Labs, I integrated vector search across 10K+ documents via HNSW indexing, sustaining sub-200ms retrieval latency at p95. At C3iHub (IIT Kanpur), I reduced database p99 latency from 450ms to 135ms through horizontal sharding and compound indexing.

Sending my resume along — would be great to connect on distributed indexing scale at Pinecone.

Pratham"""
    },
    {
        "Tier": "A",
        "Company": "Weaviate",
        "Founder": "Bob van Luijt",
        "Email": "bob@weaviate.io",
        "Confidence": "Pattern-guessed",
        "Source": "Founder Outreach",
        "Role Pitch": "Vector Database & Hybrid Search Platform Engineer",
        "Subject": "Hybrid search indexing and low-latency retrieval for Weaviate",
        "Notes": "Attached Pratham_Modi_Base_Resume.pdf; highlights Playpower Labs sub-200ms RAG pipelines and C3iHub 99.9% uptime",
        "Body": """Hi Bob,

Weaviate's multi-modal capabilities and modular vector search platform continue to lead the AI storage wave.

At Playpower Labs, I engineered retrieval pipelines over 10K+ documents achieving sub-200ms p95 latency. At C3iHub (IIT Kanpur), I maintained 99.9% uptime across microservices handling 10,000+ concurrent connections and 75k daily Kafka events.

Resume attached — github.com/PrathamModi001 if you'd like to inspect my code. Open to a quick conversation!

Pratham"""
    },

    # --- 10 Indian Tech Companies ---
    {
        "Tier": "A",
        "Company": "ShortLoop",
        "Founder": "Sumit Agarwal",
        "Email": "sumit@shortloop.dev",
        "Confidence": "Pattern-guessed",
        "Source": "Founder Outreach (YC WaaS)",
        "Role Pitch": "Fullstack / API Observability Systems Engineer",
        "Subject": "API observability pipelines and real-time tracing for ShortLoop",
        "Notes": "Attached Pratham_Modi_Base_Resume.pdf; highlights C3iHub OpenTelemetry tracing across 15+ services and 75k Kafka events/day",
        "Body": """Hi Sumit,

ShortLoop's automated API testing and live traffic replay approach addresses a huge pain point in modern microservice deployments.

At C3iHub (IIT Kanpur), I deployed OpenTelemetry distributed tracing across 15+ microservices, cutting incident response time by 85%, and handled 75k daily events via Kafka and Redis Streams. At Playpower Labs, I built Next.js and FastAPI services supporting 500+ WebSocket sessions.

Resume's attached — github.com/PrathamModi001. Would love to chat about scaling API observability and testing at ShortLoop!

Pratham"""
    },
    {
        "Tier": "A",
        "Company": "ClearFeed",
        "Founder": "Joydeep Sen Sarma",
        "Email": "joydeep@clearfeed.ai",
        "Confidence": "Pattern-guessed",
        "Source": "Founder Outreach",
        "Role Pitch": "Distributed Backend & Real-Time Messaging Engineer",
        "Subject": "Real-time state sync and Slack/Teams event streaming for ClearFeed",
        "Notes": "Attached Pratham_Modi_Base_Resume.pdf; highlights C3iHub 2k concurrent WebSocket sync and 75k Kafka events/day",
        "Body": """Hi Joydeep,

ClearFeed's bi-directional conversational ticketing between Slack, Teams, and helpdesks solves a massive coordination challenge for fast-moving teams.

At C3iHub (IIT Kanpur), I built a real-time collaborative state engine handling 2,000+ concurrent WebSocket sessions with idempotent event synchronization, and engineered notification pipelines handling 75k daily Kafka events. Also integrated vector search pipelines at Playpower Labs.

Attached is my base resume. Would love to connect about distributed backend and event streaming scale at ClearFeed!

Pratham"""
    },
    {
        "Tier": "A",
        "Company": "ToolJet",
        "Founder": "Navaneeth PK",
        "Email": "navaneeth@tooljet.com",
        "Confidence": "Pattern-guessed",
        "Source": "Founder Outreach",
        "Role Pitch": "Backend Platform & Extensibility Systems Engineer",
        "Subject": "Extensible backend plugins and container sandbox execution for ToolJet",
        "Notes": "Attached Pratham_Modi_Base_Resume.pdf; highlights C3iHub Node.js/PostgreSQL microservices and DeployMind Docker orchestration",
        "Body": """Hi Navaneeth,

Huge admirer of ToolJet's growth as an open-source low-code platform and how intuitive you've made internal tool building.

At C3iHub (IIT Kanpur), I architected core microservices serving 50K+ users with 99.9% uptime using Express.js, MongoDB, Redis, and PostgreSQL. On DeployMind, I built dynamic Docker container provisioning with automated health gates.

Resume attached — github.com/PrathamModi001. Open to discussing extensible backend plugins and runtime architecture at ToolJet!

Pratham"""
    },
    {
        "Tier": "A",
        "Company": "Shipthis Inc",
        "Founder": "Charif El Ansari",
        "Email": "charif@shipthis.co",
        "Confidence": "Pattern-guessed",
        "Source": "Founder Outreach",
        "Role Pitch": "B2B Logistics Platform & Backend Engineer",
        "Subject": "Microservice architecture and high-throughput workflows for Shipthis",
        "Notes": "Attached Pratham_Modi_Base_Resume.pdf; highlights C3iHub 450ms->135ms DB query latency drop and 75k daily Kafka events",
        "Body": """Hi Charif,

Digitizing freight forwarding operations with Shipthis's end-to-end platform brings immense efficiency to modern global logistics.

At C3iHub (IIT Kanpur), I led backend microservices serving 50K+ users, dropping database p99 latency from 450ms to 135ms through horizontal sharding and compound indexing, while maintaining 75k daily Kafka events. Strong background in TypeScript, Python, and AWS.

Sending my resume along — would be great to chat about scaling workflow engines and backend services at Shipthis.

Pratham"""
    },
    {
        "Tier": "A",
        "Company": "DevRev",
        "Founder": "Dheeraj Pandey",
        "Email": "dheeraj@devrev.ai",
        "Confidence": "Pattern-guessed",
        "Source": "Founder Outreach",
        "Role Pitch": "Developer Platform & Knowledge Graph Backend Engineer",
        "Subject": "Connecting support, product, and developer loops with DevRev",
        "Notes": "Attached Pratham_Modi_Base_Resume.pdf; highlights Mnemoniq knowledge graph memory agent and C3iHub distributed tracing",
        "Body": """Hi Dheeraj,

DevRev's unified work graph bridging support, product management, and developer velocity is a masterclass in enterprise design.

At C3iHub (IIT Kanpur), I engineered distributed microservices handling 50K+ users with OpenTelemetry tracing across 15+ services, cutting incident resolution time by 85%. I also built Mnemoniq, combining knowledge-graph traversal with vector search behind a high-concurrency FastAPI backend.

Resume's attached — github.com/PrathamModi001. Would love to discuss work graph architecture and backend scale at DevRev!

Pratham"""
    },
    {
        "Tier": "A",
        "Company": "InVideo",
        "Founder": "Sanket Shah",
        "Email": "sanket@invideo.io",
        "Confidence": "Pattern-guessed",
        "Source": "Founder Outreach",
        "Role Pitch": "Video Generation Pipeline & Async Media Systems Engineer",
        "Subject": "Async rendering queues and distributed pipelines for InVideo",
        "Notes": "Attached Pratham_Modi_Base_Resume.pdf; highlights C3iHub 75k daily Kafka/BullMQ events and AWS S3 storage cost reduction",
        "Body": """Hi Sanket,

InVideo's AI text-to-video workflow and generative capabilities have completely transformed video creation worldwide.

At C3iHub (IIT Kanpur), I cut cloud storage costs 60% via multi-tier S3 Glacier architecture and engineered an event-driven queue handling 75k daily events via Kafka and BullMQ with guaranteed delivery. At Playpower Labs, I built microservices maintaining sub-100ms response times.

Attached is my base resume. Would love to chat about scaling high-concurrency rendering queues and media ingestion at InVideo!

Pratham"""
    },
    {
        "Tier": "A",
        "Company": "Hyperverge",
        "Founder": "Kedar Kulkarni",
        "Email": "kedar@hyperverge.co",
        "Confidence": "Pattern-guessed",
        "Source": "Founder Outreach",
        "Role Pitch": "High-Throughput Verification & AI Pipeline Engineer",
        "Subject": "Low-latency identity verification and inference pipelines for Hyperverge",
        "Notes": "Attached Pratham_Modi_Base_Resume.pdf; highlights Playpower Labs sub-200ms RAG pipelines and C3iHub 99.9% uptime",
        "Body": """Hi Kedar,

Hyperverge's AI identity verification processing hundreds of millions of checks with high accuracy across fintech is inspiring.

At Playpower Labs, I engineered document extraction pipelines achieving sub-200ms p95 latency across 10K+ documents. At C3iHub (IIT Kanpur), I architected backend systems maintaining 99.9% uptime across 10,000+ concurrent connections and 75k daily Kafka events.

Resume attached — github.com/PrathamModi001. Open to connecting on high-volume verification pipeline architecture!

Pratham"""
    },
    {
        "Tier": "A",
        "Company": "Fashinza",
        "Founder": "Pawan Gupta",
        "Email": "pawan@fashinza.com",
        "Confidence": "Pattern-guessed",
        "Source": "Founder Outreach",
        "Role Pitch": "Supply Chain Platform & Event-Driven Backend Engineer",
        "Subject": "Event-driven supply chain tracking and distributed data pipelines for Fashinza",
        "Notes": "Attached Pratham_Modi_Base_Resume.pdf; highlights C3iHub Kafka 75k events/day and 450ms->135ms DB query latency",
        "Body": """Hi Pawan,

Fashinza's digitized supply chain and real-time production tracking platform brings essential transparency to global apparel manufacturing.

At C3iHub (IIT Kanpur), I engineered event-driven pipelines handling 75k daily events using Kafka and Redis Streams with consumer-side deduplication, and dropped database p99 latency from 450ms to 135ms. Proficient in Node.js, Python, and AWS infrastructure.

Sending my resume along — would be great to jump on a quick call about event-driven supply chain scale.

Pratham"""
    },
    {
        "Tier": "A",
        "Company": "Rocketlane",
        "Founder": "Srikrishnan Ganesan",
        "Email": "sri@rocketlane.com",
        "Confidence": "Pattern-guessed",
        "Source": "Founder Outreach",
        "Role Pitch": "Collaborative State & Customer Onboarding Backend Engineer",
        "Subject": "Real-time collaborative workspaces and workflow automation for Rocketlane",
        "Notes": "Attached Pratham_Modi_Base_Resume.pdf; highlights C3iHub 2k concurrent WebSocket sync and 10k connections",
        "Body": """Hi Sri,

Rocketlane's customer onboarding platform and client-facing collaboration portals have set a new bar for professional services velocity.

At C3iHub (IIT Kanpur), I built a real-time collaborative state engine supporting 2,000+ concurrent WebSocket sessions with race-condition-safe synchronization, and scaled microservices to 10,000+ concurrent connections. Skilled in TypeScript, Python, PostgreSQL, and Redis.

Resume's attached — github.com/PrathamModi001. Worth a quick conversation about collaborative workspace engineering at Rocketlane?

Pratham"""
    },
    {
        "Tier": "A",
        "Company": "Sprinto",
        "Founder": "Girish Redekar",
        "Email": "girish@sprinto.com",
        "Confidence": "Pattern-guessed",
        "Source": "Founder Outreach",
        "Role Pitch": "Security Compliance Automation & Cloud Integrations Engineer",
        "Subject": "Cloud evidence collection and continuous compliance pipelines for Sprinto",
        "Notes": "Attached Pratham_Modi_Base_Resume.pdf; highlights DeployMind security audit gates, C3iHub distributed tracing, and AWS automation",
        "Body": """Hi Girish,

Sprinto's automated continuous compliance and seamless security integrations take the immense friction out of SOC 2 and ISO audits.

On DeployMind, I engineered automated security auditing gates with conditional rollback and cloud provider integrations. At C3iHub (IIT Kanpur), I deployed OpenTelemetry distributed tracing across 15+ services (85% faster MTTR) and managed cloud infrastructure on AWS.

Attached is my base resume. Would love to discuss automated compliance evidence pipelines and integrations at Sprinto!

Pratham"""
    }
]

# Write targets to scratch json
with open("scratch/today_20_outreach_targets.json", "w") as f:
    json.dump(targets, f, indent=2)

print(f"Generated {len(targets)} targets in scratch/today_20_outreach_targets.json")
