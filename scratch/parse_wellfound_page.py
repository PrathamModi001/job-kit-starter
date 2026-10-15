import re, csv, sys
sys.stdout.reconfigure(encoding="utf-8")

# Read snapshot
with open(r"C:\Users\prathamm\.gemini\antigravity-cli\brain\cbce6071-8310-4b95-af58-ab3fde7cbaad\.system_generated\steps\184\output.txt", encoding="utf-8") as f:
    text = f.read()

# Load applied companies
applied_cos = set()
with open("job-kit-starter/output/job-search/applications.csv", encoding="utf-8", errors="ignore") as f:
    for row in csv.DictReader(f):
        c = (row.get("Company") or "").strip().lower()
        if c: applied_cos.add(c)

# Find company and job entries
# Looking for: heading "Company" [level=2] and following link "/jobs/..."
# Or regex for /jobs/<id>-<slug>
matches = re.findall(r'/jobs/(\d+-[a-z0-9-]+)', text)
print(f"Total job links found on page: {len(set(matches))}")

# Let's inspect the blocks around these
for m in set(matches):
    # Find title and company near this url
    idx = text.find(f"/jobs/{m}")
    if idx != -1:
        snippet = text[max(0, idx-600):min(len(text), idx+600)]
        co_match = re.search(r'heading \"([^\"]+)\" \[level=2\]', snippet)
        co = co_match.group(1) if co_match else "Unknown"
        title_match = re.search(r'link \"([^\"]+)\"', snippet)
        title = title_match.group(1).split("•")[0].strip() if title_match else m
        if co.lower() in applied_cos:
            continue
        print(f"Candidate: {co} | {title} | https://wellfound.com/jobs/{m}")
