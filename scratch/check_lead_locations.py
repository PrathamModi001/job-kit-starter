import urllib.request, re, json, sys
sys.path.insert(0, "job-kit-starter")
from gates import clean_html, yoe_check, title_skip

leads = [
    ("WEX", "Software Development Engineer 1", "https://careers.wexinc.com/us/en/job/WEXWEXUSR22748EXTERNALENUS/Software-Development-Engineer-1?source=jobfound.org"),
    ("ABB", "Software Engineer", "https://careers.abb/global/en/job/ABB1GLOBALJR00049493EXTERNALENGLOBAL/Software-Engineer?source=jobfound.org"),
    ("Alaan", "AI Engineer", "https://ats.rippling.com/en-GB/alaan-careers/jobs/187d971b-6e4d-4cf7-bc10-e2be2dc2f917?source=jobfound.org"),
    ("HP", "Software Applications", "https://hp.wd5.myworkdayjobs.com/ExternalCareerSite/job/Bengaluru-Karntaka-India/Software-Applications_3166748-1?source=jobfound.org"),
    ("Aumnics", "Trainee programmer", "https://www.engrip.com/jobs/apply/25/Trainee-programmer-at-Aumnics?source=jobfound.org")
]

for co, title, url in leads:
    print(f"\n=== {co}: {title} ===")
    t_skip = title_skip(title)
    if t_skip:
        print(f"Title skip: {t_skip}")
        continue
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        raw = urllib.request.urlopen(req, timeout=12).read().decode('utf-8', errors='ignore')
        cleaned = clean_html(raw)
        yoe_res, yoe_ev = yoe_check(cleaned)
        print(f"Length raw: {len(raw)}, clean: {len(cleaned)}")
        print(f"YOE: {yoe_res} ({yoe_ev})")
        # Check country / city matches
        loc_indicators = re.findall(r'(?i)\b(india|bangalore|bengaluru|hyderabad|pune|mumbai|chennai|gurgaon|noida|united states|remote|spain|poland)\b', cleaned[:2000])
        print(f"Location keywords in first 2000 chars: {set(loc_indicators)}")
    except Exception as e:
        print(f"Error fetching {url}: {e}")
