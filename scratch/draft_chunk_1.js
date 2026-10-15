(async () => {
    const targets = [{"Company": "Pairio", "Founder": "Mark", "Email": "hello@pairio.app", "Confidence": "Verified", "Source": "HN (id: 49922569)", "Tier": "B", "Role Pitch": "Real-Time Collaborative Backend Engineer", "Subject": "Real-time sync and distributed backends for Pairio", "Notes": "Attached Pratham_Modi_Base_Resume.pdf; highlights Playpower Labs 2000+ WebSocket sessions and C3iHub Kafka event engine", "Body": "Hi Mark,\n\nSaw Pairio's collaborative workspace and real-time multiplayer document synchronization on HN.\n\nAt Playpower Labs, I engineered real-time WebSocket streaming architectures supporting 2,000+ concurrent sessions with sub-100ms response times. At C3iHub (IIT Kanpur), I built an event-driven engine processing 75k daily Kafka events at 99.5% reliability with automated dead-letter recovery.\n\nResume's attached \u2014 github.com/PrathamModi001 if you want more detail. Worth a quick chat about Pairio?\n\nPratham"}, {"Company": "Sidekick Labs", "Founder": "McIntyre", "Email": "hn@sidekicklabs.com", "Confidence": "Verified", "Source": "HN (id: 49922569)", "Tier": "B", "Role Pitch": "AI Intelligence & Backend Systems Engineer", "Subject": "Low-latency retrieval and async pipelines for Sidekick Labs", "Notes": "Attached Pratham_Modi_Base_Resume.pdf; highlights Playpower Labs sub-200ms RAG and C3iHub 450ms->135ms DB query optimization", "Body": "Hi McIntyre,\n\nSaw Sidekick Labs' developer intelligence engine and focus on reliable production AI runtimes.\n\nAt Playpower Labs, I built low-latency RAG pipelines delivering sub-200ms retrieval across 10k+ documents while reducing LLM token overhead by 35%. At C3iHub (IIT Kanpur), I tuned MongoDB compound indexing and Redis caching to slash p99 query latency from 450ms to 135ms.\n\nSending my resume along \u2014 happy to jump on a quick call if useful.\n\nPratham"}, {"Company": "PAGNOS", "Founder": "Hiring Team", "Email": "recruiting@pagnos.com", "Confidence": "Verified", "Source": "HN (id: 49922569)", "Tier": "B", "Role Pitch": "Cloud Serverless & Event Ingestion Engineer", "Subject": "Serverless backends & Kafka telemetry for PAGNOS", "Notes": "Attached Pratham_Modi_Base_Resume.pdf; highlights C3iHub 75k daily Kafka events and AWS deployment automation", "Body": "Hi Team,\n\nSaw PAGNOS scaling AWS serverless architectures and distributed cloud pipelines on HN.\n\nAt C3iHub (IIT Kanpur), I engineered event-driven pipelines handling 75k daily Kafka events at 99.5% delivery reliability with automated dead-letter queues. At Playpower Labs, I built microservices supporting 500+ concurrent WebSocket connections with sub-100ms response times.\n\nResume attached. GitHub's github.com/PrathamModi001 if you want to poke around the code. Open to chatting if there's a fit.\n\nPratham"}, {"Company": "Fazeshift", "Founder": "Chris Zehner", "Email": "chris.zehner@fazeshift.com", "Confidence": "Verified", "Source": "HN (id: 49922569)", "Tier": "B", "Role Pitch": "Distributed Systems & Cloud Backend Engineer", "Subject": "10 min re: Fazeshift backend & delivery infra", "Notes": "Attached Pratham_Modi_Base_Resume.pdf; highlights C3iHub OpenTelemetry tracing across 15+ services and 85% MTTR drop", "Body": "Hi Chris,\n\nSaw Fazeshift building high-efficiency developer platforms and distributed delivery systems on HN.\n\nAt C3iHub (IIT Kanpur), I rolled out OpenTelemetry distributed tracing across 15+ microservices, reducing MTTR by 85% while handling 75k daily Kafka events. At Playpower Labs, I optimized vector retrieval latency to sub-200ms across 10k+ documents.\n\nResume's attached \u2014 github.com/PrathamModi001 if you'd like to check out recent builds. Open to connecting this week?\n\nPratham"}, {"Company": "Starbridge", "Founder": "Melissa", "Email": "recruiting@starbridge.ai", "Confidence": "Verified", "Source": "HN (id: 49922569)", "Tier": "B", "Role Pitch": "AI Agent Evaluation & Telemetry Engineer", "Subject": "AI evaluation pipelines & low-latency APIs for Starbridge", "Notes": "Attached Pratham_Modi_Base_Resume.pdf; highlights Playpower Labs 35% token reduction and C3iHub 450ms->135ms DB query optimization", "Body": "Hi Melissa,\n\nSaw Starbridge scaling autonomous AI agent systems and enterprise product infrastructure.\n\nAt Playpower Labs, I engineered evaluation pipelines that achieved a 35% token reduction on LLM calls with sub-200ms RAG retrieval. At C3iHub (IIT Kanpur), I optimized database indexing to cut p99 latency from 450ms to 135ms under heavy production load.\n\nSending my resume along \u2014 would love to chat if you need hands on backend and eval pipelines.\n\nPratham"}];
    const resp = await fetch('http://127.0.0.1:8765/resume.pdf');
    const resumeBlob = await resp.blob();

    const results = [];

    for (let i = 0; i < targets.length; i++) {
        const t = targets[i];
        
        // Find Compose button
        const composeBtn = document.querySelector('div.T-I.T-I-KE.L3') || document.querySelector('div[gh="cm"]') || document.querySelector('div[role="button"][tabindex="0"]');
        if (!composeBtn) {
            results.push({ company: t.Company, status: 'FAILED_NO_COMPOSE_BTN' });
            continue;
        }
        composeBtn.click();
        await new Promise(r => setTimeout(r, 1500));

        // Get latest compose window
        const composeWindows = document.querySelectorAll('div[role="dialog"].M9');
        const activeWin = composeWindows[composeWindows.length - 1] || document;

        // Fill recipient
        const toInput = activeWin.querySelector('input[peoplekit-id]') || activeWin.querySelector('input[aria-label="To recipients"]') || activeWin.querySelector('input.agP');
        if (toInput) {
            toInput.focus();
            document.execCommand('insertText', false, t.Email);
            toInput.dispatchEvent(new Event('input', { bubbles: true }));
            toInput.dispatchEvent(new KeyboardEvent('keydown', { key: 'Enter', keyCode: 13, bubbles: true }));
        }

        // Fill Subject
        const subjInput = activeWin.querySelector('input[name="subjectbox"]');
        if (subjInput) {
            subjInput.focus();
            document.execCommand('insertText', false, t.Subject);
            subjInput.dispatchEvent(new Event('input', { bubbles: true }));
        }

        // Fill Body
        const bodyDiv = activeWin.querySelector('div[aria-label="Message Body"]');
        if (bodyDiv) {
            bodyDiv.focus();
            document.execCommand('insertText', false, t.Body);
            bodyDiv.dispatchEvent(new Event('input', { bubbles: true }));
        }

        // Attach Resume
        const fileInput = activeWin.querySelector('input[type="file"][name="Filedata"]');
        if (fileInput) {
            const file = new File([resumeBlob], 'Pratham_Modi_Resume.pdf', { type: 'application/pdf' });
            const dataTransfer = new DataTransfer();
            dataTransfer.items.add(file);
            fileInput.files = dataTransfer.files;
            fileInput.dispatchEvent(new Event('change', { bubbles: true }));
            fileInput.dispatchEvent(new Event('input', { bubbles: true }));
        }

        await new Promise(r => setTimeout(r, 2000));

        // Save & Close (leaving as draft)
        const closeBtn = activeWin.querySelector('img[aria-label*="Save"]') || activeWin.querySelector('div[aria-label*="Save"]') || activeWin.querySelector('.Ha');
        if (closeBtn) {
            closeBtn.click();
            results.push({ company: t.Company, email: t.Email, status: 'DRAFTED_AND_CLOSED' });
        } else {
            results.push({ company: t.Company, email: t.Email, status: 'ATTACHED_NO_CLOSE' });
        }

        await new Promise(r => setTimeout(r, 600));
    }

    return results;
})();