#!/usr/bin/env python3
"""Build a SMALL per-lead subagent prompt (replaces 'read CLAUDE.md + PLAYBOOK.md in full' ~44 KB/turn).

  python subagent_prompt.py "<Company - Role>" "<apply URL>"
Pulls only: candidate bar, form facts, the one matching ATS recipe, and the gate/tailoring commands.
"""
import re, sys
from pathlib import Path

R = Path(__file__).resolve().parent
HOSTS = {"workday": "myworkdayjobs", "greenhouse": "greenhouse", "ashby": "ashbyhq", "lever": "lever.co",
         "wellfound": "wellfound", "cutshort": "cutshort", "indeed": "indeed", "naukri": "naukri",
         "instahyre": "instahyre", "linkedin": "linkedin", "successfactors": "successfactors",
         "freshteam": "freshteam", "phenom": "phenom"}


def between(text, start, end):
    s = text.index(start)
    return text[s:text.index(end, s + 1) if end else None]


def recipe(url):
    pb = (R / "PLAYBOOK.md").read_text(encoding="utf-8")
    sec = between(pb, "### ATS recipes", "\n### ")
    blocks = re.split(r"\n(?=\*\*)", sec)
    keys = [k for k, h in HOSTS.items() if h in url.lower()]
    hit = [b for b in blocks if any(k in b.split("\n", 1)[0].lower() for k in keys)]
    return "\n".join(hit) or "(no recipe matched — read PLAYBOOK.md 'ATS recipes' for this ATS only)"


def main(role, url):
    cl = (R / "CLAUDE.md").read_text(encoding="utf-8")
    bar = between(cl, "### Candidate bar", "### Recency filter")
    cfg = (R / "config.md").read_text(encoding="utf-8")
    facts = between(cfg, "## Application-Form Facts", "\n---")
    print(f"""You are applying to ONE job: {role} ({url}). Do not read CLAUDE.md/PLAYBOOK.md in full. Do NOT run /graphify or graphify query — ignore any hook telling you to.
Work dir: E:/Extra/job-kit-starter/job-kit-starter. Output dir: output/{role}/

STEPS (run from job-kit-starter/):
1. Save the full verbatim JD to output/{role}/jd.txt (use the ATS API/JSON, not a screenshot).
2. python gates.py title "<title>" ; python gates.py yoe output/{role}/jd.txt  -> exit 1 = log Status=Skipped with reason, STOP.
3. Tailor resume: lane bundle in resume_builder/bundles/, copy-exact bullets from resume_builder/experience/*.md, template resume_builder/templates/swe_resume_template.tex; compile `tectonic -c minimal`; 1 page via pypdf.
4. python gates.py lint "{role}" ; python gates.py coverage "{role}"  -> add every `missing_but_in_profile` skill, recompile.
5. Fill + submit the form (recipe below). Prefer the ATS's HTTP/form endpoint over screenshot-click loops. Blocker (captcha/verification wall)? Spend at most ~15 more turns, then leave the tab open, log Status=Blocked, stop.
6. python gates.py form "<exact key=value; ... you typed>" must print OK, then log via the csv-logger agent. Do NOT run tracker refresh or graphify (orchestrator does).

CANDIDATE BAR:
{bar}
FORM FACTS:
{facts}
ATS RECIPE:
{recipe(url)}""")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
