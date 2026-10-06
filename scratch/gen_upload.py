import base64

pdf_path = r"E:\Extra\job-kit-starter\job-kit-starter\output\Composio - Fullstack Engineer (New Grad)\Pratham_Modi_Resume.pdf"
with open(pdf_path, "rb") as f:
    b64 = base64.b64encode(f.read()).decode("utf-8")

js_code = f"""async (page) => {{
  const b64 = "{b64}";
  const result = await page.evaluate((b64str) => {{
    const byteCharacters = atob(b64str);
    const byteNumbers = new Array(byteCharacters.length);
    for (let i = 0; i < byteCharacters.length; i++) {{
        byteNumbers[i] = byteCharacters.charCodeAt(i);
    }}
    const byteArray = new Uint8Array(byteNumbers);
    const blob = new Blob([byteArray], {{ type: 'application/pdf' }});
    const file = new File([blob], 'Pratham_Modi_Resume.pdf', {{ type: 'application/pdf', lastModified: Date.now() }});

    const dt = new DataTransfer();
    dt.items.add(file);
    
    const input = document.getElementById('_systemfield_resume');
    input.files = dt.files;
    input.dispatchEvent(new Event('input', {{ bubbles: true }}));
    input.dispatchEvent(new Event('change', {{ bubbles: true }}));
    
    return {{
      filesSet: input.files.length,
      fileName: input.files[0]?.name,
      fileSize: input.files[0]?.size
    }};
  }}, b64);
  return result;
}}"""

with open(r"E:\Extra\job-kit-starter\scratch\upload_composio.js", "w", encoding="utf-8") as out:
    out.write(js_code)

print("Updated upload_composio.js successfully!")
