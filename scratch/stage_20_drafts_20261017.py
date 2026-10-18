import json, base64, csv
from pathlib import Path

# Load Base Resume as base64
resume_path = Path("job-kit-starter/output/Pratham_Modi_Base_Resume.pdf")
b64_resume = base64.b64encode(resume_path.read_bytes()).decode("utf-8")

targets = [
    # --- 10 Global / HN / YC Startups ---
    {
        "Tier": "B",
        "Company": "Namespace Labs",
        "Founder": "Hannah",
        "Email": "hannah@namespacelabs.com",
        "Confidence": "Verified",
        "Source": "HN (id: 49922569)",
        "Role Pitch": "Distributed Systems & Cloud Infrastructure Engineer",
        "Subject": "Fast cloud environments and container backends for Namespace Labs",
        "Notes": "Attached Pratham_Modi_Base_Resume.pdf; highlights C3iHub 75k daily Kafka events and OpenTelemetry distributed tracing",
        "Body": """Hi Hannah,

Saw Namespace Labs building lightning-fast remote development environments and container runtimes on HN.

At C3iHub (IIT Kanpur), I engineered event-driven pipelines handling 75k daily Kafka events at 99.5% delivery reliability and deployed OpenTelemetry distributed tracing across 15+ microservices. At Playpower Labs, I built low-latency streaming services supporting 2,000+ concurrent WebSocket sessions.

Resume is attached — github.com/PrathamModi001 for public code. Open to a quick chat if there's an engineering fit?

Pratham"""
    },
    {
        "Tier": "B",
        "Company": "VOYGR",
        "Founder": "Yarik",
        "Email": "yarik@voygr.tech",
        "Confidence": "Verified",
        "Source": "HN (id: 49922569)",
        "Role Pitch": "Founding Product & Systems Engineer",
        "Subject": "Founding backend & product systems for VOYGR",
        "Notes": "Attached Pratham_Modi_Base_Resume.pdf; highlights C3iHub 450ms->135ms DB query optimization and Playpower Labs WebSocket concurrency",
        "Body": """Hi Yarik,

Saw VOYGR scaling autonomous AI systems and high-velocity product execution on HN.

At C3iHub (IIT Kanpur), I optimized MongoDB indexing and Redis caching to slash p99 query latency from 450ms to 135ms while building event-driven workflows for 75k daily events. At Playpower Labs, I engineered real-time WebSocket pipelines maintaining sub-100ms response times.

Attached my resume — github.com/PrathamModi001 if you'd like to check out past builds. Worth 10 minutes?

Pratham"""
    },
    {
        "Tier": "B",
        "Company": "Loop Control",
        "Founder": "Hiring Team",
        "Email": "hello@loopcontrol.io",
        "Confidence": "Verified",
        "Source": "HN (id: 49922569)",
        "Role Pitch": "Low-Latency Real-Time Streaming Engineer",
        "Subject": "Sub-100ms streaming pipelines and backends for Loop Control",
        "Notes": "Attached Pratham_Modi_Base_Resume.pdf; highlights Playpower Labs 2000+ WebSocket sessions and sub-100ms response times",
        "Body": """Hi Team,

Saw Loop Control's low-latency audio/video collaboration platform on HN.

At Playpower Labs, I architected real-time WebSocket streaming services sustaining 2,000+ concurrent sessions with sub-100ms response times. At C3iHub (IIT Kanpur), I built event ingestion engines processing 75k daily Kafka events with 99.5% delivery reliability.

Resume attached — open to connecting if Loop Control is expanding backend hiring.

Pratham"""
    },
    {
        "Tier": "B",
        "Company": "VLM Run",
        "Founder": "Hiring Team",
        "Email": "hiring@vlm.run",
        "Confidence": "Verified",
        "Source": "HN (id: 49922569)",
        "Role Pitch": "Founding Infrastructure & Model Serving Engineer",
        "Subject": "High-throughput model serving & async ingestion for VLM Run",
        "Notes": "Attached Pratham_Modi_Base_Resume.pdf; highlights Playpower Labs sub-200ms RAG retrieval and 35% token overhead reduction",
        "Body": """Hi Team,

Saw VLM Run building dedicated infrastructure for vision-language models on HN.

At Playpower Labs, I engineered low-latency retrieval pipelines delivering sub-200ms queries across 10k+ documents with a 35% reduction in token overhead. At C3iHub (IIT Kanpur), I designed telemetry ingestion pipelines handling 75k daily Kafka events at 99.5% reliability.

Sending my resume along — happy to jump on a quick call if useful.

Pratham"""
    },
    {
        "Tier": "B",
        "Company": "Radar Labs",
        "Founder": "Tim",
        "Email": "tim@radar.com",
        "Confidence": "Verified",
        "Source": "HN (id: 49922569)",
        "Role Pitch": "High-Volume Telemetry & Backend Engineer",
        "Subject": "High-volume geospatial telemetry & Kafka pipelines for Radar Labs",
        "Notes": "Attached Pratham_Modi_Base_Resume.pdf; highlights C3iHub 75k daily Kafka events and 450ms->135ms DB query reduction",
        "Body": """Hi Tim,

Saw Radar's geofencing platform processing billions of location events for global developer ecosystems.

At C3iHub (IIT Kanpur), I built distributed microservices processing 75k daily Kafka events at 99.5% reliability with automated dead-letter queues, and cut query p99 latency from 450ms to 135ms via compound indexing. At Playpower Labs, I built high-concurrency microservices maintaining sub-100ms response times.

Resume's attached — would love to contribute to Radar's ingestion and telemetry pipelines.

Pratham"""
    },
    {
        "Tier": "B",
        "Company": "Superset",
        "Founder": "Kiet",
        "Email": "kiet@superset.sh",
        "Confidence": "Verified",
        "Source": "HN (id: 49922569)",
        "Role Pitch": "Founding Full-Stack & Systems Engineer",
        "Subject": "Real-time sync and fast developer backends for Superset",
        "Notes": "Attached Pratham_Modi_Base_Resume.pdf; highlights Playpower Labs 2000+ WebSocket sessions and C3iHub OpenTelemetry tracing",
        "Body": """Hi Kiet,

Saw Superset (YC P26) rethinking collaborative workspace tools with extreme responsiveness.

At Playpower Labs, I engineered real-time WebSocket streaming architectures supporting 2,000+ concurrent sessions with sub-100ms response times. At C3iHub (IIT Kanpur), I deployed OpenTelemetry distributed tracing across 15+ microservices, cutting MTTR by 85%.

Resume attached — github.com/PrathamModi001 if you'd like to poke around the code. Open to chatting?

Pratham"""
    },
    {
        "Tier": "B",
        "Company": "Modal",
        "Founder": "Erik Bernhardsson",
        "Email": "erik@modal.com",
        "Confidence": "Pattern-guessed",
        "Source": "Founder Outreach (Dev Tools)",
        "Role Pitch": "Serverless Container & Telemetry Backend Engineer",
        "Subject": "Serverless container runtimes and telemetry for Modal",
        "Notes": "Attached Pratham_Modi_Base_Resume.pdf; highlights C3iHub OpenTelemetry tracing and Playpower Labs low-latency systems",
        "Body": """Hi Erik,

Saw Modal setting the bar for cloud serverless container execution and cold-start optimization.

At C3iHub (IIT Kanpur), I deployed OpenTelemetry distributed tracing across 15+ microservices and built Kafka event pipelines handling 75k daily events at 99.5% delivery reliability. At Playpower Labs, I developed low-latency APIs supporting sub-100ms response times.

Resume's attached — github.com/PrathamModi001 if you want to inspect past systems work. Open to connecting?

Pratham"""
    },
    {
        "Tier": "B",
        "Company": "LanceDB",
        "Founder": "Chang She",
        "Email": "chang@lancedb.com",
        "Confidence": "Pattern-guessed",
        "Source": "Founder Outreach (AI Data)",
        "Role Pitch": "High-Throughput Vector Ingestion & Query Engineer",
        "Subject": "Vector retrieval optimization and query pipelines for LanceDB",
        "Notes": "Attached Pratham_Modi_Base_Resume.pdf; highlights Playpower Labs sub-200ms RAG pipelines and C3iHub 450ms->135ms DB query reduction",
        "Body": """Hi Chang,

Saw LanceDB's serverless vector database architecture built for multimodal AI and zero-copy columnar storage.

At Playpower Labs, I engineered low-latency RAG retrieval pipelines delivering sub-200ms queries across 10k+ documents while reducing token usage by 35%. At C3iHub (IIT Kanpur), I optimized database indexing to slash p99 latency from 450ms to 135ms under heavy production load.

Sending my resume along — would love to contribute to LanceDB's engine and ingestion pipelines.

Pratham"""
    },
    {
        "Tier": "B",
        "Company": "Vellum",
        "Founder": "Akash Sharma",
        "Email": "akash@vellum.ai",
        "Confidence": "Pattern-guessed",
        "Source": "Founder Outreach (AI Tooling)",
        "Role Pitch": "AI Evaluation Pipelines & Production LLM Gateway Engineer",
        "Subject": "LLM evaluation pipelines and low-latency APIs for Vellum",
        "Notes": "Attached Pratham_Modi_Base_Resume.pdf; highlights Playpower Labs 35% token overhead reduction and sub-200ms RAG retrieval",
        "Body": """Hi Akash,

Saw Vellum's production LLM application platform and prompt evaluation infrastructure on YC.

At Playpower Labs, I built evaluation pipelines that achieved a 35% token reduction on LLM calls with sub-200ms RAG retrieval. At C3iHub (IIT Kanpur), I architected an event-driven engine processing 75k daily Kafka events with 99.5% reliability.

Resume attached — open to 10 minutes if Vellum has room for backend infrastructure engineers.

Pratham"""
    },
    {
        "Tier": "B",
        "Company": "Unstructured.io",
        "Founder": "Brian Raymond",
        "Email": "brian@unstructured.io",
        "Confidence": "Pattern-guessed",
        "Source": "Founder Outreach (AI Data)",
        "Role Pitch": "ETL Ingestion & Distributed Pipeline Backend Engineer",
        "Subject": "High-throughput ingestion pipelines & distributed backends for Unstructured",
        "Notes": "Attached Pratham_Modi_Base_Resume.pdf; highlights C3iHub 75k daily Kafka events and 450ms->135ms DB query reduction",
        "Body": """Hi Brian,

Saw Unstructured.io scaling document transformation pipelines and multimodal preprocessing for LLMs.

At C3iHub (IIT Kanpur), I engineered event-driven pipelines handling 75k daily Kafka events at 99.5% delivery reliability with automated DLQ recovery, and cut database p99 latency from 450ms to 135ms. At Playpower Labs, I built microservices supporting sub-100ms response times.

Resume's attached — would love to help scale Unstructured's ETL and ingestion backends.

Pratham"""
    },

    # --- 10 Indian Startups ---
    {
        "Tier": "B",
        "Company": "Toddle",
        "Founder": "Deepanshu Arora",
        "Email": "deepanshu@toddleapp.com",
        "Confidence": "Pattern-guessed",
        "Source": "Founder Outreach (India)",
        "Role Pitch": "EdTech Real-Time Collaboration & Microservices Engineer",
        "Subject": "Real-time collaboration backends and event pipelines for Toddle",
        "Notes": "Attached Pratham_Modi_Base_Resume.pdf; highlights Playpower Labs 2000+ WebSocket sessions and C3iHub 75k daily Kafka events",
        "Body": """Hi Deepanshu,

Saw Toddle's global teaching and learning platform supporting hundreds of thousands of educators worldwide.

At Playpower Labs, I engineered real-time WebSocket streaming architectures sustaining 2,000+ concurrent sessions with sub-100ms response times. At C3iHub (IIT Kanpur), I built event-driven microservices processing 75k daily Kafka events at 99.5% delivery reliability.

Resume attached — github.com/PrathamModi001 if you want to explore the code. Worth a short call re: backend hiring?

Pratham"""
    },
    {
        "Tier": "B",
        "Company": "Jumbotail",
        "Founder": "Karthik Venkateswaran",
        "Email": "karthik@jumbotail.com",
        "Confidence": "Pattern-guessed",
        "Source": "Founder Outreach (India)",
        "Role Pitch": "B2B Marketplace & Logistics Ingestion Backend Engineer",
        "Subject": "Order dispatch telemetry and inventory sync for Jumbotail",
        "Notes": "Attached Pratham_Modi_Base_Resume.pdf; highlights C3iHub 75k daily Kafka events and 450ms->135ms query latency drop",
        "Body": """Hi Karthik,

Saw Jumbotail scaling B2B retail supply chain and logistics across millions of kiranas.

At C3iHub (IIT Kanpur), I built event-driven services processing 75k daily Kafka events at 99.5% reliability with automated recovery, and slashed database p99 latency from 450ms to 135ms. At Playpower Labs, I developed low-latency APIs supporting sub-100ms response times.

Sending my resume along — happy to jump on a quick call if useful.

Pratham"""
    },
    {
        "Tier": "B",
        "Company": "Ninjacart",
        "Founder": "Thirukumaran Nagarajan",
        "Email": "thiru@ninjacart.com",
        "Confidence": "Pattern-guessed",
        "Source": "Founder Outreach (India)",
        "Role Pitch": "Agri-Supply Logistics & Event Dispatch Engineer",
        "Subject": "Supply telemetry and high-throughput microservices for Ninjacart",
        "Notes": "Attached Pratham_Modi_Base_Resume.pdf; highlights C3iHub 75k daily Kafka events and OpenTelemetry distributed tracing",
        "Body": """Hi Thiru,

Saw Ninjacart moving millions of kilograms of produce daily with algorithmic matching and cold-chain route dispatch.

At C3iHub (IIT Kanpur), I designed an event-driven automation platform handling 75k daily Kafka events at 99.5% reliability and deployed OpenTelemetry distributed tracing across 15+ microservices. At Playpower Labs, I engineered real-time WebSocket pipelines maintaining sub-100ms response times.

Resume attached — open to a brief conversation if Ninjacart is expanding core engineering.

Pratham"""
    },
    {
        "Tier": "B",
        "Company": "Cashfree Payments",
        "Founder": "Akash Sinha",
        "Email": "akash@cashfree.com",
        "Confidence": "Pattern-guessed",
        "Source": "Founder Outreach (India)",
        "Role Pitch": "High-Reliability Payments & Transaction Backend Engineer",
        "Subject": "High-reliability payment ledgers & event pipelines for Cashfree",
        "Notes": "Attached Pratham_Modi_Base_Resume.pdf; highlights C3iHub 75k daily Kafka events and 450ms->135ms DB query optimization",
        "Body": """Hi Akash,

Saw Cashfree scaling payment gateway and banking APIs for thousands of enterprise platforms across India.

At C3iHub (IIT Kanpur), I built an event-driven system handling 75k daily Kafka events at 99.5% delivery reliability with automated DLQs, and tuned database indexing to slash p99 latency from 450ms to 135ms. At Playpower Labs, I built microservices supporting sub-100ms response times.

Resume's attached — would love to help scale Cashfree's ledger and transaction infrastructure.

Pratham"""
    },
    {
        "Tier": "B",
        "Company": "PhonePe",
        "Founder": "Sameer Nigam",
        "Email": "sameer@phonepe.com",
        "Confidence": "Pattern-guessed",
        "Source": "Founder Outreach (India)",
        "Role Pitch": "High-Concurrency Transaction & Telemetry Engineer",
        "Subject": "Transaction event pipelines and microservice scaling for PhonePe",
        "Notes": "Attached Pratham_Modi_Base_Resume.pdf; highlights C3iHub 75k daily Kafka events and 450ms->135ms latency drop",
        "Body": """Hi Sameer,

Saw PhonePe processing hundreds of millions of daily UPI transactions with industry-leading reliability.

At C3iHub (IIT Kanpur), I engineered distributed microservices processing 75k daily Kafka events at 99.5% reliability with automated dead-letter queues, and cut query p99 latency from 450ms to 135ms via compound indexing. At Playpower Labs, I built high-concurrency microservices maintaining sub-100ms response times.

Resume attached — open to 10 minutes if PhonePe is hiring in backend infrastructure.

Pratham"""
    },
    {
        "Tier": "B",
        "Company": "Blinkit",
        "Founder": "Albinder Dhindsa",
        "Email": "albinder@blinkit.com",
        "Confidence": "Pattern-guessed",
        "Source": "Founder Outreach (India)",
        "Role Pitch": "Ultra-Fast Dispatch & Inventory Telemetry Engineer",
        "Subject": "Sub-10-minute dispatch telemetry and event engines for Blinkit",
        "Notes": "Attached Pratham_Modi_Base_Resume.pdf; highlights Playpower Labs 2000+ WebSocket sessions and C3iHub Kafka processing",
        "Body": """Hi Albinder,

Saw Blinkit setting the pace for quick commerce in India with instant order routing and dark-store inventory telemetry.

At Playpower Labs, I engineered real-time WebSocket streaming architectures supporting 2,000+ concurrent sessions with sub-100ms response times. At C3iHub (IIT Kanpur), I built an event-driven engine processing 75k daily Kafka events at 99.5% reliability.

Sending my resume along — happy to jump on a quick call if useful.

Pratham"""
    },
    {
        "Tier": "B",
        "Company": "Lenskart",
        "Founder": "Peyush Bansal",
        "Email": "peyush@lenskart.in",
        "Confidence": "Pattern-guessed",
        "Source": "Founder Outreach (India)",
        "Role Pitch": "Omnichannel Inventory & Order Processing Backend Engineer",
        "Subject": "Omnichannel inventory sync and microservices for Lenskart",
        "Notes": "Attached Pratham_Modi_Base_Resume.pdf; highlights C3iHub 450ms->135ms DB query optimization and OpenTelemetry tracing",
        "Body": """Hi Peyush,

Saw Lenskart's rapid omnichannel scaling and automated eyewear manufacturing infrastructure.

At C3iHub (IIT Kanpur), I optimized high-load MongoDB indexing to cut p99 query latency from 450ms to 135ms and deployed OpenTelemetry distributed tracing across 15+ microservices, slashing MTTR by 85%. At Playpower Labs, I built microservices maintaining sub-100ms response times.

Resume's attached — github.com/PrathamModi001 if you'd like to check out past projects. Open to connecting?

Pratham"""
    },
    {
        "Tier": "B",
        "Company": "Ola",
        "Founder": "Bhavish Aggarwal",
        "Email": "bhavish@olacabs.com",
        "Confidence": "Pattern-guessed",
        "Source": "Founder Outreach (India)",
        "Role Pitch": "Real-Time Telemetry & Geospatial Matching Backend Engineer",
        "Subject": "Vehicle telemetry ingestion and real-time dispatch for Ola",
        "Notes": "Attached Pratham_Modi_Base_Resume.pdf; highlights C3iHub 75k daily Kafka events and Playpower Labs WebSocket concurrency",
        "Body": """Hi Bhavish,

Saw Ola scaling EV telemetry across the country and advancing autonomous vehicle software stacks.

At C3iHub (IIT Kanpur), I engineered a notification and workflow engine handling 75k daily Kafka events at 99.5% delivery reliability with automated DLQs, and cut database p99 latency from 450ms to 135ms. At Playpower Labs, I built microservices supporting sub-100ms response times.

Resume attached — github.com/PrathamModi001 for project receipts. Open to a brief chat if Ola has room in backend?

Pratham"""
    },
    {
        "Tier": "B",
        "Company": "Shadowfax",
        "Founder": "Abhishek Bansal",
        "Email": "abhishek@shadowfax.in",
        "Confidence": "Pattern-guessed",
        "Source": "Founder Outreach (India)",
        "Role Pitch": "Hyperlocal Logistics & Route Dispatch Microservices Engineer",
        "Subject": "Route dispatch event processing and microservices for Shadowfax",
        "Notes": "Attached Pratham_Modi_Base_Resume.pdf; highlights C3iHub 75k daily Kafka events and 450ms->135ms query latency drop",
        "Body": """Hi Abhishek,

Saw Shadowfax processing millions of daily hyperlocal deliveries and e-commerce shipments across India.

At C3iHub (IIT Kanpur), I architected distributed microservices processing 75k daily Kafka events at 99.5% reliability with automated dead-letter queues, and cut query p99 latency from 450ms to 135ms via compound indexing. At Playpower Labs, I built high-concurrency microservices maintaining sub-100ms response times.

Sending my resume along — would love to help scale Shadowfax's dispatch backends.

Pratham"""
    },
    {
        "Tier": "B",
        "Company": "DeHaat",
        "Founder": "Shashank Kumar",
        "Email": "shashank@agrevolution.in",
        "Confidence": "Pattern-guessed",
        "Source": "Founder Outreach (India)",
        "Role Pitch": "Agri-Commerce Telemetry & Inventory Backend Engineer",
        "Subject": "Agri-supply telemetry and microservice scaling for DeHaat",
        "Notes": "Attached Pratham_Modi_Base_Resume.pdf; highlights C3iHub 75k daily Kafka events and OpenTelemetry distributed tracing",
        "Body": """Hi Shashank,

Saw DeHaat empowering millions of farmers with full-stack agricultural services and AI-driven advisory platforms.

At C3iHub (IIT Kanpur), I designed an event-driven engine handling 75k daily Kafka events at 99.5% reliability and deployed OpenTelemetry distributed tracing across 15+ microservices. At Playpower Labs, I built low-latency streaming services maintaining sub-100ms response times.

Resume attached — open to a quick chat if DeHaat is expanding backend hiring.

Pratham"""
    }
]

