import os, subprocess, pypdf

roles = [
    {
        "dir": "DoorDash - Software Engineer, Backend",
        "title": r"Software Engineer, Backend $\vert$ Python, Go, Distributed Systems, Kafka, Redis, AWS",
        "summary": r"Backend software engineer with 2+ years of production experience building high-throughput distributed systems, event-driven pipelines, and reliable microservices. Architected core backend infrastructure serving 50K+ users at C3iHub (IIT Kanpur) with 99.9\% uptime at 10,000+ concurrent connections. Proficient in database query optimization (cutting p99 latency 70\%), asynchronous messaging (Kafka, BullMQ, Redis Streams), and containerized deployments across AWS and Kubernetes.",
        "skills_top": r"\textbf{Backend \& Distributed Systems:} Distributed Systems, High-Throughput APIs, Event-Driven Architecture, Microservices, Concurrency \\",
        "project1_title": r"\textbf{Autonomous Invoice Processing Platform} $\vert$ \textit{FastAPI, PostgreSQL, Kafka, Redis Streams} \hfill Hackathon Winner \\",
        "project1_desc": r"Developed event-driven platform automating intake across 3 channels (Gmail API, WhatsApp API, Google Drive) with automated validation, deduplication, audit logging, and fault-tolerant microservices with exponential backoff and DLQ.",
        "project2_title": r"\textbf{DeployMind: Automated GitOps Platform} $\vert$ \textit{FastAPI, Docker, Kubernetes, Redis, AWS} \hfill Personal Project \\",
        "project2_desc": r"Engineered automated deployment pipeline containerizing user applications via dynamic Docker daemon execution, provisioning isolated container sandboxes with automated health checking, TLS termination, and real-time build streaming."
    },
    {
        "dir": "Anyscale - Software Engineer, Platform Infrastructure",
        "title": r"Software Engineer, Platform Infrastructure $\vert$ Go, Python, Kubernetes, AWS, Prometheus, Grafana",
        "summary": r"Platform infrastructure and systems software engineer with 2+ years of production experience building cloud-native infrastructure, distributed systems, and real-time observability pipelines. Architected core services at C3iHub (IIT Kanpur) serving 50K+ users with 99.9\% uptime. Built automated GitOps deployment platforms (DeployMind) deploying isolated containers to Kubernetes and EC2 with canary rollouts. Experienced with Prometheus, Grafana, and OpenTelemetry across 15+ microservices.",
        "skills_top": r"\textbf{Platform \& Infrastructure:} Kubernetes (EKS/GKE), Docker, AWS (EC2, S3, RDS), Prometheus, Grafana, OpenTelemetry, CI/CD \\",
        "project1_title": r"\textbf{DeployMind: AI-Powered GitOps Platform} $\vert$ \textit{Python, FastAPI, Docker, Kubernetes, Redis, AWS} \hfill Personal Project \\",
        "project1_desc": r"Built automated GitOps deployment platform provisioning isolated container sandboxes via dynamic Docker daemon execution; automated deployments from GitHub to EC2 and Kubernetes (EKS/GKE) with graduated canary traffic shifting and automated rollback.",
        "project2_title": r"\textbf{Autonomous Invoice Processing Platform} $\vert$ \textit{FastAPI, PostgreSQL, Kafka, Redis Streams} \hfill Hackathon Winner \\",
        "project2_desc": r"Developed event-driven platform automating intake across 3 channels (Gmail API, WhatsApp API, Google Drive) with automated validation, deduplication, audit logging, and fault-tolerant microservices with exponential backoff and DLQ."
    },
    {
        "dir": "NCR Voyix - Full Stack Software Engineer",
        "title": r"Full Stack Software Engineer $\vert$ Go, TypeScript, React, Node.js, Cloud Microservices, PostgreSQL",
        "summary": r"Full stack software engineer with 2+ years of production experience building high-throughput web applications and resilient backend microservices. Architected core LMS backend serving 50K+ users at C3iHub (IIT Kanpur) with 99.9\% uptime at 10,000+ concurrent connections. Proficient across modern React/TypeScript frontends, Go/Node.js microservices, real-time WebSocket state synchronization, and database query optimization.",
        "skills_top": r"\textbf{Frontend \& Full Stack:} React, TypeScript, Next.js, HTML5/CSS3, Tailwind CSS, RESTful APIs, WebSockets \\",
        "project1_title": r"\textbf{Autonomous Invoice Processing Platform} $\vert$ \textit{FastAPI, PostgreSQL, Kafka, Redis Streams} \hfill Hackathon Winner \\",
        "project1_desc": r"Developed event-driven platform automating intake across 3 channels (Gmail API, WhatsApp API, Google Drive) with automated validation, deduplication, audit logging, and fault-tolerant microservices with exponential backoff and DLQ.",
        "project2_title": r"\textbf{DeployMind: Automated Deployment Platform} $\vert$ \textit{FastAPI, Docker, Kubernetes, Redis, AWS} \hfill Personal Project \\",
        "project2_desc": r"Engineered automated deployment pipeline containerizing user applications via dynamic Docker daemon execution, provisioning isolated container sandboxes with automated health checking, TLS termination, and real-time build streaming."
    },
    {
        "dir": "Cargill - Associate Software Engineer",
        "title": r"Associate Software Engineer $\vert$ Python, Node.js, RESTful APIs, CI/CD, Microservices, AWS",
        "summary": r"Software engineer with 2+ years of production experience building clean, maintainable, and reliable backend software solutions. Architected core backend systems serving 50K+ users at C3iHub (IIT Kanpur) with 99.9\% uptime at 10,000+ concurrent connections. Proficient in automated unit and integration testing, CI/CD deployment pipelines (GitHub Actions, Docker), database performance tuning, and cloud infrastructure on AWS.",
        "skills_top": r"\textbf{Software Engineering \& APIs:} RESTful Web Services, Microservices Architecture, Clean Code, Unit \& Integration Testing, CI/CD \\",
        "project1_title": r"\textbf{Autonomous Invoice Processing Platform} $\vert$ \textit{FastAPI, PostgreSQL, Kafka, Redis Streams} \hfill Hackathon Winner \\",
        "project1_desc": r"Developed event-driven platform automating intake across 3 channels (Gmail API, WhatsApp API, Google Drive) with automated validation, deduplication, audit logging, and fault-tolerant microservices with exponential backoff and DLQ.",
        "project2_title": r"\textbf{DeployMind: Automated Deployment Platform} $\vert$ \textit{FastAPI, Docker, Kubernetes, Redis, AWS} \hfill Personal Project \\",
        "project2_desc": r"Engineered automated deployment pipeline containerizing user applications via dynamic Docker daemon execution, provisioning isolated container sandboxes with automated health checking, TLS termination, and real-time build streaming."
    },
    {
        "dir": "Vertexcover Labs - AI Engineer",
        "title": r"AI Engineer $\vert$ Python, LangGraph, LLM Agents, Vector Search, Go, Distributed Systems",
        "summary": r"AI and systems engineer with 2+ years of production experience designing agentic AI systems, vector search pipelines, and distributed data workflows. Engineered multi-agent memory architectures (Mnemoniq) cutting prompt token overhead by 38\% using LangGraph and Qdrant. Built RAG pipelines over 10K+ documents at Playpower Labs with sub-200ms p95 retrieval latency. Proficient in Python, FastAPI, Go, vector databases, and containerized cloud deployment.",
        "skills_top": r"\textbf{AI Engineering \& Agents:} Multi-Agent Orchestration, LangGraph, CrewAI, RAG Pipelines, Vector Retrieval (ChromaDB, Qdrant), Prompt Engineering \\",
        "project1_title": r"\textbf{Mnemoniq: Multi-Tier Memory AI Agent} $\vert$ \textit{FastAPI, LangGraph, Qdrant, Redis, PostgreSQL} \hfill Personal Project \\",
        "project1_desc": r"Architected three-tier memory system (working, episodic, knowledge graph) for conversational AI agent orchestrated via LangGraph multi-agent pipeline, cutting injected context tokens 38\% versus naive history buffering.",
        "project2_title": r"\textbf{DeployMind: AI-Powered GitOps Platform} $\vert$ \textit{Python, FastAPI, CrewAI, Docker, Kubernetes, AWS} \hfill Personal Project \\",
        "project2_desc": r"Engineered automated GitOps deployment platform provisioning isolated container sandboxes via dynamic Docker daemon execution; automated deployments from GitHub to EC2 and Kubernetes (EKS/GKE) with graduated canary traffic shifting and automated rollback."
    }
]

