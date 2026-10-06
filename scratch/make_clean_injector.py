with open(r'E:\Extra\job-kit-starter\scratch\base_resume_b64.txt', 'r', encoding='utf-8') as f:
    b64 = f.read().strip()

chunks = [b64[i:i+4000] for i in range(0, len(b64), 4000)]
chunks_js = ",\n    ".join([f'"{c}"' for c in chunks])

js = f'''(() => {{
  const chunks = [
    {chunks_js}
  ];
  const b64Data = chunks.join("");
  const byteCharacters = atob(b64Data);
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
}})()'''

with open(r'E:\Extra\job-kit-starter\scratch\clean_injector.js', 'w', encoding='utf-8') as out:
    out.write(js)

print("clean_injector.js created! Lines:", len(js.splitlines()))
