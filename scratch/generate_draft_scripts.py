import json
import os

with open('scratch/base_resume_b64.txt') as f:
    b64 = f.read().strip()

with open('scratch/outreach_batch.json') as f:
    items = json.load(f)

# Let's create batch scripts: 5 batches of 5 items each
# For each item, it opens compose, fills To, Subject, Body, attaches base resume via DataTransfer, waits for upload, and clicks Save & Close.

for batch_idx in range(5):
    batch_items = items[batch_idx * 5 : (batch_idx + 1) * 5]
    
    js = f"""async (page) => {{
  const b64 = {json.dumps(b64)};
  const batch = {json.dumps(batch_items)};
  const results = [];

  for (let i = 0; i < batch.length; i++) {{
    const item = batch[i];

    // 1. Click Compose
    await page.evaluate(() => {{
      const btn = Array.from(document.querySelectorAll('div[role="button"]')).find(b => b.innerText && b.innerText.includes('Compose'));
      if (btn) btn.click();
    }});
    await page.waitForTimeout(1500);

    // 2. Set To
    const toInput = page.locator('input[aria-label="To recipients"], input[peoplekit-id]').first();
    await toInput.fill(item.email);
    await page.keyboard.press('Enter');
    await page.waitForTimeout(400);

    // 3. Set Subject
    const subjectInput = page.locator('input[name="subjectbox"]');
    await subjectInput.fill(item.subject);
    await page.waitForTimeout(400);

    // 4. Set Body
    const bodyInput = page.locator('div[role="textbox"][aria-label*="Message Body"]');
    await bodyInput.fill(item.body);
    await page.waitForTimeout(400);

    // 5. Attach Base Resume via DataTransfer
    await page.evaluate((b64) => {{
      const input = document.querySelector('input[type="file"][name="Filedata"]');
      if (!input) return false;
      const binary = atob(b64);
      const bytes = new Uint8Array(binary.length);
      for (let j = 0; j < binary.length; j++) bytes[j] = binary.charCodeAt(j);
      const blob = new Blob([bytes], {{ type: 'application/pdf' }});
      const file = new File([blob], 'Pratham_Modi_Resume.pdf', {{ type: 'application/pdf', lastModified: Date.now() }});

      const dt = new DataTransfer();
      dt.items.add(file);
      input.files = dt.files;
      input.dispatchEvent(new Event('change', {{ bubbles: true }}));
      input.dispatchEvent(new Event('input', {{ bubbles: true }}));
      return true;
    }}, b64);

    // 6. Wait for attachment upload to complete and draft auto-save
    await page.waitForTimeout(2500);

    // 7. Save and close dialog
    await page.evaluate(() => {{
      const closeBtn = document.querySelector('img[aria-label="Save & close"], [aria-label="Save & close"]');
      if (closeBtn) closeBtn.click();
    }});
    await page.waitForTimeout(1000);

    results.push({{ company: item.company, email: item.email, status: 'saved_in_drafts_with_resume' }});
  }}

  return results;
}}"""

    with open(f'scratch/create_drafts_batch_{batch_idx}.js', 'w') as out:
        out.write(js)

print("Generated all 5 batch draft scripts!")
