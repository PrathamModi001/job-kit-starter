#!/usr/bin/env python3
"""
Verifies that step 5's per-lead subagent dispatch actually happened during a
daily-scan run, by reading the raw Antigravity transcript log instead of
trusting the run's own self-reported "Execution-architecture disclosure".

Catches the failure mode where every lead was processed in the main session
(0 invoke_subagent calls) while the report still narrates per-lead handling.

Usage:
    python3 verify_subagent_dispatch.py [--date YYYY-MM-DD] [--transcript PATH]
                                         [--csv PATH]

Exit code is non-zero when dispatch count < lead count for the target date,
so this can gate a run report (or be wired into a CI-style check) rather than
relying on the model's own disclosure.
"""
import argparse
import csv
import glob
import json
import os
import re
import sys
from datetime import datetime, timezone

DEFAULT_CSV = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "output", "job-search", "applications.csv",
)
TRANSCRIPT_GLOB = os.path.expanduser(
    "~/.gemini/antigravity-cli/brain/*/.system_generated/logs/transcript.jsonl"
)


def find_latest_transcript():
    candidates = glob.glob(TRANSCRIPT_GLOB)
    if not candidates:
        return None
    return max(candidates, key=os.path.getmtime)


def count_subagent_dispatches(transcript_path, date=None):
    """Counts real invoke_subagent tool calls, not reasoning text that merely
    mentions the function name."""
    count = 0
    calls = []
    with open(transcript_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line or '"tool_calls"' not in line:
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            created_at = rec.get("created_at", "")
            if date and not created_at.startswith(date):
                continue
            for tc in rec.get("content", {}).get("tool_calls", []) or []:
                if tc.get("name") == "invoke_subagent":
                    count += 1
                    calls.append((rec.get("step_index"), created_at))
    return count, calls


def count_leads_for_date(csv_path, date):
    """Counts applications.csv rows Added on the target date (Applied,
    Blocked, and Skipped rows past the exclusion check all consume a
    subagent dispatch per the workflow spec)."""
    leads = []
    with open(csv_path, newline="") as f:
        for row in csv.DictReader(f):
            if row.get("Added") == date:
                leads.append((row.get("Company"), row.get("Role"), row.get("Status")))
    return leads


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", default=datetime.now(timezone.utc).strftime("%Y-%m-%d"),
                     help="Target run date, YYYY-MM-DD (default: today, UTC)")
    ap.add_argument("--transcript", default=None,
                     help="Path to transcript.jsonl (default: most recently modified session)")
    ap.add_argument("--csv", default=DEFAULT_CSV, help="Path to applications.csv")
    args = ap.parse_args()

    transcript_path = args.transcript or find_latest_transcript()
    if not transcript_path or not os.path.exists(transcript_path):
        print("ERROR: no Antigravity transcript.jsonl found "
              f"(looked in {TRANSCRIPT_GLOB}). Pass --transcript explicitly.")
        sys.exit(2)

    if not os.path.exists(args.csv):
        print(f"ERROR: applications.csv not found at {args.csv}")
        sys.exit(2)

    leads = count_leads_for_date(args.csv, args.date)
    dispatch_count, calls = count_subagent_dispatches(transcript_path, date=args.date)

    print(f"Transcript:        {transcript_path}")
    print(f"Target date:       {args.date}")
    print(f"CSV leads logged:  {len(leads)}")
    for company, role, status in leads:
        print(f"  - {company} | {role} | {status}")
    print(f"invoke_subagent calls found: {dispatch_count}")
    for idx, ts in calls:
        print(f"  - step {idx} @ {ts}")

    if len(leads) == 0:
        print("\nNo leads logged for this date — nothing to verify.")
        sys.exit(0)

    if dispatch_count < len(leads):
        print(
            f"\nFAIL: {len(leads)} lead(s) were logged for {args.date} but only "
            f"{dispatch_count} subagent dispatch(es) were found in the transcript. "
            "This run deviated from the mandatory per-lead subagent dispatch in "
            "daily_scan.md step 5, regardless of what the run's own "
            "'Execution-architecture disclosure' claims."
        )
        sys.exit(1)

    print(f"\nPASS: dispatch count ({dispatch_count}) >= lead count ({len(leads)}).")
    sys.exit(0)


if __name__ == "__main__":
    main()
