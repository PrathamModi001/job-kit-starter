with open("scratch/scale_ai_resume_b64.txt") as f:
    b64 = f.read().strip()

js_code = f"""async (page) => {{
  // 1. Upload resume
  const uploadResult = await page.evaluate((b64) => {{
    const binary = atob(b64);
    const bytes = new Uint8Array(binary.length);
    for (let i = 0; i < binary.length; i++) bytes[i] = binary.charCodeAt(i);
    const blob = new Blob([bytes], {{ type: 'application/pdf' }});
    const file = new File([blob], 'Pratham_Modi_Resume.pdf', {{ type: 'application/pdf', lastModified: Date.now() }});
    const input = document.querySelector('#resume');
    if (!input) return {{ error: 'No #resume input found' }};
    const dt = new DataTransfer();
    dt.items.add(file);
    input.files = dt.files;
    input.dispatchEvent(new Event('input', {{ bubbles: true }}));
    input.dispatchEvent(new Event('change', {{ bubbles: true }}));
    return {{ name: file.name, size: file.size, filesLen: input.files.length }};
  }}, "{b64}");

  console.log("Upload result:", uploadResult);

  // 2. Set text fields via standard helper
  await page.evaluate(() => {{
    function setVal(id, val) {{
      const el = document.getElementById(id);
      if (!el) return;
      el.focus();
      el.value = val;
      el.dispatchEvent(new Event('input', {{ bubbles: true }}));
      el.dispatchEvent(new Event('change', {{ bubbles: true }}));
      el.blur();
    }}

    setVal('first_name', 'Pratham');
    setVal('last_name', 'Modi');
    setVal('email', 'prathammodi001@gmail.com');
    setVal('phone', '+919033393729');
    setVal('candidate-location', 'Bengaluru, Karnataka, India');
    setVal('country', 'India');
    setVal('question_7459411005', 'https://www.linkedin.com/in/prathammodii001/');
    setVal('question_7459412005', 'https://prathammodi001.github.io/prathammodi/');
    setVal('question_9058160005', 'C3iHub, IIT Kanpur');
    setVal('question_9058161005', 'Software Engineer');
  }});

  return uploadResult;
}}
"""

with open("scratch/run_scale_ai_step1.js", "w") as out:
    out.write(js_code)
print("Generated scratch/run_scale_ai_step1.js")
