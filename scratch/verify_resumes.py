import os

companies = [
    'Auric AI Labs - Backend Engineer',
    'Renesas Electronics - Software Development Engineer -Backend',
    'AiPrise - Software Engineer I',
    'Avoca - Software Engineer (Product)',
    'Commure - Software Engineer (India)'
]

for c in companies:
    p1 = os.path.join('E:/Extra/job-kit-starter/output', c, 'Pratham_Modi_Resume.pdf')
    p2 = os.path.join('E:/Extra/job-kit-starter/job-kit-starter/output', c, 'Pratham_Modi_Resume.pdf')
    print(f"{c}:")
    print(f"  root output: {os.path.exists(p1)} ({p1})")
    print(f"  inner output: {os.path.exists(p2)} ({p2})")
