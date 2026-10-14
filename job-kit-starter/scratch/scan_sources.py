import urllib.request, json, re, csv, html, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

def get_applied_or_closed_companies():
    norm = lambda s: re.sub(r"[^a-z0-9]", "", s.lower())
    seen = set()
    csv_path = ROOT / "output" / "job-search" / "applications.csv"
    with open(csv_path, encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            # prompt: "Dedup: skip any company already in job-kit-starter/output/job-search/applications.csv."
            # and gates.py dedup checks Applied/Blocked/Lead/Closed
            seen.add(norm(row["Company"]))
    return seen

def evaluate_jobfound_jobs():
    seen_companies = get_applied_or_closed_companies()
    all_job_links = []
    for page in range(4):
        url = f'https://jobfound.org/?page={page}&loc=India&sal=10-20+LPA%2C20-30+LPA&exp=0-1+yr%2C1-3+yrs&work=remote%2Chybrid%2Consite&type=Full-time'
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                text = resp.read().decode('utf-8', errors='replace')
            hrefs = re.findall(r'href="(/job/[^"]+)"', text)
            for h in hrefs:
                if h not in all_job_links:
                    all_job_links.append(h)
        except Exception as e:
            print(f"Error page {page}:", e)
    
    print(f"Total jobfound links: {len(all_job_links)}")
    sys.path.insert(0, str(ROOT))
    import gates
    norm = lambda s: re.sub(r"[^a-z0-9]", "", s.lower())

    results = []
    for link in all_job_links:
        full_url = f"https://jobfound.org{link}"
        req = urllib.request.Request(full_url, headers={'User-Agent': 'Mozilla/5.0'})
        try:
            with urllib.request.urlopen(req, timeout=12) as resp:
                html_text = resp.read().decode('utf-8', errors='replace')
        except Exception as e:
            continue
        
        # extract title, company, location, applyUrl, and JD text
        # look for json-ld or text
        # Next.js props or regex
        clean_text = gates.clean_html(html_text)
        
        # company and title from slug or text
        slug = link.replace('/job/', '')
        m = re.match(r'^([^-]+(?:-[^-]+)?)-is-hiring-for-(.*)$', slug)
        co_guess = m.group(1).replace('-', ' ') if m else slug.split('-is-hiring')[0]
        
        # find external apply link
        apply_links = re.findall(r'href="(https?://[^"]+)"[^>]*>.*?Apply', html_text, re.I | re.S)
        if not apply_links:
            # any button or link
            apply_links = re.findall(r'<a[^>]+href="(https?://(?!jobfound\.org)[^"]+)"[^>]*>', html_text)
        
        apply_url = apply_links[0] if apply_links else ""
        
        # check dedup
        st = gates.dedup(co_guess)
        if st:
            continue
        
        # check title
        t_skip = gates.title_skip(slug)
        if t_skip:
            continue
            
        # check yoe
        y_stat, y_ev = gates.yoe_check(clean_text)
        if y_stat == "skip":
            continue
            
        results.append({
            "company": co_guess,
            "link": full_url,
            "apply_url": apply_url,
            "slug": slug,
            "yoe": (y_stat, y_ev),
            "len": len(clean_text)
        })
    
    print(f"Surviving leads from jobfound: {len(results)}")
    for r in results:
        print(f"Company: {r['company']} | Apply URL: {r['apply_url']} | Slug: {r['slug']}")

if __name__ == "__main__":
    evaluate_jobfound_jobs()


