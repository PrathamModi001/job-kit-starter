import base64

with open("job-kit-starter/output/ChainSecurity - Blockchain Security Engineer/Pratham_Modi_Resume.pdf", "rb") as f:
    b64 = base64.b64encode(f.read()).decode("utf-8")

js_code = f"""(async () => {{
    const toInput = document.querySelector('input[peoplekit-id]') || document.querySelector('input[aria-label="To recipients"]') || document.querySelector('input.agP');
    if (toInput) {{
        toInput.focus();
        document.execCommand('insertText', false, 'jobs@chainsecurity.com');
        toInput.dispatchEvent(new Event('input', {{ bubbles: true }}));
        toInput.dispatchEvent(new KeyboardEvent('keydown', {{ key: 'Enter', keyCode: 13, bubbles: true }}));
    }}

    const subjInput = document.querySelector('input[name="subjectbox"]');
    if (subjInput) {{
        subjInput.focus();
        document.execCommand('insertText', false, 'Blockchain Security Engineer — Pratham Modi');
        subjInput.dispatchEvent(new Event('input', {{ bubbles: true }}));
    }}

    const bodyDiv = document.querySelector('div[aria-label="Message Body"]');
    if (bodyDiv) {{
        bodyDiv.focus();
        const text = `Hi ChainSecurity Team,\\n\\nI am writing to express my strong interest in the Blockchain Security Engineer role at ChainSecurity.\\n\\nOver the past 2+ years, I have worked at C3iHub (IIT Kanpur Cyber Security Hub) and Playpower Labs engineering event-driven architectures, telemetry, and distributed systems. At C3iHub, I deployed distributed tracing across 15+ services using OpenTelemetry and Prometheus, reducing security incident response times by 85%. I also built event-driven pipelines processing 75K+ daily Kafka events with automated deduplication and strict role-based access control.\\n\\nI have a strong foundation in systems programming (Python, C++, Linux internals, Git), and deep curiosity for smart contract security, white-box auditing, and consensus protocols.\\n\\nMy tailored resume is attached for your review. My projects and code are available at github.com/PrathamModi001.\\n\\nThank you for your time and consideration.\\n\\nBest regards,\\nPratham Modi\\n+91 9033393729\\nhttps://www.linkedin.com/in/prathammodii001/`;
        document.execCommand('insertText', false, text);
        bodyDiv.dispatchEvent(new Event('input', {{ bubbles: true }}));
    }}

    const b64Data = "{b64}";
    const byteCharacters = atob(b64Data);
    const byteNumbers = new Array(byteCharacters.length);
    for (let i = 0; i < byteCharacters.length; i++) {{
        byteNumbers[i] = byteCharacters.charCodeAt(i);
    }}
    const byteArray = new Uint8Array(byteNumbers);
    const blob = new Blob([byteArray], {{ type: 'application/pdf' }});
    const file = new File([blob], 'Pratham_Modi_Resume.pdf', {{ type: 'application/pdf' }});

    const fileInput = document.querySelector('input[type="file"][name="Filedata"]');
    if (!fileInput) return 'NO_FILE_INPUT';

    const dataTransfer = new DataTransfer();
    dataTransfer.items.add(file);
    fileInput.files = dataTransfer.files;
    fileInput.dispatchEvent(new Event('change', {{ bubbles: true }}));
    fileInput.dispatchEvent(new Event('input', {{ bubbles: true }}));

    await new Promise(r => setTimeout(r, 2500));

    // Save and close
    const closeBtn = document.querySelector('img[aria-label*="Save"]') || document.querySelector('div[aria-label*="Save"]') || document.querySelector('.Ha');
    if (closeBtn) {{
        closeBtn.click();
        return 'SUCCESS_SAVED_AND_CLOSED';
    }}
    return 'ATTACHED_NO_CLOSE_BTN';
}})();
"""

with open("scratch/attach_chainsecurity.js", "w", encoding="utf-8") as f:
    f.write(js_code)

print("Generated scratch/attach_chainsecurity.js successfully.")
