#!/usr/bin/env python3
"""Pre-submit gates for the daily scan. Run from job-kit-starter/.

  python gates.py title "<job title>"          -> exit 1 if a hard-skip term matches
  python gates.py yoe <jd.txt>                 -> exit 1 on hard 4+ YOE, warns on borderline
  python gates.py form "<Personal Info Filled string>"   -> flags values that diverge from config.md facts
  python gates.py lint "<Company - Role>"      -> resume claim words must exist in SKILL_PROFILE.md
  python gates.py coverage "<Company - Role>"  -> writes output/<dir>/keyword_table.json (tool-computed JD match rate)
  python gates.py clean <raw_fetch.html>       -> strips tags/boilerplate, prints clean text (pipe into jd.txt; never save raw HTML)
"""
import html, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def strip_html(text):
    """Tags off, entities decoded, whitespace collapsed. Shared by yoe_check/coverage/clean
    so there's exactly one definition of 'clean JD text' instead of three inline copies."""
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", text or ""))).strip()

# Literal title check (daily_scan.md step 5 b2) + user-added terms (customer/client/mobile/React Native).
TITLE_SKIP = re.compile(
    r"\bjava\b|\.net\b|\bc#|asp\.net|c\+\+|\bruby\b|\brails\b|\bsenior\b|\bsr\.?(?=\W)|\bstaff\b|\bprincipal\b|"
    r"\barchitect\b|\blead\b|\bsde[- ]?(?:2|3|ii|iii)\b|\bproduct engineer\s*(?:2|ii)\b|\bpe\s*2\b|"
    r"\b(?:ii|iii)\b|\b(?:engineer|developer)\s*[23]\b|\bmts\b|member of technical staff|\bcustomer\b|\bclient\b|\bmobile\b|react[- ]native", re.I)
# Terms that, as the JD's primary focus, also disqualify (checked by a human/LLM; this only flags).
JD_FLAG = re.compile(r"customer[- ]facing|client[- ]facing|react[- ]native|mobile (?:app|engineer|developer)", re.I)


def title_skip(title):
    m = TITLE_SKIP.search(title)
    return m.group(0) if m else None


def yoe_check(text):
    """Return ('skip'|'borderline'|'ok', evidence). Hard skip: N+ with N>=4, or range with low bound >=3."""
    t = strip_html(text)
    for m in re.finditer(r"(\d+)\s*(?:\+|-|–|to)\s*(\d+)?\s*\+?\s*(?:years|yrs)", t, re.I):
        lo, hi = int(m.group(1)), int(m.group(2)) if m.group(2) else None
        ev = m.group(0)
        plus = "+" in ev and hi is None
        if (plus and lo >= 4) or (hi is not None and lo >= 3):
            return "skip", ev
    for m in re.finditer(r"(\d+)\s*(?:-|–|to)\s*(\d+)\s*(?:years|yrs)", t, re.I):
        if int(m.group(1)) >= 2 and int(m.group(2)) >= 4:
            return "borderline", m.group(0)
    return "ok", ""


def facts():
    cfg = (ROOT / "config.md").read_text(encoding="utf-8")
    return {"notice": "immediate", "ctc_min": 18, "city": "kanpur"} if "Notice period:** Immediate" in cfg else {}


def form_check(s):
    out = []
    for k, v in (p.split("=", 1) if "=" in p else p.split(":", 1) for p in re.split(r";\s*", s) if ("=" in p or ":" in p)):
        k, v = k.strip().lower(), v.strip()
        if "notice" in k and not v.lower().startswith("immediate"):
            out.append(f"{k}={v} (profile: Immediate)")
        if "expected" in k:
            nums = [int(n) for n in re.findall(r"\d+", v)]
            if nums and min(nums) < 18:
                out.append(f"{k}={v} (profile: min 18 LPA)")
        if "current ctc" in k and "12" not in v:
            out.append(f"{k}={v} (profile: 12 LPA)")
        if "address" in k and "d-203" not in v.lower():
            out.append(f"{k}={v} (profile: D-203, Ratan Planet, Near IIT Kanpur, Kanpur, 208016)")
    return out


CLAIM_WORDS = ["customer", "client", "mobile", "react native", "forward deployed", "stakeholder"]


def lint(d):
    prof = (ROOT / "SKILL_PROFILE.md").read_text(encoding="utf-8").lower()
    tex = (ROOT / "output" / d / "Pratham_Modi_Resume.tex").read_text(encoding="utf-8").lower()
    return [w for w in CLAIM_WORDS if w in tex and w not in prof]


def vocab():
    prof = (ROOT / "SKILL_PROFILE.md").read_text(encoding="utf-8")
    sk = prof.split("## Skills", 1)[1].split("##", 1)[0]
    terms = set()
    for line in sk.splitlines():
        for tok in re.split(r",|\(|\)", line.split(":", 1)[-1]):
            tok = re.sub(r"[*]", "", tok).strip()
            if 1 < len(tok) < 40:
                terms.add(tok.lower())
    return terms


def coverage(d):
    base = ROOT / "output" / d
    jd = strip_html((base / "jd.txt").read_text(encoding="utf-8")).lower()
    tex = (base / "Pratham_Modi_Resume.tex").read_text(encoding="utf-8").lower().replace("\\&", "&")
    in_jd = sorted(t for t in vocab() if re.search(r"(?<![\w])" + re.escape(t) + r"(?![\w])", jd))
    hit = [t for t in in_jd if t in tex]
    miss = [t for t in in_jd if t not in tex]
    rep = {"jd_terms_in_profile_vocab": in_jd, "matched": hit, "missing_but_in_profile": miss,
           "match_rate": round(len(hit) / len(in_jd), 2) if in_jd else None,
           "jd_flags": sorted({m.group(0).lower() for m in JD_FLAG.finditer(jd)})}
    (base / "keyword_table.json").write_text(json.dumps(rep, indent=2), encoding="utf-8")
    return rep


def clean_html(text):
    t = re.sub(r"<(?:br|p|div|li|tr|h[1-6])[^>]*>", "\n", text, flags=re.I)
    t = re.sub(r"<[^>]+>", " ", t)
    t = html.unescape(t)
    t = re.sub(r"[ \t]+", " ", t)
    t = re.sub(r"\n\s*\n+", "\n\n", t)
    return t.strip()


if __name__ == "__main__":
    cmd, arg = sys.argv[1], " ".join(sys.argv[2:])
    if cmd == "clean":
        p = Path(arg)
        raw = p.read_text(encoding="utf-8", errors="replace") if p.exists() else arg
        print(clean_html(raw))
    if cmd == "title":
        m = title_skip(arg); print(f"SKIP ({m})" if m else "CLEAR"); sys.exit(1 if m else 0)
    if cmd == "yoe":
        r, ev = yoe_check(Path(arg).read_text(encoding="utf-8")); print(r.upper(), ev); sys.exit(1 if r == "skip" else 0)
    if cmd == "form":
        bad = form_check(arg); print("\n".join(bad) or "OK"); sys.exit(1 if bad else 0)
    if cmd == "lint":
        bad = lint(arg); print("UNSUPPORTED CLAIM WORDS:", bad if bad else "none"); sys.exit(1 if bad else 0)
    if cmd == "coverage":
        print(json.dumps(coverage(arg), indent=1))
    if cmd == "clean":
        raw = Path(arg).read_text(encoding="utf-8", errors="ignore") if arg else sys.stdin.read()
        print(strip_html(raw))
