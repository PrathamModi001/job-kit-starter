async (page) => {
  const targets = [{"company": "Senzing", "founder": "Sam", "email": "enghiring@senzing.com", "confidence": "Verified", "role_pitch": "Entity Resolution & Platform Infrastructure Engineer", "subject": "High-performance entity resolution platforms for Senzing — quick note", "hook": "Saw your HN post for Senzing — real-time entity resolution at massive enterprise scale requires high-performance data systems.", "metric_a_co": "C3iHub", "metric_a": "cut database query p99 latency from 450ms to 135ms through index optimization and Redis caching", "metric_b_co": "C3iHub", "metric_b": "managed Kafka event-driven pipelines handling 75K+ telemetry and transaction events daily", "closer": "Resume attached — github.com/PrathamModi001. Would love to connect about platform engineering roles at Senzing.", "notes": "Attached Pratham_Modi_Base_Resume.pdf; highlights performance optimization and distributed systems", "source": "HN (id: 49522897)", "tier": "B", "body": "Saw your HN post for Senzing — real-time entity resolution at massive enterprise scale requires high-performance data systems.\n\nAt C3iHub, I cut database query p99 latency from 450ms to 135ms through index optimization and Redis caching. At C3iHub, I managed Kafka event-driven pipelines handling 75K+ telemetry and transaction events daily.\n\nResume attached — github.com/PrathamModi001. Would love to connect about platform engineering roles at Senzing.\n\nPratham"}, {"company": "Privy.pro", "founder": "Scott Fahl", "email": "careers@privy.pro", "confidence": "Verified", "role_pitch": "Full Stack & Growth Systems Engineer", "subject": "Scalable real estate analytics platforms for Privy.pro — quick note", "hook": "Saw your HN post for Privy.pro — automating data-driven investment analysis for real estate professionals is a fantastic market opportunity.", "metric_a_co": "C3iHub", "metric_a": "built full-stack features in Node.js and React serving 50K active users with 99.9% uptime", "metric_b_co": "Playpower Labs", "metric_b": "engineered Celery task queues and async background pipelines reducing execution wait times by 40%", "closer": "Resume attached — github.com/PrathamModi001. Worth a brief chat about engineering needs at Privy.pro?", "notes": "Attached Pratham_Modi_Base_Resume.pdf; highlights Node.js, React, and async task queues", "source": "HN (id: 49922569)", "tier": "B", "body": "Saw your HN post for Privy.pro — automating data-driven investment analysis for real estate professionals is a fantastic market opportunity.\n\nAt C3iHub, I built full-stack features in Node.js and React serving 50K active users with 99.9% uptime. At Playpower Labs, I engineered Celery task queues and async background pipelines reducing execution wait times by 40%.\n\nResume attached — github.com/PrathamModi001. Worth a brief chat about engineering needs at Privy.pro?\n\nPratham"}, {"company": "SKIES", "founder": "Julius Su", "email": "julius@skieslearn.com", "confidence": "Verified", "role_pitch": "Full Stack & Assistive AI Systems Engineer", "subject": "Mission-critical assistive communication backends for SKIES — quick note", "hook": "Saw your HN post for SKIES at UCLA Kasari Lab — building assistive communication tools for minimally verbal children is deeply inspiring work.", "metric_a_co": "Playpower Labs", "metric_a": "engineered EdTech backend services and RAG search pipelines maintaining sub-200ms latencies", "metric_b_co": "C3iHub", "metric_b": "supported 50K learners with 99.9% uptime by architecting scalable Node.js microservices", "closer": "Resume attached — github.com/PrathamModi001. Would love to contribute to SKIES engineering.", "notes": "Attached Pratham_Modi_Base_Resume.pdf; highlights mission-driven tech, EdTech scale, and microservices", "source": "HN (id: 49922569)", "tier": "B", "body": "Saw your HN post for SKIES at UCLA Kasari Lab — building assistive communication tools for minimally verbal children is deeply inspiring work.\n\nAt Playpower Labs, I engineered EdTech backend services and RAG search pipelines maintaining sub-200ms latencies. At C3iHub, I supported 50K learners with 99.9% uptime by architecting scalable Node.js microservices.\n\nResume attached — github.com/PrathamModi001. Would love to contribute to SKIES engineering.\n\nPratham"}, {"company": "Cascade Space", "founder": "Arlen", "email": "careers@cascade.space", "confidence": "Verified", "role_pitch": "Systems & Cloud Infrastructure Engineer", "subject": "Ground-segment infrastructure & telemetry backends for Cascade Space — quick note", "hook": "Saw your HN post for Cascade Space — building cutting-edge ground systems and space infrastructure requires uncompromising software reliability.", "metric_a_co": "C3iHub", "metric_a": "maintained 99.9% uptime across microservices handling 75K events daily with OpenTelemetry telemetry", "metric_b_co": "C3iHub", "metric_b": "developed cloud-native microservices serving 50K users with automated Docker and CI/CD pipelines", "closer": "Resume attached — github.com/PrathamModi001. Is Cascade Space looking for software / cloud systems engineers?", "notes": "Attached Pratham_Modi_Base_Resume.pdf; highlights high-uptime telemetry, OpenTelemetry, and Docker", "source": "HN (id: 49522897)", "tier": "B", "body": "Saw your HN post for Cascade Space — building cutting-edge ground systems and space infrastructure requires uncompromising software reliability.\n\nAt C3iHub, I maintained 99.9% uptime across microservices handling 75K events daily with OpenTelemetry telemetry. At C3iHub, I developed cloud-native microservices serving 50K users with automated Docker and CI/CD pipelines.\n\nResume attached — github.com/PrathamModi001. Is Cascade Space looking for software / cloud systems engineers?\n\nPratham"}, {"company": "Tecuity", "founder": "Melissa Thomas", "email": "hr@tecuity.com", "confidence": "Verified", "role_pitch": "Cloud Microservices & Enterprise Software Engineer", "subject": "Scalable regulatory filing backends for Tecuity — quick note", "hook": "Saw your HN post for Tecuity — streamlining state regulatory and corporate filing systems requires resilient, auditable enterprise software.", "metric_a_co": "C3iHub", "metric_a": "built secure REST/WebSocket APIs in Node.js supporting 50K users at 99.9% uptime", "metric_b_co": "C3iHub", "metric_b": "reduced MongoDB query latency from 450ms down to 135ms under continuous production load", "closer": "Resume attached — github.com/PrathamModi001. Would love to connect regarding software engineering at Tecuity.", "notes": "Attached Pratham_Modi_Base_Resume.pdf; highlights secure REST APIs, MongoDB, and enterprise uptime", "source": "HN (id: 49522897)", "tier": "B", "body": "Saw your HN post for Tecuity — streamlining state regulatory and corporate filing systems requires resilient, auditable enterprise software.\n\nAt C3iHub, I built secure REST/WebSocket APIs in Node.js supporting 50K users at 99.9% uptime. At C3iHub, I reduced MongoDB query latency from 450ms down to 135ms under continuous production load.\n\nResume attached — github.com/PrathamModi001. Would love to connect regarding software engineering at Tecuity.\n\nPratham"}];
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