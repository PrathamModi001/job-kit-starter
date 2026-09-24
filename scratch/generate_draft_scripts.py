import json

with open('/home/modi/Work/job-kit-starter/scratch/base_resume_b64.txt', 'r') as f:
    b64 = f.read().strip()

with open('/home/modi/Work/job-kit-starter/scratch/outreach_10_targets_20260924.json', 'r') as f:
    targets = json.load(f)

template = """async (page) => {{
  const b64 = {b64_json};
  const item = {item_json};

  // 0. Close any open dialogs first
  await page.evaluate(() => {{
    const closeBtns = Array.from(document.querySelectorAll('img[aria-label="Save & close"], [aria-label="Save & close"]'));
    closeBtns.forEach(b => b.click());
  }});
  await page.waitForTimeout(1500);

  // 1. Click Compose
  await page.evaluate(() => {{
    const btn = Array.from(document.querySelectorAll('div[role="button"]')).find(b => b.innerText && b.innerText.includes('Compose'));
    if (btn) btn.click();
  }});
  await page.waitForTimeout(2500);

  // 2. Set To, Subject, Body, and File
  await page.evaluate(({{ item, b64 }}) => {{
    const toInput = document.querySelector('input[aria-label="To recipients"], input.agP');
    if (toInput) {{
      toInput.focus();
      toInput.value = item.email;
      toInput.dispatchEvent(new Event('input', {{ bubbles: true }}));
      toInput.dispatchEvent(new KeyboardEvent('keydown', {{ key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true }}));
      toInput.dispatchEvent(new Event('change', {{ bubbles: true }}));
      toInput.blur();
    }}

    const subjectInput = document.querySelector('input[name="subjectbox"]');
    if (subjectInput) {{
      subjectInput.focus();
      subjectInput.value = item.subject;
      subjectInput.dispatchEvent(new Event('input', {{ bubbles: true }}));
      subjectInput.dispatchEvent(new Event('change', {{ bubbles: true }}));
    }}

    const bodyDiv = document.querySelector('div[role="textbox"][aria-label*="Message Body"]');
    if (bodyDiv) {{
      bodyDiv.focus();
      bodyDiv.innerText = item.body;
      bodyDiv.dispatchEvent(new Event('input', {{ bubbles: true }}));
    }}

    const inputs = Array.from(document.querySelectorAll('input[type="file"][name="Filedata"]'));
    const fileInput = inputs[inputs.length - 1];
    if (fileInput && b64) {{
      const binary = atob(b64);
      const bytes = new Uint8Array(binary.length);
      for (let j = 0; j < binary.length; j++) bytes[j] = binary.charCodeAt(j);
      const blob = new Blob([bytes], {{ type: 'application/pdf' }});
      const file = new File([blob], 'Pratham_Modi_Base_Resume.pdf', {{ type: 'application/pdf', lastModified: Date.now() }});

      const dt = new DataTransfer();
      dt.items.add(file);
      fileInput.files = dt.files;
      fileInput.dispatchEvent(new Event('change', {{ bubbles: true }}));
      fileInput.dispatchEvent(new Event('input', {{ bubbles: true }}));
    }}
  }}, {{ item, b64 }});

  // 3. Wait for attachment upload and auto-save
  await page.waitForTimeout(5000);

  // 4. Save & close
  await page.evaluate(() => {{
    const closeBtns = Array.from(document.querySelectorAll('img[aria-label="Save & close"], [aria-label="Save & close"]'));
    const closeBtn = closeBtns[closeBtns.length - 1];
    if (closeBtn) closeBtn.click();
  }});
  await page.waitForTimeout(2000);

  return {{ status: 'success', company: item.company, email: item.email }};
}}
"""

for idx in range(1, len(targets)):
    item = targets[idx]
    code = template.format(b64_json=json.dumps(b64), item_json=json.dumps(item))
    filename = f'/home/modi/Work/job-kit-starter/scratch/draft_target_{idx}.js'
    with open(filename, 'w') as f:
        f.write(code)
    print(f"Generated draft script {idx} for {item['company']}")

