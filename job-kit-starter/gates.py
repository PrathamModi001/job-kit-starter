#!/usr/bin/env python3
"""Pre-submit gates for the daily scan. Run from job-kit-starter/.

  python gates.py title "<job title>"          -> exit 1 if a hard-skip term matches
  python gates.py yoe <jd.txt>                 -> exit 1 on hard 4+ YOE, warns on borderline
  python gates.py form "<Personal Info Filled string>"   -> flags values that diverge from config.md facts
  python gates.py lint "<Company - Role>"      -> resume claim words must exist in SKILL_PROFILE.md
  python gates.py coverage "<Company - Role>"  -> writes output/<dir>/keyword_table.json (tool-computed JD match rate)
  python gates.py location "<job location>" [jd.txt]   -> exit 1 unless India-eligible (not region-locked, no US/UK/EU work-right in JD)
  python gates.py preflight "<title>" "<location>" <jd.txt>   -> title + location + yoe in one call; exit 1 on any SKIP
  python gates.py fit "<title>" "<location>" <jd.txt>   -> 0-12 fit score + breakdown; exit 1 below MIN_FIT (stretch role)
  python gates.py dedup "<company>"            -> exit 1 if the company is already Applied/Blocked/Lead/Closed in applications.csv
  python gates.py clean <raw_fetch.html>       -> strips tags/boilerplate, prints clean text (pipe into jd.txt; never save raw HTML)
"""
import csv, html, json, re, sys
sys.stdout.reconfigure(encoding="utf-8")
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def strip_html(text):
    """Tags off, entities decoded, whitespace collapsed. Shared by yoe_check/coverage/clean
    so there's exactly one definition of 'clean JD text' instead of three inline copies."""
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", text or ""))).strip()

LOC_INDIA = re.compile(r"\b(india|bengaluru|bangalore|hyderabad|secunderabad|pune|gurgaon|gurugram|noida|delhi|mumbai|thane|ahmedabad|chennai|kanpur|apac)\b", re.I)
LOC_REMOTE = re.compile(r"\b(remote|anywhere|worldwide|distributed|work from home)\b", re.I)
# strong "remote with no borders" signal
LOC_GLOBAL = re.compile(r"\b(anywhere|worldwide|global(ly)?|any country|any location|fully remote|remote[- ]?first)\b", re.I)
# a specific US/EU/Canada place or region in the LOCATION field => region-locked (not India-eligible)
LOC_LOCKED = re.compile(
    r"\b(united states|u\.?s\.?a?|usa|america|canada|canadian|united kingdom|\bu\.?k\.?\b|england|ireland|"
    r"germany|france|netherlands|spain|poland|portugal|sweden|switzerland|"
    r"berlin|munich|cologne|köln|london|dublin|amsterdam|paris|lisbon|madrid|warsaw|"
    r"new york|san francisco|seattle|austin|boston|chicago|denver|toronto|vancouver|"
    r"emea|namer|latam|est timezone|pst|pt timezone|eastern time|pacific time)\b", re.I)
# JD body text that makes a nominally-remote role non-India
JD_LOCKED = re.compile(r"right to work in the (?:uk|eu|us)|must (?:be|reside|live) (?:located )?in the (?:us|united states|uk|eu)|us (?:work )?authori[sz]ation required|us citizens? only", re.I)


def region(loc, desc=""):
    """india | remote | locked | unknown -- used for scoring, the --india filter and `gates.py location`."""
    loc = loc or ""
    if LOC_INDIA.search(loc) or LOC_INDIA.search(desc[:400]): return "india"
    if LOC_GLOBAL.search(loc): return "remote"
    if LOC_LOCKED.search(loc): return "locked"
    if LOC_REMOTE.search(loc): return "remote"
    return "unknown"


def location_check(loc, jd=""):
    """('ok'|'skip'|'unknown', why). Locked region or a US/UK/EU work-right in the JD => skip.
    No location text => 'unknown' (flag for a human, not an auto-skip)."""
    r = region(loc, jd)
    m = JD_LOCKED.search(strip_html(jd))
    if r == "locked": return "skip", f"region-locked: {loc}"
    if m: return "skip", f"JD requires: {m.group(0)}"
    if r == "unknown": return "unknown", "no location text -- verify manually"
    return "ok", r


