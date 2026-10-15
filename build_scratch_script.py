import base64
pdf_path = r'E:\Extra\job-kit-starter\job-kit-starter\output\Webbtreejobs - Fullstack Developer\Pratham_Modi_Resume.pdf'
b64 = base64.b64encode(open(pdf_path, 'rb').read()).decode('utf-8')

js_content = f'''async (page) => {{
  const b64Data = "{b64}";

  // 1. Resume upload
  const uploadRes = await page.evaluate((b64) => {{
    const binary = atob(b64);
    const array = new Uint8Array(binary.length);
    for (let i = 0; i < binary.length; i++) {{
      array[i] = binary.charCodeAt(i);
    }}
    const file = new File([array], "Pratham_Modi_Resume.pdf", {{ type: "application/pdf" }});
    const dt = new DataTransfer();
    dt.items.add(file);
    const input = document.querySelector('input[type="file"]');
    if (input) {{
      input.files = dt.files;
      input.dispatchEvent(new Event("input", {{ bubbles: true }}));
      input.dispatchEvent(new Event("change", {{ bubbles: true }}));
      return {{ success: true, fileName: input.files[0]?.name }};
    }}
    return {{ success: false, error: "input not found" }};
  }}, b64Data);

  await page.waitForTimeout(1000);

  // 2. Fill inputs
  const fillRes = await page.evaluate(() => {{
    const setVal = (el, val) => {{
      if (!el) return false;
      el.focus();
      el.value = val;
      el.dispatchEvent(new Event("input", {{ bubbles: true }}));
      el.dispatchEvent(new Event("change", {{ bubbles: true }}));
      return true;
    }};

    const filled = [];

    // First name
    const fn = document.querySelector('input[placeholder*="first name" i]');
    if (fn) {{ setVal(fn, 'Pratham'); filled.push('First Name'); }}

    // Last name
    const ln = document.querySelector('input[placeholder*="last name" i]');
    if (ln) {{ setVal(ln, 'Modi'); filled.push('Last Name'); }}

    // Email
    const em = document.querySelector('input[placeholder*="email" i]');
    if (em) {{ setVal(em, 'prathammodi001@gmail.com'); filled.push('Email'); }}

    // Contact number
    const ph = document.querySelector('input[placeholder*="contact" i], input[placeholder*="phone" i]');
    if (ph) {{ setVal(ph, '+919033393729'); filled.push('Phone'); }}

    // Latest work experience: Job title
    const jt = document.querySelector('input[placeholder*="Job Title" i]');
    if (jt) {{ setVal(jt, 'Software Development Engineer'); filled.push('Job Title'); }}

    // Company name
    const comp = document.querySelector('input[placeholder*="company" i]');
    if (comp) {{ setVal(comp, 'C3iHub, IIT Kanpur'); filled.push('Company'); }}

    // Location
    const loc = document.querySelector('input[placeholder*="Location" i]');
    if (loc) {{ setVal(loc, 'Kanpur, India'); filled.push('Location'); }}

    // Currently working here checkbox
    const cws = Array.from(document.querySelectorAll('input[type="checkbox"]')).filter(c => {{
      const text = c.parentElement?.innerText || '';
      return /working here/i.test(text);
    }});
    if (cws.length > 0 && !cws[0].checked) {{
      cws[0].click();
      filled.push('Currently working');
    }}

    // LinkedIn URL
    const li = document.querySelector('input[placeholder*="LinkedIn" i]');
    if (li) {{ setVal(li, 'https://www.linkedin.com/in/prathammodii001/'); filled.push('LinkedIn'); }}

    // Total years of experience
    const yoe = document.querySelector('input[placeholder*="years of experience" i]');
    if (yoe) {{ setVal(yoe, '2'); filled.push('YOE'); }}

    // Experience in AWS radio: Yes
    const awsYes = Array.from(document.querySelectorAll('input[type="radio"]')).filter(r => {{
      const text = r.parentElement?.innerText || '';
      return /yes/i.test(text);
    }});
    if (awsYes.length > 0) {{
      awsYes[0].click();
      filled.push('AWS Yes');
    }}

    // Education
    const sch = document.querySelector('input[placeholder*="school name" i]');
    if (sch) {{ setVal(sch, 'Pandit Deendayal Energy University'); filled.push('School'); }}

    const deg = document.querySelector('input[placeholder*="degree" i]');
    if (deg) {{ setVal(deg, 'B.Tech in Computer Science and Engineering'); filled.push('Degree'); }}

    return {{ filled }};
  }});

  return {{ uploadRes, fillRes }};
}}'''

open(r'E:\Extra\job-kit-starter\scratch_apply_webbtree.js', 'w', encoding='utf-8').write(js_content)
print("Saved scratch_apply_webbtree.js")
