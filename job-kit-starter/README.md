# claude-job-kit

An AI-run job-search kit for Claude Code: two subsystems that work together.

1. **Resume/CV generation** (`resume_builder/`) — extract your source material once (papers,
   code, reports), then generate tailored, accuracy-checked LaTeX resumes per job description.
2. **The daily job-search loop** (find → triage → apply → track → outreach) — company-board
   scanners (`job_hunt.py`, `job_hunt_india.py`, `hn_scan.py`, `waas_scan.py`), a CSV tracker,
   and per-ATS auto-apply/outreach recipes.

**This kit is operated by Claude Code, not read by a human step-by-step.** `CLAUDE.md` is the
canonical, auto-loaded source of truth for rules (candidate bar, auth, submission policy,
resume-tailoring gate). `PLAYBOOK.md` is the full operational manual (scans, ATS recipes,
outreach). Read those two files before anything nontrivial — this README is just a map.

---

## Prerequisites

- **[Claude Code](https://docs.anthropic.com/en/docs/claude-code)** CLI, authenticated
- **Playwright MCP**: `claude mcp add playwright -- npx @playwright/mcp@latest`
- **Python 3** with `pip install pypdf python-jobspy`
- **tectonic** (LaTeX compiler): https://tectonic-typesetting.github.io
- Optional: Gmail connector (cold-email drafts, verification links), Node.js (public tracker)

## Start here

Open the folder in Claude Code and say "set me up." On a fresh kit, Claude detects
placeholder values in `config.md` / `SKILL_PROFILE.md` and interviews you to fill in:
contact info, your candidate bar (location/comp/level/stack), and your master profile
(`SKILL_PROFILE.md`). See `CLAUDE.md` → "First-run onboarding" for the exact flow.

After setup:
- Paste a job description → Claude judges it against your bar and tailors a resume.
- Say "do the daily scan" → runs the full loop in `.agents/workflows/daily_scan.md`.
- Say "apply to `<company>`" → tailors resume, fills the ATS form, stops before Submit
  unless the lead already cleared auto-submit rules in `CLAUDE.md`.

## File map

```
CLAUDE.md                  # canonical rules — auto-loaded, read first
PLAYBOOK.md                # full operational manual (scans, ATS recipes, outreach)
config.md                  # personal configuration (contact, provenance, preferences)
SKILL_PROFILE.md           # master brag-doc — single source of truth for resume facts
.claude/skills/            # setup-extract, setup-build-kb, make-resume, make-cl, edit-resume, critique
.claude/agents/csv-logger.md   # async CSV writer — delegate all applications.csv edits here
.agents/rules/              # fast-reference summaries that point back to CLAUDE.md/PLAYBOOK.md
.agents/workflows/          # daily_scan.md — the full autonomous hunt→apply→track loop
resume_builder/             # reference docs, LaTeX templates, helpers, examples; see DOCS.md
knowledge_base/             # your raw materials (papers/, notes/, extractions/)
job_hunt.py / job_hunt_india.py / hn_scan.py / waas_scan.py   # board scanners (seen-index dedup)
tracker/                    # React + Cloudflare Pages public application tracker (refresh.sh)
output/job-search/applications.csv   # THE source of truth for every lead/application
```

## Resume/CV generation quick reference

| Skill | Purpose | Input | Output |
|-------|---------|-------|--------|
| `/setup-extract` | Extract structured data from a paper | Paper path | `knowledge_base/extractions/*.md` |
| `/setup-build-kb` | Build KB from extractions | All extractions | `resume_builder/{experience,bundles,support}/` |
| `/make-resume` | Generate tailored resume or CV | JD path | `output/<Folder>/e2e_*.tex` + session file |
| `/make-cl` | Generate matching cover letter | Session file | `output/<Folder>/*_cover_letter.tex` |
| `/edit-resume` | Edit resume/CV/CL from feedback | Session + feedback | Updated `.tex` files |
| `/critique` | Independent quality review | Session file | `output/<Folder>/critique_*.md` |

For architecture details, session-file/bundle/critique internals, and customization tables,
see [DOCS.md](DOCS.md).

## License

MIT — see [LICENSE](LICENSE).
