const targets = [
  // 10 Global / HN / YC
  {
    to: "steve@val.town",
    founder: "Steve Krouse",
    company: "Val Town",
    subject: "Backend engineer for Val Town's runtime sandbox",
    body: `Hi Steve,\n\nLove Val Town's lightweight, composable execution model and how you turned serverless TypeScript into an interactive social platform.\n\nAt IIT Kanpur (C3iHub), I built high-throughput backend services handling 75K+ daily Kafka events and tuned database indexing to cut p99 latency from 450ms to 135ms. At Playpower Labs, I engineered real-time WebSocket pipelines sustaining 2,000+ concurrent sessions with sub-100ms response times.\n\nResume's attached -- github.com/PrathamModi001 if you want to poke around the code. Open to chatting if there's a fit.\n\nPratham`,
    rolePitch: "Runtime Sandbox & Serverless Execution Engineer",
    source: "Founder Outreach (Global)",
    tier: "B",
    notes: "Attached Pratham_Modi_Base_Resume.pdf; Prepared for Gmail dispatch; Hook: Love Val Town's lightweight, composable execution model and how you turned serverless TypeScript into an interactive social platform."
  },
  {
    to: "ajay@timescale.com",
    founder: "Ajay Kulkarni",
    company: "Timescale",
    subject: "Time-series indexing & ingestion - quick note from a backend engineer",
    body: `Hi Ajay,\n\nSaw Timescale's pgvectorscale benchmarks and automated hypertable partitioning outperforming standard PostgreSQL by orders of magnitude.\n\nAt IIT Kanpur (C3iHub), I optimized database queries and indexing to cut p99 latency from 450ms to 135ms while managing telemetry over 75K+ daily Kafka events. At Playpower Labs, I engineered low-latency retrieval pipelines delivering sub-200ms responses across 10K+ documents.\n\nSending my resume along -- happy to jump on a quick call if useful.\n\nPratham`,
    rolePitch: "Time-Series Data & PostgreSQL Extensions Backend Engineer",
    source: "Founder Outreach (Global)",
    tier: "B",
    notes: "Attached Pratham_Modi_Base_Resume.pdf; Prepared for Gmail dispatch; Hook: Saw Timescale's pgvectorscale benchmarks and automated hypertable partitioning outperforming standard PostgreSQL by orders of magnitude."
  },
  {
    to: "dor@scylladb.com",
    founder: "Dor Laor",
    company: "ScyllaDB",
    subject: "Backend engineer for ScyllaDB's low-latency streaming",
    body: `Hi Dor,\n\nFollowing ScyllaDB's shared-nothing, shard-per-core architecture delivering predictable sub-millisecond p99 latencies under extreme throughput.\n\nAt IIT Kanpur (C3iHub), I designed high-throughput distributed microservices handling 75K+ daily Kafka events at 99.5% delivery across 15+ services. At Playpower Labs, I built real-time WebSocket streaming architectures sustaining 2,000+ concurrent sessions with sub-100ms response times.\n\nResume attached. GitHub's github.com/PrathamModi001 if you want to inspect prior infra builds. Open to connecting.\n\nPratham`,
    rolePitch: "Distributed NoSQL & High-Throughput Storage Engineer",
    source: "Founder Outreach (Global)",
    tier: "B",
    notes: "Attached Pratham_Modi_Base_Resume.pdf; Prepared for Gmail dispatch; Hook: Following ScyllaDB's shared-nothing, shard-per-core architecture delivering predictable sub-millisecond p99 latencies under extreme throughput."
  },
  {
    to: "charles.xie@zilliz.com",
    founder: "Charles Xie",
    company: "Milvus",
    subject: "Vector search indexing & ingestion - quick note from a backend engineer",
    body: `Hi Charles,\n\nSaw Milvus 2.4's multi-vector search architecture and GPU-accelerated IVF indexing scaling to billion-vector enterprise datasets.\n\nAt Playpower Labs, I engineered vector retrieval pipelines delivering sub-200ms latency across 10K+ documents while cutting LLM token usage by 35%. At IIT Kanpur (C3iHub), I architected distributed ingestion pipelines handling 75K+ daily Kafka events and cut MongoDB p99 latency from 450ms to 135ms.\n\nResume's attached -- github.com/PrathamModi001 if you want more detail. Worth a quick chat about Milvus?\n\nPratham`,
    rolePitch: "Vector Search Indexing & Distributed Storage Backend Engineer",
    source: "Founder Outreach (Global)",
    tier: "B",
    notes: "Attached Pratham_Modi_Base_Resume.pdf; Prepared for Gmail dispatch; Hook: Saw Milvus 2.4's multi-vector search architecture and GPU-accelerated IVF indexing scaling to billion-vector enterprise datasets."
  },
  {
    to: "milos@deepset.ai",
    founder: "Milos Rusic",
    company: "Deepset",
    subject: "Backend engineer for Deepset Haystack async pipelines",
    body: `Hi Milos,\n\nSaw Haystack 2.0's modular pipeline graphs and declarative component routing setting open-source standards for production RAG.\n\nAt Playpower Labs, I engineered low-latency RAG and evaluation pipelines delivering sub-200ms retrieval while cutting token overhead by 35%. At IIT Kanpur (C3iHub), I deployed distributed tracing across 15+ microservices and managed event streams over 75K+ daily Kafka records.\n\nSending my resume along -- open to chatting if there's a fit.\n\nPratham`,
    rolePitch: "Haystack Pipelines & LLM Orchestration Backend Engineer",
    source: "Founder Outreach (Global)",
    tier: "B",
    notes: "Attached Pratham_Modi_Base_Resume.pdf; Prepared for Gmail dispatch; Hook: Saw Haystack 2.0's modular pipeline graphs and declarative component routing setting open-source standards for production RAG."
  },
  {
    to: "keith@tome.app",
    founder: "Keith Peiris",
    company: "Tome",
    subject: "Canvas sync & streaming - quick note from a backend engineer",
    body: `Hi Keith,\n\nSaw Tome's real-time collaborative canvas and generative layout engine structuring narrative decks from unstructured prompts.\n\nAt Playpower Labs, I built real-time WebSocket streaming architectures sustaining 2,000+ concurrent sessions with sub-100ms response times. At IIT Kanpur (C3iHub), I engineered distributed backend services handling 75K+ daily Kafka events and cut p99 database query latency from 450ms to 135ms.\n\nResume attached. GitHub's github.com/PrathamModi001 if you want to look around. Open to 10 minutes?\n\nPratham`,
    rolePitch: "Generative Workflow & Canvas Sync Backend Engineer",
    source: "Founder Outreach (Global)",
    tier: "B",
    notes: "Attached Pratham_Modi_Base_Resume.pdf; Prepared for Gmail dispatch; Hook: Saw Tome's real-time collaborative canvas and generative layout engine structuring narrative decks from unstructured prompts."
  },
  {
    to: "gabriel@dust.tt",
    founder: "Gabriel Hubert",
    company: "Dust",
    subject: "Backend engineer for Dust's assistant connectors & RAG",
    body: `Hi Gabriel,\n\nSaw Dust's extensible multi-agent workspace integrations and live sync connectors synchronizing Notion, Slack, and Google Drive.\n\nAt Playpower Labs, I engineered low-latency RAG pipelines delivering sub-200ms retrieval across 10K+ documents while reducing LLM token consumption by 35%. At IIT Kanpur (C3iHub), I designed high-throughput distributed microservices serving 50K+ users and handling 75K+ daily Kafka events.\n\nResume's attached -- github.com/PrathamModi001 if you want to explore the code. Worth a brief chat?\n\nPratham`,
    rolePitch: "Multi-Agent Data Connectors & Enterprise Knowledge Engineer",
    source: "Founder Outreach (Global)",
    tier: "B",
    notes: "Attached Pratham_Modi_Base_Resume.pdf; Prepared for Gmail dispatch; Hook: Saw Dust's extensible multi-agent workspace integrations and live sync connectors synchronizing Notion, Slack, and Google Drive."
  },
  {
    to: "mohamed@agenta.ai",
    founder: "Mohamed Razgallah",
    company: "Agenta",
    subject: "Prompt eval harnesses & tracing - quick note from a backend engineer",
    body: `Hi Mohamed,\n\nSaw Agenta's open-source LLM developer platform and automated evaluation playground accelerating agent iteration cycles.\n\nAt IIT Kanpur (C3iHub), I standardized OpenTelemetry distributed tracing across 15+ microservices, cutting MTTR by 85% over 75K+ daily Kafka events. At Playpower Labs, I engineered low-latency evaluation pipelines delivering sub-200ms retrieval and a 35% reduction in token overhead.\n\nSending my resume along -- happy to jump on a quick call if useful.\n\nPratham`,
    rolePitch: "LLM Evaluation Harness & Observability Backend Engineer",
    source: "Founder Outreach (Global)",
    tier: "B",
    notes: "Attached Pratham_Modi_Base_Resume.pdf; Prepared for Gmail dispatch; Hook: Saw Agenta's open-source LLM developer platform and automated evaluation playground accelerating agent iteration cycles."
  },
  {
    to: "daniel@unsloth.ai",
    founder: "Daniel Han",
    company: "Unsloth",
    subject: "Fine-tuning infra & memory optimization - quick note from a backend engineer",
    body: `Hi Daniel,\n\nSaw Unsloth's custom Triton kernels and manual backpropagation derivations achieving 2-5x faster fine-tuning with 80% less VRAM.\n\nAt IIT Kanpur (C3iHub), I designed high-throughput distributed microservices serving 50K+ users and cut database p99 latency from 450ms to 135ms. At Playpower Labs, I optimized retrieval and execution pipelines achieving sub-200ms response times while cutting token usage by 35%.\n\nResume attached. GitHub's github.com/PrathamModi001 if you want to inspect prior builds. Open to connecting.\n\nPratham`,
    rolePitch: "High-Performance LLM Fine-Tuning Infrastructure Engineer",
    source: "Founder Outreach (Global)",
    tier: "B",
    notes: "Attached Pratham_Modi_Base_Resume.pdf; Prepared for Gmail dispatch; Hook: Saw Unsloth's custom Triton kernels and manual backpropagation derivations achieving 2-5x faster fine-tuning with 80% less VRAM."
  },
  {
    to: "filip@wordware.ai",
    founder: "Filip Kozera",
    company: "Wordware",
    subject: "Backend engineer for Wordware's agent execution engine",
    body: `Hi Filip,\n\nSaw Wordware's web-first IDE and markdown-based prompt execution loops enabling rapid domain-specific agent orchestration.\n\nAt Playpower Labs, I built real-time WebSocket streaming architectures sustaining 2,000+ concurrent sessions with sub-100ms response times. At IIT Kanpur (C3iHub), I architected distributed event pipelines handling 75K+ daily Kafka events at 99.5% delivery with automated DLQ recovery.\n\nResume's attached -- github.com/PrathamModi001 if you want more details. Open to chatting if there's a fit.\n\nPratham`,
    rolePitch: "IDE Agent Execution & LLM Toolchain Systems Engineer",
    source: "Founder Outreach (Global)",
    tier: "B",
    notes: "Attached Pratham_Modi_Base_Resume.pdf; Prepared for Gmail dispatch; Hook: Saw Wordware's web-first IDE and markdown-based prompt execution loops enabling rapid domain-specific agent orchestration."
  },

  // 10 Indian Startups
  {
    to: "aravind@rivermobility.com",
    founder: "Aravind Mani",
    company: "River Mobility",
    subject: "IoT telemetry streaming - quick note from a backend engineer",
    body: `Hi Aravind,\n\nFollowing River's Indie SUV electric scooter rollout and how you engineered rugged hardware alongside connected vehicle telemetry in Bengaluru.\n\nAt IIT Kanpur (C3iHub), I architected an event-driven telemetry platform handling 75K+ daily Kafka events at 99.5% delivery with automated recovery. At Playpower Labs, I engineered real-time WebSocket pipelines supporting 2,000+ concurrent sessions with sub-100ms response times.\n\nResume attached. Based in Bengaluru and available immediately -- open to connecting this week?\n\nPratham`,
    rolePitch: "EV Telemetry Streaming & Fleet IoT Systems Engineer",
    source: "Founder Outreach (India)",
    tier: "B",
    notes: "Attached Pratham_Modi_Base_Resume.pdf; Prepared for Gmail dispatch; Closer: Resume attached. Based in Bengaluru and available immediately.; Hook: Following River's Indie SUV electric scooter rollout and how you engineered rugged hardware alongside connected vehicle telemetry in Bengaluru."
  },
  {
    to: "girish@greythr.com",
    founder: "Girish Rowjee",
    company: "GreytHR",
    subject: "Payroll transaction queues - quick note from a backend engineer",
    body: `Hi Girish,\n\nAdmire how GreytHR reliably processes monthly payroll and statutory compliance for over 2.3 million employees across 23,000+ companies in India.\n\nAt IIT Kanpur (C3iHub), I optimized database schemas and indexing to cut p99 query latency from 450ms to 135ms while processing 75K+ daily Kafka streaming events. At Playpower Labs, I built resilient backend microservices handling high-concurrency workloads with 99.5% delivery.\n\nResume's attached -- github.com/PrathamModi001 if you want to inspect prior builds. Open to chatting if there's a fit.\n\nPratham`,
    rolePitch: "Enterprise HRMS Cloud & Payroll Settlement Microservices Engineer",
    source: "Founder Outreach (India)",
    tier: "B",
    notes: "Attached Pratham_Modi_Base_Resume.pdf; Prepared for Gmail dispatch; Closer: Resume's attached -- github.com/PrathamModi001 if you want to inspect prior builds.; Hook: Admire how GreytHR reliably processes monthly payroll and statutory compliance for over 2.3 million employees across 23,000+ companies in India."
  },
  {
    to: "adit@leena.ai",
    founder: "Adit Jain",
    company: "Leena AI",
    subject: "Backend engineer for Leena AI's employee resolution agent",
    body: `Hi Adit,\n\nSaw Leena AI's enterprise autonomous agent WorkLM resolving complex HR, IT, and finance tickets across 400+ global enterprises.\n\nAt Playpower Labs, I engineered low-latency RAG pipelines delivering sub-200ms retrieval across 10K+ documents while cutting LLM token usage by 35%. At IIT Kanpur (C3iHub), I designed high-throughput distributed microservices serving 50K+ users and handling 75K+ daily Kafka events.\n\nSending my resume along -- based in India and open to a quick call if useful.\n\nPratham`,
    rolePitch: "Enterprise Agentic Workflow & Autonomous Resolution Backend Engineer",
    source: "Founder Outreach (India)",
    tier: "B",
    notes: "Attached Pratham_Modi_Base_Resume.pdf; Prepared for Gmail dispatch; Closer: Sending my resume along -- based in India and open to a quick call if useful.; Hook: Saw Leena AI's enterprise autonomous agent WorkLM resolving complex HR, IT, and finance tickets across 400+ global enterprises."
  },
  {
    to: "aakrit@haptik.ai",
    founder: "Aakrit Vaish",
    company: "Haptik",
    subject: "Conversational webhook backends - quick note from a backend engineer",
    body: `Hi Aakrit,\n\nSaw Haptik's Generative AI assistant gateway handling millions of conversational interactions for Jio, Whirlpool, and Zurich Insurance.\n\nAt Playpower Labs, I built real-time WebSocket streaming architectures sustaining 2,000+ concurrent sessions with sub-100ms response times. At IIT Kanpur (C3iHub), I architected distributed event pipelines handling 75K+ daily Kafka events with automated dead-letter queue recovery.\n\nResume attached. Based in Bengaluru and open to connecting if there's a fit.\n\nPratham`,
    rolePitch: "Conversational AI Gateway & High-Volume Webhook Backend Engineer",
    source: "Founder Outreach (India)",
    tier: "B",
    notes: "Attached Pratham_Modi_Base_Resume.pdf; Prepared for Gmail dispatch; Closer: Resume attached. Based in Bengaluru and open to connecting if there's a fit.; Hook: Saw Haptik's Generative AI assistant gateway handling millions of conversational interactions for Jio, Whirlpool, and Zurich Insurance."
  },
  {
    to: "naveen@glance.com",
    founder: "Naveen Tewari",
    company: "Glance",
    subject: "Backend engineer for Glance's real-time feed streaming",
    body: `Hi Naveen,\n\nFollowing Glance's scale delivering personalized lock-screen content to 300M+ active users with sub-second recommendation refreshes.\n\nAt IIT Kanpur (C3iHub), I designed high-throughput distributed microservices serving 50K+ users at 10,000+ concurrent connections, and optimized database indexing to slash p99 latency from 450ms to 135ms. At Playpower Labs, I built real-time streaming architectures with sub-100ms response times.\n\nResume's attached -- github.com/PrathamModi001 if you want to explore the code. Worth a quick chat about Glance backend scale?\n\nPratham`,
    rolePitch: "Lock-Screen Feed Ingestion & Real-Time Content Streaming Engineer",
    source: "Founder Outreach (India)",
    tier: "B",
    notes: "Attached Pratham_Modi_Base_Resume.pdf; Prepared for Gmail dispatch; Closer: Resume's attached -- github.com/PrathamModi001 if you want to explore the code.; Hook: Following Glance's scale delivering personalized lock-screen content to 300M+ active users with sub-second recommendation refreshes."
  },
  {
    to: "achuthanand@kula.ai",
    founder: "Achuthanand Ravi",
    company: "Kula AI",
    subject: "Outbound automation sync - quick note from a backend engineer",
    body: `Hi Achuthanand,\n\nSaw Kula's recruitment CRM unifying outbound sourcing across LinkedIn, GitHub, and email with automated hyper-personalized sequences.\n\nAt Playpower Labs, I engineered low-latency retrieval pipelines delivering sub-200ms responses while cutting LLM token overhead by 35%. At IIT Kanpur (C3iHub), I architected event-driven pipelines handling 75K+ daily Kafka events with 99.5% delivery.\n\nSending my resume along -- based in Bengaluru with immediate availability.\n\nPratham`,
    rolePitch: "Recruiting Workflow Sync & Outbound Automation Systems Engineer",
    source: "Founder Outreach (India)",
    tier: "B",
    notes: "Attached Pratham_Modi_Base_Resume.pdf; Prepared for Gmail dispatch; Closer: Sending my resume along -- based in Bengaluru with immediate availability.; Hook: Saw Kula's recruitment CRM unifying outbound sourcing across LinkedIn, GitHub, and email with automated hyper-personalized sequences."
  },
  {
    to: "nikunj@cutshort.io",
    founder: "Nikunj Verma",
    company: "Cutshort",
    subject: "Backend engineer for Cutshort's matchmaking workflows",
    body: `Hi Nikunj,\n\nSaw Cutshort's Voila AI recruiter automating talent matchmaking and candidate trust verification for over 25,000 tech companies in India.\n\nAt Playpower Labs, I engineered low-latency RAG pipelines delivering sub-200ms retrieval across 10K+ documents while cutting LLM token usage by 35%. In parallel at IIT Kanpur (C3iHub), I built an event-driven telemetry platform handling 75K+ daily Kafka events and cut p99 database latency from 450ms to 135ms.\n\nResume attached. GitHub's github.com/PrathamModi001 if you want to poke around the code. Open to chatting.\n\nPratham`,
    rolePitch: "Talent Intelligence & Sourcing Workflow Microservices Engineer",
    source: "Founder Outreach (India)",
    tier: "B",
    notes: "Attached Pratham_Modi_Base_Resume.pdf; Prepared for Gmail dispatch; Closer: Resume attached. GitHub's github.com/PrathamModi001 if you want to poke around the code.; Hook: Saw Cutshort's Voila AI recruiter automating talent matchmaking and candidate trust verification for over 25,000 tech companies in India."
  },
  {
    to: "yamini@vymo.com",
    founder: "Yamini Bhat",
    company: "Vymo",
    subject: "Mobile telemetry ingestion - quick note from a backend engineer",
    body: `Hi Yamini,\n\nFollowing Vymo's sales engagement platform powering 350K+ financial advisors across top global BFSI institutions like Berkshire Hathaway and HDFC Bank.\n\nAt IIT Kanpur (C3iHub), I architected distributed microservices handling 75K+ daily Kafka events at 99.5% delivery across 15+ services with automated DLQ recovery. At Playpower Labs, I built real-time WebSocket streaming architectures sustaining 2,000+ concurrent sessions with sub-100ms response times.\n\nResume's attached -- based in Bengaluru and open to a quick call if useful.\n\nPratham`,
    rolePitch: "Sales Engagement Cloud & Distributed Mobile Telemetry Engineer",
    source: "Founder Outreach (India)",
    tier: "B",
    notes: "Attached Pratham_Modi_Base_Resume.pdf; Prepared for Gmail dispatch; Closer: Resume's attached -- based in Bengaluru and open to a quick call if useful.; Hook: Following Vymo's sales engagement platform powering 350K+ financial advisors across top global BFSI institutions like Berkshire Hathaway and HDFC Bank."
  },
  {
    to: "sanjeev@wizcommerce.com",
    founder: "Sanjeev Neelarapu",
    company: "WizCommerce",
    subject: "B2B order processing & catalog search - quick note from a backend engineer",
    body: `Hi Sanjeev,\n\nSaw WizCommerce digitizing wholesale order capture and AI visual discovery for global B2B manufacturers and enterprise suppliers.\n\nAt IIT Kanpur (C3iHub), I optimized database schemas and indexing to cut p99 query latency from 450ms to 135ms while serving 50K+ users. At Playpower Labs, I engineered low-latency retrieval pipelines delivering sub-200ms responses across 10K+ catalog entries while reducing token usage by 35%.\n\nSending my resume along -- based in Bengaluru with immediate availability.\n\nPratham`,
    rolePitch: "B2B Catalog Search & Order Processing Systems Engineer",
    source: "Founder Outreach (India)",
    tier: "B",
    notes: "Attached Pratham_Modi_Base_Resume.pdf; Prepared for Gmail dispatch; Closer: Sending my resume along -- based in Bengaluru with immediate availability.; Hook: Saw WizCommerce digitizing wholesale order capture and AI visual discovery for global B2B manufacturers and enterprise suppliers."
  },
  {
    to: "kunal@onfinance.ai",
    founder: "Kunal Kislay",
    company: "OnFinance AI",
    subject: "BFSI financial copilot & RAG - quick note from a backend engineer",
    body: `Hi Kunal,\n\nSaw OnFinance's NeoGPT reasoning copilot driving compliance and financial research workflows with accurate regulatory RAG.\n\nAt Playpower Labs, I engineered low-latency RAG pipelines delivering sub-200ms retrieval across 10K+ documents while cutting LLM token usage by 35%. At IIT Kanpur (C3iHub), I designed high-throughput distributed microservices handling 75K+ daily Kafka events at 99.5% delivery.\n\nResume attached. GitHub's github.com/PrathamModi001 if you want to look at prior builds. Worth exploring?\n\nPratham`,
    rolePitch: "BFSI Financial Copilot & Regulatory Rag Infrastructure Engineer",
    source: "Founder Outreach (India)",
    tier: "B",
    notes: "Attached Pratham_Modi_Base_Resume.pdf; Prepared for Gmail dispatch; Closer: Resume attached. GitHub's github.com/PrathamModi001 if you want to look at prior builds.; Hook: Saw OnFinance's NeoGPT reasoning copilot driving compliance and financial research workflows with accurate regulatory RAG."
  }
];

