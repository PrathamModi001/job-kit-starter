import csv, os

targets = [
    # --- 10 Global / HN / YC Startups ---
    {
        "Company": "Pairio",
        "Founder": "Mark",
        "Email": "hello@pairio.app",
        "Confidence": "Verified",
        "Source": "HN (id: 49922569)",
        "Tier": "B",
        "Role Pitch": "Real-Time Collaborative Backend Engineer",
        "Subject": "Real-time sync and distributed backends for Pairio",
        "Notes": "Attached Pratham_Modi_Base_Resume.pdf; highlights Playpower Labs 2000+ WebSocket sessions and C3iHub Kafka event engine",
        "Body": """Hi Mark,

Saw Pairio's collaborative workspace and real-time multiplayer document synchronization on HN.

At Playpower Labs, I engineered real-time WebSocket streaming architectures supporting 2,000+ concurrent sessions with sub-100ms response times. At C3iHub (IIT Kanpur), I built an event-driven engine processing 75k daily Kafka events at 99.5% reliability with automated dead-letter recovery.

Resume's attached — github.com/PrathamModi001 if you want more detail. Worth a quick chat about Pairio?

Pratham"""
    },
    {
        "Company": "Sidekick Labs",
        "Founder": "McIntyre",
        "Email": "hn@sidekicklabs.com",
        "Confidence": "Verified",
        "Source": "HN (id: 49922569)",
        "Tier": "B",
        "Role Pitch": "AI Intelligence & Backend Systems Engineer",
        "Subject": "Low-latency retrieval and async pipelines for Sidekick Labs",
        "Notes": "Attached Pratham_Modi_Base_Resume.pdf; highlights Playpower Labs sub-200ms RAG and C3iHub 450ms->135ms DB query optimization",
        "Body": """Hi McIntyre,

Saw Sidekick Labs' developer intelligence engine and focus on reliable production AI runtimes.

At Playpower Labs, I built low-latency RAG pipelines delivering sub-200ms retrieval across 10k+ documents while reducing LLM token overhead by 35%. At C3iHub (IIT Kanpur), I tuned MongoDB compound indexing and Redis caching to slash p99 query latency from 450ms to 135ms.

Sending my resume along — happy to jump on a quick call if useful.

Pratham"""
    },
    {
        "Company": "PAGNOS",
        "Founder": "Hiring Team",
        "Email": "recruiting@pagnos.com",
        "Confidence": "Verified",
        "Source": "HN (id: 49922569)",
        "Tier": "B",
        "Role Pitch": "Cloud Serverless & Event Ingestion Engineer",
        "Subject": "Serverless backends & Kafka telemetry for PAGNOS",
        "Notes": "Attached Pratham_Modi_Base_Resume.pdf; highlights C3iHub 75k daily Kafka events and AWS deployment automation",
        "Body": """Hi Team,

Saw PAGNOS scaling AWS serverless architectures and distributed cloud pipelines on HN.

At C3iHub (IIT Kanpur), I engineered event-driven pipelines handling 75k daily Kafka events at 99.5% delivery reliability with automated dead-letter queues. At Playpower Labs, I built microservices supporting 500+ concurrent WebSocket connections with sub-100ms response times.

Resume attached. GitHub's github.com/PrathamModi001 if you want to poke around the code. Open to chatting if there's a fit.

Pratham"""
    },
    {
        "Company": "Fazeshift",
        "Founder": "Chris Zehner",
        "Email": "chris.zehner@fazeshift.com",
        "Confidence": "Verified",
        "Source": "HN (id: 49922569)",
        "Tier": "B",
        "Role Pitch": "Distributed Systems & Cloud Backend Engineer",
        "Subject": "10 min re: Fazeshift backend & delivery infra",
        "Notes": "Attached Pratham_Modi_Base_Resume.pdf; highlights C3iHub OpenTelemetry tracing across 15+ services and 85% MTTR drop",
        "Body": """Hi Chris,

Saw Fazeshift building high-efficiency developer platforms and distributed delivery systems on HN.

At C3iHub (IIT Kanpur), I rolled out OpenTelemetry distributed tracing across 15+ microservices, reducing MTTR by 85% while handling 75k daily Kafka events. At Playpower Labs, I optimized vector retrieval latency to sub-200ms across 10k+ documents.

Resume's attached — github.com/PrathamModi001 if you'd like to check out recent builds. Open to connecting this week?

Pratham"""
    },
    {
        "Company": "Starbridge",
        "Founder": "Melissa",
        "Email": "recruiting@starbridge.ai",
        "Confidence": "Verified",
        "Source": "HN (id: 49922569)",
        "Tier": "B",
        "Role Pitch": "AI Agent Evaluation & Telemetry Engineer",
        "Subject": "AI evaluation pipelines & low-latency APIs for Starbridge",
        "Notes": "Attached Pratham_Modi_Base_Resume.pdf; highlights Playpower Labs 35% token reduction and C3iHub 450ms->135ms DB query optimization",
        "Body": """Hi Melissa,

Saw Starbridge scaling autonomous AI agent systems and enterprise product infrastructure.

At Playpower Labs, I engineered evaluation pipelines that achieved a 35% token reduction on LLM calls with sub-200ms RAG retrieval. At C3iHub (IIT Kanpur), I optimized database indexing to cut p99 latency from 450ms to 135ms under heavy production load.

Sending my resume along — would love to chat if you need hands on backend and eval pipelines.

Pratham"""
    },
    {
        "Company": "Baserow",
        "Founder": "Bram Wiepjes",
        "Email": "bram@baserow.io",
        "Confidence": "Pattern-guessed",
        "Source": "HN (id: 50075162)",
        "Tier": "B",
        "Role Pitch": "Open-Source High-Throughput Database Backend Engineer",
        "Subject": "Database indexing and real-time backend for Baserow",
        "Notes": "Attached Pratham_Modi_Base_Resume.pdf; highlights C3iHub 450ms->135ms latency drop and Playpower Labs WebSocket concurrency",
        "Body": """Hi Bram,

Saw Baserow's open-core database platform scaling real-time collaboration and formula calculation engines.

At C3iHub (IIT Kanpur), I cut database p99 query latency from 450ms to 135ms via compound indexing and Redis caching across large datasets. At Playpower Labs, I architected real-time WebSocket pipelines sustaining 2,000+ concurrent sessions with sub-100ms response times.

Resume attached — github.com/PrathamModi001 for public code. Open to chatting if there's a fit for Baserow.

Pratham"""
    },
    {
        "Company": "Reflex",
        "Founder": "Nikhil Rao",
        "Email": "nikhil@reflex.dev",
        "Confidence": "Pattern-guessed",
        "Source": "YC Founder Outreach",
        "Tier": "B",
        "Role Pitch": "Python Async Runtime & WebSocket Infrastructure Engineer",
        "Subject": "Python async runtimes and distributed backends for Reflex",
        "Notes": "Attached Pratham_Modi_Base_Resume.pdf; highlights Playpower Labs 2000+ concurrent WebSocket sessions and C3iHub Kafka processing",
        "Body": """Hi Nikhil,

Saw Reflex enabling developers to build full-stack web apps in pure Python with stateful WebSocket syncing.

At Playpower Labs, I built real-time WebSocket streaming services supporting 2,000+ concurrent sessions with sub-100ms response times. At C3iHub (IIT Kanpur), I engineered distributed event-driven microservices handling 75k daily Kafka events with 99.5% delivery reliability.

Resume's attached — would love to contribute to Reflex's compiler and state runtime if you are expanding backend hiring.

Pratham"""
    },
    {
        "Company": "Cursor",
        "Founder": "Michael Truell",
        "Email": "michael@anysphere.co",
        "Confidence": "Pattern-guessed",
        "Source": "Founder Outreach (Dev Tools)",
        "Tier": "B",
        "Role Pitch": "Fast Context Retrieval & Model-Serving Backend Engineer",
        "Subject": "Fast context retrieval and model-serving backends for Cursor",
        "Notes": "Attached Pratham_Modi_Base_Resume.pdf; highlights Playpower Labs sub-200ms RAG pipelines and 35% token reduction",
        "Body": """Hi Michael,

Saw Cursor setting the frontier standard for agentic codebase indexing and instant shadow workspace execution.

At Playpower Labs, I engineered low-latency RAG retrieval pipelines delivering sub-200ms queries across 10k+ code documents while reducing token usage by 35%. At C3iHub (IIT Kanpur), I designed telemetry ingestion pipelines handling 75k daily Kafka events at 99.5% reliability.

Sending my resume along — open to 10 minutes if Cursor has room for backend infrastructure engineers.

Pratham"""
    },
    {
        "Company": "K-Scale Labs",
        "Founder": "Benjamin Bolte",
        "Email": "ben@kscale.ai",
        "Confidence": "Pattern-guessed",
        "Source": "YC Founder Outreach",
        "Tier": "B",
        "Role Pitch": "Real-Time Telemetry & Distributed Robotics Backend Engineer",
        "Subject": "Real-time telemetry ingestion and distributed systems for K-Scale",
        "Notes": "Attached Pratham_Modi_Base_Resume.pdf; highlights C3iHub 75k daily Kafka events and OpenTelemetry distributed tracing",
        "Body": """Hi Ben,

Saw K-Scale's open-source humanoid robotics builds and real-time simulation pipelines.

At C3iHub (IIT Kanpur), I built an event-driven engine handling 75k daily Kafka events at 99.5% reliability and deployed OpenTelemetry distributed tracing across 15+ microservices. At Playpower Labs, I engineered streaming microservices supporting sub-100ms response times.

Resume attached — github.com/PrathamModi001 if you want to inspect past systems work. Open to connecting?

Pratham"""
    },
    {
        "Company": "Axiom",
        "Founder": "Neil Carvalho",
        "Email": "neil@axiom.co",
        "Confidence": "Pattern-guessed",
        "Source": "Founder Outreach (Observability)",
        "Tier": "B",
        "Role Pitch": "High-Cardinality Ingestion & Observability Engineer",
        "Subject": "OpenTelemetry tracing and high-throughput ingestion for Axiom",
        "Notes": "Attached Pratham_Modi_Base_Resume.pdf; highlights C3iHub OpenTelemetry tracing across 15+ services and 450ms->135ms DB query optimization",
        "Body": """Hi Neil,

Saw Axiom's cloud-native logging platform and high-performance ingestion engine handling terabytes of telemetry.

At C3iHub (IIT Kanpur), I deployed OpenTelemetry distributed tracing across 15+ microservices, cutting MTTR by 85% and tuning database queries to slash p99 latency from 450ms to 135ms. At Playpower Labs, I built low-latency streaming services maintaining sub-100ms response times.

Resume's attached — would love to help scale Axiom's query and ingestion pipelines if there's a fit.

Pratham"""
    },

    # --- 10 Indian Tech Startups ---
    {
        "Company": "Plum",
        "Founder": "Abhishek Poddar",
        "Email": "abhishek@plumhq.com",
        "Confidence": "Pattern-guessed",
        "Source": "Founder Outreach (India)",
        "Tier": "B",
        "Role Pitch": "Real-Time Claims Telemetry & Microservices Backend Engineer",
        "Subject": "High-throughput microservices and event processing for Plum",
        "Notes": "Attached Pratham_Modi_Base_Resume.pdf; highlights C3iHub 75k daily Kafka events and 450ms->135ms database query reduction",
        "Body": """Hi Abhishek,

Saw Plum's automated health insurance infrastructure and real-time claims disbursement platform.

At C3iHub (IIT Kanpur), I engineered a notification and workflow engine handling 75k daily Kafka events at 99.5% delivery reliability with automated DLQs, and cut database p99 latency from 450ms to 135ms. At Playpower Labs, I built microservices supporting sub-100ms response times.

Resume's attached — github.com/PrathamModi001 for project receipts. Open to a brief chat if Plum is hiring in backend?

Pratham"""
    },
    {
        "Company": "Pocket FM",
        "Founder": "Rohan Nayak",
        "Email": "rohan@pocketfm.com",
        "Confidence": "Pattern-guessed",
        "Source": "Founder Outreach (India)",
        "Tier": "B",
        "Role Pitch": "Audio Streaming Telemetry & High-Concurrency Backend Engineer",
        "Subject": "High-concurrency streaming backends and event pipelines for Pocket FM",
        "Notes": "Attached Pratham_Modi_Base_Resume.pdf; highlights Playpower Labs 2000+ WebSocket sessions and C3iHub Kafka event processing",
        "Body": """Hi Rohan,

Saw Pocket FM's global expansion and audio series personalization platform handling millions of daily streaming minutes.

At Playpower Labs, I engineered real-time WebSocket streaming architectures sustaining 2,000+ concurrent sessions with sub-100ms response times. At C3iHub (IIT Kanpur), I built event-driven microservices processing 75k daily Kafka events at 99.5% delivery reliability.

Resume attached — github.com/PrathamModi001 if you want to explore the code. Worth a short call re: backend hiring?

Pratham"""
    },
    {
        "Company": "Rebel Foods",
        "Founder": "Jaydeep Barman",
        "Email": "jaydeep@rebelfoods.com",
        "Confidence": "Pattern-guessed",
        "Source": "Founder Outreach (India)",
        "Tier": "B",
        "Role Pitch": "Cloud Kitchen KitchenOS & Order Dispatch Backend Engineer",
        "Subject": "Order dispatch telemetry and microservice scaling for Rebel Foods",
        "Notes": "Attached Pratham_Modi_Base_Resume.pdf; highlights C3iHub 75k daily Kafka events and 450ms->135ms query latency reduction",
        "Body": """Hi Jaydeep,

Saw Rebel Foods' KitchenOS operating across hundreds of cloud kitchens with automated order routing and multi-brand dispatch.

At C3iHub (IIT Kanpur), I built event-driven services processing 75k daily Kafka events at 99.5% reliability with automated recovery, and slashed database p99 latency from 450ms to 135ms. At Playpower Labs, I developed low-latency APIs supporting sub-100ms response times.

Sending my resume along — happy to jump on a quick call if useful.

Pratham"""
    },
    {
        "Company": "Curefoods",
        "Founder": "Ankit Nagori",
        "Email": "ankit@curefoods.in",
        "Confidence": "Pattern-guessed",
        "Source": "Founder Outreach (India)",
        "Tier": "B",
        "Role Pitch": "Multi-Brand Inventory & Order Management Backend Engineer",
        "Subject": "Inventory sync and distributed microservices for Curefoods",
        "Notes": "Attached Pratham_Modi_Base_Resume.pdf; highlights C3iHub 450ms->135ms query latency reduction and OpenTelemetry MTTR reduction",
        "Body": """Hi Ankit,

Saw Curefoods' rapid scaling of multi-brand kitchen networks and unified supply chain operations across India.

At C3iHub (IIT Kanpur), I optimized high-load MongoDB indexing to cut p99 query latency from 450ms to 135ms and deployed OpenTelemetry distributed tracing across 15+ microservices, slashing MTTR by 85%. At Playpower Labs, I built microservices maintaining sub-100ms response times.

Resume's attached — github.com/PrathamModi001 if you'd like to check out past projects. Open to connecting?

Pratham"""
    },
    {
        "Company": "Captain Fresh",
        "Founder": "Utham Gowda",
        "Email": "utham@captainfresh.com",
        "Confidence": "Pattern-guessed",
        "Source": "Founder Outreach (India)",
        "Tier": "B",
        "Role Pitch": "Cold-Chain Supply Telemetry & Logistics Engine Engineer",
        "Subject": "Real-time supply telemetry and event processing for Captain Fresh",
        "Notes": "Attached Pratham_Modi_Base_Resume.pdf; highlights C3iHub 75k daily Kafka events and Redis pub/sub caching",
        "Body": """Hi Utham,

Saw Captain Fresh scaling global seafood B2B supply chains with algorithmic matching and cold-chain traceability.

At C3iHub (IIT Kanpur), I designed an event-driven automation platform handling 75k daily Kafka events at 99.5% reliability with Redis pub/sub caching. At Playpower Labs, I engineered real-time WebSocket pipelines supporting 2,000+ concurrent sessions with sub-100ms response times.

Resume attached. Open to a brief conversation if Captain Fresh is expanding the core engineering team.

Pratham"""
    },
    {
        "Company": "Ultrahuman",
        "Founder": "Mohit Kumar",
        "Email": "mohit@ultrahuman.com",
        "Confidence": "Pattern-guessed",
        "Source": "Founder Outreach (India)",
        "Tier": "B",
        "Role Pitch": "Biometric Telemetry Ingestion & Real-Time Sync Engineer",
        "Subject": "Biometric telemetry ingestion and low-latency sync for Ultrahuman",
        "Notes": "Attached Pratham_Modi_Base_Resume.pdf; highlights Playpower Labs 2000+ WebSocket sessions and C3iHub Kafka event processing",
        "Body": """Hi Mohit,

Saw Ultrahuman Ring AIR and PowerPlugs expanding globally with real-time biomarker tracking and sleep telemetry.

At Playpower Labs, I engineered streaming architectures sustaining 2,000+ concurrent WebSocket sessions with sub-100ms response times. At C3iHub (IIT Kanpur), I built an event pipeline handling 75k daily Kafka events at 99.5% delivery reliability and cut database p99 latency from 450ms to 135ms.

Resume's attached — would love to help scale Ultrahuman's telemetry ingestion backends. Open to chatting?

Pratham"""
    },
    {
        "Company": "Park+",
        "Founder": "Amit Lakhotia",
        "Email": "amit@myparkplus.com",
        "Confidence": "Pattern-guessed",
        "Source": "Founder Outreach (India)",
        "Tier": "B",
        "Role Pitch": "FASTag Telemetry & Geospatial Microservices Backend Engineer",
        "Subject": "High-volume FASTag event processing and microservices for Park+",
        "Notes": "Attached Pratham_Modi_Base_Resume.pdf; highlights C3iHub 75k daily Kafka events and 450ms->135ms query latency drop",
        "Body": """Hi Amit,

Saw Park+ processing millions of daily FASTag transactions and parking automations across India.

At C3iHub (IIT Kanpur), I architected distributed microservices processing 75k daily Kafka events at 99.5% reliability with automated dead-letter queues, and cut query p99 latency from 450ms to 135ms via compound indexing. At Playpower Labs, I built high-concurrency microservices maintaining sub-100ms response times.

Sending my resume along — happy to jump on a quick call if useful.

Pratham"""
    },
    {
        "Company": "Gupshup",
        "Founder": "Beerud Sheth",
        "Email": "beerud@gupshup.io",
        "Confidence": "Pattern-guessed",
        "Source": "Founder Outreach (India)",
        "Tier": "B",
        "Role Pitch": "Conversational AI Messaging & Ingestion Infrastructure Engineer",
        "Subject": "High-throughput messaging pipelines and AI evals for Gupshup",
        "Notes": "Attached Pratham_Modi_Base_Resume.pdf; highlights C3iHub 75k daily Kafka events and Playpower Labs 35% token reduction",
        "Body": """Hi Beerud,

Saw Gupshup's conversational AI cloud powering billions of enterprise messaging workflows across WhatsApp and RCS.

At C3iHub (IIT Kanpur), I engineered event-driven pipelines handling 75k daily Kafka events at 99.5% delivery reliability with automated DLQ recovery. At Playpower Labs, I built evaluation and RAG pipelines delivering sub-200ms retrieval and a 35% reduction in token overhead.

Resume attached — github.com/PrathamModi001 for public code. Open to a quick chat if there is an engineering fit.

Pratham"""
    },
    {
        "Company": "Yellow.ai",
        "Founder": "Raghu Ravinutala",
        "Email": "raghu@yellow.ai",
        "Confidence": "Pattern-guessed",
        "Source": "Founder Outreach (India)",
        "Tier": "B",
        "Role Pitch": "Autonomous Agent Runtime & Real-Time Orchestration Engineer",
        "Subject": "Agentic orchestration runtimes and low-latency RAG for Yellow.ai",
        "Notes": "Attached Pratham_Modi_Base_Resume.pdf; highlights Playpower Labs sub-200ms RAG pipelines and C3iHub Kafka processing",
        "Body": """Hi Raghu,

Saw Yellow.ai's multi-agent dynamic automation platform delivering human-like voice and chat resolutions globally.

At Playpower Labs, I engineered low-latency RAG pipelines delivering sub-200ms retrieval across 10k+ documents with a 35% token reduction. At C3iHub (IIT Kanpur), I architected an event-driven engine processing 75k daily Kafka events with OpenTelemetry distributed tracing across 15+ services.

Resume's attached — would love to contribute to Yellow.ai's agent runtime infrastructure. Open to connecting?

Pratham"""
    },
    {
        "Company": "CoinSwitch",
        "Founder": "Ashish Singhal",
        "Email": "ashish@coinswitch.co",
        "Confidence": "Pattern-guessed",
        "Source": "Founder Outreach (India)",
        "Tier": "B",
        "Role Pitch": "High-Frequency Order Routing & Ledger Backend Engineer",
        "Subject": "High-throughput transaction backends and Kafka pipelines for CoinSwitch",
        "Notes": "Attached Pratham_Modi_Base_Resume.pdf; highlights C3iHub 75k daily Kafka events and 450ms->135ms DB query optimization",
        "Body": """Hi Ashish,

Saw CoinSwitch scaling multi-asset trading, wealth products, and crypto exchange infrastructure for 20M+ users.

At C3iHub (IIT Kanpur), I built an event-driven system handling 75k daily Kafka events at 99.5% delivery reliability, and tuned database indexing to slash p99 latency from 450ms to 135ms. At Playpower Labs, I built real-time WebSocket pipelines maintaining sub-100ms response times.

Resume attached — github.com/PrathamModi001 if you'd like to check out past systems. Open to 10 minutes?

Pratham"""
    }
]

print(f"Total staged targets: {len(targets)}")
