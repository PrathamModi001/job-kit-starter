import os

pdf_b64_file = r'E:\Extra\job-kit-starter\job-kit-starter\output\Linde - Software Engineer - AI Hub\resume_b64.txt'
with open(pdf_b64_file, 'r', encoding='utf-8') as f:
    b64 = f.read().strip()

js_code = f"""async (page) => {{
  const b64 = "{b64}";
  return await page.evaluate((b64) => {{
    const binary = atob(b64);
    const bytes = new Uint8Array(binary.length);
    for (let i = 0; i < binary.length; i++) bytes[i] = binary.charCodeAt(i);
    const blob = new Blob([bytes], {{ type: 'application/pdf' }});
    const file = new File([blob], 'Pratham_Modi_Resume.pdf', {{ type: 'application/pdf', lastModified: Date.now() }});
    const input = document.querySelector('#resumeFileUpload');
    const dt = new DataTransfer();
    dt.items.add(file);
    input.files = dt.files;
    input.dispatchEvent(new Event('change', {{ bubbles: true }}));
    input.dispatchEvent(new Event('input', {{ bubbles: true }}));
    return {{ name: file.name, size: file.size, filesLen: input.files.length }};
  }}, b64);
}}
"""

with open(r'E:\Extra\job-kit-starter\scratch\inject_resume_linde.js', 'w', encoding='utf-8') as f:
    f.write(js_code)
print('Generated scratch/inject_resume_linde.js')