# Literal title check (daily_scan.md step 5 b2) + user-added terms (customer/client/mobile/React Native).
TITLE_SKIP = re.compile(
    r"\bjava\b|\.net\b|\bc#|asp\.net|c\+\+|\bruby\b|\brails\b|\bsenior\b|\bsr\.?(?=\W)|\bstaff\b|\bprincipal\b|"
    r"\barchitect\b|\blead\b|\bsde[- ]?(?:2|3|ii|iii)\b|\bproduct engineer\s*(?:2|ii)\b|\bpe\s*2\b|"
    r"\b(?:ii|iii)\b|\b(?:engineer|developer)\s*[23]\b|\bmts\b|member of technical staff|\bcustomer\b|\bclient\b|\bmobile\b|react[- ]native|forward[- ]deployed|\bsolutions? engineer|\bsales engineer", re.I)
# Terms that, as the JD's primary focus, also disqualify (checked by a human/LLM; this only flags).
JD_FLAG = re.compile(r"founding engineer|forward[- ]deployed|customer[- ]facing|client[- ]facing|react[- ]native|mobile (?:app|engineer|developer)", re.I)


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


def personal_info_valid(s):
    """True only if s is a 'key=value; key=value; ...' audit trail of what was actually
    entered (CLAUDE.md's contract for this field) -- rejects placeholders like 'Yes' or
    'Yes (WaaS profile)' that assert a form was filled without logging what was filled."""
    if re.match(r"(?i)^\s*(yes|no)\b", s.strip()):
        return False
    pairs = [p for p in re.split(r";\s*", s.strip()) if ("=" in p or ":" in p)]
    return len(pairs) >= 3


def form_check(s):
    out = []
    if not personal_info_valid(s):
        return [f"Personal Info Filled must be a verbatim 'key=value; key=value' audit trail of what was "
                f"entered, not a placeholder like 'Yes' (got: {s!r})"]
    pairs = [(p.split("=", 1) if "=" in p else p.split(":", 1)) for p in re.split(r";\s*", s) if ("=" in p or ":" in p)]
    keys = [k.strip().lower() for k, _ in pairs]
    for k in keys:
        if re.search(r"password|passcode|\botp\b|secret|token", k):
            out.append(f"{k}: credentials must never be logged -- store them in output/<dir>/account_credentials.txt")
    # every audit trail must show these; if the form genuinely lacks a field, log it as 'key=n/a'
    for label, pat in (("name", r"name"), ("email", r"e-?mail"), ("phone", r"phone|mobile"),
                       ("location", r"location|city"), ("ctc", r"ctc|salary|compensation"), ("notice", r"notice")):
        if not any(re.search(pat, k) for k in keys):
            out.append(f"missing {label} (log '{label}=n/a' if the form has no such field)")
    for k, v in pairs:
        k, v = k.strip().lower(), v.strip()
        if v.lower() in ("n/a", "na", "none"):
            continue
        if "notice" in k and not v.lower().startswith("immediate"):
            out.append(f"{k}={v} (profile: Immediate)")
        if "expected" in k:
            nums = [int(n) for n in re.findall(r"\d+", v)]
            if nums and min(nums) < 18:
                out.append(f"{k}={v} (profile: min 18 LPA)")
            if not re.search(r"lpa|lakh", v, re.I):
                out.append(f"{k}={v} (must be quoted in LPA, e.g. 18-20 LPA -- never USD/other currency)")
        if k == "location" and "kanpur" not in v.lower():
            out.append(f"{k}={v} (profile: Kanpur)")
        if "current ctc" in k and "12" not in v:
            out.append(f"{k}={v} (profile: 12 LPA)")
        if "address" in k and "d-203" not in v.lower():
            out.append(f"{k}={v} (profile: D-203, Ratan Planet, Near IIT Kanpur, Kanpur, 208016)")
    return out


LANE = re.compile(r"back[- ]?end|full[- ]?stack|\bnode|software (?:engineer|developer)|\bsde\b|platform|developer", re.I)
MIN_FIT = 11  # of 15; calibrated on 46 saved JDs (median ~10-11): below this is a stretch -- tune here


def fit_score(title, jd, loc):
    """0-15 fit: lane (0-3) + profile-stack overlap (0-8) + stated YOE (0-2) + location (0-2).
    Hard skips (title/yoe/location) are separate gates; this ranks what survives them."""
    t = strip_html(jd).lower()
    lane = 3 if LANE.search(title) else (1 if re.search(r"engineer|developer", title, re.I) else 0)
    n = sum(1 for v in vocab() if re.search(r"(?<![\w])" + re.escape(v) + r"(?![\w])", t))
    stack = min(n, 8)
    yrs = [int(m.group(1)) for m in re.finditer(r"(\d+)\s*(?:\+|-|–|to)\s*\d*\s*\+?\s*(?:years|yrs)", t)]
    yoe = 2 if yrs and min(yrs) <= 3 else (1 if not yrs else 0)
    r = region(loc, jd)
    place = 2 if r == "india" else (1 if r == "remote" else 0)
    parts = {"lane": lane, "stack": stack, "yoe": yoe, "location": place, "jd_profile_terms": n}
    return lane + stack + yoe + place, parts


