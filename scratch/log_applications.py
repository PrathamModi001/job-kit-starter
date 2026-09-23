import csv

new_rows = [
    {
        "Company": "Wells Fargo",
        "Role": "Software Engineer (Req R-570569)",
        "Location": "Hyderabad, India",
        "Channel": "Jobfound (Workday ATS)",
        "Comp": "Not listed (~18-28 LPA)",
        "Status": "Blocked",
        "Added": "2026-09-19",
        "Applied": "",
        "Updated": "2026-09-19",
        "Resume": "output/Wells Fargo - Software Engineer/Pratham_Modi_Resume.pdf",
        "Job URL": "https://wd1.myworkdaysite.com/recruiting/wf/WellsFargoJobs/job/Hyderabad-India/Software-Engineer_R-570569",
        "Next step": "BLOCKED on Workday automated browser detection / session reset; browser tab left open at apply page for user manual sign-in and completion."
    },
    {
        "Company": "Wells Fargo",
        "Role": "Software Engineer",
        "Location": "Hyderabad, India",
        "Channel": "Jobfound",
        "Comp": "Not listed (~18-28 LPA)",
        "Status": "Skipped",
        "Added": "2026-09-19",
        "Applied": "",
        "Updated": "2026-09-19",
        "Resume": "",
        "Job URL": "https://jobfound.org/job/wells-fargo-is-hiring-for-software-engineer-hyderabad-india-17-september-2026",
        "Next step": "SKIPPED: Duplicate listing of Req R-570569 posted on 17-Sep."
    },
    {
        "Company": "Cargill",
        "Role": "Platform Engineer (Req 328292)",
        "Location": "Bengaluru, Karnataka, India",
        "Channel": "Jobfound (SuccessFactors ATS)",
        "Comp": "20,00,000 INR",
        "Status": "Applied",
        "Added": "2026-09-19",
        "Applied": "2026-09-19",
        "Updated": "2026-09-19",
        "Resume": "output/Cargill - Platform Engineer/Pratham_Modi_Resume.pdf",
        "Job URL": "https://career2.successfactors.eu/portalcareer?career_job_req_id=328292&company=cargill",
        "Next step": "Applied via SAP SuccessFactors ATS (Req 328292); confirmed on completion page (\"Successfully Applied to Platform Engineer (328292)\")."
    },
    {
        "Company": "Avoca",
        "Role": "Deployment Engineer",
        "Location": "Bengaluru, India (Remote)",
        "Channel": "Jobfound (Ashby ATS)",
        "Comp": "Not listed (~20-30 LPA)",
        "Status": "Applied",
        "Added": "2026-09-19",
        "Applied": "2026-09-19",
        "Updated": "2026-09-19",
        "Resume": "output/Avoca - Deployment Engineer/Pratham_Modi_Resume.pdf",
        "Job URL": "https://jobs.ashbyhq.com/avoca/6758ee84-51b4-4d0d-a3a6-d40ec164de49/application",
        "Next step": "Applied via Ashby ATS with tailored 1-page resume; confirmed on completion page (\"Thank you for applying to Avoca!\")."
    },
    {
        "Company": "Lattice Semiconductor",
        "Role": "Member of Technical Staff I",
        "Location": "Chennai, India",
        "Channel": "Jobfound",
        "Comp": "Not listed",
        "Status": "Skipped",
        "Added": "2026-09-19",
        "Applied": "",
        "Updated": "2026-09-19",
        "Resume": "",
        "Job URL": "https://latticesemi.wd5.myworkdayjobs.com/latticesemiconductorscareers/job/Chennai-India/Member-of-Technical-Staff-I_R-103176",
        "Next step": "SKIPPED on mechanical exclusion check: matched \"Member of Technical Staff / MTS\" title bar and primary stack \"C++\"."
    },
    {
        "Company": "Wells Fargo",
        "Role": "Software Engineer - Java",
        "Location": "Hyderabad, India",
        "Channel": "Jobfound",
        "Comp": "Not listed",
        "Status": "Skipped",
        "Added": "2026-09-19",
        "Applied": "",
        "Updated": "2026-09-19",
        "Resume": "",
        "Job URL": "https://www.wellsfargojobs.com/en/jobs/r-573491/software-engineer-java/",
        "Next step": "SKIPPED on mechanical exclusion check: matched \"Java\" hard stack exclusion in title and primary requirements."
    },
    {
        "Company": "GoComet",
        "Role": "Fullstack AI Engineer",
        "Location": "Bangalore, Noida, India",
        "Channel": "Jobfound (Instahyre)",
        "Comp": "Not listed",
        "Status": "Skipped",
        "Added": "2026-09-19",
        "Applied": "",
        "Updated": "2026-09-19",
        "Resume": "",
        "Job URL": "https://www.instahyre.com/job-422266-fullstack-ai-engineer-at-gocomet-3-bangalore-noida/",
        "Next step": "SKIPPED on platform exclusion check: \"instahyre\" is excluded from current scan; candidate also already applied on 2026-09-11."
    },
    {
        "Company": "Confidential Client",
        "Role": "FDE - AI",
        "Location": "Bangalore, India",
        "Channel": "Jobfound (Michael Page)",
        "Comp": "Not listed",
        "Status": "Skipped",
        "Added": "2026-09-19",
        "Applied": "",
        "Updated": "2026-09-19",
        "Resume": "",
        "Job URL": "https://www.michaelpage.co.in/job-detail/fde-ai/ref/jn-092026-7098249",
        "Next step": "SKIPPED on agency check: 3rd-party staffing/recruitment agency listing (Michael Page)."
    },
    {
        "Company": "Brevo",
        "Role": "Associate Platform Engineer - Data Storage",
        "Location": "Noida, Uttar Pradesh (Hybrid), India",
        "Channel": "Jobfound (LinkedIn)",
        "Comp": "Not listed",
        "Status": "Skipped",
        "Added": "2026-09-19",
        "Applied": "",
        "Updated": "2026-09-19",
        "Resume": "",
        "Job URL": "https://www.linkedin.com/jobs/view/4462691533/",
        "Next step": "SKIPPED on platform exclusion check: \"linkedin\" is an excluded platform."
    },
    {
        "Company": "Caterpillar",
        "Role": "Software Engineer - D365 F&O",
        "Location": "Bangalore, Chennai, India",
        "Channel": "Jobfound",
        "Comp": "Not listed",
        "Status": "Skipped",
        "Added": "2026-09-19",
        "Applied": "",
        "Updated": "2026-09-19",
        "Resume": "",
        "Job URL": "https://careers.caterpillar.com/en/jobs/r0000386730/software-engineer-d365-fo/",
        "Next step": "SKIPPED: Job requisition returned 404/closed on Caterpillar careers site; also requires specialized ERP (X++ / Dynamics 365)."
    },
    {
        "Company": "Hevo Data",
        "Role": "SDE I",
        "Location": "Bangalore, India",
        "Channel": "Jobfound (Lever)",
        "Comp": "Not listed (~18-24 LPA)",
        "Status": "Skipped",
        "Added": "2026-09-19",
        "Applied": "",
        "Updated": "2026-09-19",
        "Resume": "",
        "Job URL": "https://jobs.lever.co/hevodata/6cbbe304-e065-4711-bf3e-756795d2bc2a",
        "Next step": "SKIPPED on mechanical exclusion check: primary stack requires core Java data pipeline connectors."
    },
    {
        "Company": "Writesonic",
        "Role": "Software Engineer",
        "Location": "Remote, India",
        "Channel": "Jobfound (LinkedIn)",
        "Comp": "Not listed (~18-25 LPA)",
        "Status": "Skipped",
        "Added": "2026-09-19",
        "Applied": "",
        "Updated": "2026-09-19",
        "Resume": "",
        "Job URL": "https://www.linkedin.com/jobs/view/4461709552/",
        "Next step": "SKIPPED on platform exclusion check: \"linkedin\" is an excluded platform."
    },
    {
        "Company": "OnMeta",
        "Role": "Software Development Engineer I",
        "Location": "Bengaluru, Karnataka, India",
        "Channel": "Jobfound (LinkedIn)",
        "Comp": "Not listed",
        "Status": "Skipped",
        "Added": "2026-09-19",
        "Applied": "",
        "Updated": "2026-09-19",
        "Resume": "",
        "Job URL": "https://www.linkedin.com/jobs/view/4459481003/",
        "Next step": "SKIPPED on platform exclusion check: \"linkedin\" is an excluded platform."
    },
    {
        "Company": "Velocity",
        "Role": "Data Analyst",
        "Location": "Bengaluru, India",
        "Channel": "Jobfound (Wellfound)",
        "Comp": "Not listed",
        "Status": "Skipped",
        "Added": "2026-09-19",
        "Applied": "",
        "Updated": "2026-09-19",
        "Resume": "",
        "Job URL": "https://wellfound.com/jobs/4215166-data-analyst",
        "Next step": "SKIPPED on platform & lane exclusion check: \"wellfound\" is an excluded platform, and role is non-engineering Data Analyst."
    },
    {
        "Company": "MeshDefend",
        "Role": "Full Stack Engineer",
        "Location": "Bengaluru, Karnataka, India",
        "Channel": "Jobfound (LinkedIn)",
        "Comp": "Not listed",
        "Status": "Skipped",
        "Added": "2026-09-19",
        "Applied": "",
        "Updated": "2026-09-19",
        "Resume": "",
        "Job URL": "https://www.linkedin.com/jobs/view/4457945107/",
        "Next step": "SKIPPED on platform exclusion check: \"linkedin\" is an excluded platform."
    },
    {
        "Company": "Kredivo Group",
        "Role": "Backend Engineer (SDE 1)",
        "Location": "Bengaluru, Karnataka, India",
        "Channel": "Jobfound (LinkedIn)",
        "Comp": "Not listed",
        "Status": "Skipped",
        "Added": "2026-09-19",
        "Applied": "",
        "Updated": "2026-09-19",
        "Resume": "",
        "Job URL": "https://www.linkedin.com/jobs/view/4456861392/",
        "Next step": "SKIPPED on platform exclusion check: \"linkedin\" is an excluded platform."
    }
]

csv_path = "job-kit-starter/output/job-search/applications.csv"
fieldnames = ["Company", "Role", "Location", "Channel", "Comp", "Status", "Added", "Applied", "Updated", "Resume", "Job URL", "Next step"]

existing_urls = set()
with open(csv_path, mode="r", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        existing_urls.add(row["Job URL"].strip())

appended = 0
with open(csv_path, mode="a", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    for r in new_rows:
        url = r["Job URL"].strip()
        if url not in existing_urls:
            writer.writerow(r)
            existing_urls.add(url)
            appended += 1
            print(f"Appended: {r['Company']} - {r['Role']} [{r['Status']}]")
        else:
            print(f"Already exists: {r['Company']} - {r['Role']}")

print(f"\nTotal new rows appended: {appended}")