# Write targets to json
out_json = Path("scratch/today_20_outreach_targets.json")
out_json.parent.mkdir(parents=True, exist_ok=True)
out_json.write_text(json.dumps(targets, indent=2), encoding="utf-8")
print(f"Wrote {len(targets)} targets to {out_json}")

# Generate JS chunks for Playwright (4 chunks of 5 targets each)
js_template = """async () => {{
    const b64 = {b64_json};
    const targets = {targets_chunk_json};
    const results = [];

    const binary = atob(b64);
    const bytes = new Uint8Array(binary.length);
    for (let j = 0; j < binary.length; j++) bytes[j] = binary.charCodeAt(j);
    const resumeBlob = new Blob([bytes], {{ type: 'application/pdf' }});

    for (let i = 0; i < targets.length; i++) {{
        const t = targets[i];
        console.log(`Processing [${{i+1}}/${{targets.length}}]: ${{t.Company}} -> ${{t.Email}}`);

        // Close any lingering compose dialogs
        const existingClose = Array.from(document.querySelectorAll('img[aria-label*="Save & close"], div[aria-label*="Save & close"], .Ha'));
        existingClose.forEach(b => b.click());
        await new Promise(r => setTimeout(r, 800));

        // Click Compose button
        const composeBtn = document.querySelector('div.T-I.T-I-KE.L3') || document.querySelector('div[gh="cm"]') || Array.from(document.querySelectorAll('div[role="button"]')).find(b => b.innerText && b.innerText.includes('Compose'));
        if (!composeBtn) {{
            results.push({{ company: t.Company, status: 'FAILED_NO_COMPOSE_BTN' }});
            continue;
        }}
        composeBtn.click();
        await new Promise(r => setTimeout(r, 1800));

        // Target active compose window
        const composeWins = document.querySelectorAll('div[role="dialog"].M9');
        const activeWin = composeWins[composeWins.length - 1] || document;

        // Fill To
        const toInput = activeWin.querySelector('input[aria-label="To recipients"], input.agP, input[peoplekit-id]');
        if (toInput) {{
            toInput.focus();
            document.execCommand('insertText', false, t.Email);
            toInput.dispatchEvent(new Event('input', {{ bubbles: true }}));
            toInput.dispatchEvent(new KeyboardEvent('keydown', {{ key: 'Enter', keyCode: 13, bubbles: true }}));
        }}

        // Fill Subject
        const subjInput = activeWin.querySelector('input[name="subjectbox"]');
        if (subjInput) {{
            subjInput.focus();
            document.execCommand('insertText', false, t.Subject);
            subjInput.dispatchEvent(new Event('input', {{ bubbles: true }}));
        }}

        // Fill Body
        const bodyDiv = activeWin.querySelector('div[aria-label="Message Body"]');
        if (bodyDiv) {{
            bodyDiv.focus();
            document.execCommand('insertText', false, t.Body);
            bodyDiv.dispatchEvent(new Event('input', {{ bubbles: true }}));
        }}

        // Attach Resume
        const fileInput = activeWin.querySelector('input[type="file"][name="Filedata"]');
        if (fileInput) {{
            const file = new File([resumeBlob], 'Pratham_Modi_Base_Resume.pdf', {{ type: 'application/pdf', lastModified: Date.now() }});
            const dt = new DataTransfer();
            dt.items.add(file);
            fileInput.files = dt.files;
            fileInput.dispatchEvent(new Event('change', {{ bubbles: true }}));
            fileInput.dispatchEvent(new Event('input', {{ bubbles: true }}));
        }}

        // Wait 3.5s for upload to initiate and complete attachment
        await new Promise(r => setTimeout(r, 3500));

        // Save & Close (leaving as draft, NEVER send)
        const closeBtn = activeWin.querySelector('img[aria-label*="Save"], div[aria-label*="Save"], .Ha');
        if (closeBtn) {{
            closeBtn.click();
            results.push({{ company: t.Company, email: t.Email, status: 'DRAFTED_AND_CLOSED' }});
        }} else {{
            results.push({{ company: t.Company, email: t.Email, status: 'ATTACHED_NO_CLOSE' }});
        }}

        await new Promise(r => setTimeout(r, 1000));
    }}

    return results;
}}
"""

chunk_size = 5
for c_idx in range(0, len(targets), chunk_size):
    chunk = targets[c_idx:c_idx+chunk_size]
    chunk_code = js_template.format(
        b64_json=json.dumps(b64_resume),
        targets_chunk_json=json.dumps(chunk)
    )
    Path(f"scratch/create_drafts_chunk_{c_idx//chunk_size}.js").write_text(chunk_code, encoding="utf-8")
    print(f"Generated scratch/create_drafts_chunk_{c_idx//chunk_size}.js for targets {c_idx+1} to {c_idx+len(chunk)}")
