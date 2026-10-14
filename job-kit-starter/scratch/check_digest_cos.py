import csv, re, sys
sys.stdout.reconfigure(encoding="utf-8")

applied = {r['Company'].strip().lower() for r in csv.DictReader(open('job-kit-starter/output/job-search/applications.csv', encoding='utf-8'))}

# Parse digest.md
digest = open('job-kit-starter/output/job-search/digest.md', encoding='utf-8').read()
rows = [line for line in digest.splitlines() if line.startswith("|") and "Score" not in line and "---" not in line]

print("Matches in digest.md:")
for row in rows:
    parts = [p.strip() for p in row.split("|")]
    if len(parts) >= 8:
        score = parts[2]
        role_raw = parts[3]
        company = parts[4]
        loc = parts[5]
        m_link = re.search(r"\[(.*?)\]\((.*?)\)", role_raw)
        title = m_link.group(1) if m_link else role_raw
        url = m_link.group(2) if m_link else ""
        is_app = company.lower() in applied
        print(f"Company: {company:20s} | In CSV: {str(is_app):5s} | Role: {title[:40]:40s} | Loc: {loc} | URL: {url}")
