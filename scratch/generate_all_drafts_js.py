import json

with open("scratch/outreach_targets.json", "r", encoding="utf-8") as f:
    targets = json.load(f)

print(f"Loaded {len(targets)} targets.")

# We will generate a clean runner that fetches the PDF from http://127.0.0.1:8765/resume.pdf
js = """(async () => {
    const targets = """ + json.dumps(targets) + """;
    
    // Fetch base resume blob from local daemon
    const resp = await fetch('http://127.0.0.1:8765/resume.pdf');
    const resumeBlob = await resp.blob();
    console.log('Fetched resume blob size:', resumeBlob.size);

    const results = [];

    for (let i = 0; i < targets.length; i++) {
        const t = targets[i];
        console.log(`Processing [${i+1}/${targets.length}]: ${t.Company} -> ${t.Email}`);
        
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

        // Wait 2.2s for upload to initiate/attach
        await new Promise(r => setTimeout(r, 2200));

        // Save & Close (leaving as draft, never send)
        const closeBtn = activeWin.querySelector('img[aria-label*="Save"]') || activeWin.querySelector('div[aria-label*="Save"]') || activeWin.querySelector('.Ha');
        if (closeBtn) {
            closeBtn.click();
            results.push({ company: t.Company, email: t.Email, status: 'DRAFTED_AND_CLOSED' });
        } else {
            results.push({ company: t.Company, email: t.Email, status: 'ATTACHED_NO_CLOSE' });
        }

        await new Promise(r => setTimeout(r, 800));
    }

    return results;
})();"""

with open("scratch/run_all_20_drafts.js", "w", encoding="utf-8") as out:
    out.write(js)

print("Saved scratch/run_all_20_drafts.js successfully. Length:", len(js))
