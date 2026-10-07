import base64
import os

pdf_path = r'E:\Extra\job-kit-starter\job-kit-starter\output\FutureStrive - AI Engineer\Pratham_Modi_Resume.pdf'
with open(pdf_path, 'rb') as f:
    b64 = base64.b64encode(f.read()).decode('utf-8')

code = f"""async (page) => {{
  return await page.evaluate((b64) => {{
    const binary = atob(b64);
    const array = new Uint8Array(binary.length);
    for (let i = 0; i < binary.length; i++) {{
      array[i] = binary.charCodeAt(i);
    }}
    const file = new File([array], 'Pratham_Modi_Resume.pdf', {{ type: 'application/pdf' }});
    const dt = new DataTransfer();
    dt.items.add(file);
    const input = document.querySelector('input[type="file"][accept*="pdf"]');
    if (!input) return {{ success: false, error: 'input not found' }};
    input.files = dt.files;
    input.dispatchEvent(new Event('input', {{ bubbles: true }}));
    input.dispatchEvent(new Event('change', {{ bubbles: true }}));
    return {{ success: true, fileName: input.files[0]?.name, filesCount: input.files.length }};
  }}, '{b64}');
}}"""

out_js = r'E:\Extra\job-kit-starter\scratch\scratch_upload_futurestrive.js'
with open(out_js, 'w', encoding='utf-8') as f:
    f.write(code)

print("Created", out_js)
