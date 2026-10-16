import pathlib
b64 = pathlib.Path('E:/Extra/job-kit-starter/job-kit-starter/output/Deepgram - Backend Engineer- Inference Services/resume_b64.txt').read_text(encoding='utf-8').strip()
code = f"""() => {{
  const b64 = "{b64}";
  const binary = atob(b64);
  const array = new Uint8Array(binary.length);
  for (let i = 0; i < binary.length; i++) {{
    array[i] = binary.charCodeAt(i);
  }}
  const file = new File([array], "Pratham_Modi_Resume.pdf", {{ type: "application/pdf" }});
  const dt = new DataTransfer();
  dt.items.add(file);
  const input = document.getElementById("_systemfield_resume");
  if (input) {{
    input.files = dt.files;
    input.dispatchEvent(new Event("input", {{ bubbles: true }}));
    input.dispatchEvent(new Event("change", {{ bubbles: true }}));
    return {{ success: true, fileName: input.files[0]?.name }};
  }}
  return {{ success: false, error: "input not found" }};
}}"""
pathlib.Path('E:/Extra/job-kit-starter/scratch_upload_deepgram.js').write_text(code, encoding='utf-8')
print("Successfully generated scratch_upload_deepgram.js")
