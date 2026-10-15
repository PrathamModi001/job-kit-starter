import urllib.request, json, re, sys, os
from pathlib import Path

# Add job-kit-starter to sys.path so we can import gates
sys.path.insert(0, str(Path("job-kit-starter").resolve()))
import gates

base_url = "https://jobfound.org/?page={page}&loc=India&sal=10-20+LPA%2C20-30+LPA&exp=0-1+yr%2C1-3+yrs&work=remote%2Chybrid%2Consite&type=Full-time"

leads = []

for page in range(3):
    url = base_url.format(page=page)
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        with urllib.request.urlopen(req) as resp:
            html = resp.read().decode('utf-8')
            m = re.search(r'<script id="job-list-structured-data" type="application/ld\+json">(.*?)</script>', html)
            if not m:
                continue
            data = json.loads(m.group(1))
            items = data.get('itemListElement', [])
            print(f"Page {page}: found {len(items)} items")
            for it in items:
                name = it.get('name', '')
                jurl = it.get('url', '')
                leads.append((name, jurl))
    except Exception as e:
        print(f"Error fetching page {page}: {e}")

print(f"\nTotal leads collected from jobfound.org: {len(leads)}")

qualifying = []

for name, jurl in leads:
    # Fetch job detail
    try:
        req = urllib.request.Request(jurl, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        with urllib.request.urlopen(req) as resp:
            jhtml = resp.read().decode('utf-8')
            m = re.search(r'<script id="job-posting-structured-data" type="application/ld\+json">(.*?)</script>', jhtml)
            if not m:
                continue
            jd_data = json.loads(m.group(1))
            title = jd_data.get('title', '')
            co = jd_data.get('hiringOrganization', {}).get('name', '')
            apply_url = jd_data.get('applyUrl', '')
            desc = jd_data.get('description', '')
            loc_dict = jd_data.get('jobLocation', {}).get('address', {})
            loc_str = loc_dict.get('addressLocality', '') + ", " + loc_dict.get('addressCountry', 'IN')
            exp = jd_data.get('experienceRequirements', '')
            
            # Check gates
            # 1. Title gate
            tskip = gates.title_skip(title)
            if tskip:
                # print(f"SKIP Title [{co}]: {title} -> {tskip}")
                continue
            
            # 2. Dedup
            dup = gates.dedup(co)
            if dup:
                # print(f"SKIP Dedup [{co}]: already {dup}")
                continue
            
            # 3. YOE check on description
            cleaned_desc = gates.clean_html(desc)
            yoe_st, yoe_ev = gates.yoe_check(cleaned_desc)
            if yoe_st == 'skip':
                # print(f"SKIP YOE [{co}]: {title} -> {yoe_ev}")
                continue
                
            # 4. Location check
            loc_st, loc_why = gates.location_check(loc_str, cleaned_desc)
            if loc_st == 'skip':
                # print(f"SKIP Location [{co}]: {loc_str} -> {loc_why}")
                continue

            # 5. Fit score
            sc, parts = gates.fit_score(title, cleaned_desc, loc_str)
            print(f"SURVIVED: {co} | {title} | {loc_str} | YOE: {yoe_st} ({yoe_ev}) | Fit: {sc}/15 | Apply: {apply_url}")
            qualifying.append({
                "company": co,
                "title": title,
                "location": loc_str,
                "apply_url": apply_url,
                "jobfound_url": jurl,
                "yoe_st": yoe_st,
                "yoe_ev": yoe_ev,
                "fit_score": sc,
                "fit_parts": parts,
                "desc": cleaned_desc
            })
    except Exception as e:
        # print(f"Error checking {name}: {e}")
        pass

print(f"\nTotal qualifying leads from jobfound: {len(qualifying)}")
with open("E:/Extra/job-kit-starter/scratch/qualifying_jobfound.json", "w", encoding="utf-8") as f:
    json.dump(qualifying, f, indent=2)
