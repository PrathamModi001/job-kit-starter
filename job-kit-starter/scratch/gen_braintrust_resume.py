import os, subprocess, pypdf, json, sys

out_dir = "output/Braintrust - Software Engineer, SDK"
os.makedirs(out_dir, exist_ok=True)
tex_path = os.path.join(out_dir, "Pratham_Modi_Resume.tex")
pdf_path = os.path.join(out_dir, "Pratham_Modi_Resume.pdf")

tex_content = r"""\documentclass[10pt]{article}
\usepackage[left=0.55in,right=0.55in,top=0.4in,bottom=0.4in]{geometry}
\usepackage{hyperref}
\usepackage{enumitem}
\usepackage{titlesec}
\usepackage{xcolor}
\usepackage{parskip}
\pagestyle{empty}

\hypersetup{colorlinks=true, urlcolor=blue, linkcolor=black}

\titleformat{\section}{\large\bfseries}{}{0em}{}[\titlerule]
\titlespacing{\section}{0pt}{5pt}{2.5pt}

\newcommand{\rItemList}{\begin{itemize}[leftmargin=1.1em, itemsep=1pt, topsep=1.5pt, parsep=0pt, label=\textbullet]}
\newcommand{\rEndItemList}{\end{itemize}}

\begin{document}

\begin{center}
{\Huge \textbf{Pratham Modi}} \\[2pt]
prathammodi001@gmail.com $\vert$ +91-9033393729 $\vert$ Bengaluru, Karnataka, India \\[1pt]
\href{https://github.com/PrathamModi001}{github.com/PrathamModi001} $\vert$ \href{https://www.linkedin.com/in/prathammodii001/}{linkedin.com/in/prathammodii001} \\[3pt]
\textbf{Software Engineer $\vert$ SDK \& Developer Tooling $\vert$ Python, TypeScript, OpenTelemetry, LLM Observability}
\end{center}

\vspace{-5pt}
\section{Summary}
Software engineer with 2+ years of production experience developing developer tooling, SDKs, distributed observability instrumentation, and high-performance backend infrastructure. Deployed production-grade distributed tracing across 15+ microservices with OpenTelemetry, Prometheus, and Grafana at C3iHub (IIT Kanpur). Deeply proficient in Python, TypeScript, JavaScript, OpenTelemetry, automated testing harnesses, API design, and building robust developer tooling for AI evaluation and tracing.

\section{Technical Skills}
\textbf{Languages:} Python, TypeScript, JavaScript, Golang, SQL \\
\textbf{Observability \& Developer Tools:} OpenTelemetry, Distributed Tracing, Prometheus, Grafana, SDK Development, API Design, Profiling \\
\textbf{AI \& LLM Systems:} LLM Evaluation, Prompt Engineering, RAG Pipelines, Vector Databases (ChromaDB), LangGraph \\
\textbf{Backend \& APIs:} FastAPI, Express.js, RESTful APIs, Asynchronous Programming, WebSocket, Microservices \\
\textbf{Cloud \& DevOps:} AWS (EC2, S3), Docker, Kubernetes, CI/CD, GitHub Actions, Automated Testing, Git, Linux

\section{Experience}

\textbf{C3iHub, IIT Kanpur} \hfill Jul 2025 -- Present \\
\textit{Software Development Engineer} \hfill Kanpur, India
\rItemList
\item Improved incident response time 85\% by deploying distributed tracing across 15+ services using OpenTelemetry, Prometheus, and Grafana; established alerting SLOs across engineering teams.
\item Engineered event-driven notification pipeline handling 75K+ daily events at 99.5\% delivery reliability using Kafka, BullMQ, and Redis Pub/Sub with consumer-side deduplication.
\item Architected core LMS backend serving 50K+ users across microservices for auth, notifications, and content delivery using Express.js, MongoDB, Redis, and Socket.IO, achieving 99.9\% uptime at 10,000+ concurrent connections.
\item Led development of the official IITK hackathon platform onboarding 10K+ participants pan-India; productized into multi-tenant SaaS serving both public and private deployments with RBAC.
\rEndItemList

\textbf{Playpower Labs} \hfill Nov 2024 -- Jun 2025 \\
\textit{Software Development Engineer} \hfill Remote
\rItemList
\item Developed AI tutoring platform using Next.js alongside FastAPI microservices, supporting 500+ concurrent WebSocket sessions with sub-100ms response times.
\item Integrated ChromaDB vector search over 10K+ documents via a RAG pipeline, increasing user session depth 35\% with sub-200ms retrieval latency at p95.
\item Implemented automated LLM evaluation harnesses measuring retrieval accuracy and hallucination rates across prompt variations, establishing reproducible benchmarking for model updates.
\item Reduced release cycle time by 65\% by implementing blue-green CI/CD on AWS with GitHub Actions and automated rollback triggers for zero-downtime deployments.
\rEndItemList

\section{Projects}
\textbf{DeployMind: AI-Powered GitOps Platform} $\vert$ \textit{CrewAI, FastAPI, Next.js, Docker, Redis} \\
Engineered a multi-agent AI system orchestrating code analysis, automated test generation, and container deployment pipelines with distributed locks and automatic rollback triggers.

\textbf{Autonomous Invoice Processing Platform} $\vert$ \textit{Kafka, Redis Streams, FastAPI, PostgreSQL} \hfill Hackathon Winner \\
Event-driven platform automating document parsing and payment workflows across 3 channels with dead-letter queues, exponential backoff retries, and RBAC review workflows.

\section{Education}
\textbf{Pandit Deendayal Energy University} \hfill Aug 2021 -- May 2025 \\
Bachelor of Technology in Computer Science and Engineering $\vert$ CGPA: 9.20/10.00 \hfill Gandhinagar, Gujarat

\end{document}
"""

with open(tex_path, "w", encoding="utf-8") as f:
    f.write(tex_content)

# Compile
res = subprocess.run(["tectonic", "-c", "minimal", "Pratham_Modi_Resume.tex"], cwd=out_dir, capture_output=True, text=True)
print("Tectonic exit:", res.returncode)
if res.returncode != 0:
    print("STDOUT:", res.stdout)
    print("STDERR:", res.stderr)

# Verify 1 page
reader = pypdf.PdfReader(pdf_path)
page_count = len(reader.pages)
print(f"PDF Page count: {page_count} (must be 1)")
assert page_count == 1, f"Expected 1 page, got {page_count}"
