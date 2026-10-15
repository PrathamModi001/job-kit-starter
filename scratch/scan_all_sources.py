import sys, os, csv, re, json
sys.path.insert(0, 'job-kit-starter')
import job_hunt
from gates import title_skip

# Applied companies
applied_cos = set()
with open('job-kit-starter/output/job-search/applications.csv', encoding='utf-8', errors='ignore') as f:
    for row in csv.DictReader(f):
        c = (row.get('Company') or '').strip().lower()
        if c: applied_cos.add(c)

print(f"Applied companies count: {len(applied_cos)}")

# Let's inspect seen.json entries or query the boards directly
# Let's see what is inside output/job-search/digest_india.md or other outputs
if os.path.exists('job-kit-starter/output/job-search/digest_india.md'):
    print("digest_india.md exists")
