import os, subprocess, pypdf

def build_resume(role_dir, title, summary, skills_top, project1_title, project1_desc, project2_title, project2_desc):
    os.makedirs(role_dir, exist_ok=True)
    with open('scratch/compile_all_resumes.py') as f:
        text = f.read()

    template = text.split('template = r"""')[1].split('"""')[0]

    content = template
    content = content.replace('__TITLE__', title)
    content = content.replace('__SUMMARY__', summary)
    content = content.replace('__SKILLS_TOP__', skills_top)
    content = content.replace('__PROJECT1_TITLE__', project1_title)
    content = content.replace('__PROJECT1_DESC__', project1_desc)
    content = content.replace('__PROJECT2_TITLE__', project2_title)
    content = content.replace('__PROJECT2_DESC__', project2_desc)

    tex_path = os.path.join(role_dir, 'Pratham_Modi_Resume.tex')
    with open(tex_path, 'w') as f:
        f.write(content)

    res = subprocess.run(['tectonic', '-c', 'minimal', tex_path, '--outdir', role_dir], capture_output=True, text=True)
    pdf_path = os.path.join(role_dir, 'Pratham_Modi_Resume.pdf')
    if os.path.exists(pdf_path):
        reader = pypdf.PdfReader(pdf_path)
        print(f"SUCCESS: {role_dir} compiled to {len(reader.pages)} page(s)")
        assert len(reader.pages) == 1, "Resume is not 1 page!"
        return pdf_path
    else:
        print(f"ERROR: {role_dir} failed to compile!\n{res.stderr}")
        return None

if __name__ == '__main__':
    # 1. Salesforge
    # 2. Commenda
    # 3. Amazon
    build_resume(
        role_dir='job-kit-starter/output/Amazon - Software Development Engineer I',
        title=r'Software Development Engineer I $\vert$ Go, Python, Distributed Systems, High-Throughput APIs, AWS',
        summary=r'Backend software engineer with 2+ years of production experience building high-throughput microservices, distributed architectures, and resilient event pipelines. Architected core backend systems serving 50K+ users at C3iHub (IIT Kanpur) with 99.9\% uptime at 10,000+ concurrent connections. Strong background in event-driven systems (Kafka, BullMQ, Redis Streams), database query optimization (cutting p99 latency by 70\%), and containerized cloud deployment (AWS, Docker, Kubernetes).',
        skills_top=r'\textbf{Backend \& Distributed Systems:} Go (Golang), Python, High-Throughput APIs, Microservices, Distributed Systems, Event-Driven Architecture \\',
        project1_title=r'\textbf{DeployMind: Automated Deployment Platform} $\vert$ \textit{FastAPI, Docker, Kubernetes, Redis, AWS} \hfill Personal Project \\',
        project1_desc=r'Engineered automated deployment pipeline containerizing user applications via dynamic Docker daemon execution, provisioning isolated container sandboxes with automated health checking, TLS termination, and real-time build streaming.',
        project2_title=r'\textbf{Autonomous Invoice Processing Platform} $\vert$ \textit{FastAPI, PostgreSQL, Kafka, Redis Streams} \hfill Hackathon Winner \\',
        project2_desc=r'Developed event-driven platform automating intake across 3 channels (Gmail API, WhatsApp API, Google Drive) with automated validation, deduplication, audit logging, and fault-tolerant microservices with exponential backoff and DLQ.'
    )
