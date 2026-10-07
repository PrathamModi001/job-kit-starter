import argparse
import json
import os
import re
import sqlite3
import sys

conv_dir = os.path.expanduser("~/.gemini/antigravity-cli/conversations")
brain_dir = os.path.expanduser("~/.gemini/antigravity-cli/brain")

DEFAULT_MAIN_ID = "18456a7e-1e39-4b5a-aec7-711c21fd84ed"

def discover_conversations(main_id):
    conv_list = [("Main Session", main_id)]
    transcript_path = os.path.join(brain_dir, main_id, ".system_generated", "logs", "transcript.jsonl")
    if os.path.exists(transcript_path):
        with open(transcript_path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                if not line.strip():
                    continue
                try:
                    obj = json.loads(line)
                    # Check tool calls
                    for tc in obj.get("tool_calls", []):
                        if tc.get("name") == "invoke_subagent":
                            args = tc.get("args") or tc.get("arguments") or {}
                            for sub in args.get("Subagents", []):
                                role = sub.get("Role", "Subagent")
                                # Subagent ID might be in tool response or manage_subagents
                    # Check for tool responses containing conversationId
                    content = obj.get("content", "")
                    if "conversationId" in content or "conversation_id" in content:
                        for m in re.finditer(r'["\']?(?:conversationId|conversation_id)["\']?\s*[:=]\s*["\']([a-f0-9\-]{36})["\']', content):
                            cid = m.group(1)
                            if cid != main_id and not any(c[1] == cid for c in conv_list):
                                conv_list.append((f"Subagent ({cid[:8]})", cid))
                except Exception:
                    pass
    return conv_list

def decode_varints(data):
    i = 0
    l = len(data)
    fields = []
    while i < l:
        key = 0
        shift = 0
        while i < l:
            b = data[i]
            i += 1
            key |= (b & 0x7F) << shift
            if not (b & 0x80):
                break
            shift += 7
        field_num = key >> 3
        wire_type = key & 0x7
        if wire_type == 0:
            val = 0
            shift = 0
            while i < l:
                b = data[i]
                i += 1
                val |= (b & 0x7F) << shift
                if not (b & 0x80):
                    break
                shift += 7
            fields.append((field_num, "varint", val))
        elif wire_type == 2:
            length = 0
            shift = 0
            while i < l:
                b = data[i]
                i += 1
                length |= (b & 0x7F) << shift
                if not (b & 0x80):
                    break
                shift += 7
            val = data[i:i+length]
            i += length
            fields.append((field_num, "bytes", val))
        elif wire_type == 1:
            i += 8
        elif wire_type == 5:
            i += 4
        else:
            break
    return fields

def process_db(label, cid):
    db_path = os.path.join(conv_dir, f"{cid}.db")
    if not os.path.exists(db_path):
        return None
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT idx, data FROM gen_metadata")
    rows = c.fetchall()
    
    total_calls = len(rows)
    total_prompt_tokens = 0
    total_cached_tokens = 0
    total_output_tokens = 0
    
    for idx, data in rows:
        parsed = decode_varints(data)
        for f in parsed:
            if f[0] == 1 and f[1] == "bytes":
                sf = decode_varints(f[2])
                for s in sf:
                    if s[0] == 4 and s[1] == "bytes":
                        token_fields = decode_varints(s[2])
                        p_tokens = 0
                        c_tokens = 0
                        o_tokens = 0
                        for tf in token_fields:
                            if tf[0] == 2 and tf[1] == "varint":
                                p_tokens = tf[2]
                            elif tf[0] == 3 and tf[1] == "varint":
                                o_tokens = tf[2]
                            elif tf[0] == 5 and tf[1] == "varint":
                                c_tokens = tf[2]
                        total_prompt_tokens += p_tokens
                        total_cached_tokens += c_tokens
                        total_output_tokens += o_tokens

    return {
        "label": label,
        "cid": cid,
        "turns": total_calls,
        "input_uncached": total_prompt_tokens,
        "input_cached": total_cached_tokens,
        "total_input": total_prompt_tokens + total_cached_tokens,
        "output_tokens": total_output_tokens,
        "total_tokens": total_prompt_tokens + total_cached_tokens + total_output_tokens
    }

parser = argparse.ArgumentParser(description="Aggregate tokens across session and subagents.")
parser.add_argument("--conv-id", default=os.environ.get("CONV_ID", DEFAULT_MAIN_ID), help="Main conversation ID")
args = parser.parse_args()

conv_ids = discover_conversations(args.conv_id)
if len(conv_ids) == 1 and not os.path.exists(os.path.join(conv_dir, f"{args.conv_id}.db")):
    # Fallback to historical hardcoded list if current ID database not found
    conv_ids = [
        ("Main Session", "cba11062-f2b2-490d-8a2e-c46131def99c"),
        ("Subagent Observe.ai", "8d3a8099-759f-4fa0-a0fe-7a6e402a0dac"),
        ("Subagent SingleStore", "79de6e89-9fa1-4e1a-ae72-1248c1616b8e"),
        ("Subagent SuperKalam", "783d30d3-975e-4e04-9b36-47c81befbe8e"),
        ("Subagent FutureStrive", "edc45ac8-5c9f-4948-9a84-d45540b2cea8"),
        ("Subagent Certa", "3b5d898c-17d4-40c7-b568-5dc654f25e0b"),
        ("Subagent Gravity", "3c5b5239-ed80-4532-ae5f-e3506da1ccae")
    ]

print("=== REAL TOKEN USAGE MEASURED FROM SQLITE GEN_METADATA ===")
grand_input = 0
grand_output = 0
grand_total = 0
grand_turns = 0

for label, cid in conv_ids:
    res = process_db(label, cid)
    if res:
        print(f"{res['label']} ({res['cid'][:8]}):")
        print(f"  Turns / Model Calls: {res['turns']}")
        print(f"  Input Tokens: {res['total_input']:,} (Uncached: {res['input_uncached']:,}, Cached: {res['input_cached']:,})")
        print(f"  Output Tokens: {res['output_tokens']:,}")
        print(f"  Total Tokens: {res['total_tokens']:,}")
        grand_turns += res['turns']
        grand_input += res['total_input']
        grand_output += res['output_tokens']
        grand_total += res['total_tokens']

print("------------------------------------------------------------")
print(f"GRAND TOTAL:")
print(f"  Total Turns / Model Calls: {grand_turns}")
print(f"  Total Input Tokens: {grand_input:,}")
print(f"  Total Output Tokens: {grand_output:,}")
print(f"  Grand Total Tokens: {grand_total:,}")
