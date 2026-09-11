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
    
    // Helper to set input value
    const setVal = (sel, val) => {{
      const el = document.querySelector(sel);
      if (el) {{
        el.value = val;
        el.dispatchEvent(new Event('input', {{ bubbles: true }}));
        el.dispatchEvent(new Event('change', {{ bubbles: true }}));
      }}
    }};

    // Helper to check radio or checkbox
    const checkVal = (name, val) => {{
      const els = Array.from(document.querySelectorAll(`input[name="${{name}}"]`));
      const target = els.find(e => e.value === val);
      if (target) {{
        target.checked = true;
        target.dispatchEvent(new Event('change', {{ bubbles: true }}));
        target.dispatchEvent(new Event('click', {{ bubbles: true }}));
      }}
    }};

    setVal('input[name="name"]', 'Pratham Modi');
    setVal('input[name="email"]', 'prathammodi001@gmail.com');
    setVal('input[name="phone"]', '+91-9033393729');
    setVal('input[name="org"]', 'C3iHub, IIT Kanpur');
    setVal('input[name="location"]', 'Bengaluru, India');
    setVal('input[name="urls[LinkedIn]"]', 'https://www.linkedin.com/in/prathammodii001/');
    setVal('input[name="urls[GitHub]"]', 'https://github.com/PrathamModi001');

    // Salary expectations
    setVal('input[name="cards[ea38b1ed-4f15-4e73-97ba-4706178cbde8][field0]"]', '18-20 LPA');

    // Notice period
    checkVal('cards[d3a8215f-b12b-46c7-94fd-8dc26fc6d420][field0]', 'Immediate/less than 15 Days');

    // Known employee
    setVal('input[name="cards[c6354515-d2ee-4639-a52a-58ebc8252821][field0]"]', 'No');

    // Hybrid relocation
    checkVal('cards[a269057d-ce5b-49ca-aadb-5557fd8e686d][field0]', 'No, I’m not based in this location but willing to relocate');

    // Years of Experience: 2-3 Years
    checkVal('cards[c91923fe-e52c-4224-a414-d85a100b12d4][field0]', '2-3 Years');

    // Databases: PostgreSQL, MongoDB
    checkVal('cards[c91923fe-e52c-4224-a414-d85a100b12d4][field1]', 'PostgreSQL');
    checkVal('cards[c91923fe-e52c-4224-a414-d85a100b12d4][field1]', 'MongoDB');

    // Linux experience: Hands-on in production environments
    checkVal('cards[c91923fe-e52c-4224-a414-d85a100b12d4][field2]', 'Hands-on in production environments');

    // Automation / scripting tools: Python, Terraform, Bash/Shell Scripting
    checkVal('cards[c91923fe-e52c-4224-a414-d85a100b12d4][field3]', 'Python');
    checkVal('cards[c91923fe-e52c-4224-a414-d85a100b12d4][field3]', 'Terraform');
    checkVal('cards[c91923fe-e52c-4224-a414-d85a100b12d4][field3]', 'Bash/Shell Scripting');

    // AI tools
    checkVal('cards[c91923fe-e52c-4224-a414-d85a100b12d4][field4]', 'Code generation and autocompletion (e.g. GitHub Copilot, Cursor)');
    checkVal('cards[c91923fe-e52c-4224-a414-d85a100b12d4][field4]', 'Debugging and troubleshooting assistance (e.g. ChatGPT, Claude)');
    checkVal('cards[c91923fe-e52c-4224-a414-d85a100b12d4][field4]', 'Understanding new concepts or documentation');
    checkVal('cards[c91923fe-e52c-4224-a414-d85a100b12d4][field4]', 'Writing scripts or configuration files');

    return 'Brevo form filled completely';
  }});
  return res;
}}"""

with open(r'E:\Extra\job-kit-starter\apply_brevo.js', 'w', encoding='utf-8') as f:
    f.write(js)
print('Generated apply_brevo.js successfully')