template = r"""\documentclass[10pt]{article}
\usepackage[left=0.55in,right=0.55in,top=0.4in,bottom=0.4in]{geometry}
\usepackage{hyperref}
\usepackage{enumitem}
\usepackage{titlesec}
\usepackage{xcolor}
\usepackage{parskip}
\pagestyle{empty}

\hypersetup{colorlinks=true, urlcolor=black, linkcolor=black}

\titleformat{\section}{\large\bfseries}{}{0em}{}[\titlerule]
\titlespacing{\section}{0pt}{5pt}{2pt}

\newcommand{\rItemList}{\begin{itemize}[leftmargin=1.1em, itemsep=1.2pt, topsep=1.2pt, parsep=0pt, label=\textbullet]}
\newcommand{\rEndItemList}{\end{itemize}}

\begin{document}

\begin{center}
{\Huge \textbf{Pratham Modi}} \\[2pt]
+91-9033393729 $\vert$ \href{mailto:prathammodi001@gmail.com}{prathammodi001@gmail.com} $\vert$ Koramangala, Bengaluru, India \\[1pt]
\href{https://github.com/PrathamModi001}{github.com/PrathamModi001} $\vert$ \href{https://www.linkedin.com/in/prathammodii001/}{linkedin.com/in/prathammodii001} \\[2pt]
\textbf{__TITLE__}
\end{center}

\vspace{-6pt}
\section{Summary}
__SUMMARY__

\section{Technical Skills}
__SKILLS_TOP__
\textbf{Databases \& Caching:} PostgreSQL, MySQL, MongoDB, Redis (Streams, Pub/Sub), Query Optimization, Indexing, Schema Design \\
\textbf{Messaging \& Streaming:} Kafka, BullMQ, Redis Streams, Event-Driven Architecture \\
\textbf{Cloud, DevOps \& Observability:} AWS (EC2, S3, RDS), Docker, Kubernetes, CI/CD (GitHub Actions), Grafana, Prometheus, OpenTelemetry \\
\textbf{Languages:} Python, Node.js, TypeScript, SQL

\section{Experience}

\textbf{C3iHub, IIT Kanpur} \hfill Jul 2025 -- Present \\
\textit{Software Development Engineer} \hfill Kanpur, India
\rItemList
\item Architected core LMS backend serving 50K+ users across microservices for auth, notifications, and content delivery using Express.js, MongoDB, Redis, and Socket.IO, achieving 99.9\% uptime at 10,000+ concurrent connections.
\item Reduced cloud storage costs 60\% (~Rs. 4.8L/year) via S3 Object Lock and Glacier; cut database p99 latency from 450ms $\rightarrow$ 135ms through compound indexing, horizontal sharding, and Redis caching.
\item Engineered event-driven notification pipeline handling 75K+ daily events at 99.5\% delivery reliability using Kafka, BullMQ, and Redis Pub/Sub -- guaranteed at-least-once delivery with consumer-side deduplication.
\item Improved incident response time 85\% by deploying distributed tracing across 15+ services using OpenTelemetry, Prometheus, and Grafana; defined alerting SLOs across cross-functional teams.
\rEndItemList

\textbf{Playpower Labs} \hfill Nov 2024 -- Jun 2025 \\
\textit{Software Development Engineer} \hfill Remote
\rItemList
\item Architected automated CI/CD pipeline using GitHub Actions and Docker, reducing release deployment cycles by 40\% and establishing comprehensive integration testing.
\item Developed high-concurrency real-time tutoring backend microservices, supporting 500+ concurrent WebSocket sessions with sub-100ms response times.
\item Increased user session depth by 35\% by integrating ChromaDB vector search over 10K+ documents via a RAG pipeline, achieving sub-200ms retrieval latency at p95.
\rEndItemList

\section{Projects}
__PROJECT1_TITLE__
__PROJECT1_DESC__

\vspace{2pt}
__PROJECT2_TITLE__
__PROJECT2_DESC__

\section{Education}
\textbf{B.Tech, Computer Science and Engineering} \hfill 2021 -- 2025 \\
Pandit Deendayal Energy University \hfill GPA: 9.20/10.0

\end{document}
"""

