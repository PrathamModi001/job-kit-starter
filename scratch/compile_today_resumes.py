import os, subprocess
import pypdf

roles = [
    {
        "dir": "Hyperproof - Software Engineer, Risk Management",
        "title": r"Software Engineer $\vert$ Node.js, React, TypeScript, PostgreSQL, Distributed Systems, APIs",
        "summary": r"Full-stack software engineer with 2+ years of production experience building reliable web applications, distributed backend services, and scalable APIs. Architected core systems serving 50K+ users at C3iHub (IIT Kanpur) with 99.9\% uptime at 10,000+ concurrent connections. Proficient in React/TypeScript frontends, Node.js/Python microservices, PostgreSQL query optimization, and event-driven architectures with Kafka and Redis.",
        "skills_top": r"\textbf{Full Stack \& Frontend:} React, TypeScript, Next.js, HTML5/CSS3, Tailwind CSS, RESTful APIs, State Management \\",
        "project1_title": r"\textbf{Autonomous Invoice Processing Platform} $\vert$ \textit{FastAPI, PostgreSQL, Kafka, Redis Streams} \hfill Hackathon Winner \\",
        "project1_desc": r"Developed event-driven platform automating invoice intake across 3 channels (Gmail API, WhatsApp Business API, Google Drive) with automated validation, deduplication, full audit trail, and fault-tolerant microservices with exponential backoff and DLQ.",
        "project2_title": r"\textbf{DeployMind: AI-Powered GitOps Platform} $\vert$ \textit{FastAPI, Docker, Kubernetes, Redis, AWS} \hfill Personal Project \\",
        "project2_desc": r"Engineered automated deployment pipeline containerizing user applications via dynamic Docker daemon execution, provisioning isolated container sandboxes with automated health checking, TLS termination, and real-time build streaming."
    },
    {
        "dir": "Cardboard - Fullstack Engineer",
        "title": r"Fullstack Engineer $\vert$ TypeScript, React, Node.js, Python, Real-Time Systems, Media AI",
        "summary": r"Fullstack engineer with 2+ years of production experience building high-performance browser applications, real-time collaborative state engines, and media/AI workflows. Built real-time collaborative round engine handling 2,000+ concurrent WebSocket sessions at C3iHub (IIT Kanpur) with idempotent state synchronization. Experienced in React/Next.js, FastAPI/Node.js, Docker containerization, and sub-200ms vector search pipelines.",
        "skills_top": r"\textbf{Full Stack \& Real-Time:} TypeScript, React, Next.js, Node.js, WebSockets, Real-Time State Sync, Canvas/Media \\",
        "project1_title": r"\textbf{DeployMind: AI-Powered GitOps Platform} $\vert$ \textit{Python, FastAPI, Docker, Kubernetes, Redis, AWS} \hfill Personal Project \\",
        "project1_desc": r"Built automated GitOps deployment platform provisioning isolated container sandboxes via dynamic Docker daemon execution; automated deployments from GitHub to EC2 and Kubernetes (EKS/GKE) with graduated canary traffic shifting and automated rollback.",
        "project2_title": r"\textbf{Mnemoniq: Multi-Tier Memory AI Agent} $\vert$ \textit{FastAPI, LangGraph, Qdrant, Redis, PostgreSQL} \hfill Personal Project \\",
        "project2_desc": r"Architected three-tier memory system (working, episodic, knowledge graph) for conversational AI agent orchestrated via LangGraph multi-agent pipeline, cutting injected context tokens 38\% versus naive history buffering."
    },
    {
        "dir": "Plaza - SDE I (Backend)",
        "title": r"Software Development Engineer I (Backend) $\vert$ Python, Go, Microservices, Redis, Kafka, AWS",
        "summary": r"Backend software engineer with 2+ years of production experience building high-throughput microservices, concurrent architectures, and distributed message pipelines. Architected core backend systems serving 50K+ users at C3iHub (IIT Kanpur) with 99.9\% uptime at 10,000+ concurrent connections. Strong foundation in distributed caching (Redis), asynchronous queues (Kafka, BullMQ), cloud infrastructure (AWS, Docker), and database query optimization (cutting p99 latency 70\%).",
        "skills_top": r"\textbf{Backend \& Distributed Systems:} Python, Go, Microservices, RESTful APIs, High-Throughput Architecture, Redis, Kafka \\",
        "project1_title": r"\textbf{Autonomous Invoice Processing Platform} $\vert$ \textit{FastAPI, PostgreSQL, Kafka, Redis Streams} \hfill Hackathon Winner \\",
        "project1_desc": r"Developed event-driven platform automating intake across 3 channels (Gmail API, WhatsApp API, Google Drive) with automated validation, deduplication, audit logging, and fault-tolerant microservices with exponential backoff and DLQ.",
        "project2_title": r"\textbf{DeployMind: AI-Powered GitOps Platform} $\vert$ \textit{FastAPI, Docker, Kubernetes, Redis, AWS} \hfill Personal Project \\",
        "project2_desc": r"Engineered automated deployment pipeline containerizing user applications via dynamic Docker daemon execution, provisioning isolated container sandboxes with automated health checking, TLS termination, and real-time build streaming."
    },
    {
        "dir": "Goldcast - Founding Platform Engineer",
        "title": r"Founding Platform Engineer $\vert$ Distributed Systems, AWS, Docker, Kafka, Redis, Python, Microservices",
        "summary": r"Systems and platform backend engineer with 2+ years of production experience building cloud-native infrastructure, high-concurrency event streams, and distributed observability pipelines. Architected core backend serving 50K+ users at C3iHub (IIT Kanpur) with 99.9\% uptime at 10,000+ concurrent connections. Deployed distributed tracing across 15+ microservices with OpenTelemetry, Prometheus, and Grafana, improving MTTR by 85\%.",
        "skills_top": r"\textbf{Platform \& Infrastructure:} AWS (EC2, S3, RDS), Docker, Kubernetes, Kafka, Redis Streams, OpenTelemetry, Grafana \\",
        "project1_title": r"\textbf{DeployMind: AI-Powered GitOps Platform} $\vert$ \textit{Python, FastAPI, Docker, Kubernetes, Redis, AWS} \hfill Personal Project \\",
        "project1_desc": r"Engineered automated GitOps deployment platform provisioning isolated container sandboxes via dynamic Docker daemon execution; automated deployments from GitHub to EC2 and Kubernetes (EKS/GKE) with graduated canary traffic shifting and automated rollback.",
        "project2_title": r"\textbf{Autonomous Invoice Processing Platform} $\vert$ \textit{FastAPI, PostgreSQL, Kafka, Redis Streams} \hfill Hackathon Winner \\",
        "project2_desc": r"Developed event-driven platform automating intake across 3 channels (Gmail API, WhatsApp API, Google Drive) with automated validation, deduplication, audit logging, and fault-tolerant microservices with exponential backoff and DLQ."
    },
    {
        "dir": "Synthio Labs - Software Engineer - AI",
        "title": r"Software Engineer - AI $\vert$ Python, LLM Agents, LangGraph, RAG, FastAPI, Vector Search, AWS",
        "summary": r"AI systems and backend software engineer with 2+ years of production experience designing agentic AI systems, vector search pipelines, and distributed data workflows. Engineered multi-agent memory architectures (Mnemoniq) cutting prompt token overhead by 38\% using LangGraph and Qdrant. Built RAG pipelines over 10K+ documents at Playpower Labs with sub-200ms p95 retrieval latency. Proficient in Python, FastAPI, Anthropic/OpenAI APIs, and containerized deployment.",
        "skills_top": r"\textbf{AI Engineering \& Agents:} Multi-Agent Orchestration, LangGraph, CrewAI, RAG Pipelines, Vector Retrieval (ChromaDB, Qdrant), Prompt Engineering \\",
        "project1_title": r"\textbf{Mnemoniq: Multi-Tier Memory AI Agent} $\vert$ \textit{FastAPI, LangGraph, Qdrant, Redis, PostgreSQL} \hfill Personal Project \\",
        "project1_desc": r"Architected three-tier memory system (working, episodic, knowledge graph) for conversational AI agent orchestrated via LangGraph multi-agent pipeline, cutting injected context tokens 38\% versus naive history buffering.",
        "project2_title": r"\textbf{DeployMind: AI-Powered GitOps Platform} $\vert$ \textit{Python, FastAPI, CrewAI, Docker, Kubernetes, AWS} \hfill Personal Project \\",
        "project2_desc": r"Engineered automated GitOps deployment platform provisioning isolated container sandboxes via dynamic Docker daemon execution; automated deployments from GitHub to EC2 and Kubernetes (EKS/GKE) with graduated canary traffic shifting and automated rollback."
    },
    {
        "dir": "Neufin - Fullstack Developer",
        "title": r"Fullstack Developer $\vert$ Node.js, React, TypeScript, Python, PostgreSQL, Redis, Cloud APIs",
        "summary": r"Full-stack engineer with 2+ years of production experience building high-throughput consumer web platforms and resilient backend services. Architected core LMS backend serving 50K+ users at C3iHub (IIT Kanpur) with 99.9\% uptime at 10,000+ concurrent connections. Proficient across modern React/TypeScript frontends, Express.js microservices, real-time WebSocket state synchronization, and database query optimization.",
        "skills_top": r"\textbf{Frontend \& Full Stack:} React, TypeScript, Next.js, HTML5/CSS3, Tailwind CSS, State Management, Responsive Design \\",
        "project1_title": r"\textbf{Autonomous Invoice Processing Platform} $\vert$ \textit{FastAPI, PostgreSQL, Kafka, Redis Streams} \hfill Hackathon Winner \\",
        "project1_desc": r"Developed event-driven platform automating intake across 3 channels (Gmail API, WhatsApp API, Google Drive) with automated validation, deduplication, audit logging, and fault-tolerant microservices with exponential backoff and DLQ.",
        "project2_title": r"\textbf{DeployMind: AI-Powered GitOps Platform} $\vert$ \textit{FastAPI, Docker, Kubernetes, Redis, AWS} \hfill Personal Project \\",
        "project2_desc": r"Engineered automated deployment pipeline containerizing user applications via dynamic Docker daemon execution, provisioning isolated container sandboxes with automated health checking, TLS termination, and real-time build streaming."
    },
    {
        "dir": "Attributics - GenAI Developer",
        "title": r"GenAI Developer $\vert$ Multi-Agent Systems, LangGraph, CrewAI, RAG, Python, FastAPI, Vector Search",
        "summary": r"GenAI and backend software engineer with 2+ years of production experience building agentic workflows, multi-agent orchestration, and production RAG pipelines. Built Mnemoniq, a multi-tier memory system with LangGraph and Qdrant cutting context token overhead by 38\%. Integrated ChromaDB vector search over 10K+ documents at Playpower Labs achieving sub-200ms p95 latency. Strong in Python, FastAPI, vector databases, and event-driven microservices.",
        "skills_top": r"\textbf{GenAI \& Agent Systems:} LangGraph, CrewAI, Multi-Agent Orchestration, RAG Pipelines, Vector Retrieval (Qdrant, ChromaDB), Prompt Engineering \\",
        "project1_title": r"\textbf{Mnemoniq: Multi-Tier Memory AI Agent} $\vert$ \textit{FastAPI, LangGraph, Qdrant, Redis, PostgreSQL} \hfill Personal Project \\",
        "project1_desc": r"Architected three-tier memory system (working, episodic, knowledge graph) for conversational AI agent orchestrated via LangGraph multi-agent pipeline, cutting injected context tokens 38\% versus naive history buffering.",
        "project2_title": r"\textbf{DeployMind: AI-Powered GitOps Platform} $\vert$ \textit{Python, FastAPI, CrewAI, Docker, Kubernetes, AWS} \hfill Personal Project \\",
        "project2_desc": r"Engineered automated GitOps deployment platform provisioning isolated container sandboxes via dynamic Docker daemon execution; automated deployments from GitHub to EC2 and Kubernetes (EKS/GKE) with graduated canary traffic shifting and automated rollback."
    },
    {
        "dir": "Emplay Analytics - Associate - Agentic AI Automation Engineer",
        "title": r"Agentic AI Automation Engineer $\vert$ LangGraph, LangChain, RAG, Python, FastAPI, SQL, Workflows",
        "summary": r"AI automation and backend software engineer with 2+ years of production experience developing agentic workflows, multi-tier memory systems, and scalable backend pipelines. Engineered multi-agent memory architectures (Mnemoniq) cutting prompt token overhead by 38\% using LangGraph and Qdrant. Built event-driven notification pipelines handling 75K+ daily events at C3iHub (IIT Kanpur). Proficient in Python, LangGraph, FastAPI, SQL, and automation.",
        "skills_top": r"\textbf{Agentic AI \& Workflows:} Agentic Automation, LangGraph, LangChain, RAG Pipelines, Vector Search (Qdrant, ChromaDB), Workflow Orchestration \\",
        "project1_title": r"\textbf{Mnemoniq: Multi-Tier Memory AI Agent} $\vert$ \textit{FastAPI, LangGraph, Qdrant, Redis, PostgreSQL} \hfill Personal Project \\",
        "project1_desc": r"Architected three-tier memory system (working, episodic, knowledge graph) for conversational AI agent orchestrated via LangGraph multi-agent pipeline, cutting injected context tokens 38\% versus naive history buffering.",
        "project2_title": r"\textbf{Autonomous Invoice Processing Platform} $\vert$ \textit{FastAPI, PostgreSQL, Kafka, Redis Streams} \hfill Hackathon Winner \\",
        "project2_desc": r"Developed event-driven platform automating intake across 3 channels (Gmail API, WhatsApp API, Google Drive) with automated validation, deduplication, audit logging, and fault-tolerant microservices with exponential backoff and DLQ."
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
    
    # assert 1-page via pypdf
    reader = pypdf.PdfReader(pdf_path)
    page_count = len(reader.pages)
    print(f"[{'PASS' if page_count == 1 else 'FAIL'}] {r['dir']}: {page_count} page(s) (compile code {res.returncode})")
    assert page_count == 1, f"Expected 1 page, got {page_count} for {r['dir']}"
