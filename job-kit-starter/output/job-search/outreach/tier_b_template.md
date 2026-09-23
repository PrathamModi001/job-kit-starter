# Tier B cold email — slot template (volume lane)

Used for the 20-30/day volume tier. Tier A (3-5/day, fully bespoke) stays as-is —
see PLAYBOOK.md Phase 4.

## Why a template at all
Fully bespoke writing doesn't scale past ~5/day. A fixed skeleton with a few
research-backed slots gets close to Tier A quality per-email in a fraction of the
time, while staying far from "Dear Founder, I love what you're doing" fluff.

## Sounding human, not generated
Apply `resume_builder/support/ai_fingerprint_rules.md`'s Tier 1 banned-word list here too (delve, leverage/leveraged, robust-as-filler, showcase, seamless, etc.) — it's written for resumes but the same "does this read like a real person typed it" bar applies to `{HOOK}` and `{CLOSER}`. Also avoid template-variable-sounding adjectives even if not on that list — "tailored," "pinned," "curated" — anything that reads like a slot got filled in rather than written.

## Slots (fill from a 2-minute lookup per company, never invent)
- `{HOOK}` — one sentence tied to something real and specific about them: their HN
  post text, a changelog/launch post, a funding headline, their product page. Never
  generic ("I love your mission").
- `{METRIC_A}` / `{METRIC_B}` — pick 2 from the pre-approved pool below that best
  mirror their stack/problem. Do not mix-and-match facts across roles.
- `{COMPANY}` — exact name as they use it.

## Pre-approved metric pool (grounded in SKILL_PROFILE.md — pick, never paraphrase numbers)
- C3iHub: notification engine handling 75k daily Kafka events at 99.5% reliability
- C3iHub: cut MongoDB p99 latency from 450ms to 135ms
- Playpower Labs: sub-200ms RAG pipelines
- Playpower Labs: 35% token reduction on LLM pipeline
(Extend this list only by copying verbatim from `experience/*.md` — never write a new number here.)

## Body skeleton (75-100 words, plain text, no HTML/tracking links)
```
Subject: <pick one of the subject variants below — never repeat the same subject twice in a batch>

{HOOK}

At {METRIC_A_COMPANY}, I {METRIC_A}. At {METRIC_B_COMPANY}, I {METRIC_B}.

{CLOSER}

Pratham
```
- **`{CLOSER}`** — vary this per email, don't reuse the same sentence across a batch (a fixed closing line is as much of a spam/AI tell as a fixed subject). Keep it short, plain, and resume-forward without sounding like a form letter. Rotate/adapt from, e.g.:
  - "Resume's attached — github.com/PrathamModi001 if you want more detail. Worth a quick chat about {COMPANY}?"
  - "Sending my resume along — happy to jump on a quick call if useful."
  - "Resume attached. GitHub's github.com/PrathamModi001 if you want to poke around the code. Open to chatting if there's a fit."
  - Or write a fresh one-liner that fits the tone of `{HOOK}` — do not default to "Attached my resume" or any phrasing that reads like a template variable being filled in ("tailored", "pinned", "leveraged", etc.) — write it the way a person would actually type it.

## Subject line variants (rotate — identical subjects across a batch is a spam-clustering signal)
- "Backend engineer for {COMPANY}'s <their specific problem>"
- "{HOOK topic} — quick note from a backend engineer"
- "Re: {COMPANY}'s <launch/post title>"
- "10 min re: {COMPANY} backend hiring"

## Volume + deliverability rules
- **Always attach the base resume — exact path: `output/Pratham_Modi_Base_Resume.pdf`.** Same file every time, never a per-company tailored variant. Draft via the Gmail connector's `create_draft` with the PDF base64-encoded into `attachments` — the Gmail URL-compose pattern can't carry an attachment, so don't use it here unless you then manually attach the file before the draft counts as done.
- Hard cap: 20-30 Tier B drafts/day, on top of the 3-5 Tier A. Stage as Gmail
  drafts only — user sends, per CLAUDE.md outbound policy (never auto-send).
- No two bodies in a batch may be byte-identical — the `{HOOK}` and metric choice
  must vary per company even if the skeleton repeats.
- Plain text only (no images, no tracking pixels, no shortened links) — reduces
  spam-filter risk on a personal Gmail account.
- Source diversity for volume: HN "Who is hiring?" (`hn_scan.py`, now extracts
  emails per match), funding-news/YC-batch research, WaaS index, founder posts —
  don't pull 30 leads from one channel in a day.

## Tracking
Every Tier B send goes into `output/job-search/outreach/startups_outreach.csv`
(the same canonical file as Tier A) with `Tier=B` and `Source=<HN|Funding News|WaaS|...>`
so volume and response rate are visible across tiers, not siloed.
