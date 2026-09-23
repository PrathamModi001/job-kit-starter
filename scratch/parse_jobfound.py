import urllib.request
import json
import re

url = 'https://jobfound.org/?page=0&loc=India&exp=0-1+yr%2C1-3+yrs&sal=10-20+LPA%2C20-30+LPA&posted=30'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
html = urllib.request.urlopen(req).read().decode('utf-8')

# Extract all job links or objects
# In Next.js App Router, RSC payload contains JSON objects
# Let's find all slugs from the 16 jobs we saw in the snapshot:
slugs = [
    'wells-fargo-is-hiring-for-software-engineer-hyderabad-india-18-september-2026',
    'wells-fargo-is-hiring-for-software-engineer-hyderabad-india-17-september-2026',
    'cargill-is-hiring-for-platform-engineer-bengaluru-india-india-13-september-2026',
    'avoca-is-hiring-for-deployment-engineer-bengaluru-karnataka-remote-india-12-september-2026',
    'lattice-semiconductor-is-hiring-for-member-of-technical-staff-i-chennai-india-10-september-2026-2',
    'wells-fargo-is-hiring-for-software-engineer-hyderabad-india-9-september-2026',
    'gocomet-is-hiring-for-fullstack-ai-engineer-bangalore-noida-india-9-september-2026',
    'confidential-client-is-hiring-for-fde-ai-bangalore-india-8-september-2026',
    'brevo-is-hiring-for-associate-platform-engineer-data-storage-noida-uttar-pradesh-hybrid-india-7-september-2026',
    'caterpillar-is-hiring-for-software-engineer-d365-f-o-bangalore-chennai-india-7-september-2026',
    'hevo-data-is-hiring-for-sde-i-bangalore-india-3-september-2026',
    'writesonic-is-hiring-for-software-engineer-remote-india-1-september-2026',
    'onmeta-is-hiring-for-software-development-engineer-i-bengaluru-karnataka-india-31-august-2026',
    'velocity-is-hiring-for-data-analyst-bengaluru-india-29-august-2026',
    'meshdefend-is-hiring-for-full-stack-engineer-bengaluru-karnataka-india-26-august-2026',
    'kredivo-group-is-hiring-for-backend-engineer-sde-1-bengaluru-karnataka-india-24-august-2026'
]

print(f"Total slugs: {len(slugs)}")
for s in slugs:
    # fetch each job page to get applyUrl and description
    job_url = f"https://jobfound.org/job/{s}"
    try:
        jreq = urllib.request.Request(job_url, headers={'User-Agent': 'Mozilla/5.0'})
        jhtml = urllib.request.urlopen(jreq).read().decode('utf-8')
        # find applyUrl
        m_apply = re.search(r'"applyUrl":\s*"([^"]+)"', jhtml)
        apply_url = m_apply.group(1) if m_apply else "NOT_FOUND"
        # decode unicode escapes
        apply_url = apply_url.encode().decode('unicode-escape')
        
        m_title = re.search(r'"title":\s*"([^"]+)"', jhtml)
        title = m_title.group(1) if m_title else "UNKNOWN"
        title = title.encode().decode('unicode-escape')
        
        m_company = re.search(r'"companyName":\s*"([^"]+)"', jhtml)
        company = m_company.group(1) if m_company else "UNKNOWN"
        company = company.encode().decode('unicode-escape')
        
        m_skills = re.search(r'"skills":\s*"([^"]+)"', jhtml)
        skills = m_skills.group(1) if m_skills else ""
        skills = skills.encode().decode('unicode-escape')

        m_salary = re.search(r'"salary":\s*"([^"]+)"', jhtml)
        salary = m_salary.group(1) if m_salary else ""

        m_exp = re.search(r'"experience":\s*"([^"]+)"', jhtml)
        exp = m_exp.group(1) if m_exp else ""

        m_loc = re.search(r'"location":\s*"([^"]+)"', jhtml)
        loc = m_loc.group(1) if m_loc else ""

        print(f"---")
        print(f"Company: {company}")
        print(f"Title: {title}")
        print(f"Location: {loc} | Exp: {exp} | Sal: {salary}")
        print(f"Skills: {skills}")
        print(f"ApplyUrl: {apply_url}")
        print(f"JobFoundUrl: {job_url}")
    except Exception as e:
        print(f"Error fetching {s}: {e}")
