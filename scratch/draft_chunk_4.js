(async () => {
    const targets = [{"Company": "Ultrahuman", "Founder": "Mohit Kumar", "Email": "mohit@ultrahuman.com", "Confidence": "Pattern-guessed", "Source": "Founder Outreach (India)", "Tier": "B", "Role Pitch": "Biometric Telemetry Ingestion & Real-Time Sync Engineer", "Subject": "Biometric telemetry ingestion and low-latency sync for Ultrahuman", "Notes": "Attached Pratham_Modi_Base_Resume.pdf; highlights Playpower Labs 2000+ WebSocket sessions and C3iHub Kafka event processing", "Body": "Hi Mohit,\n\nSaw Ultrahuman Ring AIR and PowerPlugs expanding globally with real-time biomarker tracking and sleep telemetry.\n\nAt Playpower Labs, I engineered streaming architectures sustaining 2,000+ concurrent WebSocket sessions with sub-100ms response times. At C3iHub (IIT Kanpur), I built an event pipeline handling 75k daily Kafka events at 99.5% delivery reliability and cut database p99 latency from 450ms to 135ms.\n\nResume's attached \u2014 would love to help scale Ultrahuman's telemetry ingestion backends. Open to chatting?\n\nPratham"}, {"Company": "Park+", "Founder": "Amit Lakhotia", "Email": "amit@myparkplus.com", "Confidence": "Pattern-guessed", "Source": "Founder Outreach (India)", "Tier": "B", "Role Pitch": "FASTag Telemetry & Geospatial Microservices Backend Engineer", "Subject": "High-volume FASTag event processing and microservices for Park+", "Notes": "Attached Pratham_Modi_Base_Resume.pdf; highlights C3iHub 75k daily Kafka events and 450ms->135ms query latency drop", "Body": "Hi Amit,\n\nSaw Park+ processing millions of daily FASTag transactions and parking automations across India.\n\nAt C3iHub (IIT Kanpur), I architected distributed microservices processing 75k daily Kafka events at 99.5% reliability with automated dead-letter queues, and cut query p99 latency from 450ms to 135ms via compound indexing. At Playpower Labs, I built high-concurrency microservices maintaining sub-100ms response times.\n\nSending my resume along \u2014 happy to jump on a quick call if useful.\n\nPratham"}, {"Company": "Gupshup", "Founder": "Beerud Sheth", "Email": "beerud@gupshup.io", "Confidence": "Pattern-guessed", "Source": "Founder Outreach (India)", "Tier": "B", "Role Pitch": "Conversational AI Messaging & Ingestion Infrastructure Engineer", "Subject": "High-throughput messaging pipelines and AI evals for Gupshup", "Notes": "Attached Pratham_Modi_Base_Resume.pdf; highlights C3iHub 75k daily Kafka events and Playpower Labs 35% token reduction", "Body": "Hi Beerud,\n\nSaw Gupshup's conversational AI cloud powering billions of enterprise messaging workflows across WhatsApp and RCS.\n\nAt C3iHub (IIT Kanpur), I engineered event-driven pipelines handling 75k daily Kafka events at 99.5% delivery reliability with automated DLQ recovery. At Playpower Labs, I built evaluation and RAG pipelines delivering sub-200ms retrieval and a 35% reduction in token overhead.\n\nResume attached \u2014 github.com/PrathamModi001 for public code. Open to a quick chat if there is an engineering fit.\n\nPratham"}, {"Company": "Yellow.ai", "Founder": "Raghu Ravinutala", "Email": "raghu@yellow.ai", "Confidence": "Pattern-guessed", "Source": "Founder Outreach (India)", "Tier": "B", "Role Pitch": "Autonomous Agent Runtime & Real-Time Orchestration Engineer", "Subject": "Agentic orchestration runtimes and low-latency RAG for Yellow.ai", "Notes": "Attached Pratham_Modi_Base_Resume.pdf; highlights Playpower Labs sub-200ms RAG pipelines and C3iHub Kafka processing", "Body": "Hi Raghu,\n\nSaw Yellow.ai's multi-agent dynamic automation platform delivering human-like voice and chat resolutions globally.\n\nAt Playpower Labs, I engineered low-latency RAG pipelines delivering sub-200ms retrieval across 10k+ documents with a 35% token reduction. At C3iHub (IIT Kanpur), I architected an event-driven engine processing 75k daily Kafka events with OpenTelemetry distributed tracing across 15+ services.\n\nResume's attached \u2014 would love to contribute to Yellow.ai's agent runtime infrastructure. Open to connecting?\n\nPratham"}, {"Company": "CoinSwitch", "Founder": "Ashish Singhal", "Email": "ashish@coinswitch.co", "Confidence": "Pattern-guessed", "Source": "Founder Outreach (India)", "Tier": "B", "Role Pitch": "High-Frequency Order Routing & Ledger Backend Engineer", "Subject": "High-throughput transaction backends and Kafka pipelines for CoinSwitch", "Notes": "Attached Pratham_Modi_Base_Resume.pdf; highlights C3iHub 75k daily Kafka events and 450ms->135ms DB query optimization", "Body": "Hi Ashish,\n\nSaw CoinSwitch scaling multi-asset trading, wealth products, and crypto exchange infrastructure for 20M+ users.\n\nAt C3iHub (IIT Kanpur), I built an event-driven system handling 75k daily Kafka events at 99.5% delivery reliability, and tuned database indexing to slash p99 latency from 450ms to 135ms. At Playpower Labs, I built real-time WebSocket pipelines maintaining sub-100ms response times.\n\nResume attached \u2014 github.com/PrathamModi001 if you'd like to check out past systems. Open to 10 minutes?\n\nPratham"}];
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