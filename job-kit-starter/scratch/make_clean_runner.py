import json

with open(r'E:\Extra\job-kit-starter\job-kit-starter\scratch\prepared_drafts.json', 'r') as f:
    drafts = json.load(f)

with open(r'E:\Extra\job-kit-starter\job-kit-starter\scratch\resume_b64.txt', 'r') as f:
    b64 = f.read().strip()

drafts_json = json.dumps(drafts)

script = f"""async (page) => {{
  const drafts = {drafts_json};
  const b64 = "{b64}";

  page.on('dialog', async dialog => {{
    try {{
      await dialog.accept();
    }} catch (e) {{}}
  }});

  for (let i = 0; i < drafts.length; i++) {{
    const d = drafts[i];
    const params = new URLSearchParams({{
      to: d.email,
      su: d.subject,
      body: d.body
    }});
    const url = 'https://mail.google.com/mail/u/0/?fs=1&tf=cm&' + params.toString();

    await page.goto(url);
    await page.waitForTimeout(2000);

    // Disable beforeunload
    await page.evaluate(() => {{
      window.onbeforeunload = null;
    }});

    // Attach resume
    await page.evaluate(async (base64) => {{
      const bstr = atob(base64);
      let n = bstr.length;
      const u8arr = new Uint8Array(n);
      while (n--) {{
        u8arr[n] = bstr.charCodeAt(n);
      }}
      const file = new File([u8arr], 'Pratham_Modi_Base_Resume.pdf', {{ type: 'application/pdf' }});
      const dataTransfer = new DataTransfer();
      dataTransfer.items.add(file);

      const input = document.querySelector('input[type="file"][name="Filedata"]');
      if (input) {{
        input.files = dataTransfer.files;
        input.dispatchEvent(new Event('input', {{ bubbles: true }}));
        input.dispatchEvent(new Event('change', {{ bubbles: true }}));
      }}
    }}, b64);

    await page.waitForTimeout(2500);

    // Disable beforeunload again after attachment
    await page.evaluate(() => {{
      window.onbeforeunload = null;
    }});

    // Close window / draft
    await page.evaluate(() => {{
      const closeBtn = document.querySelector('img[alt="Close"], img.Ha');
      if (closeBtn) closeBtn.click();
    }});

    await page.waitForTimeout(1000);
  }}

  return 'All 20 drafts processed successfully!';
}}
"""

with open(r'E:\Extra\job-kit-starter\job-kit-starter\scratch\clean_draft_runner.js', 'w', encoding='utf-8') as f:
    f.write(script)

print('Generated clean_draft_runner.js successfully!')
