import os, subprocess, pypdf, json, sys

out_dir = "output/HP - Software Applications"
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
\textbf{Software Engineer $\vert$ Full-Stack Development $\vert$ Python, React, Next.js, Node.js, Microservices, AWS}
\end{center}

\vspace{-5pt}
\section{Summary}
Full-stack software engineer with 2+ years of production experience building high-performance web applications, scalable microservices, and automated deployment pipelines. Built and deployed responsive React/Next.js frontends and FastAPI/Node.js backends serving 50K+ users with 99.9\% uptime at C3iHub (IIT Kanpur) and Playpower Labs. Proficient in Python, JavaScript, TypeScript, React.js, Next.js, RESTful APIs, Docker, Kubernetes, SQL databases, and AWS cloud infrastructure.

\section{Technical Skills}
\textbf{Languages:} Python, JavaScript, TypeScript, SQL, Node.js \\
\textbf{Frontend:} React, Next.js, React.js, HTML5, CSS3, Tailwind CSS, State Management (Redux, Zustand) \\
\textbf{Backend \& APIs:} FastAPI, Express.js, RESTful APIs, Microservices, Asynchronous Programming, WebSocket, Socket.IO \\
\textbf{Databases \& Messaging:} PostgreSQL, MongoDB, Redis, Kafka, BullMQ \\
\textbf{Cloud \& DevOps:} AWS (EC2, S3), Docker, Kubernetes, CI/CD, GitHub Actions, OpenTelemetry, Prometheus, Grafana, Git, Linux

\section{Experience}

\textbf{C3iHub, IIT Kanpur} \hfill Jul 2025 -- Present \\
\textit{Software Development Engineer} \hfill Kanpur, India
\rItemList
\item Architected core LMS backend serving 50K+ users across microservices for auth, notifications, and content delivery using Express.js, MongoDB, Redis, and Socket.IO, achieving 99.9\% uptime at 10,000+ concurrent connections.
\item Led development of the official IITK hackathon platform onboarding 10K+ participants pan-India; productized into multi-tenant SaaS serving both public and private deployments with RBAC.
\item Engineered event-driven notification pipeline handling 75K+ daily events at 99.5\% delivery reliability using Kafka, BullMQ, and Redis Pub/Sub with consumer-side deduplication.
\item Improved incident response time 85\% by deploying distributed tracing across 15+ services using OpenTelemetry, Prometheus, and Grafana; established alerting SLOs across engineering teams.
\rEndItemList

\textbf{Playpower Labs} \hfill Nov 2024 -- Jun 2025 \\
\textit{Software Development Engineer} \hfill Remote
\rItemList
\item Developed AI tutoring platform using Next.js with SSR/ISR alongside FastAPI microservices, supporting 500+ concurrent WebSocket sessions with sub-100ms response times.
\item Integrated ChromaDB vector search over 10K+ documents via a RAG pipeline, increasing user session depth 35\% with sub-200ms retrieval latency at p95.
\item Reduced release cycle time by 65\% by implementing blue-green CI/CD on AWS with GitHub Actions and automated rollback triggers for zero-downtime deployments.
\rEndItemList

\section{Projects}
\textbf{DeployMind: AI-Powered GitOps Platform} $\vert$ \textit{FastAPI, Next.js, React, Docker, Redis} \\
Engineered a full-stack platform orchestrating code analysis, automated test generation, and container deployment pipelines with distributed locks and automatic rollback triggers.

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
