import base64
from pathlib import Path

b64 = base64.b64encode(open('job-kit-starter/output/Trackerbot - Full-Stack Developer (Node.js)/Pratham_Modi_Resume.pdf', 'rb').read()).decode('ascii')

js = f"""async (page) => {{
  const b64Data = "{b64}";
  const res = await page.evaluate(async (b64) => {{
    const byteCharacters = atob(b64);
    const byteNumbers = new Array(byteCharacters.length);
    for (let i = 0; i < byteCharacters.length; i++) {{
      byteNumbers[i] = byteCharacters.charCodeAt(i);
    }}
    const byteArray = new Uint8Array(byteNumbers);
    const blob = new Blob([byteArray], {{ type: 'application/pdf' }});
    const file = new File([blob], 'Pratham_Modi_Resume.pdf', {{ type: 'application/pdf', lastModified: Date.now() }});

    const fileInputs = Array.from(document.querySelectorAll('input[type="file"]'));
    let input = fileInputs.find(i => i.name === 'Filedata') || fileInputs[0];
    if (!input) {{
      return {{ success: false, error: 'No file input found' }};
    }}

    const dt = new DataTransfer();
    dt.items.add(file);
    input.files = dt.files;
    input.dispatchEvent(new Event('input', {{ bubbles: true }}));
    input.dispatchEvent(new Event('change', {{ bubbles: true }}));

    return {{ success: true, fileName: file.name, fileSize: file.size }};
  }}, b64Data);

  await page.waitForTimeout(3000);

  // Click Save & Close button
  const closeRes = await page.evaluate(() => {{
    const closeBtn = document.querySelector('img[aria-label="Save & close"]') || 
                     document.querySelector('button[aria-label="Save & close"]') || 
                     document.querySelector('[data-tooltip="Save & close"]') ||
                     document.querySelector('div.Ha');
    if (closeBtn) {{
      closeBtn.click();
      return true;
    }}
    return false;
  }});

  return {{ upload: res, closed: closeRes }};
}}
"""

Path('attach_trackerbot_resume.js').write_text(js, encoding='utf-8')
print('Generated attach_trackerbot_resume.js successfully!')
