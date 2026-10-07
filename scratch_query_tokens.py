import sqlite3
import os
import glob

conv_id = "cba11062-f2b2-490d-8a2e-c46131def99c"
conv_dir = os.path.expanduser("~/.gemini/antigravity-cli/conversations")
target_db = os.path.join(conv_dir, f"{conv_id}.db")

print("Target DB:", target_db, "Exists:", os.path.exists(target_db))

subagent_ids = [
    "8d3a8099-759f-4fa0-a0fe-7a6e402a0dac", # Observe.ai
    "79de6e89-9fa1-4e1a-ae72-1248c1616b8e", # SingleStore
    "783d30d3-975e-4e04-9b36-47c81befbe8e", # SuperKalam
    "edc45ac8-5c9f-4948-9a84-d45540b2cea8", # FutureStrive
    "3b5d898c-17d4-40c7-b568-5dc654f25e0b", # Certa
    "3c5b5239-ed80-4532-ae5f-e3506da1ccae", # Gravity
]

def analyze_db(db_path, label):
    if not os.path.exists(db_path):
        print(f"[{label}] DB not found: {db_path}")
        return
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in c.fetchall()]
    print(f"\n[{label}] Tables in {os.path.basename(db_path)}: {tables}")
    for t in tables:
        c.execute(f"SELECT count(*) FROM '{t}'")
        cnt = c.fetchone()[0]
        c.execute(f"PRAGMA table_info('{t}')")
        cols = [col[1] for col in c.fetchall()]
        print(f"  Table '{t}' ({cnt} rows): {cols}")
        if "metadata" in t.lower() or "gen" in t.lower() or "token" in "".join(cols).lower():
            c.execute(f"SELECT * FROM '{t}' LIMIT 5")
            samples = c.fetchall()
            print(f"  Sample data from '{t}':")
            for s in samples:
                print("   ", s)

analyze_db(target_db, "Main Session")

for sid in subagent_ids:
    s_db = os.path.join(conv_dir, f"{sid}.db")
    analyze_db(s_db, f"Subagent {sid[:8]}")
