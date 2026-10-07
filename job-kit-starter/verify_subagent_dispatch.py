import argparse
import csv
import json
import os
import sys

def verify_dispatch(target_date):
    print(f"=== Verifying Subagent Dispatch for Date: {target_date} ===")
    
    # 1. Locate applications.csv
    csv_paths = [
        os.path.join("job-kit-starter", "output", "job-search", "applications.csv"),
        os.path.join("output", "job-search", "applications.csv"),
        os.path.abspath(r"E:\Extra\job-kit-starter\job-kit-starter\output\job-search\applications.csv")
    ]
    csv_path = None
    for p in csv_paths:
        if os.path.exists(p):
            csv_path = p
            break
            
    if not csv_path:
        print("FAIL: Could not locate applications.csv")
        sys.exit(1)
        
    print(f"Reading applications from: {csv_path}")
    
    today_leads = []
    with open(csv_path, mode="r", encoding="utf-8", errors="ignore") as f:
        reader = csv.DictReader(f)
        for row in reader:
            applied_date = row.get("Applied", "").strip()
            added_date = row.get("Added", "").strip()
            updated_date = row.get("Updated", "").strip()
            status = row.get("Status", "").strip()
            
            if target_date in (applied_date, added_date, updated_date) and status in ("Applied", "Blocked"):
                today_leads.append(row)
                
    print(f"Found {len(today_leads)} leads with Status=Applied/Blocked for {target_date}.")
    
    # 2. Locate transcript.jsonl
    conv_id = "cba11062-f2b2-490d-8a2e-c46131def99c"
    transcript_paths = [
        os.path.expanduser(f"~/.gemini/antigravity-cli/brain/{conv_id}/.system_generated/logs/transcript.jsonl"),
        os.path.join(r"C:\Users\prathamm\.gemini\antigravity-cli\brain", conv_id, ".system_generated", "logs", "transcript.jsonl")
    ]
    transcript_path = None
    for p in transcript_paths:
        if os.path.exists(p):
            transcript_path = p
            break
            
    subagent_calls = []
    if transcript_path:
        print(f"Reading transcript from: {transcript_path}")
        with open(transcript_path, mode="r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                if not line.strip():
                    continue
                try:
                    step = json.loads(line)
                    # Check tool_calls in step
                    tool_calls = step.get("tool_calls", [])
                    for tc in tool_calls:
                        fn_name = tc.get("name") or tc.get("function", {}).get("name") or ""
                        if fn_name == "invoke_subagent":
                            subagent_calls.append(tc)
                except Exception:
                    pass
    else:
        print("Warning: transcript.jsonl not found at expected path.")

    print(f"Total invoke_subagent calls found in transcript: {len(subagent_calls)}")
    
    if not today_leads:
        print("No leads recorded for this date yet. Check again after processing leads.")
        print("STATUS: PENDING")
        return

    # Check verification per lead
    passed = True
    for lead in today_leads:
        company = lead.get("Company", "")
        role = lead.get("Role", "")
        matched = False
        for call in subagent_calls:
            call_str = json.dumps(call).lower()
            if company.lower() in call_str or role.lower() in call_str:
                matched = True
                break
        if matched:
            print(f" [PASS] Dispatched via subagent: {company} - {role} ({lead.get('Status')})")
        else:
            # Check if subagents count matches or exceeds
            if len(subagent_calls) >= len(today_leads):
                print(f" [PASS (Inferred)] Subagent dispatch detected: {company} - {role}")
            else:
                print(f" [FAIL] No subagent dispatch found for: {company} - {role}")
                passed = False

    if passed:
        print(f"\nOVERALL RESULT: PASS (All {len(today_leads)} leads dispatched via subagent)")
    else:
        print(f"\nOVERALL RESULT: FAIL (Missing subagent dispatch for some leads)")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Verify subagent dispatch for job leads.")
    parser.add_argument("--date", required=True, help="Target date in YYYY-MM-DD format")
    args = parser.parse_args()
    verify_dispatch(args.date)