def dedup(company):
    """Row Status of the first existing row for this company (Applied/Blocked/Lead/Closed), else None.
    Skipped rows don't count: a skip for one role shouldn't block a better role there."""
    norm = lambda s: re.sub(r"[^a-z0-9]", "", s.lower())
    with open(ROOT / "output" / "job-search" / "applications.csv", encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            if norm(row["Company"]) == norm(company) and row["Status"] in ("Applied", "Blocked", "Lead", "Closed"):
                return row["Status"]
    return None


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
    rep["status"] = "OK" if len(in_jd) >= 4 else "EMPTY"  # <4 profile terms in the JD => match_rate is meaningless
    (base / "keyword_table.json").write_text(json.dumps(rep, indent=2), encoding="utf-8")
    return rep


def clean_html(text):
    t = html.unescape(text or "")
    t = re.sub(r"<(?:br|p|div|li|tr|h[1-6])[^>]*>", "\n", t, flags=re.I)
    t = re.sub(r"<[^>]+>", " ", t)
    t = re.sub(r"[ \t]+", " ", t)
    t = re.sub(r"\n\s*\n+", "\n\n", t)
    return t.strip()


if __name__ == "__main__":
    cmd, arg = sys.argv[1], " ".join(sys.argv[2:])
    if cmd == "clean":
        p = Path(arg) if arg else None
        raw = p.read_text(encoding="utf-8", errors="replace") if (p and p.exists()) else (arg or sys.stdin.read())
        print(clean_html(raw))
        sys.exit(0)
    if cmd == "title":
        m = title_skip(arg); print(f"SKIP ({m})" if m else "CLEAR"); sys.exit(1 if m else 0)
    if cmd == "yoe":
        r, ev = yoe_check(Path(arg).read_text(encoding="utf-8")); print(r.upper(), ev); sys.exit(1 if r == "skip" else 0)
    if cmd == "form":
        bad = form_check(arg); print("\n".join(bad) or "OK"); sys.exit(1 if bad else 0)
    if cmd == "lint":
        bad = lint(arg); print("UNSUPPORTED CLAIM WORDS:", bad if bad else "none"); sys.exit(1 if bad else 0)
    if cmd == "coverage":
        rep = coverage(arg); print(json.dumps(rep, indent=1))
        sys.exit(1 if rep["status"] == "EMPTY" else 0)
    if cmd == "location":
        loc, jdp = (sys.argv[2], sys.argv[3]) if len(sys.argv) > 3 else (arg, None)
        r, why = location_check(loc, Path(jdp).read_text(encoding="utf-8") if jdp else ""); print(r.upper(), why); sys.exit(1 if r == "skip" else 0)
    if cmd == "fit":
        sc, parts = fit_score(sys.argv[2], Path(sys.argv[4]).read_text(encoding="utf-8"), sys.argv[3])
        print(f"FIT {sc}/15 (min {MIN_FIT}) {parts}"); sys.exit(1 if (sc < MIN_FIT or parts["lane"] < 3) else 0)
    if cmd == "dedup":
        st = dedup(arg); print(f"DUPLICATE ({st})" if st else "NEW"); sys.exit(1 if st else 0)
    if cmd == "preflight":
        title, loc, jd = sys.argv[2], sys.argv[3], Path(sys.argv[4]).read_text(encoding="utf-8")
        t = title_skip(title); l, lw = location_check(loc, jd); y, ye = yoe_check(jd)
        print(f"title: {'SKIP (' + t + ')' if t else 'CLEAR'} | location: {l.upper()} {lw} | yoe: {y.upper()} {ye}")
        sc, parts = fit_score(title, jd, loc)
        print(f"fit: {sc}/15 (min {MIN_FIT}) {parts}" + ("  OFF-LANE: title is not backend/full-stack/software engineer/developer/platform" if parts["lane"] < 3 else ""))
        (Path(sys.argv[4]).parent / "fit.json").write_text(json.dumps({"title": title, "location": loc, "fit": sc, **parts}), encoding="utf-8")
        print("flags:", sorted({m.group(0).lower() for m in JD_FLAG.finditer(strip_html(jd))}) or "none")
        sys.exit(1 if (t or l == "skip" or y == "skip" or sc < MIN_FIT or parts["lane"] < 3) else 0)
