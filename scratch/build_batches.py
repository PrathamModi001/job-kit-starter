import json

import os
BASE = r"E:\Extra\job-kit-starter"

with open(os.path.join(BASE, 'job-kit-starter', 'drafts_payload.json'), 'r', encoding='utf-8') as f:
    items = json.load(f)

with open(os.path.join(BASE, 'job-kit-starter', 'output', 'base_resume_b64.txt'), 'r', encoding='utf-8') as f:
    b64 = f.read().strip()

print(f"Total items: {len(items)}, b64 len: {len(b64)}")

chunks = [items[i:i+5] for i in range(0, len(items), 5)]
for idx, chunk in enumerate(chunks):
    fname = os.path.join(BASE, 'scratch', f'batch_{idx}.js')
    b64_json = json.dumps(b64)
    chunk_json = json.dumps(chunk, ensure_ascii=False)
    
    code = f"""async (page) => {{
  const b64 = {b64_json};
  const targets = {chunk_json};
  const results = [];

  for (let i = 0; i < targets.length; i++) {{
    const item = targets[i];
    const url = 'https://mail.google.com/mail/u/0/?fs=1&tf=cm&to=' + encodeURIComponent(item.email) +
                '&su=' + encodeURIComponent(item.subject) +
                '&body=' + encodeURIComponent(item.body);

    try {{
      await page.goto(url, {{ waitUntil: 'load', timeout: 30000 }});
      await page.waitForTimeout(2500);

      // Inject PDF resume
      const attachRes = await page.evaluate((pdfB64) => {{
        const input = document.querySelector("input[type='file'][name='Filedata']");
        if (!input) return {{ ok: false, error: 'no Filedata input' }};

        const binary = atob(pdfB64);
        const bytes = new Uint8Array(binary.length);
        for (let j = 0; j < binary.length; j++) bytes[j] = binary.charCodeAt(j);
        const blob = new Blob([bytes], {{ type: 'application/pdf' }});
        const file = new File([blob], 'Pratham_Modi_Resume.pdf', {{ type: 'application/pdf', lastModified: Date.now() }});

        const dt = new DataTransfer();
        dt.items.add(file);
        input.files = dt.files;
        input.dispatchEvent(new Event('change', {{ bubbles: true }}));
        input.dispatchEvent(new Event('input', {{ bubbles: true }}));
        return {{ ok: true }};
      }}, b64);

      // Wait for upload and auto-save
      await page.waitForTimeout(3000);

      const status = await page.evaluate(() => {{
        const text = document.body.innerText;
        return {{
          hasAttachment: text.includes('Pratham_Modi_Resume.pdf'),
          draftSaved: text.includes('Draft saved') || text.includes('Attachment')
        }};
      }});

      results.push({{
        company: item.company,
        email: item.email,
        subject: item.subject,
        status: status.hasAttachment ? 'Drafted' : 'Drafted_No_Attachment',
        details: status
      }});
    }} catch (e) {{
      results.push({{
        company: item.company,
        email: item.email,
        status: 'Error: ' + e.message
      }});
    }}
  }}

  return results;
}}"""
    with open(fname, 'w', encoding='utf-8') as out:
        out.write(code)
    print(f"Wrote {fname} with {len(chunk)} items")
