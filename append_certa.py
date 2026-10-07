import csv

row = [
    'Certa',
    'Forward Deployed Engineer',
    'India (Remote)',
    'Wellfound (native Apply)',
    'Top of market salary + bonuses and equity',
    'Applied',
    '2026-10-06',
    '2026-10-06',
    '2026-10-06',
    'output/Certa - Forward Deployed Engineer/Pratham_Modi_Resume.pdf',
    'https://wellfound.com/jobs/4640030-forward-deployed-engineer',
    'Applied via Wellfound native modal with custom screener answers; tailored resume uploaded to Wellfound profile; confirmed on post-apply page ("✓ Applied").',
    'Phone Number: +919033393729; Referred: No; Sponsorship required: No; Location requirement India: Yes; Customer-facing technical delivery experience: 2 years; REST APIs / JSON / webhooks / data mapping: Strong - I work with these regularly; LLMs / GenAI production: Yes, I have built/deployed LLM-powered solutions in production; Resume: Pratham_Modi_Resume.pdf uploaded to Wellfound profile'
]

csv_path = r'E:\Extra\job-kit-starter\job-kit-starter\output\job-search\applications.csv'
with open(csv_path, 'a', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(row)

print('Appended successfully')
