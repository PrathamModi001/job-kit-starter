import base64
import os

pdf_path = r'E:\Extra\job-kit-starter\job-kit-starter\output\Pratham_Modi_Base_Resume.pdf'
with open(pdf_path, 'rb') as f:
    b64 = base64.b64encode(f.read()).decode('utf-8')

js_content = f"""async (page) => {{
  const res = await page.evaluate(() => {{
    const b64Pdf = "{b64}";
    const byteCharacters = atob(b64Pdf);
    const byteNumbers = new Array(byteCharacters.length);
    for (let i = 0; i < byteCharacters.length; i++) {{
        byteNumbers[i] = byteCharacters.charCodeAt(i);
    }}
    const byteArray = new Uint8Array(byteNumbers);
    const resumeBlob = new Blob([byteArray], {{ type: 'application/pdf' }});

    const activeWin = document.querySelector('div[role="dialog"]') || document;
    const fileInput = activeWin.querySelector('input[type="file"][name="Filedata"]');
    if (fileInput) {{
        const file = new File([resumeBlob], 'Pratham_Modi_Resume.pdf', {{ type: 'application/pdf' }});
        const dataTransfer = new DataTransfer();
        dataTransfer.items.add(file);
        fileInput.files = dataTransfer.files;
        fileInput.dispatchEvent(new Event('change', {{ bubbles: true }}));
        fileInput.dispatchEvent(new Event('input', {{ bubbles: true }}));
        return "Attachment added successfully";
    }}
    return "File input not found";
  }});

  await page.waitForTimeout(3000);
  
  // Close and save draft
  await page.evaluate(() => {{
    const closeBtn = document.querySelector('div[role="dialog"] img[aria-label*="Save & close"]') || document.querySelector('div[role="dialog"] [aria-label*="Save & close"]');
    if (closeBtn) closeBtn.click();
  }});
  await page.waitForTimeout(1500);

  return res;
}}"""

out_path = r'E:\Extra\job-kit-starter\scratch\attach_pagnos.js'
with open(out_path, 'w', encoding='utf-8') as f:
    f.write(js_content)

print("Generated scratch/attach_pagnos.js as Playwright async function")
