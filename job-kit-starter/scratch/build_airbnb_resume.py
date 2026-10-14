import os, subprocess, pypdf, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
output_dir = ROOT / "output" / "Airbnb - Operations Engineer, Tech Foundations"
output_dir.mkdir(parents=True, exist_ok=True)
tex_path = output_dir / "Pratham_Modi_Resume.tex"
pdf_path = output_dir / "Pratham_Modi_Resume.pdf"

tex_content = r"""\documentclass[10pt]{article}
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

\newcommand{\rItemList}{\begin{itemize}[leftmargin=1.1em, itemsep=1.5pt, topsep=1.5pt, parsep=0pt, label=\textbullet]}
\newcommand{\rEndItemList}{\end{itemize}}

\begin{document}

\begin{center}
{\Huge \textbf{Pratham Modi}} \\[2pt]
+91-9033393729 $\vert$ \href{mailto:prathammodi001@gmail.com}{prathammodi001@gmail.com} $\vert$ Kanpur, Uttar Pradesh, India \\[1pt]
\href{https://github.com/PrathamModi001}{github.com/PrathamModi001} $\vert$ \href{https://www.linkedin.com/in/prathammodii001/}{linkedin.com/in/prathammodii001} \\[3pt]
\textbf{Software Engineer $\vert$ Operations \& Observability $\vert$ Prometheus, Grafana, OpenTelemetry, AWS}
\end{center}

\vspace{-6pt}
\section{Summary}
Operations and backend software engineer with 2+ years in production. Led backend and observability architecture of an event-driven LMS platform serving 50K+ users at C3iHub (IIT Kanpur), spanning microservices, distributed tracing, and cloud infrastructure. Strong in Python, TypeScript, OpenTelemetry, Prometheus, Grafana, and AWS, with a track record of cutting incident response times by 85\% and automating CI/CD workflows with AI-assisted tooling.

\section{Technical Skills}
\textbf{Observability \& Operations:} Prometheus, Grafana, OpenTelemetry, Distributed Tracing, Incident Management, SLOs \\
\textbf{Cloud \& DevOps:} AWS (EC2, S3, Lambda, EKS), Docker, Kubernetes, GitHub Actions, CI/CD, Microservices \\
\textbf{Languages:} Python, TypeScript, JavaScript, SQL, Bash \\
\textbf{Backend \& Messaging:} Node.js, Express.js, FastAPI, Kafka, Redis, PostgreSQL, MongoDB, RESTful APIs \\
\textbf{AI/ML \& Tools:} Prompt Engineering, LLM Evaluation, Agentic Workflows, LangGraph, Vector Databases (ChromaDB, Qdrant)

\section{Experience}

\textbf{C3iHub, IIT Kanpur} \hfill Jul 2025 -- Present \\
\textit{Software Development Engineer} \hfill Kanpur, India
\rItemList
\item Improved incident response time 85\% by deploying distributed tracing across 15+ services using OpenTelemetry, Prometheus, and Grafana with defined SLO alerts.
\item Architected core LMS backend serving 50K+ users across microservices for auth, notifications, and content delivery using Express.js, MongoDB, Redis, and Socket.IO, achieving 99.9\% uptime at 10,000+ concurrent connections.
\item Engineered event-driven notification pipeline handling 75K+ daily events at 99.5\% delivery reliability using Kafka, BullMQ, and Redis Pub/Sub with consumer-side deduplication.
\item Led development of the official IITK hackathon platform onboarding 10K+ participants pan-India; productized into multi-tenant SaaS serving both public and private corporate deployments with RBAC.
\rEndItemList

\textbf{Playpower Labs} \hfill Nov 2024 -- Jun 2025 \\
\textit{Software Development Engineer} \hfill Remote
\rItemList
\item Reduced release cycle time by 65\% by implementing blue-green CI/CD on AWS with GitHub Actions and automated rollback triggers for zero-downtime deployments.
\item Developed AI tutoring platform using FastAPI microservices and Next.js, supporting 500+ concurrent WebSocket sessions with sub-100ms response times.
\item Integrated ChromaDB vector search over 10K+ documents via a RAG pipeline, increasing user session depth 35\% with sub-200ms retrieval latency at p95.
\rEndItemList

\section{Projects}

\textbf{DeployMind — AI-Powered GitOps Platform} $\vert$ \textit{Python, FastAPI, CrewAI, Kubernetes, Docker} \hfill \href{https://github.com/PrathamModi001/DeployMind}{github.com/PrathamModi001/DeployMind} \\
GitOps platform automating GitHub-to-Kubernetes (EKS/GKE) deployments via a 3-agent AI pipeline (CrewAI) with Rolling/Canary/Blue-Green strategies, Redis-backed distributed locking, and automated rollback.

\vspace{2pt}
\textbf{Mnemoniq — Multi-Tier Memory AI Agent} $\vert$ \textit{FastAPI, LangGraph, PostgreSQL, Qdrant, Redis} \hfill \href{https://github.com/PrathamModi001/Mnemoniq}{github.com/PrathamModi001/Mnemoniq} \\
Orchestrated 3-tier memory pipeline cutting context tokens 38\% vs. naive buffering; integrated Qdrant vector search and NetworkX graph traversal behind FastAPI + SSE streaming.

\section{Education}
\textbf{Pandit Deendayal Energy University} \hfill 2021 -- 2025 \\
Bachelor of Technology in Computer Science and Engineering $\vert$ GPA: 9.20 / 10.0 \hfill Gandhinagar, India

\end{document}
"""

tex_path.write_text(tex_content, encoding="utf-8")
print(f"Wrote {tex_path}")

# Compile with tectonic
cmd = ["tectonic", "-c", "minimal", str(tex_path)]
res = subprocess.run(cmd, capture_output=True, text=True, cwd=str(output_dir))
if res.returncode != 0:
    print(f"Compilation failed: {res.stderr}")
    sys.exit(1)
print("Compiled PDF successfully.")

# Check page count
reader = pypdf.PdfReader(str(pdf_path))
num_pages = len(reader.pages)
print(f"Page count: {num_pages}")
if num_pages != 1:
    print(f"ERROR: Page count is {num_pages}, must be 1!")
    sys.exit(1)

# Check extracted text for facts
text = "".join(p.extract_text() for p in reader.pages)
for fact in ["85%", "50K+", "10,000+", "75K+", "65%", "9.20"]:
    if fact in text:
        print(f"Fact verified: {fact}")
    else:
        print(f"Fact missing: {fact}")
