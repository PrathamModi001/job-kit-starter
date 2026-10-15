import json
from pathlib import Path
import scratch.stage_20_outreach as o

runner_template = """
const targets = __TARGETS__;

async function draftAll() {
  const results = [];
  const res = await fetch("http://127.0.0.1:8765/resume.pdf");
  const blob = await res.blob();
  
  for (let i = 0; i < targets.length; i++) {
    const t = targets[i];
    console.log(`[${i+1}/${targets.length}] Processing ${t.to}...`);
    
    // 1. Click Compose
    const composeBtn = document.querySelector('div[gh="cm"]') || 
                       Array.from(document.querySelectorAll('div[role="button"]')).find(el => el.innerText.trim() === 'Compose');
    if (!composeBtn) {
      results.push({ target: t.to, error: "Compose button not found" });
      continue;
    }
    composeBtn.click();
    await new Promise(r => setTimeout(r, 1800));
    
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
    await new Promise(r => setTimeout(r, 600));
    
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
    await new Promise(r => setTimeout(r, 600));
    
    // 4. Body
    const bodyEl = document.querySelector('div[role="textbox"][aria-label="Message Body"]');
    if (!bodyEl) {
      results.push({ target: t.to, error: "Body textbox not found" });
      continue;
    }
    bodyEl.focus();
    bodyEl.innerText = t.body;
    bodyEl.dispatchEvent(new Event("input", { bubbles: true }));
    await new Promise(r => setTimeout(r, 600));
    
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
    await new Promise(r => setTimeout(r, 2200));
    
    // 6. Save and close
    const closeBtn = document.querySelector('img[aria-label="Save & close"]') || 
                     document.querySelector('button[aria-label="Save & close"]') || 
                     document.querySelector('[data-tooltip="Save & close"]') ||
                     document.querySelector('div.Ha');
    if (!closeBtn) {
      results.push({ target: t.to, error: "Save and close button not found" });
      continue;
    }
    closeBtn.click();
    await new Promise(r => setTimeout(r, 1200));
    
    results.push({ target: t.to, success: true });
  }
  return results;
}
return await draftAll();
"""

js_targets = []
for t in o.targets:
    js_targets.append({
        'to': t['Email'],
        'subject': t['Subject'],
        'body': t['Body']
    })

full_script = runner_template.replace('__TARGETS__', json.dumps(js_targets, indent=2))
Path('scratch/run_all_20_drafts.js').write_text(full_script, encoding='utf-8')
print(f"Successfully generated scratch/run_all_20_drafts.js with {len(js_targets)} targets")
