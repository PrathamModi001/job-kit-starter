with open('E:/Extra/job-kit-starter/scratch/base_resume_b64.txt') as f:
    b64 = f.read().strip()

js = f'''() => {{
  const b64 = "{b64}";
  const byteCharacters = atob(b64);
  const byteNumbers = new Array(byteCharacters.length);
  for (let i = 0; i < byteCharacters.length; i++) {{
    byteNumbers[i] = byteCharacters.charCodeAt(i);
  }}
  const byteArray = new Uint8Array(byteNumbers);
  const blob = new Blob([byteArray], {{ type: "application/pdf" }});
  const file = new File([blob], "Pratham_Modi_Base_Resume.pdf", {{ type: "application/pdf" }});
  const input = document.querySelector('input[type="file"][name="Filedata"]') || document.querySelector('input[type="file"]');
  if (!input) return "file input not found";
  const dt = new DataTransfer();
  dt.items.add(file);
  input.files = dt.files;
  input.dispatchEvent(new Event("input", {{ bubbles: true }}));
  input.dispatchEvent(new Event("change", {{ bubbles: true }}));
  return "attached successfully, size: " + blob.size;
}}'''

with open('E:/Extra/job-kit-starter/scratch/injector_func.js', 'w') as f:
    f.write(js)
print("written successfully")
