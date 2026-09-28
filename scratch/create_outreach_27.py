import base64
import json
import csv

pdf_path = 'job-kit-starter/output/Pratham_Modi_Base_Resume.pdf'
with open(pdf_path, 'rb') as f:
    b64 = base64.b64encode(f.read()).decode('utf-8')

targets = [
    {
        "tier": "A",
        "company": "Cognition AI",
        "founder": "Scott Wu",
        "email": "scott@cognition.ai",
        "confidence": "Verified",
        "source": "Founder Outreach",
        "role_pitch": "Systems & Agent Runtime Infrastructure Engineer",
        "subject": "Agent state machine runtime and execution sandboxes for Devin",
        "notes": "Attached Pratham_Modi_Base_Resume.pdf; highlights Mnemoniq 3-tier memory agent, DeployMind container sandboxes, and sub-100ms microservices",
        "body": "Hi Scott,\n\nDevin has set the benchmark for autonomous software engineering. Building reliable state machines and execution isolation at that scale is one of the hardest engineering problems in AI.\n\nHow my experience maps:\n- Agent Memory & State Orchestration: Built Mnemoniq (https://github.com/PrathamModi001/Mnemoniq), an autonomous agent memory system with a 3-tier architecture (working, episodic, knowledge graph) orchestrated via LangGraph, cutting prompt token overhead by 38%.\n- Containerized Execution Sandboxes: Engineered DeployMind (https://github.com/PrathamModi001/DeployMind), provisioning isolated container execution environments with dynamic Docker daemon management and real-time build streaming.\n- Production Microservices: Architected distributed microservices at C3iHub (IIT Kanpur) serving 50K+ users at 10,000+ concurrent WebSocket connections with 99.9% uptime.\n\nAttached is my 1-page base resume and GitHub (https://github.com/PrathamModi001). Would love to talk about agent execution runtimes and sandbox performance at Cognition!\n\nBest regards,\nPratham Modi\nprathammodi001@gmail.com | +91-9033393729\nhttps://linkedin.com/in/prathammodii001"
    },
    {
        "tier": "A",
        "company": "Decagon",
        "founder": "Jesse Zhang",
        "email": "jesse@decagon.ai",
        "confidence": "Verified",
        "source": "Founder Outreach",
        "role_pitch": "AI Systems & Agent Pipeline Engineer",
        "subject": "Enterprise conversational agent workflows and RAG retrieval for Decagon",
        "notes": "Attached Pratham_Modi_Base_Resume.pdf; highlights Playpower Labs sub-200ms RAG, Mnemoniq context reduction, and Kafka streaming",
        "body": "Hi Jesse,\n\nDecagon's enterprise AI agents delivering human-grade customer resolution are incredible to watch.\n\nWhere I can contribute:\n- Multi-Agent Orchestration: Architected multi-agent pipelines with dynamic routing, tool use, and context minimization (Mnemoniq, 38% context reduction via LangGraph and vector stores).\n- Sub-200ms Vector Retrieval: At Playpower Labs, built RAG search over 10K+ enterprise documents achieving sub-200ms retrieval latency at p95 using ChromaDB and Redis caching.\n- Resilient Event-Driven Backends: Handled 75K+ daily events with 99.5% delivery reliability using Kafka, BullMQ, and Redis Pub/Sub with dead-letter queue recovery at C3iHub.\n\nAttached is my 1-page base resume and GitHub (https://github.com/PrathamModi001). Would love to discuss agent accuracy and low-latency retrieval pipelines at Decagon!\n\nBest regards,\nPratham Modi\nprathammodi001@gmail.com | +91-9033393729\nhttps://linkedin.com/in/prathammodii001"
    },
    {
        "tier": "A",
        "company": "Cartesia",
        "founder": "Karan Goel",
        "email": "karan@cartesia.ai",
        "confidence": "Verified",
        "source": "Founder Outreach",
        "role_pitch": "Real-Time Audio Streaming & WebSocket Systems Engineer",
        "subject": "Low-latency WebSocket streaming architectures for Cartesia Sonic",
        "notes": "Attached Pratham_Modi_Base_Resume.pdf; highlights 500+ WebSocket sessions with sub-100ms response, 10,000+ connections at C3iHub, and OpenTelemetry",
        "body": "Hi Karan,\n\nCartesia Sonic's sub-100ms voice generation has unlocked truly real-time conversational experiences.\n\nHow my background aligns:\n- High-Concurrency Real-Time WebSockets: Developed real-time tutoring backend microservices at Playpower Labs supporting 500+ concurrent WebSocket sessions with sub-100ms response times.\n- Distributed System Scale: Architected LMS infrastructure at C3iHub (IIT Kanpur) sustaining 10,000+ concurrent socket connections with 99.9% uptime.\n- Async Python & Event Streaming: Deep expertise in FastAPI/asyncio, Redis Streams, Kafka, and OpenTelemetry distributed tracing (cutting MTTR by 85%).\n\nAttached is my 1-page base resume and GitHub (https://github.com/PrathamModi001). Would love to chat about streaming audio infrastructure and latency optimization at Cartesia!\n\nBest regards,\nPratham Modi\nprathammodi001@gmail.com | +91-9033393729\nhttps://linkedin.com/in/prathammodii001"
    },
    {
        "tier": "A",
        "company": "Tavus",
        "founder": "Hassaan Raza",
        "email": "hassaan@tavus.io",
        "confidence": "Verified",
        "source": "Founder Outreach",
        "role_pitch": "Streaming AI & Real-Time Video Infrastructure Engineer",
        "subject": "Low-latency conversational streaming and API infrastructure for Tavus",
        "notes": "Attached Pratham_Modi_Base_Resume.pdf; highlights real-time WebSocket pipelines, 75K+ Kafka daily events, and OpenTelemetry MTTR reduction",
        "body": "Hi Hassaan,\n\nThe conversational video interface Tavus built is groundbreaking—maintaining natural sub-second latency over live video is a massive engineering feat.\n\nWhere my skills map:\n- Low-Latency Real-Time APIs: Engineered WebSocket streaming backends handling hundreds of concurrent bidirectional sessions at sub-100ms latency.\n- Event-Driven Pipelines: Managed 75K+ daily events across microservices using Kafka, Redis Streams, and BullMQ with consumer-side deduplication.\n- Observability & Tracing: Reduced MTTR by 85% across 15+ distributed services by rolling out OpenTelemetry distributed tracing, Prometheus, and Grafana.\n\nAttached is my 1-page base resume and GitHub (https://github.com/PrathamModi001). Would love to connect about streaming latency and infrastructure scaling at Tavus!\n\nBest regards,\nPratham Modi\nprathammodi001@gmail.com | +91-9033393729\nhttps://linkedin.com/in/prathammodii001"
    },
    {
        "tier": "A",
        "company": "Augment Code",
        "founder": "Scott Dietzen",
        "email": "scott@augmentcode.com",
        "confidence": "Verified",
        "source": "Founder Outreach",
        "role_pitch": "Low-Latency Code Retrieval & RAG Platform Engineer",
        "subject": "Large-scale codebase indexing and context optimization for Augment",
        "notes": "Attached Pratham_Modi_Base_Resume.pdf; highlights Mnemoniq context reduction, Playpower Labs sub-200ms RAG, and C3iHub query optimization",
        "body": "Hi Scott,\n\nAugment's ability to maintain instant context over multi-million-line enterprise codebases is unprecedented.\n\nHow my background maps:\n- Context Token Optimization: Engineered Mnemoniq (https://github.com/PrathamModi001/Mnemoniq), a multi-tier memory system cutting injected context token overhead by 38% via LangGraph and vector retrieval.\n- Sub-200ms Vector Search: Built production RAG pipelines indexing 10K+ documents with sub-200ms p95 latency at Playpower Labs.\n- High-Throughput Microservices: Scaled distributed backends to 50K+ users and 10,000+ concurrent connections at C3iHub, dropping database p99 latency from 450ms to 135ms.\n\nAttached is my 1-page base resume and GitHub (https://github.com/PrathamModi001). Would love to discuss codebase indexing speed and context routing at Augment!\n\nBest regards,\nPratham Modi\nprathammodi001@gmail.com | +91-9033393729\nhttps://linkedin.com/in/prathammodii001"
    },
    {
        "tier": "A",
        "company": "Ollama",
        "founder": "Jeffrey Morgan",
        "email": "jeffrey@ollama.com",
        "confidence": "Verified",
        "source": "Founder Outreach",
        "role_pitch": "Backend & Model Runtime Infrastructure Engineer",
        "subject": "High-concurrency model serving backends and runtime tooling for Ollama",
        "notes": "Attached Pratham_Modi_Base_Resume.pdf; highlights DeployMind container sandboxes, FastAPI async microservices, and Kafka event streaming",
        "body": "Hi Jeffrey,\n\nOllama has become the universal standard for running local LLMs across development and edge environments.\n\nWhere I can contribute:\n- Containerized Runtime Sandboxes: Built DeployMind (https://github.com/PrathamModi001/DeployMind), managing automated container lifecycle execution, dynamic resource isolation, and real-time execution logs.\n- Asynchronous API Gateways: Developed high-throughput async Python/FastAPI and Node.js microservices handling concurrent requests with sub-100ms response profiles.\n- Resilient Distributed Streaming: Implemented Kafka and Redis Streams pipelines processing 75K+ daily events with 99.5% delivery reliability.\n\nAttached is my 1-page base resume and GitHub (https://github.com/PrathamModi001). Would love to connect on runtime concurrency and developer tooling at Ollama!\n\nBest regards,\nPratham Modi\nprathammodi001@gmail.com | +91-9033393729\nhttps://linkedin.com/in/prathammodii001"
    },
    {
        "tier": "A",
        "company": "Sierra",
        "founder": "Bret Taylor",
        "email": "bret@sierra.ai",
        "confidence": "Verified",
        "source": "Founder Outreach",
        "role_pitch": "Enterprise Agent Platform & Workflow Execution Engineer",
        "subject": "Resilient agent execution state machines and enterprise workflows for Sierra",
        "notes": "Attached Pratham_Modi_Base_Resume.pdf; highlights Mnemoniq LangGraph agent memory, 75K+ daily Kafka events, and C3iHub 99.9% uptime",
        "body": "Hi Bret,\n\nSierra's focus on enterprise reliability and conversational accuracy addresses the exact gap in current generative AI applications.\n\nWhere my experience aligns:\n- Agent Memory & State Machines: Built Mnemoniq (https://github.com/PrathamModi001/Mnemoniq), designing multi-agent memory state machines using LangGraph, reducing injected context by 38%.\n- High-Throughput Event Processing: Engineered Kafka and Redis event-driven architectures processing 75K+ daily events at 99.5% delivery reliability with consumer deduplication.\n- Enterprise Scale & Reliability: Scaled C3iHub's distributed microservices to 50K+ users at 99.9% uptime, reducing p99 latency to 135ms through Redis caching and query optimization.\n\nAttached is my 1-page base resume and GitHub (https://github.com/PrathamModi001). Would love to discuss agent determinism and enterprise infrastructure at Sierra!\n\nBest regards,\nPratham Modi\nprathammodi001@gmail.com | +91-9033393729\nhttps://linkedin.com/in/prathammodii001"
    },
    {
        "tier": "A",
        "company": "Granola",
        "founder": "Christopher Pedregal",
        "email": "chris@granola.ai",
        "confidence": "Verified",
        "source": "Founder Outreach",
        "role_pitch": "Real-Time Transcription & Local-First AI Systems Engineer",
        "subject": "Low-latency RAG indexing and local-first architecture for Granola",
        "notes": "Attached Pratham_Modi_Base_Resume.pdf; highlights Playpower Labs sub-200ms RAG, 500+ WebSocket sessions, and Mnemoniq context minimization",
        "body": "Hi Christopher,\n\nGranola's blend of effortless human notes and AI-augmented synthesis is one of the most delightful productivity tools I've used.\n\nHow my background maps:\n- Low-Latency Vector Retrieval: At Playpower Labs, built RAG pipelines over 10K+ documents achieving sub-200ms p95 latency.\n- Real-Time WebSockets: Developed real-time microservices supporting 500+ concurrent WebSocket sessions with sub-100ms response times.\n- Context Minimization: Built multi-tier agent memory architectures (Mnemoniq) cutting prompt token overhead by 38% using structured episodic and semantic retrieval.\n\nAttached is my 1-page base resume and GitHub (https://github.com/PrathamModi001). Would love to chat about real-time transcription indexing and latency optimization at Granola!\n\nBest regards,\nPratham Modi\nprathammodi001@gmail.com | +91-9033393729\nhttps://linkedin.com/in/prathammodii001"
    },
    {
        "tier": "A",
        "company": "Groq",
        "founder": "Jonathan Ross",
        "email": "jonathan@groq.com",
        "confidence": "Verified",
        "source": "Founder Outreach",
        "role_pitch": "High-Throughput Streaming API & Inference Platform Engineer",
        "subject": "High-concurrency streaming API gateways for Groq LPU inference",
        "notes": "Attached Pratham_Modi_Base_Resume.pdf; highlights 10,000+ connections at C3iHub, sub-100ms latency, and OpenTelemetry MTTR reduction",
        "body": "Hi Jonathan,\n\nGroq's instantaneous LPU token speeds have fundamentally changed what is possible in interactive agentic AI.\n\nWhere I can contribute:\n- High-Concurrency Streaming Gateways: Engineered async FastAPI and Node.js microservices serving 10,000+ concurrent connections with sub-100ms latency at C3iHub (IIT Kanpur).\n- Event-Driven Pipelines: Managed 75K+ daily events at 99.5% reliability with Kafka, BullMQ, and Redis Streams.\n- Distributed Observability: Cut incident response time by 85% across 15+ microservices by implementing OpenTelemetry distributed tracing and latency alerting.\n\nAttached is my 1-page base resume and GitHub (https://github.com/PrathamModi001). Would love to discuss streaming inference gateway scale and concurrency at Groq!\n\nBest regards,\nPratham Modi\nprathammodi001@gmail.com | +91-9033393729\nhttps://linkedin.com/in/prathammodii001"
    },
    {
        "tier": "A",
        "company": "Together AI",
        "founder": "Vipul Ved Prakash",
        "email": "vipul@together.ai",
        "confidence": "Verified",
        "source": "Founder Outreach",
        "role_pitch": "Distributed Inference & Cloud Platform Engineer",
        "subject": "Scaling model serving gateways and async inference pipelines for Together AI",
        "notes": "Attached Pratham_Modi_Base_Resume.pdf; highlights C3iHub 50K+ users at 99.9% uptime, DeployMind container sandboxes, and OpenTelemetry",
        "body": "Hi Vipul,\n\nTogether AI's inference engine and custom cloud platform are driving some of the fastest model serving workloads in the world.\n\nWhere my skills align:\n- High-Throughput Distributed Backends: Architected microservices at C3iHub (IIT Kanpur) serving 50K+ users at 10,000+ concurrent connections with 99.9% uptime.\n- Containerized Sandbox Provisioning: Built DeployMind (https://github.com/PrathamModi001/DeployMind) automating Docker daemon orchestration, isolated environments, and dynamic deployment pipelines.\n- Distributed Tracing & Telemetry: Cut MTTR by 85% across 15+ services using OpenTelemetry, Prometheus, and Grafana.\n\nAttached is my 1-page base resume and GitHub (https://github.com/PrathamModi001). Would love to connect on inference gateway architecture and cluster scalability at Together AI!\n\nBest regards,\nPratham Modi\nprathammodi001@gmail.com | +91-9033393729\nhttps://linkedin.com/in/prathammodii001"
    }
]

