# PLAYBOOK — the full job-search campaign, end to end

> This is the operational manual, distilled from a real 90+ application campaign run
> entirely through Claude Code. It tells Claude (you, the agent reading this) exactly
> what to do at every phase and records every hard-won automation quirk so you don't
> re-learn them. CLAUDE.md holds the rules; this holds the HOW.
>
> Prereq for almost everything here: the **Playwright MCP** browser. The user logs into
> job platforms in that browser once; you drive it afterwards.

---

## Phase 0 — Setup (first session)

1. Run the onboarding in CLAUDE.md: fill `config.md`, the Candidate bar, `SKILL_PROFILE.md`, and the application-form facts.
2. Build the **base resume**: use `/make-resume` against a representative JD in the user's lane. Keep the resulting `.tex` as the BASE for all variants (see "Resume variant system" below).
3. Verify the toolchain: `tectonic -c minimal` compiles, `pypdf` imports, `python3 job_hunt.py` runs.
4. Ask the user to log into their job platforms in the Playwright browser (one at a time, as needed).

## Phase 1 — Platform profiles (do these early; they compound)

Set up strong profiles on the user's regional platforms (in India: Naukri, Instahyre, Cutshort; elsewhere: the local equivalents + Wellfound/LinkedIn everywhere). For each:
- Upload the freshly built resume PDF, fix headline to a keyword-rich one-liner, correct employment history (titles/dates/company names), set true skills (delete junk auto-added skills), set comp + notice period + preferred locations.
- These profiles power (a) match-feeds you scan daily and (b) auto-answered recruiter questionnaires (Cutshort's "Voila" bot answers location/notice/comp screeners from the profile — get the profile right and screeners handle themselves).

## Phase 2 — Daily scan (say "do the daily scan")

All sources are capped to postings from the **last 7 days** (see CLAUDE.md "Recency filter") — older leads never reach the digest, so there's no need to manually date-check results.

Sources, in order:
1. `python3 hn_scan.py` — HN Who is Hiring (seen-index; CSV-deduped; always the latest thread).
2. `python3 job_hunt.py` — ~90 ATS boards, last 7 days (`--days N` to widen). Edit the company list in the script to the user's targets.
3. `python3 job_hunt_india.py` — JobSpy over Indeed+LinkedIn, last 7 days (`hours_old`, arg 1). Edit queries/location for the user.
4. Browser feeds via Playwright:
   - Match-feed platforms (e.g., Instahyre `candidate/opportunities/?matching=true`): scroll-collect all cards, diff vs. previously seen + CSV.
   - Naukri-style search with `jobAge=1` (last 24h) for "backend engineer" / "[lane] engineer" in the user's city.
   - Cutshort-style matches page (`/profile/all-jobs?matchesfor=<id>` — the ID is in the user's profile URL).
5. Triage EVERYTHING against the Candidate bar. Present a short table: lead / source / why. Skip-noise honestly (services firms, below-floor bands, wrong level, region-locked). Log genuinely good leads to the CSV via csv-logger (Status=Lead), then refresh the tracker.

Expect diminishing returns after the first week — fresh supply at one level/city is finite. When scans go quiet, the highest-value work moves to reply-checking and outreach.

## Phase 3 — Applying (auto-submit allowed once a lead clears the bar; see CLAUDE.md top rule)

### Resume variant system
- ONE base `.tex` (backend or whatever the user's core lane is). For each application lane, copy it and swap ONLY the header tagline + summary paragraph (keep every fact identical). Typical variants: backend base / AI-engineer / fullstack.
- Every variant: compile with `tectonic -c minimal`, assert 1 page via pypdf, grep extracted text for the load-bearing facts, copy as `<Name>_Resume.pdf` into `output/<Company> - <Role>/`.
- The `resume.cls` must sit next to the `.tex` when compiling (copy it into each folder).

### Where the Apply button leads (triage on click)
- **Native platform apply** (Naukri "Apply", Instahyre modal, Cutshort modal): 1-30 seconds each. Do these first.
- **"Apply on company site"** → an ATS. Identify it from the URL and use the recipe below.
- A stale listing may 404 on the company site → check the company's board for a live equivalent; if none, mark the lead Closed with the reason.

### ATS recipes (every quirk here was hit in production)

**Workday** (`<company>.wd<N>.myworkdayjobs.com`) — the big one; expect 15-30 min each:
- Flow: Apply → "Autofill with Resume" → Create Account (email + `<Company>Apply#<year><initials>` password — SAVE to `output/<Company> - <Role>/account_credentials.txt`) → 5-7 steps.
- Some tenants require **email verification** before sign-in (fetch the activation link from the user's Gmail via the Gmail connector). Some report "account exists, admin requires password reset" — do Forgot Password → fetch the reset link from Gmail → set new password.
- **Autofill is buggy, always verify**: it routinely puts a resume section header as Company ("AI API & Model-Serving Infrastructure" instead of the employer) and garbage in City (literally "Engineer"). Fix every field.
- Date fields are **spinbuttons**: focus via JS then `page.keyboard.type('10')` — locator.fill fails.
- Dropdown buttons (`aria-haspopup="listbox"`): click, then **type-ahead + Enter** ("Karn"→Karnataka, "Mob"→Mobile, "Bach"→Bachelor's). CAUTION: type-ahead picks the FIRST prefix match — "Bach"+Enter can land on "Bachelor of Commerce". For precision, list visible `[role="option"]` texts and mouse-click the exact one by coordinates.
- Source ("How did you hear") is often a **category tree** (Job Board → Naukri/Indeed/...). Clicks on options sometimes silently fail — the reliable fallback is **keyboard**: ArrowDown until the target is highlighted, Enter to expand/select. If the exact source doesn't exist, pick the closest truthful option ("Jobboard Other", "Careers Site → Job Site") — never a false one.
- **Selecting a dropdown option can wipe unsaved text fields** (re-render). After picking dropdowns, re-verify every text field before hitting Next.
- Virtualized long lists (countries, fields of study) don't filter on typing on some tenants: find the scrollable ancestor of a `promptOption`, jump `scrollTop` to the alphabetical fraction (C≈12-15%, I≈38-40%), then micro-step ±100-120px until the target renders. Watch out: some lists render entries doubled.
- Watch for **hidden required fields** with no visible error until submit: Prefix (Mr./Ms.), mandatory Date of Birth / Citizenship / Gender on some tenants (JioStar-style). Citizenship may be a tree: "India" expands to "Citizen (India)".
- If a school/institution picker's search returns "No Items." for everything (broken tenant DB), the education block may be undeletable-required → put education facts in the role description + rely on the resume PDF, and if you added an optional education block you can't complete, delete THAT block (find its Delete button by y-proximity to the "Education 1" header — a naive ancestor-walk can delete the WRONG section).
- Application Questions: answer truthfully from the form facts. Trade-control/sanctions questions cascade one at a time — loop until the step advances. "Next" only advances when every question on the page is answered; no visible error ≠ no problem — enumerate `button[id*=Questionnaire]` still showing "Select One".
- Verify submission: URL becomes `/jobTasks/completed/application` or Candidate Home shows the req with a status. Log the req ID.

**SAP SuccessFactors** (`career<N>.sapsf.com`, Gigya registration):
- Register via "Don't have an account yet?": country select is `select[name="profile.country"]` (set by value, e.g. IN), fields need REAL typing (`pressSequentially`) — JS value-setting fails validation.
- CRITICAL: multiple copies of the form exist in DOM; the LIVE one is inside `#gigya-register-screen`. Fill THAT one.
- The privacy-consent checkbox is disabled until the statement link is clicked.
- Some tenants force **TOTP 2FA at signup**: the page shows the secret (input[name=secret]) — read it, compute the 6-digit code locally (`python: hmac+base32, SHA1, 30s`), SAVE THE SECRET in the credentials file and tell the user to add it to their authenticator.
- Attachment upload: the clickable is the plus icon (`[id$="_attachIcon"]`, onclick `juic.fire(...)`), which opens a source dialog with a real `input[type=file]`.
- Autocomplete fields ("country code"): type then pick the suggestion (keyboard ArrowDown+Enter works).

**Phenom** (`jobs.<company>.com/us/en/apply` — e.g. eBay): no account needed. Upload resume FIRST (it autofills the whole form well, including parsed work history + descriptions). Fix region/postal/source, answer the questionnaire selects, accept terms, Submit → thank-you URL has `status=success` + candidate ID.

**Naukri native**:
- Some applies are one-click (instant `multiApplyResp {jobid: 200}` in the URL). Others open a **chatbot** (`._chatBotContainer`).
- Chatbot text answers MUST be typed for real: click `.textArea[contenteditable="true"]`, `page.keyboard.type(answer)`, then click Save via `getByText('Save')`. `.fill()` produces a 406 "incomplete information" rejection at the end.
- Radio questions: the labels are the clickable part; `getByText` can match old transcript text — scope to the LAST radio group / use `label[for]`. Save button container can intercept clicks — dispatch click on `[id^="sendMsgbtn_container"]` or the `.sendMsg` div.
- Success = `multiApplyResp {id: 200}` + "Applied to <role>" text. 202 = external-redirect click tracked (NOT an application).
- Profile-edit dropdowns ("droope"): ONLY keyboard ArrowDown/ArrowUp + Enter works; JS/mouse clicks silently fail; **Escape closes the whole modal and loses all edits**.

**Instahyre**: card click opens a modal (`openApplyModal`) → Apply is `[ng-click*="submitChoice(opp, true)"]`. Quirks: modals are position:fixed so `offsetParent` is null — check `getComputedStyle(...).display` instead; a stale `noscroll` body class after an apply blocks the next modal (reload the feed page between applies); after applying, the NEXT match's modal auto-opens — close it via `.close` WITHOUT clicking Apply/Not-interested; clicking coordinates must be re-read after scrolling settles (stale rects land off-viewport). Verify: the card disappears from the feed.

**Cutshort**: matches at `/profile/all-jobs?matchesfor=<id>`. Apply now → modal — VERIFY it says "You are applying for <role> at <company>" before clicking Send (the wrong card's modal can open). Employer screeners arrive as `[Questionnaire]` threads under candidate-conversations, but the "Voila" bot auto-submits them from the profile — the "awaiting" tab means awaiting EMPLOYER, not you.

**Freshteam** (`<co>.freshteam.com`): simple form + a reCAPTCHA labeled "Are you a Robot?". Checkbox-click the anchor frame (`#recaptcha-anchor`) — it usually passes without an image challenge. Verify "You have successfully applied".

**Custom company forms** (e.g. weareroku.com): beware MULTIPLE forms on one page (apply form + talent-community form) — click the button in the RIGHT form ("Submit Application", not "Submit"). Verify by the form disappearing + an explicit confirmation string, not by generic "thanks" text that was already on the page.

**Captcha policy**: clicking a checkbox captcha yourself is fine. If an image/grid challenge or a Cloudflare "Additional Verification Required" wall appears, STOP and ask the user to click it in the browser tab, then continue.

### After every apply batch
csv-logger updates (Status=Applied + dated Next step + req IDs + credentials-file pointers) → THEN `./tracker/refresh.sh`. Never refresh before the CSV write lands.

## Phase 4 — Cold email outreach (startups without open roles)

1. **Research** with parallel subagents across angles: recent YC batches, regional funding news (last ~12 months, seed/Series A in the user's lane), accelerator cohorts, viral launches/build-in-public founders. Each returns structured JSON: company / what / why-fit / founders / guessed email / source.
2. **Verify emails** before sending (email-prospecting connector if available) — fix guesses, drop dead ones.
3. Per company: tailored resume variant + a SHORT honest email (openable hook referencing THEIR product, 3-4 lines of the user's most relevant receipts, link, minimal signature). No AI-sounding fluff.
4. Draft into Gmail via the connector (drafts only — the USER hits send). Track in `output/job-search/outreach/startups_outreach.csv` with Status + dates.
5. Follow-up pass ~4 days later: check for replies first, bump politely (drafts again), never re-pitch.

## Phase 5 — X/Twitter cold DMs

1. Research founders' X handles the same fan-out way; verify each handle live in the logged-in browser (bio mentions the company) and record follower count + whether DMs are open.
2. DM automation (user must be logged into X in the Playwright browser, and must approve the named recipient list): open `x.com/<handle>` → `[data-testid="sendDMFromProfile"]` → composer is `[data-testid="dm-composer-textarea"]` → fill → `[data-testid="dm-composer-send-button"]` → verify the message text appears in-thread. Pace sends 8-10s apart.
3. **The Premium gate**: many accounts only accept message requests from verified users — the chat opens but no composer, with "Get verified to continue". Workarounds: follow them (DM unlocks on follow-back), reply publicly to a recent post, or the user buys Premium. Unverified senders' DMs land in Message Requests — tell the user replies will be slow.
4. Messages: 60-110 words, one founder-specific hook (their launch/tweet/product), 2-3 verified receipts, one link. Never invent facts.
5. Track in `output/job-search/outreach/startups_twitter_dm.csv` (handle, confidence, DMs-open, pitch angle, Status).

## Phase 6 — Public tracker (Cloudflare Pages)

`tracker/` is a small Vite+React app reading `src/data.json` generated from applications.csv by `make_data.py`. First-time setup on the USER's Cloudflare account: `npx wrangler login`, `npx wrangler pages project create my-job-tracker`, then `./tracker/refresh.sh` after every CSV change. Edge caches index.html — verify via the deployment-specific URL wrangler prints.

## Phase 7 — Cadence and priorities

- Daily: scan → triage → apply to approved leads → refresh tracker.
- When scans go quiet (they will): check Gmail/X/platform inboxes for replies; run outreach batches; hit big-tech portals (prep-heavy, do as a deliberate batch).
- Everything the user needs to act on lives in the CSV's Next step column. Blocked items (captcha walls, missing personal facts like DOB) get a BLOCKED note there.
- Save durable facts (form facts, platform quirks you newly discover, account credentials locations) to memory as you go — future sessions should never re-ask or re-learn.
