import re, base64, os

with open('/home/modi/Work/job-kit-starter/apply_brevo.js', 'r', encoding='utf-8') as f:
    content = f.read()

m = re.search(r'const b64 = "([^"]+)"', content)
if m:
    b64_str = m.group(1)
    pdf_bytes = base64.b64decode(b64_str)
    out_dir = '/home/modi/Work/job-kit-starter/job-kit-starter/output/Wells Fargo - AI Engineer'
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, 'Pratham_Modi_Resume.pdf')
    with open(out_path, 'wb') as out_f:
        out_f.write(pdf_bytes)
    print('Successfully extracted, size:', len(pdf_bytes))
else:
    print('Not found')
