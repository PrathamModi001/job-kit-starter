# 👋 Start here

This is a complete AI-driven job-search kit for **Claude Code**. A friend ran his whole
campaign with it — 90+ tailored applications across Workday/SuccessFactors/Naukri/
Instahyre/Cutshort/company sites, 50+ cold emails, cold X DMs to founders, and a live
public tracker — with Claude doing nearly everything.

## What you need installed

1. **Claude Code** — https://claude.com/claude-code (the terminal app or desktop app)
2. **Playwright MCP** for Claude Code (browser automation — this is how Claude fills
   application forms). In Claude Code run: `claude mcp add playwright -- npx @playwright/mcp@latest`
3. **Python 3** with: `pip install pypdf python-jobspy`
4. **tectonic** (LaTeX compiler for resumes) — https://tectonic-typesetting.github.io
5. Optional but very useful: connect the **Gmail** connector in Claude Code
   (email verification links, cold-email drafts), and **Node.js** if you want the
   public tracker (Cloudflare Pages, free).

## How to start (2 minutes)

```bash
cd job-kit-starter
claude
```

Then just say:

> **"Set me up."**

Claude will detect the fresh kit, interview you (contact info, your job-search bar,
your resume/background, the facts forms always ask for), and write all the config
itself. Don't hand-edit anything.

After setup:
- Paste any job description → Claude tells you if it's worth it and tailors your resume.
- Say **"do the daily scan"** → Claude hunts across HN, ~90 startup ATS boards,
  Indeed/LinkedIn, and your job-platform feeds, and triages everything against your bar.
- Say **"apply to <company>"** → Claude fills the whole application (any ATS) and
  submits with your approval.
- Read `PLAYBOOK.md` if you're curious how everything works under the hood.

## Two rules that keep this safe and honest

1. **Claude never submits/sends anything without you naming the recipient.** You stay
   in control of every application, email, and DM.
2. **Everything on your resume must be true.** The kit's #1 rule is
   Accuracy > Relevance > Impact. Claude will refuse to inflate numbers — that's a
   feature.

Good hunting. 🎯
