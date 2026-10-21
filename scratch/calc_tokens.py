import json

log_path = r'C:\Users\prathamm\.gemini\antigravity-cli\brain\e33ec6b2-6327-4c19-906d-b0a52f020e72\.system_generated\logs\transcript.jsonl'

input_tokens = 0
output_tokens = 0
cache_read_tokens = 0

with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
    for line in f:
        data = json.loads(line)
        input_tokens += data.get('input_tokens', 0) or 0
        output_tokens += data.get('output_tokens', 0) or 0
        cache_read_tokens += data.get('cache_read_tokens', 0) or 0

total_tokens = input_tokens + output_tokens + cache_read_tokens

print(f"Exact Input Tokens: {input_tokens:,}")
print(f"Exact Output Tokens: {output_tokens:,}")
print(f"Exact Cache Read Tokens: {cache_read_tokens:,}")
print(f"Total Processed Tokens: {total_tokens:,}")
