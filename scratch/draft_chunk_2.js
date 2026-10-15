(async () => {
    const targets = [{"Company": "Baserow", "Founder": "Bram Wiepjes", "Email": "bram@baserow.io", "Confidence": "Pattern-guessed", "Source": "HN (id: 50075162)", "Tier": "B", "Role Pitch": "Open-Source High-Throughput Database Backend Engineer", "Subject": "Database indexing and real-time backend for Baserow", "Notes": "Attached Pratham_Modi_Base_Resume.pdf; highlights C3iHub 450ms->135ms latency drop and Playpower Labs WebSocket concurrency", "Body": "Hi Bram,\n\nSaw Baserow's open-core database platform scaling real-time collaboration and formula calculation engines.\n\nAt C3iHub (IIT Kanpur), I cut database p99 query latency from 450ms to 135ms via compound indexing and Redis caching across large datasets. At Playpower Labs, I architected real-time WebSocket pipelines sustaining 2,000+ concurrent sessions with sub-100ms response times.\n\nResume attached \u2014 github.com/PrathamModi001 for public code. Open to chatting if there's a fit for Baserow.\n\nPratham"}, {"Company": "Reflex", "Founder": "Nikhil Rao", "Email": "nikhil@reflex.dev", "Confidence": "Pattern-guessed", "Source": "YC Founder Outreach", "Tier": "B", "Role Pitch": "Python Async Runtime & WebSocket Infrastructure Engineer", "Subject": "Python async runtimes and distributed backends for Reflex", "Notes": "Attached Pratham_Modi_Base_Resume.pdf; highlights Playpower Labs 2000+ concurrent WebSocket sessions and C3iHub Kafka processing", "Body": "Hi Nikhil,\n\nSaw Reflex enabling developers to build full-stack web apps in pure Python with stateful WebSocket syncing.\n\nAt Playpower Labs, I built real-time WebSocket streaming services supporting 2,000+ concurrent sessions with sub-100ms response times. At C3iHub (IIT Kanpur), I engineered distributed event-driven microservices handling 75k daily Kafka events with 99.5% delivery reliability.\n\nResume's attached \u2014 would love to contribute to Reflex's compiler and state runtime if you are expanding backend hiring.\n\nPratham"}, {"Company": "Cursor", "Founder": "Michael Truell", "Email": "michael@anysphere.co", "Confidence": "Pattern-guessed", "Source": "Founder Outreach (Dev Tools)", "Tier": "B", "Role Pitch": "Fast Context Retrieval & Model-Serving Backend Engineer", "Subject": "Fast context retrieval and model-serving backends for Cursor", "Notes": "Attached Pratham_Modi_Base_Resume.pdf; highlights Playpower Labs sub-200ms RAG pipelines and 35% token reduction", "Body": "Hi Michael,\n\nSaw Cursor setting the frontier standard for agentic codebase indexing and instant shadow workspace execution.\n\nAt Playpower Labs, I engineered low-latency RAG retrieval pipelines delivering sub-200ms queries across 10k+ code documents while reducing token usage by 35%. At C3iHub (IIT Kanpur), I designed telemetry ingestion pipelines handling 75k daily Kafka events at 99.5% reliability.\n\nSending my resume along \u2014 open to 10 minutes if Cursor has room for backend infrastructure engineers.\n\nPratham"}, {"Company": "K-Scale Labs", "Founder": "Benjamin Bolte", "Email": "ben@kscale.ai", "Confidence": "Pattern-guessed", "Source": "YC Founder Outreach", "Tier": "B", "Role Pitch": "Real-Time Telemetry & Distributed Robotics Backend Engineer", "Subject": "Real-time telemetry ingestion and distributed systems for K-Scale", "Notes": "Attached Pratham_Modi_Base_Resume.pdf; highlights C3iHub 75k daily Kafka events and OpenTelemetry distributed tracing", "Body": "Hi Ben,\n\nSaw K-Scale's open-source humanoid robotics builds and real-time simulation pipelines.\n\nAt C3iHub (IIT Kanpur), I built an event-driven engine handling 75k daily Kafka events at 99.5% reliability and deployed OpenTelemetry distributed tracing across 15+ microservices. At Playpower Labs, I engineered streaming microservices supporting sub-100ms response times.\n\nResume attached \u2014 github.com/PrathamModi001 if you want to inspect past systems work. Open to connecting?\n\nPratham"}, {"Company": "Axiom", "Founder": "Neil Carvalho", "Email": "neil@axiom.co", "Confidence": "Pattern-guessed", "Source": "Founder Outreach (Observability)", "Tier": "B", "Role Pitch": "High-Cardinality Ingestion & Observability Engineer", "Subject": "OpenTelemetry tracing and high-throughput ingestion for Axiom", "Notes": "Attached Pratham_Modi_Base_Resume.pdf; highlights C3iHub OpenTelemetry tracing across 15+ services and 450ms->135ms DB query optimization", "Body": "Hi Neil,\n\nSaw Axiom's cloud-native logging platform and high-performance ingestion engine handling terabytes of telemetry.\n\nAt C3iHub (IIT Kanpur), I deployed OpenTelemetry distributed tracing across 15+ microservices, cutting MTTR by 85% and tuning database queries to slash p99 latency from 450ms to 135ms. At Playpower Labs, I built low-latency streaming services maintaining sub-100ms response times.\n\nResume's attached \u2014 would love to help scale Axiom's query and ingestion pipelines if there's a fit.\n\nPratham"}];
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