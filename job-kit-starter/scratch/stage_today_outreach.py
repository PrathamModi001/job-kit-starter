import csv, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
csv_path = ROOT / "output" / "job-search" / "outreach" / "startups_outreach.csv"
html_path = ROOT / "output" / "job-search" / "outreach" / "send_drafts.html"

# Load existing emails to avoid duplicates
existing_emails = set()
if csv_path.exists():
    with open(csv_path, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            em = r.get("Email", "").strip().lower()
            if em: existing_emails.add(em)

today_targets = [
    # --- 10 Indian Companies (Engineers / Team Leads) ---
    {
        "Tier": "B",
        "Company": "Razorpay",
        "Founder": "Saurav Rastogi",
        "Email": "saurav.rastogi@razorpay.com",
        "Confidence": "Verified",
        "Source": "GitHub commit author",
        "Role Pitch": "Backend Software Engineer (High-Throughput FinTech)",
        "Subject": "Reaching out re: backend engineering at Razorpay",
        "Notes": "Attached Pratham_Modi_Base_Resume.pdf; highlights C3iHub 75k Kafka events/day and 450ms->135ms latency reduction",
        "Body": """Hi Saurav,

Saw your engineering work on Razorpay's frontend/system libraries on GitHub and wanted to reach out directly.

At C3iHub (IIT Kanpur), I engineered an event-driven notification engine handling 75k daily Kafka events at 99.5% reliability and cut MongoDB p99 latency from 450ms to 135ms. At Playpower Labs, I developed microservices maintaining sub-100ms response times.

Resume is attached — GitHub is github.com/PrathamModi001. Open to connecting if your team is exploring backend engineering talent or if you'd be open to referring my profile.

Best,
Pratham Modi"""
    },
    {
        "Tier": "B",
        "Company": "Razorpay",
        "Founder": "Rohan Kokane",
        "Email": "rohan.kokane@razorpay.com",
        "Confidence": "Verified",
        "Source": "GitHub commit author",
        "Role Pitch": "Backend Software Engineer (Distributed Systems)",
        "Subject": "Quick note from a backend engineer re: Razorpay",
        "Notes": "Attached Pratham_Modi_Base_Resume.pdf; highlights C3iHub 50K users at 99.9% uptime and Kafka pipelines",
        "Body": """Hi Rohan,

Saw your commits on Blade at Razorpay. Reaching out to ask if your team is currently looking for backend engineers who work with Node.js and distributed systems.

At C3iHub (IIT Kanpur), I architected microservices serving 50K+ users at 10,000+ concurrent connections and managed event streams over Kafka. At Playpower Labs, I built low-latency RAG and async API pipelines.

Resume is attached — happy to connect if you're open to referring or passing my profile along.

Best,
Pratham Modi"""
    },
    {
        "Tier": "B",
        "Company": "SigNoz",
        "Founder": "Tushar Vats",
        "Email": "tushar@signoz.io",
        "Confidence": "Verified",
        "Source": "GitHub commit author",
        "Role Pitch": "Distributed Tracing & Telemetry Systems Engineer",
        "Subject": "Telemetry pipelines & distributed tracing for SigNoz",
        "Notes": "Attached Pratham_Modi_Base_Resume.pdf; highlights OpenTelemetry distributed tracing across 15+ services and 85% MTTR drop",
        "Body": """Hi Tushar,

Following your work on SigNoz's OpenTelemetry collector and query pipelines on GitHub.

At C3iHub (IIT Kanpur), I deployed distributed tracing across 15+ services using OpenTelemetry, Prometheus, and Grafana with defined SLO alerts, cutting incident response times by 85%. I also built event pipelines processing 75k daily Kafka events.

Sending my resume along — would love to contribute to SigNoz's telemetry backends if the team is hiring.

Best,
Pratham Modi"""
    },
    {
        "Tier": "B",
        "Company": "SigNoz",
        "Founder": "Nikhil Soni",
        "Email": "nikhil.soni@signoz.io",
        "Confidence": "Verified",
        "Source": "GitHub commit author",
        "Role Pitch": "Backend & Observability Systems Engineer",
        "Subject": "Re: SigNoz telemetry & backend hiring",
        "Notes": "Attached Pratham_Modi_Base_Resume.pdf; highlights C3iHub OpenTelemetry and Kafka event pipelines",
        "Body": """Hi Nikhil,

Saw your recent contributions to SigNoz. Reaching out to see if the backend and observability teams are adding engineers.

At C3iHub (IIT Kanpur), I deployed OpenTelemetry distributed tracing across 15+ microservices and scaled an event-driven engine handling 75k daily Kafka events at 99.5% delivery. At Playpower Labs, I built sub-200ms RAG pipelines.

Resume is attached — github.com/PrathamModi001 if you'd like to check out my projects. Open to connecting if there's an opening.

Best,
Pratham Modi"""
    },
    {
        "Tier": "B",
        "Company": "Atlan",
        "Founder": "Faizan Shaik",
        "Email": "faizan.shaik@atlan.com",
        "Confidence": "Verified",
        "Source": "GitHub commit author",
        "Role Pitch": "Backend & Metadata Platform Engineer",
        "Subject": "Metadata pipelines & backend engineering for Atlan",
        "Notes": "Attached Pratham_Modi_Base_Resume.pdf; highlights C3iHub 75k Kafka events/day and sub-200ms latency",
        "Body": """Hi Faizan,

Saw your work on Atlan's Python SDK on GitHub. Reaching out to ask if your team is hiring backend or data platform engineers.

At C3iHub (IIT Kanpur), I engineered an event-driven notification pipeline handling 75k daily Kafka events at 99.5% reliability and cut database p99 latency from 450ms to 135ms. At Playpower Labs, I built sub-200ms RAG retrieval pipelines.

Resume is attached — happy to connect if you're open to referring or passing my profile along to the engineering manager.

Best,
Pratham Modi"""
    },
    {
        "Tier": "B",
        "Company": "Hasura",
        "Founder": "Brandon Simmons",
        "Email": "brandon@hasura.io",
        "Confidence": "Verified",
        "Source": "GitHub commit author",
        "Role Pitch": "Data Engine & High-Throughput Backend Engineer",
        "Subject": "High-throughput data backends for Hasura",
        "Notes": "Attached Pratham_Modi_Base_Resume.pdf; highlights C3iHub 450ms->135ms latency optimization and Kafka streaming",
        "Body": """Hi Brandon,

Saw your contributions to Hasura's GraphQL engine on GitHub. Reaching out to ask if your team has openings for backend engineers passionate about high-performance data systems.

At C3iHub (IIT Kanpur), I cut database p99 query latency from 450ms to 135ms via indexing and Redis caching, and handled 75k daily Kafka events at 99.5% reliability.

Resume attached — github.com/PrathamModi001 if you'd like to poke around the code. Open to chatting if there is a fit.

Best,
Pratham Modi"""
    },
    {
        "Tier": "B",
        "Company": "BrowserStack",
        "Founder": "Savio Dias",
        "Email": "savio@browserstack.com",
        "Confidence": "Verified",
        "Source": "GitHub commit author",
        "Role Pitch": "Cloud Infrastructure & Testing Platform Engineer",
        "Subject": "MCP & developer infrastructure for BrowserStack",
        "Notes": "Attached Pratham_Modi_Base_Resume.pdf; highlights DeployMind GitOps containerization and C3iHub 99.9% uptime",
        "Body": """Hi Savio,

Saw your commits on BrowserStack's MCP server on GitHub — great to see BrowserStack adopting Model Context Protocol tooling.

At C3iHub (IIT Kanpur), I architected microservices serving 50K+ users with 99.9% uptime and deployed distributed tracing across 15+ services. I also built DeployMind, an autonomous GitOps deployment runtime with Docker and Kubernetes.

Resume is attached — happy to connect if your team is hiring backend or developer infrastructure engineers.

Best,
Pratham Modi"""
    },
    {
        "Tier": "B",
        "Company": "BrowserStack",
        "Founder": "Gaurav Singh",
        "Email": "gaurav.sin@browserstack.com",
        "Confidence": "Verified",
        "Source": "GitHub commit author",
        "Role Pitch": "Backend & Cloud Platform Engineer",
        "Subject": "Re: Developer platform & backend engineering at BrowserStack",
        "Notes": "Attached Pratham_Modi_Base_Resume.pdf; highlights C3iHub 75k Kafka events/day and 50K user scale",
        "Body": """Hi Gaurav,

Saw your engineering work on BrowserStack's MCP and cloud test runners. Reaching out to see if your team has backend openings.

At C3iHub (IIT Kanpur), I engineered an event-driven notification engine handling 75k daily Kafka events at 99.5% delivery and built microservices supporting 10,000+ concurrent connections.

Resume is attached — happy to jump on a quick call or share more details if you're open to referring my profile.

Best,
Pratham Modi"""
    },
    {
        "Tier": "B",
        "Company": "Postman",
        "Founder": "Ayush Shrivastav",
        "Email": "ayush.shrivastav@postman.com",
        "Confidence": "Verified",
        "Source": "GitHub commit author",
        "Role Pitch": "API Platform & Backend Software Engineer",
        "Subject": "API tooling & backend engineering for Postman",
        "Notes": "Attached Pratham_Modi_Base_Resume.pdf; highlights C3iHub 50K users at 99.9% uptime and sub-200ms RAG pipelines",
        "Body": """Hi Ayush,

Saw your contributions to Postman's openapi-to-postman parser on GitHub. Reaching out to ask if Postman's backend or API platform teams are hiring.

At C3iHub (IIT Kanpur), I architected microservices serving 50K+ users at 10,000+ concurrent connections and cut database p99 query latency from 450ms to 135ms. At Playpower Labs, I developed FastAPI microservices and sub-200ms RAG pipelines.

Resume is attached — github.com/PrathamModi001. Open to connecting if there's a fit.

Best,
Pratham Modi"""
    },
    {
        "Tier": "B",
        "Company": "Postman",
        "Founder": "Shubhi Srivastava",
        "Email": "shubhi.srivastava@postman.com",
        "Confidence": "Verified",
        "Source": "GitHub commit author",
        "Role Pitch": "Backend & Developer Tooling Engineer",
        "Subject": "Quick note re: Postman backend engineering",
        "Notes": "Attached Pratham_Modi_Base_Resume.pdf; highlights C3iHub Kafka event pipelines and 15+ service tracing",
        "Body": """Hi Shubhi,

Saw your work on OpenAPI tools at Postman on GitHub. Reaching out to ask if your team is exploring backend engineering talent.

At C3iHub (IIT Kanpur), I built an event-driven notification engine handling 75k daily Kafka events at 99.5% delivery and deployed distributed tracing across 15+ services with OpenTelemetry.

Sending my resume along — happy to connect if you're open to referring or passing my profile along.

Best,
Pratham Modi"""
    },

    # --- 10 Global / HN / YC Startups (Founders & Team Leads) ---
    {
        "Tier": "B",
        "Company": "Twenty",
        "Founder": "Felix Vemmer",
        "Email": "felix@twenty.com",
        "Confidence": "Verified",
        "Source": "GitHub / Open Source",
        "Role Pitch": "Backend Engineer (CRM Architecture)",
        "Subject": "Backend engineering for Twenty's open-source CRM architecture",
        "Notes": "Attached Pratham_Modi_Base_Resume.pdf; highlights C3iHub 75k Kafka events/day and sub-200ms RAG pipelines",
        "Body": """Hi Felix,

Saw Twenty's modular architecture and open-source CRM momentum on GitHub.

At C3iHub (IIT Kanpur), I architected an event-driven notification pipeline handling 75k daily Kafka events at 99.5% reliability with consumer-side deduplication. At Playpower Labs, I built sub-200ms RAG retrieval pipelines over vector storage.

Resume is attached — GitHub is github.com/PrathamModi001 if you want to poke around the code. Open to chatting if there's a fit for backend engineering at Twenty.

Best,
Pratham Modi"""
    },
    {
        "Tier": "B",
        "Company": "Svix",
        "Founder": "Tom Hacohen",
        "Email": "tom@svix.com",
        "Confidence": "Verified",
        "Source": "Founder bio / YC",
        "Role Pitch": "High-Throughput Webhook Infrastructure Engineer",
        "Subject": "High-throughput webhook delivery pipelines for Svix",
        "Notes": "Attached Pratham_Modi_Base_Resume.pdf; highlights C3iHub 75k daily Kafka events with deduplication",
        "Body": """Hi Tom,

Following Svix's focus on enterprise webhook delivery and reliability.

At C3iHub (IIT Kanpur), I built an event-driven notification engine handling 75k daily Kafka events at 99.5% reliability with consumer-side deduplication and dead-letter queues. At Playpower Labs, I developed microservices maintaining sub-100ms response times.

Resume is attached — github.com/PrathamModi001 if you want more detail. Open to chatting if there's a fit for Svix.

Best,
Pratham Modi"""
    },
    {
        "Tier": "B",
        "Company": "Knock",
        "Founder": "Chris Bell",
        "Email": "chris@knock.app",
        "Confidence": "Verified",
        "Source": "Founder bio",
        "Role Pitch": "Notification Infrastructure & Distributed Systems Engineer",
        "Subject": "Notification delivery engines & event routing for Knock",
        "Notes": "Attached Pratham_Modi_Base_Resume.pdf; direct match with Kafka event pipelines and 99.5% delivery",
        "Body": """Hi Chris,

Admiring Knock's cross-channel notification orchestration and developer experience.

At C3iHub (IIT Kanpur), I engineered an event-driven notification pipeline handling 75k daily Kafka events at 99.5% reliability with consumer-side deduplication, BullMQ, and Redis Pub/Sub. I also cut database p99 query latency from 450ms to 135ms.

Sending my resume along — happy to jump on a quick call if useful.

Best,
Pratham Modi"""
    },
    {
        "Tier": "B",
        "Company": "Trigger.dev",
        "Founder": "James Perkins",
        "Email": "james@trigger.dev",
        "Confidence": "Verified",
        "Source": "YC / GitHub",
        "Role Pitch": "Background Job Orchestration & Backend Engineer",
        "Subject": "Background job execution runtimes for Trigger.dev",
        "Notes": "Attached Pratham_Modi_Base_Resume.pdf; highlights C3iHub Kafka event pipelines and DeployMind GitOps execution",
        "Body": """Hi James,

Following Trigger.dev's v3 rollout and serverless background job orchestration.

At C3iHub (IIT Kanpur), I architected microservices serving 50K+ users at 10,000+ concurrent connections and managed event streams over Kafka and Redis. I also built DeployMind, an autonomous GitOps deployment runtime with Docker and Kubernetes.

Resume attached — github.com/PrathamModi001 if you want to poke around the code. Open to chatting if there's a fit.

Best,
Pratham Modi"""
    },
    {
        "Tier": "B",
        "Company": "Linear",
        "Founder": "Karri Saarinen",
        "Email": "karri@linear.app",
        "Confidence": "Verified",
        "Source": "Founder bio",
        "Role Pitch": "Sync Engine & Low-Latency Backend Engineer",
        "Subject": "Real-time sync engines & backend engineering for Linear",
        "Notes": "Attached Pratham_Modi_Base_Resume.pdf; highlights C3iHub 2,000+ WebSocket concurrency and 450ms->135ms latency reduction",
        "Body": """Hi Karri,

Long-time admirer of Linear's craft, real-time sync architecture, and client-side performance.

At C3iHub (IIT Kanpur), I built a real-time collaborative round engine handling 2,000+ concurrent WebSocket sessions with idempotent, race-condition-safe state synchronization, and cut database query latency from 450ms to 135ms.

Resume's attached — github.com/PrathamModi001. Worth a quick chat if Linear is adding backend engineers?

Best,
Pratham Modi"""
    },
    {
        "Tier": "B",
        "Company": "Warp",
        "Founder": "Zach Lloyd",
        "Email": "zach@warp.dev",
        "Confidence": "Verified",
        "Source": "Founder bio",
        "Role Pitch": "Cloud Infrastructure & Backend Systems Engineer",
        "Subject": "Backend systems & developer loops for Warp",
        "Notes": "Attached Pratham_Modi_Base_Resume.pdf; highlights C3iHub 50K users at 99.9% uptime and OpenTelemetry tracing",
        "Body": """Hi Zach,

Following Warp's terminal innovations and AI workflows with great interest.

At C3iHub (IIT Kanpur), I architected core microservices serving 50K+ users with 99.9% uptime and standardized OpenTelemetry distributed tracing across 15+ services, cutting MTTR by 85%. At Playpower Labs, I built sub-200ms AI retrieval pipelines.

Resume attached — github.com/PrathamModi001 if you want to poke around. Open to connecting if there's a fit.

Best,
Pratham Modi"""
    },
    {
        "Tier": "B",
        "Company": "Decagon",
        "Founder": "Jesse Zhang",
        "Email": "jesse@decagon.ai",
        "Confidence": "Verified",
        "Source": "Founder bio",
        "Role Pitch": "Agent Execution & AI Platform Engineer",
        "Subject": "Agentic runtimes & low-latency backends for Decagon",
        "Notes": "Attached Pratham_Modi_Base_Resume.pdf; highlights Playpower Labs sub-200ms RAG and Mnemoniq LangGraph agent",
        "Body": """Hi Jesse,

Seeing Decagon's impressive expansion in enterprise customer-service AI agents.

At Playpower Labs, I engineered low-latency RAG pipelines delivering sub-200ms retrieval across 10K+ documents. I also built Mnemoniq, an autonomous multi-tier memory agent orchestrated with LangGraph, cutting token overhead by 38%. At C3iHub, I scaled event pipelines over Kafka.

Resume is attached — happy to jump on a quick call if useful.

Best,
Pratham Modi"""
    },
    {
        "Tier": "B",
        "Company": "Sidekick Labs",
        "Founder": "Founding Team",
        "Email": "hn@sidekicklabs.com",
        "Confidence": "Verified",
        "Source": "HN (id: 49922569)",
        "Role Pitch": "Backend & AI Infrastructure Engineer",
        "Subject": "AI execution backends & async pipelines for Sidekick Labs",
        "Notes": "Attached Pratham_Modi_Base_Resume.pdf; highlights C3iHub 75k Kafka events/day and sub-200ms RAG pipelines",
        "Body": """Hi Team,

Saw your post on HN for Sidekick Labs — building AI infrastructure and high-concurrency developer workflows.

At C3iHub (IIT Kanpur), I engineered a notification engine handling 75k daily Kafka events at 99.5% reliability and cut database p99 latency from 450ms to 135ms. At Playpower Labs, I built sub-200ms RAG retrieval pipelines.

Resume's attached — github.com/PrathamModi001. Open to chatting if there's a fit for Sidekick Labs.

Best,
Pratham Modi"""
    },
    {
        "Tier": "B",
        "Company": "Datamint",
        "Founder": "Engineering Team",
        "Email": "jobs@datamint.xyz",
        "Confidence": "Verified",
        "Source": "HN (id: 49922569)",
        "Role Pitch": "Extraction Infrastructure & Backend Engineer",
        "Subject": "Structured extraction pipelines & backend scale for Datamint",
        "Notes": "Attached Pratham_Modi_Base_Resume.pdf; highlights C3iHub 75k daily Kafka events and 450ms->135ms latency reduction",
        "Body": """Hi Team,

Saw your HN post for Datamint — building structured extraction pipelines for AI models.

At C3iHub (IIT Kanpur), I built an event-driven notification engine handling 75k daily Kafka events at 99.5% reliability and optimized indexing to cut MongoDB p99 latency from 450ms to 135ms. At Playpower Labs, I engineered sub-200ms document retrieval pipelines.

Sending my resume along — happy to jump on a quick call if useful.

Best,
Pratham Modi"""
    },
    {
        "Tier": "B",
        "Company": "Vistulo",
        "Founder": "Founding Team",
        "Email": "contact@vistulo.com",
        "Confidence": "Verified",
        "Source": "HN (id: 49922569)",
        "Role Pitch": "Backend & Event-Driven Systems Engineer",
        "Subject": "Event-driven backends & microservices for Vistulo",
        "Notes": "Attached Pratham_Modi_Base_Resume.pdf; highlights C3iHub 50K users at 99.9% uptime and Kafka pipelines",
        "Body": """Hi Team,

Saw your engineering post on HN for Vistulo.

At C3iHub (IIT Kanpur), I architected microservices serving 50K+ users at 10,000+ concurrent connections and managed event streams over Kafka. At Playpower Labs, I developed microservices maintaining sub-100ms response times.

Resume is attached — github.com/PrathamModi001. Open to chatting if there's a fit.

Best,
Pratham Modi"""
    }
]

# Append to startups_outreach.csv
fieldnames = [
    "Company", "Founder", "Email", "Confidence", "Role Pitch",
    "Subject", "Status", "Drafted Date", "Notes", "Source", "Tier"
]

added_count = 0
with open(csv_path, "a", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    for t in today_targets:
        if t["Email"].lower() not in existing_emails:
            writer.writerow({
                "Company": t["Company"],
                "Founder": t["Founder"],
                "Email": t["Email"],
                "Confidence": t["Confidence"],
                "Role Pitch": t["Role Pitch"],
                "Subject": t["Subject"],
                "Status": "Drafted",
                "Drafted Date": "2026-10-14",
                "Notes": t["Notes"],
                "Source": t["Source"],
                "Tier": t["Tier"]
            })
            existing_emails.add(t["Email"].lower())
            added_count += 1

print(f"Logged {added_count} new outreach rows to {csv_path}")

# Write send_drafts.html with one-click compose links
cards_html = []
import urllib.parse

for i, t in enumerate(today_targets, 1):
    su_enc = urllib.parse.quote(t["Subject"])
    b_enc = urllib.parse.quote(t["Body"])
    to_enc = urllib.parse.quote(t["Email"])
    gmail_url = f"https://mail.google.com/mail/?view=cm&fs=1&to={to_enc}&su={su_enc}&body={b_enc}"
    
    badge_cls = "verified" if t["Confidence"] == "Verified" else "guessed"
    card = f"""<div class="card">
  <h3>{i}. {t['Company']} &nbsp;<span class="badge {badge_cls}">{t['Confidence']}</span> &nbsp;<span style="font-size:12px;color:#94a3b8;">({t['Source']})</span></h3>
  <p><strong>To:</strong> <code>{t['Email']}</code> ({t['Founder']})</p>
  <p><strong>Subject:</strong> {t['Subject']}</p>
  <p><strong>Role Pitch:</strong> {t['Role Pitch']}</p>
  <div style="background:#0f172a;padding:12px;border-radius:6px;font-size:13px;white-space:pre-wrap;margin-top:8px;">{t['Body']}</div>
  <a class="btn" href="{gmail_url}" target="_blank">✉️ Open Draft in Gmail Web Composer</a>
</div>"""
    cards_html.append(card)

html_content = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Cold Outreach Gmail Drafts (2026-10-14)</title>
<style>
body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; margin: 30px; background: #0f172a; color: #f8fafc; }}
h1, h2 {{ color: #38bdf8; }}
.card {{ background: #1e293b; border-radius: 8px; padding: 18px; margin-bottom: 16px; border: 1px solid #334155; }}
.btn {{ display: inline-block; background: #2563eb; color: #fff; padding: 8px 16px; text-decoration: none; border-radius: 6px; font-weight: 600; margin-top: 10px; }}
.btn:hover {{ background: #1d4ed8; }}
.badge {{ display: inline-block; padding: 3px 8px; border-radius: 4px; font-size: 12px; font-weight: bold; }}
.verified {{ background: #065f46; color: #34d399; }}
.guessed {{ background: #854d0e; color: #fde047; }}
code {{ background: #0f172a; padding: 2px 6px; border-radius: 4px; color: #e2e8f0; }}
</style>
</head>
<body>
<h1>20 Staged Cold Outreach Drafts (2026-10-14)</h1>
<p><strong>Base Resume to Attach:</strong> <code>E:\\Extra\\job-kit-starter\\job-kit-starter\\output\\Pratham_Modi_Base_Resume.pdf</code></p>
<p>10 Global Startups + 10 Indian Engineering Targets (Engineers / Leads)</p>
<hr style="border: 1px solid #334155; margin: 20px 0;">
{"".join(cards_html)}
</body>
</html>
"""

html_path.write_text(html_content, encoding="utf-8")
print(f"Wrote {html_path}")
