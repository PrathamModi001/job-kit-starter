with open("scratch/bicsom_resume_b64.txt") as f:
    b64 = f.read().strip()

cl_text = """Hi BiCSoM Team,

I am writing to express my strong interest in the Node.JS Developer position at BiCSoM. With hands-on experience architecting high-concurrency microservices, REST APIs, and database-backed distributed systems, I am excited by the opportunity to build scalable digital products at BiCSoM.

At C3iHub, IIT Kanpur, I engineered and maintained core Node.js/TypeScript microservices serving 50,000+ users and 10,000+ concurrent connections with 99.9% uptime. I optimized database query throughput across MongoDB and PostgreSQL, reducing p99 latency from 450ms to 135ms through compound indexing, query profiling, and multi-tier Redis caching. Additionally, I built event-driven architectures processing 75,000+ daily Kafka messages and automated containerized CI/CD deployment pipelines on AWS with Docker and GitHub Actions.

At Playpower Labs, I developed low-latency API services and integrated databases with Node.js/Python backends, utilizing Jest for comprehensive unit and integration testing.

I am based in Bengaluru, available to join immediately, and look forward to contributing to BiCSoM's engineering team.

Best regards,
Pratham Modi"""

# Clean CL text for JS string literal
cl_escaped = cl_text.replace("\\", "\\\\").replace("`", "\\`").replace("$", "\\$")

js_code = f"""async (page) => {{
  return await page.evaluate((b64) => {{
    function setVal(id, val) {{
      const el = document.getElementById(id);
      if (!el) return false;
      el.focus();
      el.value = val;
      el.dispatchEvent(new Event('input', {{ bubbles: true }}));
      el.dispatchEvent(new Event('change', {{ bubbles: true }}));
      el.blur();
      return true;
    }}

    setVal('awsm-applicant-name', 'Pratham Modi');
    setVal('awsm-applicant-email', 'prathammodi001@gmail.com');
    setVal('awsm-applicant-phone', '+919033393729');
    setVal('awsm-cover-letter', `{cl_escaped}`);
    setVal('awsm_number_1', '12');
    setVal('awsm_number_2', '18');

    const radioImm = document.getElementById('awsm_radio_1_1');
    if (radioImm) {{
      radioImm.checked = true;
      radioImm.dispatchEvent(new Event('change', {{ bubbles: true }}));
    }}

    const privacyCb = document.getElementById('awsm_form_privacy_policy');
    if (privacyCb) {{
      privacyCb.checked = true;
      privacyCb.dispatchEvent(new Event('change', {{ bubbles: true }}));
    }}

    // File upload
    const fileInput = document.getElementById('awsm-application-file');
    if (!fileInput) return {{ error: 'No file input' }};

    const binary = atob(b64);
    const bytes = new Uint8Array(binary.length);
    for (let i = 0; i < binary.length; i++) bytes[i] = binary.charCodeAt(i);
    const blob = new Blob([bytes], {{ type: 'application/pdf' }});
    const file = new File([blob], 'Pratham_Modi_Resume.pdf', {{ type: 'application/pdf', lastModified: Date.now() }});

    const dt = new DataTransfer();
    dt.items.add(file);
    fileInput.files = dt.files;
    fileInput.dispatchEvent(new Event('input', {{ bubbles: true }}));
    fileInput.dispatchEvent(new Event('change', {{ bubbles: true }}));

    return {{
      name: document.getElementById('awsm-applicant-name')?.value,
      email: document.getElementById('awsm-applicant-email')?.value,
      phone: document.getElementById('awsm-applicant-phone')?.value,
      curr_ctc: document.getElementById('awsm_number_1')?.value,
      exp_ctc: document.getElementById('awsm_number_2')?.value,
      radio: radioImm?.checked,
      privacy: privacyCb?.checked,
      file: fileInput.files[0]?.name,
      fileSize: fileInput.files[0]?.size
    }};
  }}, "{b64}");
}}
"""

with open("scratch/fill_bicsom.js", "w") as out:
    out.write(js_code)
print("Generated scratch/fill_bicsom.js")
