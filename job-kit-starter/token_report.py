#!/usr/bin/env python3
"""Per-step + total token usage from a transcript.jsonl, run OUTSIDE the chat (never ask the agent to parse it).
  python token_report.py <transcript.jsonl> [--steps]
Tolerant: finds any dict with input/cache-read/output token fields, whatever the nesting. Field names
unverified for Antigravity -- if totals are 0, run with --steps and check which keys your file uses."""
import json, sys
sys.stdout.reconfigure(encoding="utf-8")
KEYS = {"in": ("input_tokens", "prompt_tokens", "new_input_tokens"),
        "cache": ("cache_read_input_tokens", "cache_read_tokens", "cached_tokens"),
        "out": ("output_tokens", "completion_tokens")}


def find_usage(o):
    if isinstance(o, dict):
        u = {k: next((o[n] for n in ns if isinstance(o.get(n), int)), 0) for k, ns in KEYS.items()}
        if any(u.values()):
            return u
        for v in o.values():
            if (r := find_usage(v)): return r
    elif isinstance(o, list):
        for v in o:
            if (r := find_usage(v)): return r
    return None


def report(path):
    rows = []
    for i, line in enumerate(open(path, encoding="utf-8", errors="replace")):
        try: u = find_usage(json.loads(line))
        except ValueError: continue
        if u: rows.append((i, u))
    return rows


if __name__ == "__main__":
    rows = report(sys.argv[1])
    if "--steps" in sys.argv:
        for i, u in rows: print(f"line {i}: in={u['in']:,} cache={u['cache']:,} out={u['out']:,}")
    t = {k: sum(u[k] for _, u in rows) for k in KEYS}
    tot = sum(t.values())
    print(f"steps with usage: {len(rows)} | new input {t['in']:,} | cache-read {t['cache']:,} | output {t['out']:,} | total {tot:,}")
    if tot: print(f"cache share: {t['cache'] / tot:.1%}")
