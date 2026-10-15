(async () => {
    const targets = [{"Company": "Plum", "Founder": "Abhishek Poddar", "Email": "abhishek@plumhq.com", "Confidence": "Pattern-guessed", "Source": "Founder Outreach (India)", "Tier": "B", "Role Pitch": "Real-Time Claims Telemetry & Microservices Backend Engineer", "Subject": "High-throughput microservices and event processing for Plum", "Notes": "Attached Pratham_Modi_Base_Resume.pdf; highlights C3iHub 75k daily Kafka events and 450ms->135ms database query reduction", "Body": "Hi Abhishek,\n\nSaw Plum's automated health insurance infrastructure and real-time claims disbursement platform.\n\nAt C3iHub (IIT Kanpur), I engineered a notification and workflow engine handling 75k daily Kafka events at 99.5% delivery reliability with automated DLQs, and cut database p99 latency from 450ms to 135ms. At Playpower Labs, I built microservices supporting sub-100ms response times.\n\nResume's attached \u2014 github.com/PrathamModi001 for project receipts. Open to a brief chat if Plum is hiring in backend?\n\nPratham"}, {"Company": "Pocket FM", "Founder": "Rohan Nayak", "Email": "rohan@pocketfm.com", "Confidence": "Pattern-guessed", "Source": "Founder Outreach (India)", "Tier": "B", "Role Pitch": "Audio Streaming Telemetry & High-Concurrency Backend Engineer", "Subject": "High-concurrency streaming backends and event pipelines for Pocket FM", "Notes": "Attached Pratham_Modi_Base_Resume.pdf; highlights Playpower Labs 2000+ WebSocket sessions and C3iHub Kafka event processing", "Body": "Hi Rohan,\n\nSaw Pocket FM's global expansion and audio series personalization platform handling millions of daily streaming minutes.\n\nAt Playpower Labs, I engineered real-time WebSocket streaming architectures sustaining 2,000+ concurrent sessions with sub-100ms response times. At C3iHub (IIT Kanpur), I built event-driven microservices processing 75k daily Kafka events at 99.5% delivery reliability.\n\nResume attached \u2014 github.com/PrathamModi001 if you want to explore the code. Worth a short call re: backend hiring?\n\nPratham"}, {"Company": "Rebel Foods", "Founder": "Jaydeep Barman", "Email": "jaydeep@rebelfoods.com", "Confidence": "Pattern-guessed", "Source": "Founder Outreach (India)", "Tier": "B", "Role Pitch": "Cloud Kitchen KitchenOS & Order Dispatch Backend Engineer", "Subject": "Order dispatch telemetry and microservice scaling for Rebel Foods", "Notes": "Attached Pratham_Modi_Base_Resume.pdf; highlights C3iHub 75k daily Kafka events and 450ms->135ms query latency reduction", "Body": "Hi Jaydeep,\n\nSaw Rebel Foods' KitchenOS operating across hundreds of cloud kitchens with automated order routing and multi-brand dispatch.\n\nAt C3iHub (IIT Kanpur), I built event-driven services processing 75k daily Kafka events at 99.5% reliability with automated recovery, and slashed database p99 latency from 450ms to 135ms. At Playpower Labs, I developed low-latency APIs supporting sub-100ms response times.\n\nSending my resume along \u2014 happy to jump on a quick call if useful.\n\nPratham"}, {"Company": "Curefoods", "Founder": "Ankit Nagori", "Email": "ankit@curefoods.in", "Confidence": "Pattern-guessed", "Source": "Founder Outreach (India)", "Tier": "B", "Role Pitch": "Multi-Brand Inventory & Order Management Backend Engineer", "Subject": "Inventory sync and distributed microservices for Curefoods", "Notes": "Attached Pratham_Modi_Base_Resume.pdf; highlights C3iHub 450ms->135ms query latency reduction and OpenTelemetry MTTR reduction", "Body": "Hi Ankit,\n\nSaw Curefoods' rapid scaling of multi-brand kitchen networks and unified supply chain operations across India.\n\nAt C3iHub (IIT Kanpur), I optimized high-load MongoDB indexing to cut p99 query latency from 450ms to 135ms and deployed OpenTelemetry distributed tracing across 15+ microservices, slashing MTTR by 85%. At Playpower Labs, I built microservices maintaining sub-100ms response times.\n\nResume's attached \u2014 github.com/PrathamModi001 if you'd like to check out past projects. Open to connecting?\n\nPratham"}, {"Company": "Captain Fresh", "Founder": "Utham Gowda", "Email": "utham@captainfresh.com", "Confidence": "Pattern-guessed", "Source": "Founder Outreach (India)", "Tier": "B", "Role Pitch": "Cold-Chain Supply Telemetry & Logistics Engine Engineer", "Subject": "Real-time supply telemetry and event processing for Captain Fresh", "Notes": "Attached Pratham_Modi_Base_Resume.pdf; highlights C3iHub 75k daily Kafka events and Redis pub/sub caching", "Body": "Hi Utham,\n\nSaw Captain Fresh scaling global seafood B2B supply chains with algorithmic matching and cold-chain traceability.\n\nAt C3iHub (IIT Kanpur), I designed an event-driven automation platform handling 75k daily Kafka events at 99.5% reliability with Redis pub/sub caching. At Playpower Labs, I engineered real-time WebSocket pipelines supporting 2,000+ concurrent sessions with sub-100ms response times.\n\nResume attached. Open to a brief conversation if Captain Fresh is expanding the core engineering team.\n\nPratham"}];
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