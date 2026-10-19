import os

with open(r'E:\Extra\job-kit-starter\job-kit-starter\scratch\resume_b64.txt', 'r') as f:
    b64 = f.read().strip()

script = f"""async (page) => {{
  const b64 = "{b64}";
  const res = await page.evaluate(async (base64) => {{
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
    if (!input) return 'No input found';

    input.files = dataTransfer.files;
    input.dispatchEvent(new Event('input', {{ bubbles: true }}));
    input.dispatchEvent(new Event('change', {{ bubbles: true }}));
    return 'Dispatched change event to input!';
  }}, b64);
  return res;
}}
"""

with open(r'E:\Extra\job-kit-starter\job-kit-starter\scratch\attach_script.js', 'w', encoding='utf-8') as f:
    f.write(script)

print('Saved attach_script.js')
