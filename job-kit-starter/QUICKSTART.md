# Quickstart

You don't set this up by hand — **Claude does it for you.** You just talk to it.

## 1. Install the prerequisites (one-time)

- **[Claude Code](https://docs.anthropic.com/en/docs/claude-code)** — the CLI this kit runs in.
- **git** and **python3** (already on most Macs/Linux).
- **[tectonic](https://tectonic-typesetting.github.io/)** — compiles resumes to PDF. Mac: `brew install tectonic`.
- Optional Python bits (Claude will tell you if/when you need them):
  ```bash
  pip install pypdf            # resume verification
  pip install python-jobspy    # only for job_hunt_india.py
  ```

## 2. Open the kit in Claude Code

```bash
git clone <repo-url> claude-job-kit    # or unzip the folder
cd claude-job-kit
claude                                  # start Claude Code here
```

## 3. Say hi

That's it. Claude auto-loads the rules and, on a fresh kit, **offers to set you up**. If it doesn't greet you first, just say:

> **"Help me get set up."**

It will then:
- ask for your basics and fill in `config.md`
- ask about your job criteria (location, comp floor, level, target companies) and write your "bar"
- ask you to **paste your current resume** (or just talk through your background) and build your master profile

You answer questions in chat. Claude writes every file. No manual editing.

## 4. Start applying

Once set up:

> **"Here's a job description [paste link or text]. Worth applying to? If yes, tailor my resume."**

Claude judges it against your bar, tailors your resume, drafts the application, and can even fill web forms — but it **always stops before submitting.** You review and send every application yourself.

That's the only rule that never changes: **Claude prepares everything, you click send.**

---

Want the full picture? See [`docs/claude-code-for-job-search.md`](docs/claude-code-for-job-search.md) and the [README](README.md).