all_ok = True
for r in roles:
    d = os.path.join("job-kit-starter", "output", r["dir"])
    os.makedirs(d, exist_ok=True)
    tex_content = template.replace("__TITLE__", r["title"])
    tex_content = tex_content.replace("__SUMMARY__", r["summary"])
    tex_content = tex_content.replace("__SKILLS_TOP__", r["skills_top"])
    tex_content = tex_content.replace("__PROJECT1_TITLE__", r["project1_title"])
    tex_content = tex_content.replace("__PROJECT1_DESC__", r["project1_desc"])
    tex_content = tex_content.replace("__PROJECT2_TITLE__", r["project2_title"])
    tex_content = tex_content.replace("__PROJECT2_DESC__", r["project2_desc"])
    
    tex_path = os.path.join(d, "Pratham_Modi_Resume.tex")
    with open(tex_path, "w") as f:
        f.write(tex_content)
        
    res = subprocess.run(["tectonic", "-c", "minimal", tex_path, "--outdir", d], capture_output=True, text=True)
    pdf_path = os.path.join(d, "Pratham_Modi_Resume.pdf")
    
    if res.returncode != 0 or not os.path.exists(pdf_path):
        print(f"FAILED {r['dir']}: {res.stderr}")
        all_ok = False
        continue
        
    reader = pypdf.PdfReader(pdf_path)
    page_count = len(reader.pages)
    if page_count != 1:
        print(f"PAGE COUNT WARNING {r['dir']}: {page_count} pages!")
        all_ok = False
    else:
        print(f"SUCCESS: {r['dir']} -> 1-page PDF generated at {pdf_path}")

if all_ok:
    print("\nALL 5 TAILORED RESUMES SUCCESSFULLY GENERATED AND VERIFIED (1 PAGE EACH)!")
