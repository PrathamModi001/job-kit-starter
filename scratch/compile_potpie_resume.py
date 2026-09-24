import os, subprocess, pypdf

role = {
    'dir': 'job-kit-starter/output/Potpie AI - Full stack engineer',
    'title': r'Full Stack Engineer $\vert$ React, Next.js, Node.js, Python, PostgreSQL, Redis, AI Systems',
    'summary': r'Full stack software engineer with 2+ years of production experience building high-performance web applications, resilient backend microservices, and AI-driven workflows. Architected core LMS backend serving 50K+ users at C3iHub (IIT Kanpur) with 99.9\% uptime at 10,000+ concurrent connections. Proficient across modern React/Next.js frontends, Node.js and Python microservices, distributed caching with Redis, PostgreSQL query optimization, and structured context agentic systems.',
    'skills_top': r'\textbf{Full Stack \& Frontend:} React, Next.js, TypeScript, JavaScript, Tailwind CSS, HTML5/CSS3, WebSockets, RESTful APIs \\\\',
    'project1_title': r'\textbf{Mnemoniq: Structured Context \& Memory Agent} $\vert$ \textit{FastAPI, LangGraph, Qdrant, Redis, PostgreSQL} \hfill Personal Project \\\\',
    'project1_desc': r'Architected three-tier memory system (working, episodic, knowledge graph) for structured context retrieval, orchestrated via LangGraph multi-agent pipeline, cutting injected context tokens 38\% versus naive history buffering.',
    'project2_title': r'\textbf{DeployMind: Automated GitOps Platform} $\vert$ \textit{Next.js, FastAPI, Docker, Kubernetes, Redis, AWS} \hfill Personal Project \\\\',
    'project2_desc': r'Engineered automated GitOps developer platform provisioning isolated container sandboxes via dynamic Docker daemon execution; automated deployments from GitHub with real-time build streaming and telemetry.'
}

with open('scratch/compile_batch_resumes.py') as f:
    orig = f.read()

template_idx = orig.find('template = r"""')
template = orig[template_idx + len('template = r"""'):orig.rfind('"""')]

tex = template.replace('__TITLE__', role['title'])
tex = tex.replace('__SUMMARY__', role['summary'])
tex = tex.replace('__SKILLS_TOP__', role['skills_top'])
tex = tex.replace('__PROJECT1_TITLE__', role['project1_title'])
tex = tex.replace('__PROJECT1_DESC__', role['project1_desc'])
tex = tex.replace('__PROJECT2_TITLE__', role['project2_title'])
tex = tex.replace('__PROJECT2_DESC__', role['project2_desc'])

out_dir = role['dir']
os.makedirs(out_dir, exist_ok=True)
tex_path = os.path.join(out_dir, 'Pratham_Modi_Resume.tex')
pdf_path = os.path.join(out_dir, 'Pratham_Modi_Resume.pdf')

with open(tex_path, 'w') as f:
    f.write(tex)

cmd = ['tectonic', '-c', 'minimal', tex_path, '--outdir', out_dir]
subprocess.run(cmd, check=True)

reader = pypdf.PdfReader(pdf_path)
page_count = len(reader.pages)
size = os.path.getsize(pdf_path)
print(f'Compiled {pdf_path}: {page_count} page(s), {size} bytes')
assert page_count == 1, f'Resume must be exactly 1 page, got {page_count}!'
print('SUCCESS!')
