import os, subprocess, pypdf

output_dir = "job-kit-starter/output/India Health Link - Full stack Engineer"
os.makedirs(output_dir, exist_ok=True)
tex_path = os.path.join(output_dir, "Pratham_Modi_Resume.tex")
pdf_path = os.path.join(output_dir, "Pratham_Modi_Resume.pdf")

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
\titlespacing{\section}{0pt}{6pt}{3pt}

\newcommand{\rItemList}{\begin{itemize}[leftmargin=1.1em, itemsep=1.5pt, topsep=1.5pt, parsep=0pt, label=\textbullet]}
\newcommand{\rEndItemList}{\end{itemize}}

\begin{document}

\begin{center}
{\Huge \textbf{Pratham Modi}} \\[2pt]
+91-9033393729 $\vert$ \href{mailto:prathammodi001@gmail.com}{prathammodi001@gmail.com} $\vert$ Koramangala, Bengaluru, India \\[1pt]
\href{https://github.com/PrathamModi001}{github.com/PrathamModi001} $\vert$ \href{https://www.linkedin.com/in/prathammodii001/}{linkedin.com/in/prathammodii001} \\[3pt]
\textbf{Software Engineer $\vert$ Full-Stack Development $\vert$ React/Next.js, Python/FastAPI, PostgreSQL, AWS}
\end{center}

\vspace{-6pt}
\section{Summary}
Full-stack software engineer with 2+ years in production, owning systems end-to-end across backend, frontend, and DevOps. Built and scaled a multi-tenant SaaS platform onboarding 10K+ users at C3iHub (IIT Kanpur) and an AI-driven Next.js product at Playpower Labs, spanning Python/FastAPI and Node.js backends, React/Next.js frontends, PostgreSQL, and AWS infrastructure with automated CI/CD and AI-assisted workflows.

\section{Technical Skills}
\textbf{Frontend:} Next.js, React, TypeScript, JavaScript, Tailwind CSS, Redux, Zustand \\
\textbf{Backend:} Python, FastAPI, Django, Node.js, Express.js, RESTful APIs, WebSocket, GraphQL \\
\textbf{Databases:} PostgreSQL, Redis, MongoDB, Snowflake \\
\textbf{Cloud \& DevOps:} AWS (EC2, S3, RDS, Lambda), Docker, GitHub Actions, CI/CD, Microservices \\
\textbf{AI-Assisted Development \& Tools:} Cursor, Claude Code, Multi-Agent Systems (LangGraph), Git, Linux

\section{Experience}

\textbf{C3iHub, IIT Kanpur} \hfill Jul 2025 -- Present \\
\textit{Software Development Engineer} \hfill Kanpur, India
\rItemList
\item Led development of the official IITK hackathon platform onboarding 10K+ participants pan-India; productized into multi-tenant SaaS serving both public and private corporate deployments with RBAC.
\item Architected core LMS backend serving 50K+ users across microservices for auth, notifications, and content delivery using Express.js, MongoDB, Redis, and Socket.IO, achieving 99.9\% uptime at 10,000+ concurrent connections.
\item Built real-time collaborative round engine handling 2,000+ concurrent WebSocket sessions via Django Channels (ASGI) and Redis channel groups -- idempotent submission handling and race-condition-safe team answer sync with timer-enforced auto-submit.
\item Engineered event-driven notification pipeline handling 75K+ daily events at 99.5\% delivery reliability using Kafka, BullMQ, and Redis Pub/Sub -- guaranteed at-least-once delivery with consumer-side deduplication.
\rEndItemList

\textbf{Playpower Labs} \hfill Nov 2024 -- Jun 2025 \\
\textit{Software Development Engineer} \hfill Remote
\rItemList
\item Developed AI tutoring platform using Next.js with SSR/ISR and React Server Components alongside FastAPI microservices, supporting 500+ concurrent WebSocket sessions with sub-100ms response times.
\item Increased user session depth by 35\% by integrating ChromaDB vector search over 10K+ documents via a RAG pipeline, achieving sub-200ms retrieval latency at p95.
\item Reduced release cycle time by 65\% by implementing blue-green CI/CD on AWS with GitHub Actions and automated rollback triggers for zero-downtime deployments.
\rEndItemList

\section{Projects}
\textbf{Autonomous Invoice Processing Platform} $\vert$ \textit{FastAPI, PostgreSQL, Kafka, Redis Streams} \hfill Hackathon Winner \\
Developed event-driven platform automating invoice intake across 3 channels (Gmail API, WhatsApp Business API, Google Drive) with automated validation, deduplication, full audit trail, and fault-tolerant microservices.

\vspace{3pt}
\textbf{Mnemoniq: Multi-Tier Memory AI Agent} $\vert$ \textit{FastAPI, LangGraph, PostgreSQL, Qdrant, Redis} \hfill Personal Project \\
Built a three-tier memory system (working, episodic, knowledge graph) for a conversational AI agent orchestrated via a LangGraph multi-agent pipeline, cutting injected context tokens 38\% behind a FastAPI + SSE backend with PostgreSQL.

\section{Education}
\textbf{B.Tech, Computer Science and Engineering} \hfill 2021 -- 2025 \\
Pandit Deendayal Energy University \hfill GPA: 9.20/10.0

\end{document}
"""

with open(tex_path, "w", encoding="utf-8") as f:
    f.write(tex_content)

print("Saved .tex to", tex_path)
cmd = ["tectonic", "-c", "minimal", tex_path, "-o", output_dir]
res = subprocess.run(cmd, capture_output=True, text=True)
if res.returncode != 0:
    print("Compilation failed:")
    print(res.stderr)
    exit(1)

reader = pypdf.PdfReader(pdf_path)
num_pages = len(reader.pages)
print(f"Compilation successful! Page count: {num_pages}")
assert num_pages == 1, f"Expected 1 page, got {num_pages}"
text = "".join(p.extract_text() for p in reader.pages)
print("Verified 1-page fit. Length of text:", len(text))