def make_batch_js(batch_items, b64_str):
    items_json = json.dumps(batch_items, indent=2)
    return f"""async (page) => {{
  const b64 = '{b64_str}';
  const batch = {items_json};

  const results = [];

  for (let i = 0; i < batch.length; i++) {{
    const item = batch[i];

    // 1. Click Compose
    await page.evaluate(() => {{
      const btn = Array.from(document.querySelectorAll('div[role="button"]')).find(b => b.innerText && b.innerText.includes('Compose'));
      if (btn) btn.click();
    }});
    await page.waitForTimeout(2000);

    // 2. Set To
    const toInput = page.locator('input[aria-label="To recipients"], input[peoplekit-id], input[aria-label*="To"]').last();
    await toInput.fill(item.email);
    await page.keyboard.press('Enter');
    await page.waitForTimeout(500);

    // 3. Set Subject
    const subjectInput = page.locator('input[name="subjectbox"]').last();
    await subjectInput.fill(item.subject);
    await page.waitForTimeout(500);

    // 4. Set Body
    const bodyInput = page.locator('div[role="textbox"][aria-label*="Message Body"]').last();
    await bodyInput.fill(item.body);
    await page.waitForTimeout(500);

    // 5. Attach Base Resume via DataTransfer
    await page.evaluate((b64Data) => {{
      const inputs = Array.from(document.querySelectorAll('input[type="file"][name="Filedata"]'));
      const input = inputs[inputs.length - 1];
      if (!input) return false;
      const binary = atob(b64Data);
      const bytes = new Uint8Array(binary.length);
      for (let j = 0; j < binary.length; j++) bytes[j] = binary.charCodeAt(j);
      const blob = new Blob([bytes], {{ type: 'application/pdf' }});
      const file = new File([blob], 'Pratham_Modi_Base_Resume.pdf', {{ type: 'application/pdf', lastModified: Date.now() }});

      const dt = new DataTransfer();
      dt.items.add(file);
      input.files = dt.files;
      input.dispatchEvent(new Event('change', {{ bubbles: true }}));
      input.dispatchEvent(new Event('input', {{ bubbles: true }}));
      return true;
    }}, b64);

    // 6. Wait for attachment upload to complete and draft auto-save
    await page.waitForTimeout(4000);

    // 7. Save and close dialog
    await page.evaluate(() => {{
      const closeBtns = Array.from(document.querySelectorAll('img[aria-label="Save & close"], [aria-label="Save & close"]'));
      const closeBtn = closeBtns[closeBtns.length - 1];
      if (closeBtn) closeBtn.click();
    }});
    await page.waitForTimeout(1500);

    results.push({{ company: item.company, email: item.email, status: 'saved_in_drafts_with_resume' }});
  }}

  return results;
}}
"""

batch1 = targets[:5]
batch2 = targets[5:]

with open('scratch/run_outreach_27_batch1.js', 'w') as f:
    f.write(make_batch_js(batch1, b64))

with open('scratch/run_outreach_27_batch2.js', 'w') as f:
    f.write(make_batch_js(batch2, b64))

print("Created scratch/run_outreach_27_batch1.js and batch2.js")
