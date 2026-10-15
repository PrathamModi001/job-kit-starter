import urllib.request, json, re, sys, time
from pathlib import Path

sys.path.insert(0, str(Path("job-kit-starter").resolve()))
import gates

urls = [
    "https://wellfound.com/role/l/software-engineer/india",
    "https://wellfound.com/role/l/backend-engineer/india",
    "https://wellfound.com/role/l/full-stack-engineer/india",
]

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

all_job_links = set()

for u in urls:
    try:
        req = urllib.request.Request(u, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as resp:
            html = resp.read().decode('utf-8', errors='replace')
            links = re.findall(r'href="(/jobs/\d+-[^"]+)"', html)
            print(f"{u} -> {len(links)} links")
            all_job_links.update(links)
    except Exception as e:
        print(f"Error {u}: {e}")

print(f"Total unique Wellfound job links: {len(all_job_links)}")

wellfound_leads = []

for path in sorted(all_job_links):
    jurl = f"https://wellfound.com{path}"
    try:
        req = urllib.request.Request(jurl, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            jhtml = resp.read().decode('utf-8', errors='replace')
            
            # extract title, company, location, salary, description
            # Title is usually in <title> or h1
            title_m = re.search(r'<h1[^>]*>(.*?)</h1>', jhtml, re.I | re.DOTALL)
            title = re.sub(r'<[^>]+>', ' ', title_m.group(1)).strip() if title_m else ""
            if not title:
                tm = re.search(r'<title>(.*?)</title>', jhtml)
                if tm:
                    title = tm.group(1).split('|')[0].strip()
            
            # Company
            co_m = re.search(r'href="/company/([^"]+)"', jhtml)
            co = co_m.group(1).replace('-', ' ').title() if co_m else ""
            
            # Check gates
            tskip = gates.title_skip(title)
            if tskip:
                continue
                
            if co:
                dup = gates.dedup(co)
                if dup:
                    continue
            
            # Extract description
            cleaned_desc = gates.clean_html(jhtml)
            yoe_st, yoe_ev = gates.yoe_check(cleaned_desc)
            if yoe_st == 'skip':
                continue
                
            loc_st, loc_why = gates.location_check("India", cleaned_desc)
            if loc_st == 'skip':
                continue
                
            sc, parts = gates.fit_score(title, cleaned_desc, "India")
            print(f"WF SURVIVED: {co} | {title} | YOE: {yoe_st} ({yoe_ev}) | Fit: {sc}/15 | {jurl}")
            wellfound_leads.append({
                "company": co,
                "title": title,
                "location": "India",
                "apply_url": jurl,
                "yoe_st": yoe_st,
                "yoe_ev": yoe_ev,
                "fit_score": sc,
                "fit_parts": parts,
                "desc": cleaned_desc[:2000]
            })
    except Exception as e:
        # print(f"Error {jurl}: {e}")
        pass

print(f"\nTotal surviving Wellfound leads: {len(wellfound_leads)}")
with open("E:/Extra/job-kit-starter/scratch/qualifying_wellfound.json", "w", encoding="utf-8") as f:
    json.dump(wellfound_leads, f, indent=2)
