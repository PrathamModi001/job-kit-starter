const targets = [
  {
    to: "michael@phind.com",
    subject: "Fast search pipelines & agent runtimes for Phind",
    body: `Hi Michael,\n\nSaw Phind's 70B model iterations and instant search-to-answer latency outperforming traditional developer search engines.\n\nAt Playpower Labs, I engineered low-latency RAG pipelines delivering sub-200ms retrieval across 10K+ documents while cutting LLM token usage by 35%. Previously at IIT Kanpur (C3iHub), I built an event-driven telemetry platform processing 75K+ daily Kafka events and tuned database indexing to slash p99 query latency from 450ms to 135ms.\n\nAttached is my resume. Would love to bring these low-latency retrieval and indexing techniques to Phind's search infrastructure—worth a quick conversation?\n\nWarmly,\nPratham Modi`
  },
  {
    to: "karan@cartesia.ai",
    subject: "Low-latency streaming & async pipelines for Cartesia",
    body: `Hi Karan,\n\nSaw Cartesia's Sonic voice model achieving sub-100ms end-to-end voice latency and state-space architectures.\n\nAt Playpower Labs, I built real-time WebSocket streaming architectures sustaining 2,000+ concurrent sessions with sub-100ms response times. At IIT Kanpur (C3iHub), I architected distributed event pipelines handling 75K+ daily Kafka events at 99.5% delivery across 15+ microservices with automated DLQ recovery.\n\nAttached is my resume. Would love to help scale Cartesia's real-time streaming audio backends and low-latency API infrastructure—open to connecting this week?\n\nCheers,\nPratham Modi`
  },
  {
    to: "dean@decart.ai",
    subject: "10 min re: Decart AI backend & real-time infra",
    body: `Hi Dean,\n\nSaw Decart's Oasis world model generating playable real-time video simulations at interactive framerates.\n\nAt IIT Kanpur (C3iHub), I designed high-throughput distributed microservices serving 50K+ users at 10,000+ concurrent connections, and optimized database indexing to cut p99 latency from 450ms to 135ms. At Playpower Labs, I built low-latency RAG and streaming pipelines achieving sub-200ms response times while cutting token overhead by 35%.\n\nAttached is my resume. Would love to contribute to Decart's high-performance inference delivery and state orchestration pipelines—open to 10 minutes?\n\nBest,\nPratham Modi`
  },
  {
    to: "taranjeet@mem0.ai",
    subject: "Memory retrieval & high-throughput pipelines for Mem0",
    body: `Hi Taranjeet,\n\nSaw Mem0's universal memory layer and graph-memory hybrid retrieval solving long-term context retention for AI agents.\n\nAt Playpower Labs, I engineered low-latency RAG pipelines delivering sub-200ms retrieval across 10K+ documents while reducing LLM token consumption by 35%. In parallel at IIT Kanpur (C3iHub), I built an event-driven telemetry platform handling 75K+ daily Kafka events and cut p99 database query latency from 450ms to 135ms.\n\nAttached is my resume. Would love to bring these memory indexing and high-throughput backend patterns to Mem0—worth exploring?\n\nRegards,\nPratham Modi`
  },
  {
    to: "joel@parea.ai",
    subject: "LLM evaluation tracing & backend systems for Parea AI",
    body: `Hi Joel,\n\nSaw Parea's evaluation logging and automated prompt experiment suites helping production teams debug complex agentic graphs.\n\nAt IIT Kanpur (C3iHub), I deployed OpenTelemetry distributed tracing across 15+ microservices, cutting MTTR by 85% and processing 75K+ daily Kafka events at 99.5% delivery. At Playpower Labs, I built low-latency evaluation and RAG pipelines achieving sub-200ms retrieval and a 35% reduction in token overhead.\n\nAttached is my resume. Would love to help build high-throughput telemetry ingestion and tracing backends for Parea—open to a quick chat?\n\nThanks,\nPratham Modi`
  },
  {
    to: "jason@arize.com",
    subject: "Distributed tracing & agent observability for Arize",
    body: `Hi Jason,\n\nSaw Arize AX and Phoenix establishing deep tracing standards for multi-agent workflows and evals.\n\nAt IIT Kanpur (C3iHub), I standardized OpenTelemetry distributed tracing across 15+ microservices, reducing MTTR by 85% and maintaining real-time telemetry over 75K+ daily Kafka events. At Playpower Labs, I optimized vector retrieval latency to sub-200ms across 10K+ documents and reduced LLM token footprint by 35%.\n\nAttached is my resume. Would love to contribute to Arize's high-cardinality telemetry ingestion and Phoenix tracing pipelines—open to connecting?\n\nSincerely,\nPratham Modi`
  },
  {
    to: "david@tracecat.com",
    subject: "Event-driven workflow engines & queue infra for Tracecat",
    body: `Hi David,\n\nSaw Tracecat's open-source security orchestration engine and async workflow builders automating complex alert response.\n\nAt IIT Kanpur (C3iHub), I architected an event-driven automation platform handling 75K+ daily Kafka events at 99.5% delivery with automated dead-letter queue recovery. At Playpower Labs, I engineered real-time WebSocket pipelines supporting 2,000+ concurrent sessions with sub-100ms response times.\n\nAttached is my resume. Would love to help scale Tracecat's workflow runner and distributed execution queues—worth a short call?\n\nBest regards,\nPratham Modi`
  },
  {
    to: "nick@cohere.com",
    subject: "RAG retrieval latency & tool-use backends for Cohere",
    body: `Hi Nick,\n\nSaw Cohere's Command R+ model series and high-precision RAG connectors setting enterprise benchmarks in grounded generation.\n\nAt Playpower Labs, I engineered low-latency RAG pipelines delivering sub-200ms retrieval across 10K+ documents while cutting LLM token usage by 35%. At IIT Kanpur (C3iHub), I designed high-throughput distributed microservices serving 50K+ users at 10,000+ concurrent connections, and optimized database indexing to slash p99 latency from 450ms to 135ms.\n\nAttached is my resume. Would love to bring these high-performance retrieval and API patterns to Cohere's platform team—open to a brief chat?\n\nWarm regards,\nPratham Modi`
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
    await new Promise(r => setTimeout(r, 2000));
    
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
