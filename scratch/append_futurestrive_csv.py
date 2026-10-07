import csv

csv_path = r'E:\Extra\job-kit-starter\job-kit-starter\output\job-search\applications.csv'

new_row = [
    "FutureStrive",
    "AI Engineer",
    "Chennai (In office)",
    "Wellfound (native Apply)",
    "₹12L – ₹22L",
    "Applied",
    "2026-10-06",
    "2026-10-06",
    "2026-10-06",
    "output/FutureStrive - AI Engineer/Pratham_Modi_Resume.pdf",
    "https://wellfound.com/jobs/4809721-ai-engineer",
    'Applied via Wellfound native modal; relocation preference set to Chennai; tailored note submitted; confirmed on post-apply page ("✓ Applied")',
    'Full Name: Pratham Modi; Email: prathammodi001@gmail.com; Phone: +91-9033393729; Location: Bengaluru, India (Open to Relocate to Chennai); Location Preference Selected: "I can relocate to... Chennai"; Note: Tailored note with Mnemoniq/LangGraph, Playpower/FastAPI/RAG, and C3iHub receipts; Resume: Pratham_Modi_Resume.pdf uploaded to Wellfound profile'
]

with open(csv_path, 'a', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(new_row)

print("Successfully appended FutureStrive row to applications.csv")