async function draftAll() {
  const results = [];
  const res = await fetch("http://127.0.0.1:8765/resume.pdf");
  const blob = await res.blob();
  
  for (let i = 0; i < targets.length; i++) {
    const t = targets[i];
    
    // 1. Click Compose
    const composeBtn = document.querySelector('div[gh="cm"]') || 
                       Array.from(document.querySelectorAll('div[role="button"]')).find(el => el.innerText.trim() === 'Compose');
    if (!composeBtn) {
      results.push({ target: t.to, error: "Compose button not found" });
      continue;
    }
    composeBtn.click();
    await new Promise(r => setTimeout(r, 1500));
    
    // 2. Recipient
    const toInput = document.querySelector('input[aria-label="To recipients"]') || 
                    document.querySelector('input[name="to"]') || 
                    document.querySelector('input[role="combobox"]');
    if (!toInput) {
      results.push({ target: t.to, error: "To input not found" });
      continue;
    }
    toInput.focus();
    toInput.value = t.to;
    toInput.dispatchEvent(new Event("input", { bubbles: true }));
    toInput.dispatchEvent(new KeyboardEvent("keydown", { key: "Enter", keyCode: 13, bubbles: true }));
    toInput.dispatchEvent(new KeyboardEvent("keyup", { key: "Enter", keyCode: 13, bubbles: true }));
    await new Promise(r => setTimeout(r, 500));
    
    // 3. Subject
    const subjectInput = document.querySelector('input[name="subjectbox"]') || 
                         document.querySelector('input[placeholder="Subject"]');
    if (!subjectInput) {
      results.push({ target: t.to, error: "Subject input not found" });
      continue;
    }
    subjectInput.focus();
    subjectInput.value = t.subject;
    subjectInput.dispatchEvent(new Event("input", { bubbles: true }));
    await new Promise(r => setTimeout(r, 500));
    
    // 4. Body
    const bodyEl = document.querySelector('div[role="textbox"][aria-label="Message Body"]');
    if (!bodyEl) {
      results.push({ target: t.to, error: "Body textbox not found" });
      continue;
    }
    bodyEl.focus();
    bodyEl.innerText = t.body;
    bodyEl.dispatchEvent(new Event("input", { bubbles: true }));
    await new Promise(r => setTimeout(r, 500));
    
    // 5. Attach Resume
    const file = new File([blob], "Pratham_Modi_Base_Resume.pdf", { type: "application/pdf" });
    const fileInput = document.querySelector('input[type="file"][name="Filedata"]') || document.querySelector('input[type="file"]');
    if (!fileInput) {
      results.push({ target: t.to, error: "File input not found" });
      continue;
    }
    const dt = new DataTransfer();
    dt.items.add(file);
    fileInput.files = dt.files;
    fileInput.dispatchEvent(new Event("input", { bubbles: true }));
    fileInput.dispatchEvent(new Event("change", { bubbles: true }));
    
    // Wait for attachment to finish attaching
    await new Promise(r => setTimeout(r, 2200));
    
    // 6. Save & close
    const closeBtn = document.querySelector('img[aria-label="Save & close"]') || 
                     document.querySelector('button[aria-label="Save & close"]') || 
                     document.querySelector('[data-tooltip="Save & close"]') ||
                     document.querySelector('div.Ha');
    if (!closeBtn) {
      results.push({ target: t.to, error: "Save & close button not found" });
      continue;
    }
    closeBtn.click();
    await new Promise(r => setTimeout(r, 1200));
    
    results.push({ target: t.to, success: true });
  }
  return results;
}

draftAll();
