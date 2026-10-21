import json
import base64

targets = json.load(open('scratch/today_20_outreach_targets.json', encoding='utf-8'))
b64 = base64.b64encode(open('job-kit-starter/output/Pratham_Modi_Base_Resume.pdf', 'rb').read()).decode('utf-8')

def gen_batch(batch_idx, batch_targets):
    js_code = f"""async (page) => {{
  const targets = {json.dumps(batch_targets, ensure_ascii=False)};
  const b64 = '{b64}';
  const results = [];

  for (let i = 0; i < targets.length; i++) {{
    const item = targets[i];

    // 0. Close any open dialogs
    await page.evaluate(() => {{
      const closeBtns = Array.from(document.querySelectorAll('img[aria-label="Save & close"], [aria-label="Save & close"]'));
      closeBtns.forEach(b => b.click());
    }});
    await page.waitForTimeout(1000);

    // 1. Click Compose button
    await page.evaluate(() => {{
      const btn = Array.from(document.querySelectorAll('div[role="button"]')).find(b => b.innerText && b.innerText.includes('Compose'));
      if (btn) btn.click();
    }});
    await page.waitForTimeout(2000);

    // 2. Set To, Subject, Body, and File
    await page.evaluate(({{ item, b64 }}) => {{
      const toInput = document.querySelector('input[aria-label="To recipients"], input.agP');
      if (toInput) {{
        toInput.focus();
        toInput.value = item.Email;
        toInput.dispatchEvent(new Event('input', {{ bubbles: true }}));
        toInput.dispatchEvent(new KeyboardEvent('keydown', {{ key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true }}));
        toInput.dispatchEvent(new Event('change', {{ bubbles: true }}));
        toInput.blur();
      }}

      const subjectInput = document.querySelector('input[name="subjectbox"]');
      if (subjectInput) {{
        subjectInput.focus();
        subjectInput.value = item.Subject;
        subjectInput.dispatchEvent(new Event('input', {{ bubbles: true }}));
        subjectInput.dispatchEvent(new Event('change', {{ bubbles: true }}));
      }}

      const bodyDiv = document.querySelector('div[role="textbox"][aria-label*="Message Body"]');
      if (bodyDiv) {{
        bodyDiv.focus();
        bodyDiv.innerText = item.Body;
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

    // 3. Wait for attachment upload (3.5 seconds)
    await page.waitForTimeout(3500);

    // 4. Save & close
    await page.evaluate(() => {{
      const closeBtns = Array.from(document.querySelectorAll('img[aria-label="Save & close"], [aria-label="Save & close"]'));
      const closeBtn = closeBtns[closeBtns.length - 1];
      if (closeBtn) closeBtn.click();
    }});
    await page.waitForTimeout(1500);

    results.push({{
      batch: {batch_idx},
      index: i + 1,
      company: item.Company,
      email: item.Email,
      subject: item.Subject,
      status: 'Drafted in Gmail'
    }});
  }}

  return {{ batch: {batch_idx}, total: results.length, drafts: results }};
}}
"""
    filename = f'scratch/draft_batch_{batch_idx}.js'
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(js_code)
    print(f'Wrote {filename} ({len(batch_targets)} targets)')

gen_batch(1, targets[0:5])
gen_batch(2, targets[5:10])
gen_batch(3, targets[10:15])
gen_batch(4, targets[15:20])
