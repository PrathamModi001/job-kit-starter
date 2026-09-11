import base64

pdf_path = r'E:\Extra\job-kit-starter\job-kit-starter\output\Wells Fargo - AI Engineer\Pratham_Modi_Resume.pdf'
b64 = open(pdf_path, 'rb').read()
b64_str = base64.b64encode(b64).decode('utf-8')

js = f"""async (page) => {{
  const res = await page.evaluate(() => {{
    const b64 = "{b64_str}";
    const binary = atob(b64);
    const bytes = new Uint8Array(binary.length);
    for (let i = 0; i < binary.length; i++) {{
      bytes[i] = binary.charCodeAt(i);
    }}
    const blob = new Blob([bytes], {{ type: 'application/pdf' }});
    const file = new File([blob], 'Pratham_Modi_Resume.pdf', {{ type: 'application/pdf' }});
    const dt = new DataTransfer();
    dt.items.add(file);
    const input = document.querySelector('#resume-upload-input');
    if (input) {{
      input.files = dt.files;
      input.dispatchEvent(new Event('change', {{ bubbles: true }}));
    }}
    
    const setName = document.querySelector('input[name="name"]');
    if (setName) {{ setName.value = 'Pratham Modi'; setName.dispatchEvent(new Event('input', {{ bubbles: true }})); }}

    const setEmail = document.querySelector('input[name="email"]');
    if (setEmail) {{ setEmail.value = 'prathammodi001@gmail.com'; setEmail.dispatchEvent(new Event('input', {{ bubbles: true }})); }}

    const setPhone = document.querySelector('input[name="phone"]');
    if (setPhone) {{ setPhone.value = '+91-9033393729'; setPhone.dispatchEvent(new Event('input', {{ bubbles: true }})); }}

    const setOrg = document.querySelector('input[name="org"]');
    if (setOrg) {{ setOrg.value = 'C3iHub, IIT Kanpur'; setOrg.dispatchEvent(new Event('input', {{ bubbles: true }})); }}

    const setLoc = document.querySelector('input[name="location"]');
    if (setLoc) {{ setLoc.value = 'Bengaluru, India'; setLoc.dispatchEvent(new Event('input', {{ bubbles: true }})); }}

    const setLi = document.querySelector('input[name="urls[LinkedIn]"]');
    if (setLi) {{ setLi.value = 'https://www.linkedin.com/in/prathammodii001/'; setLi.dispatchEvent(new Event('input', {{ bubbles: true }})); }}

    return 'Form filled successfully';
  }});
  return res;
}}"""

with open(r'E:\Extra\job-kit-starter\apply_hevo.js', 'w', encoding='utf-8') as f:
    f.write(js)
print('Generated apply_hevo.js successfully')
