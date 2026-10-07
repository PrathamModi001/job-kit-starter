import csv
import os

csv_path = r'E:\Extra\job-kit-starter\job-kit-starter\output\job-search\applications.csv'

row = {
    'Company': 'Observe.ai',
    'Role': 'AI Agent Engineer',
    'Location': 'Hyderabad, Telangana, India',
    'Channel': 'job_hunt.py (Greenhouse)',
    'Comp': 'Not listed',
    'Status': 'Blocked',
    'Added': '2026-10-06',
    'Applied': '',
    'Updated': '2026-10-06',
    'Resume': 'output/Observe.ai - AI Agent Engineer/Pratham_Modi_Resume.pdf',
    'Job URL': 'https://job-boards.greenhouse.io/observeai/jobs/5432596008',
    'Next step': "BLOCKED on Greenhouse 8-character email verification code sent to prathammodi001@gmail.com; form completely filled and tailored resume uploaded, browser tab left open on desktop for user to enter code and click Submit application",
    'Personal Info Filled': 'first_name=Pratham, last_name=Modi, email=prathammodi001@gmail.com, country=+91 (India), phone=9033393729, candidate-location=Hyderabad, Telangana, India, question_18769800008=https://www.linkedin.com/in/prathammodii001/, question_18769801008=https://prathammodi001.github.io/prathammodi/, resume=Pratham_Modi_Resume.pdf'
}

with open(csv_path, 'r', encoding='utf-8', newline='') as f:
    reader = csv.reader(f)
    header = next(reader)

with open(csv_path, 'a', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=header)
    writer.writerow(row)

print("Appended Observe.ai row to applications.csv successfully.")
