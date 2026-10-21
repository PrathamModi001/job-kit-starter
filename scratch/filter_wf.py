import json, csv, re, subprocess, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")

apps_csv = Path(r"job-kit-starter/output/job-search/applications.csv")
applied_cos = set()
with apps_csv.open(encoding="utf-8") as f:
    for row in csv.DictReader(f):
        if row.get("Company"):
            applied_cos.add(row["Company"].strip().lower())

raw_txt = Path(r"C:\Users\prathamm\.gemini\antigravity-cli\brain\e33ec6b2-6327-4c19-906d-b0a52f020e72\.system_generated\steps\257\output.txt").read_text(encoding="utf-8")
start = raw_txt.find("[")
count = 0
end = -1
for i, c in enumerate(raw_txt[start:], start):
    if c == "[": count += 1
    elif c == "]":
        count -= 1
        if count == 0:
            end = i + 1
            break

cards = json.loads(raw_txt[start:end])
print(f"Total cards extracted: {len(cards)}")
seen_urls = set()
for c in cards:
    u = c["url"]
    if u in seen_urls: continue
    seen_urls.add(u)
    txt = c["text"]
    title = c["title"]
    
    # check title gate
    cmd = ["python", "job-kit-starter/gates.py", "title", title]
    res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    if res.returncode != 0:
        continue
    
    # check salary in text >= 18 LPA or >= $40k
    if not re.search(r"(?:₹\s*(?:1[89]|[2-9]\d)|(?:1[89]|[2-9]\d)\s*LPA|\$(?:[4-9]\d|\d{3})k)", txt, re.I):
        continue
        
    print("MATCH:")
    print("  Title:", title)
    print("  URL:", u)
    print("  Text snippet:", repr(txt[:150]))
