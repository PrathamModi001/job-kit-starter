async (page) => {
  const targets = [{"company": "Pango", "founder": "Steve", "email": "steve@pango.ai", "confidence": "Verified", "role_pitch": "Founding Backend & AI Agent Engineer", "subject": "Autonomous agent infrastructure for Pango — quick note", "hook": "Saw Pango’s YC S26 launch — building the world’s first autonomous agent workforce requires robust, reproducible backend tooling.", "metric_a_co": "Playpower Labs", "metric_a": "designed and shipped multi-agent workflows and sub-200ms RAG retrieval architectures", "metric_b_co": "C3iHub", "metric_b": "managed Kafka event-driven pipelines handling 75K+ telemetry and transaction events daily", "closer": "Resume attached — github.com/PrathamModi001. Worth a brief chat about founding backend engineering at Pango?", "notes": "Attached Pratham_Modi_Base_Resume.pdf; highlights agent workflows, LangGraph, and Kafka streaming", "source": "HN (id: 49522897)", "tier": "B", "body": "Saw Pango’s YC S26 launch — building the world’s first autonomous agent workforce requires robust, reproducible backend tooling.\n\nAt Playpower Labs, I designed and shipped multi-agent workflows and sub-200ms RAG retrieval architectures. At C3iHub, I managed Kafka event-driven pipelines handling 75K+ telemetry and transaction events daily.\n\nResume attached — github.com/PrathamModi001. Worth a brief chat about founding backend engineering at Pango?\n\nPratham"}, {"company": "Catalyst Wayfare AI", "founder": "Hiring Team", "email": "hn@cwai.co", "confidence": "Verified", "role_pitch": "AI Agent Systems & Execution Backends Engineer", "subject": "Scalable agent execution runtimes for Catalyst Wayfare AI — quick note", "hook": "Saw your HN post for Catalyst Wayfare AI — building production agent architectures that reliably solve enterprise tasks is the real frontier.", "metric_a_co": "Playpower Labs", "metric_a": "engineered low-latency RAG vector ingestion pipelines maintaining sub-200ms query response times", "metric_b_co": "C3iHub", "metric_b": "implemented OpenTelemetry tracing and Prometheus dashboards achieving 99.9% system uptime", "closer": "Resume attached — github.com/PrathamModi001. Would love to connect about agent engineering at Catalyst Wayfare AI.", "notes": "Attached Pratham_Modi_Base_Resume.pdf; highlights RAG, OpenTelemetry, and agent runtimes", "source": "HN (id: 49522897)", "tier": "B", "body": "Saw your HN post for Catalyst Wayfare AI — building production agent architectures that reliably solve enterprise tasks is the real frontier.\n\nAt Playpower Labs, I engineered low-latency RAG vector ingestion pipelines maintaining sub-200ms query response times. At C3iHub, I implemented OpenTelemetry tracing and Prometheus dashboards achieving 99.9% system uptime.\n\nResume attached — github.com/PrathamModi001. Would love to connect about agent engineering at Catalyst Wayfare AI.\n\nPratham"}, {"company": "Biobase", "founder": "Hiring Team", "email": "jobs@biobase.ai", "confidence": "Verified", "role_pitch": "Technical Product & Platform Infrastructure Engineer", "subject": "Scalable life-sciences data platforms for Biobase — quick note", "hook": "Saw your HN post for Biobase — building modern technical software platforms for biotechnology requires uncompromising data reliability.", "metric_a_co": "C3iHub", "metric_a": "optimized complex MongoDB document queries, cutting p99 latency from 450ms down to 135ms", "metric_b_co": "C3iHub", "metric_b": "orchestrated distributed Kafka pipelines handling 75K events daily with sub-second delivery", "closer": "Resume attached — github.com/PrathamModi001. Is Biobase open to technical product / platform engineers?", "notes": "Attached Pratham_Modi_Base_Resume.pdf; highlights database query optimization and event streaming", "source": "HN (id: 49522897)", "tier": "B", "body": "Saw your HN post for Biobase — building modern technical software platforms for biotechnology requires uncompromising data reliability.\n\nAt C3iHub, I optimized complex MongoDB document queries, cutting p99 latency from 450ms down to 135ms. At C3iHub, I orchestrated distributed Kafka pipelines handling 75K events daily with sub-second delivery.\n\nResume attached — github.com/PrathamModi001. Is Biobase open to technical product / platform engineers?\n\nPratham"}, {"company": "Lucia", "founder": "Emily Thompson", "email": "emily.thompson@luciaprotocol.com", "confidence": "Verified", "role_pitch": "Distributed Systems & MLOps Infrastructure Engineer", "subject": "High-throughput protocol backends & MLOps for Lucia — quick note", "hook": "Saw your HN post for Lucia — scaling decentralized protocols and AI coordination requires robust, deterministic systems engineering.", "metric_a_co": "C3iHub", "metric_a": "achieved 99.9% uptime for 50K users by deploying Dockerized microservices and automated CI/CD", "metric_b_co": "C3iHub", "metric_b": "cut database query p99 latency from 450ms to 135ms through index optimization and Redis caching", "closer": "Resume attached — github.com/PrathamModi001. Would love to know if Lucia is hiring backend / MLOps engineers.", "notes": "Attached Pratham_Modi_Base_Resume.pdf; highlights Docker, CI/CD, and Redis caching", "source": "HN (id: 49522897)", "tier": "B", "body": "Saw your HN post for Lucia — scaling decentralized protocols and AI coordination requires robust, deterministic systems engineering.\n\nAt C3iHub, I achieved 99.9% uptime for 50K users by deploying Dockerized microservices and automated CI/CD. At C3iHub, I cut database query p99 latency from 450ms to 135ms through index optimization and Redis caching.\n\nResume attached — github.com/PrathamModi001. Would love to know if Lucia is hiring backend / MLOps engineers.\n\nPratham"}, {"company": "Noricum", "founder": "Michael", "email": "michael@noricum.io", "confidence": "Verified", "role_pitch": "Payments & Distributed Ledger Backend Engineer", "subject": "High-reliability payment ledgers for Noricum — quick note", "hook": "Saw your HN post for Noricum — building provably fair, high-throughput payment ledgers requires absolute data integrity and zero message loss.", "metric_a_co": "C3iHub", "metric_a": "scaled event streaming on Apache Kafka to 75K+ events per day with zero message loss", "metric_b_co": "C3iHub", "metric_b": "implemented distributed locking in Redis and optimized p99 response times from 450ms to 135ms", "closer": "Resume attached — github.com/PrathamModi001. Worth a quick conversation about backend ledger engineering at Noricum?", "notes": "Attached Pratham_Modi_Base_Resume.pdf; highlights Kafka pipelines, distributed locking, and high availability", "source": "HN (id: 49522897)", "tier": "B", "body": "Saw your HN post for Noricum — building provably fair, high-throughput payment ledgers requires absolute data integrity and zero message loss.\n\nAt C3iHub, I scaled event streaming on Apache Kafka to 75K+ events per day with zero message loss. At C3iHub, I implemented distributed locking in Redis and optimized p99 response times from 450ms to 135ms.\n\nResume attached — github.com/PrathamModi001. Worth a quick conversation about backend ledger engineering at Noricum?\n\nPratham"}];
  const results = [];

  for (let i = 0; i < targets.length; i++) {
    const item = targets[i];
    const searchUrl = 'https://mail.google.com/mail/u/0/#search/in%3Adrafts+' + encodeURIComponent(item.email);

    try {
      await page.goto(searchUrl, { waitUntil: 'load', timeout: 30000 });
      await page.waitForTimeout(2500);

      // Find and click the draft row
      const clicked = await page.evaluate((targetComp) => {
        const rows = Array.from(document.querySelectorAll("tr[role='row']"));
        const row = rows.find(r => r.innerText.toLowerCase().includes(targetComp.toLowerCase())) || rows[0];
        if (row) {
          row.click();
          return true;
        }
        return false;
      }, item.company);

      if (!clicked) {
        results.push({ company: item.company, email: item.email, status: 'Error: Draft row not found' });
        continue;
      }

      await page.waitForTimeout(2000);

      // Click Send
      const sendResult = await page.evaluate(() => {
        const sendBtn = document.querySelector("div[role='button'][aria-label*='Send'], div[data-tooltip*='Send']");
        if (sendBtn) {
          sendBtn.click();
          return true;
        }
        return false;
      });

      await page.waitForTimeout(3000);

      const check = await page.evaluate(() => {
        const text = document.body.innerText;
        const dialog = document.querySelector("[role='dialog']");
        return {
          sent: text.includes('Message sent') || text.includes('Sending') || !dialog,
          dialogOpen: !!dialog
        };
      });

      results.push({
        company: item.company,
        email: item.email,
        status: check.sent ? 'Sent' : 'Send_Unconfirmed',
        details: check
      });
    } catch (e) {
      results.push({
        company: item.company,
        email: item.email,
        status: 'Error: ' + e.message
      });
    }
  }

  return results;
}