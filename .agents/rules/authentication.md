# Authentication & Session Persistence Rule

## ⛔ Never Logout Accidentally
- Never intentionally or accidentally trigger a log out from any job platform, browser profile, or active portal session.

---

## 🔐 Sign-In & Recovery Protocol
Whenever sign-in problems, expired sessions, or accidental logouts occur:
- **Target Account:** Sign into the **`prathammodi001@gmail.com`** account.
- **Google OAuth via Cursor Click:** Always sign in using **Google OAuth** by clicking the "Sign in with Google" / OAuth button with the cursor. **DO NOT** attempt to sign in via email/password text input fields ("not signin via email").
- **Agent Environment / Tooling:**
  - When running in **AGY (Antigravity)**: Perform OAuth sign-in via **Playwright**.
  - When running in **Claude**: Perform OAuth sign-in via **Claude in Chrome** (`claude-in-chrome`).

---

## 🚫 Board Exception (jobfound)
- **jobfound.org**: Do **NOT** log in if navigating or scanning the jobfound board. Login is not needed for jobfound.
