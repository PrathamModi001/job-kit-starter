import urllib.request, re, json

leads = [
    {
        "company": "QualityAI",
        "title": "Full stack Developer",
        "url": "https://careers.quality-ai.com/job/Bangalore-Full-stack-Developer-560045/59881544/?source=jobfound.org"
    },
    {
        "company": "Commure",
        "title": "Forward Deployed Engineer",
        "url": "https://jobs.ashbyhq.com/Commure/b7f99d0b-e511-41ba-a585-ce636f454e99?source=jobfound.org"
    },
    {
        "company": "Magnitude Software",
        "title": "Associate Software Engineer",
        "url": "https://magnitudesoftware.wd1.myworkdayjobs.com/External/job/India---Hyderabad---Remote/Associate-Software-Engineer_REQ001103-1?source=jobfound.org"
    },
    {
        "company": "Continental",
        "title": "Software Engineer – Data Platform",
        "url": "https://jobs.smartrecruiters.com/ContinentalGroupSectorContiTech/744000151757750-software-engineer-data-platform?trid=2d92f286-613b-4daf-9dfa-6340ffbecf73&source=jobfound.org"
    },
    {
        "company": "Brillio",
        "title": "Engineer",
        "url": "https://jobs.lever.co/brillio-2/00ebf0ec-b6b2-4850-a617-242e2896c762/?lever-source=jobfound.org&source=jobfound.org"
    },
    {
        "company": "Blackbaud",
        "title": "Web Developer",
        "url": "https://careers.blackbaud.com/us/en/job/BLBBUSR0013779EXTERNALENUS/Web-Developer?source=jobfound.org"
    },
    {
        "company": "Oracle",
        "title": "Application Software Engineer 1",
        "url": "https://careers.oracle.com/en/sites/jobsearch/job/344317?source=jobfound.org"
    }
]

for l in leads:
    print("==================================================")
    print("COMPANY:", l["company"])
    print("TITLE:", l["title"])
    print("URL:", l["url"])
    try:
        req = urllib.request.Request(l["url"], headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64)"})
        html = urllib.request.urlopen(req, timeout=10).read().decode("utf-8", errors="replace")
        
        # Clean text
        text = re.sub(r"<script[^>]*>.*?</script>", " ", html, flags=re.DOTALL)
        text = re.sub(r"<style[^>]*>.*?</style>", " ", text, flags=re.DOTALL)
        text = re.sub(r"<[^>]+>", " ", text)
        text = re.sub(r"\s+", " ", text).strip()
        
        print("LENGTH:", len(text))
        print("PREVIEW:", text[:1000])
    except Exception as e:
        print("FETCH ERROR:", e)
