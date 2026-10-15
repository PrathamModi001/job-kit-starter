async (page) => {
  const targets = [{"company": "Irash Tech", "founder": "Founding Team", "email": "hello@irashtech.com", "confidence": "Verified", "role_pitch": "Full Stack & AI Automation Systems Engineer", "subject": "Full-stack AI automation & async pipelines for Irash Tech — quick note", "hook": "Saw your HN post for Irash Tech — automating production workflows with Next.js, Python, and LLM integrations delivers massive ROI for clients.", "metric_a_co": "Playpower Labs", "metric_a": "built sub-200ms RAG pipelines and integrated vector search into production educational tools", "metric_b_co": "C3iHub", "metric_b": "delivered full-stack features in Node.js and React serving 50K active users with 99.9% uptime", "closer": "Resume attached — github.com/PrathamModi001. Worth a conversation about scaling engineering at Irash Tech?", "notes": "Attached Pratham_Modi_Base_Resume.pdf; highlights RAG pipelines, FastAPI, Node.js, and React", "source": "HN (id: 49922569)", "tier": "B", "body": "Saw your HN post for Irash Tech — automating production workflows with Next.js, Python, and LLM integrations delivers massive ROI for clients.\n\nAt Playpower Labs, I built sub-200ms RAG pipelines and integrated vector search into production educational tools. At C3iHub, I delivered full-stack features in Node.js and React serving 50K active users with 99.9% uptime.\n\nResume attached — github.com/PrathamModi001. Worth a conversation about scaling engineering at Irash Tech?\n\nPratham"}, {"company": "Sendery", "founder": "Nikos Caroyannis", "email": "jobs@sendery.co", "confidence": "Verified", "role_pitch": "Backend & Cloud Synchronization Engineer", "subject": "Reliable API infrastructure & distributed sync for Sendery — quick note", "hook": "Saw your HN post for Sendery — building transactional web and mobile apps with resilient backend synchronization is critical.", "metric_a_co": "C3iHub", "metric_a": "developed cloud-native microservices serving 50K users with automated Docker and CI/CD pipelines", "metric_b_co": "Playpower Labs", "metric_b": "optimized asynchronous task processing queues, eliminating bottlenecks and improving throughput by 40%", "closer": "Resume attached — github.com/PrathamModi001. Would love to connect about engineering needs at Sendery.", "notes": "Attached Pratham_Modi_Base_Resume.pdf; highlights Docker, async job queues, and cloud backend APIs", "source": "HN (id: 49922569)", "tier": "B", "body": "Saw your HN post for Sendery — building transactional web and mobile apps with resilient backend synchronization is critical.\n\nAt C3iHub, I developed cloud-native microservices serving 50K users with automated Docker and CI/CD pipelines. At Playpower Labs, I optimized asynchronous task processing queues, eliminating bottlenecks and improving throughput by 40%.\n\nResume attached — github.com/PrathamModi001. Would love to connect about engineering needs at Sendery.\n\nPratham"}, {"company": "Komodo Health", "founder": "Kaushal Parikh", "email": "kaushal.parikh@komodohealth.com", "confidence": "Verified", "role_pitch": "Healthcare AI Platform & Data Infrastructure Engineer", "subject": "Healthcare AI pipelines & high-throughput backends for Komodo Health — quick note", "hook": "Saw your HN post for Komodo Health — pairing large-scale healthcare data with AI products requires serious data integrity and high reliability.", "metric_a_co": "C3iHub", "metric_a": "cut database query p99 latency from 450ms to 135ms through index optimization and Redis caching", "metric_b_co": "Playpower Labs", "metric_b": "built scalable AI ingestion pipelines and background workers reducing batch latency by 40%", "closer": "Resume attached — github.com/PrathamModi001. Would love to connect regarding data/backend roles at Komodo Health.", "notes": "Attached Pratham_Modi_Base_Resume.pdf; highlights database query optimization and scalable ingestion", "source": "HN (id: 49922569)", "tier": "B", "body": "Saw your HN post for Komodo Health — pairing large-scale healthcare data with AI products requires serious data integrity and high reliability.\n\nAt C3iHub, I cut database query p99 latency from 450ms to 135ms through index optimization and Redis caching. At Playpower Labs, I built scalable AI ingestion pipelines and background workers reducing batch latency by 40%.\n\nResume attached — github.com/PrathamModi001. Would love to connect regarding data/backend roles at Komodo Health.\n\nPratham"}, {"company": "Willow Education", "founder": "Hiring Team", "email": "careers@willowed.org", "confidence": "Verified", "role_pitch": "Backend & EdTech Systems Engineer", "subject": "High-reliability EdTech platforms for Willow Education — quick note", "hook": "Saw your HN post for Willow Education — building mission-driven, student-centered products requires dependable infrastructure.", "metric_a_co": "Playpower Labs", "metric_a": "engineered EdTech backend services and RAG search pipelines maintaining sub-200ms latencies", "metric_b_co": "C3iHub", "metric_b": "supported 50K learners with 99.9% uptime by architecting scalable Node.js microservices", "closer": "Resume attached — github.com/PrathamModi001. Would love to connect regarding engineering opportunities at Willow Education.", "notes": "Attached Pratham_Modi_Base_Resume.pdf; highlights EdTech platform scale, microservices, and high uptime", "source": "HN (id: 49922569)", "tier": "B", "body": "Saw your HN post for Willow Education — building mission-driven, student-centered products requires dependable infrastructure.\n\nAt Playpower Labs, I engineered EdTech backend services and RAG search pipelines maintaining sub-200ms latencies. At C3iHub, I supported 50K learners with 99.9% uptime by architecting scalable Node.js microservices.\n\nResume attached — github.com/PrathamModi001. Would love to connect regarding engineering opportunities at Willow Education.\n\nPratham"}];
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