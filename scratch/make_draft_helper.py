with open(r'E:\Extra\job-kit-starter\scratch\base_resume_b64.txt', 'r', encoding='utf-8') as f:
    b64 = f.read().strip()

js = f'''window.attachBaseResume = function() {{
    const b64Data = "{b64}";
    const byteCharacters = atob(b64Data);
    const byteNumbers = new Array(byteCharacters.length);
    for (let i = 0; i < byteCharacters.length; i++) {{
        byteNumbers[i] = byteCharacters.charCodeAt(i);
    }}
    const byteArray = new Uint8Array(byteNumbers);
    const blob = new Blob([byteArray], {{ type: 'application/pdf' }});
    const file = new File([blob], 'Pratham_Modi_Base_Resume.pdf', {{ type: 'application/pdf' }});
    
    const input = document.querySelector('input[type="file"][name="Filedata"]') || document.querySelector('input[type="file"]');
    if (!input) return 'file input not found';
    
    const dt = new DataTransfer();
    dt.items.add(file);
    input.files = dt.files;
    input.dispatchEvent(new Event('input', {{ bubbles: true }}));
    input.dispatchEvent(new Event('change', {{ bubbles: true }}));
    return 'attached successfully';
}};
'''

with open(r'E:\Extra\job-kit-starter\scratch\draft_helper.js', 'w', encoding='utf-8') as out:
    out.write(js)

print("draft_helper.js written successfully!")
