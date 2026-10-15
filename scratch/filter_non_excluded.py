import json

with open('E:/Extra/job-kit-starter/scratch/qualifying_jobfound.json', encoding='utf-8') as f:
    jobs = json.load(f)

print(f"Total jobs in json: {len(jobs)}")
non_excluded = []
for j in jobs:
    apply_url = j.get('apply_url', '')
    if any(p in apply_url.lower() for p in ['linkedin', 'naukri', 'indeed', 'instahyre']):
        continue
    non_excluded.append(j)

print(f"Non-excluded platform leads: {len(non_excluded)}")
for j in non_excluded:
    print(f"- {j['company']} | {j['title']} | Fit: {j['fit_score']} | YOE: {j['yoe_st']} ({j['yoe_ev']}) | Loc: {j['location']}")
    print(f"  Apply: {j['apply_url']}")
