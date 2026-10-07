import sqlite3
import os

conv_id = "cba11062-f2b2-490d-8a2e-c46131def99c"
conv_dir = os.path.expanduser("~/.gemini/antigravity-cli/conversations")
target_db = os.path.join(conv_dir, f"{conv_id}.db")

conn = sqlite3.connect(target_db)
c = conn.cursor()
c.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [r[0] for r in c.fetchall()]

print("Tables in main DB:")
for t in tables:
    c.execute(f"SELECT count(*) FROM '{t}'")
    cnt = c.fetchone()[0]
    print(f"- {t}: {cnt} rows")

# Check if gen_metadata exists
if "gen_metadata" in tables:
    c.execute("PRAGMA table_info('gen_metadata')")
    cols = [col[1] for col in c.fetchall()]
    print("gen_metadata columns:", cols)
    c.execute("SELECT * FROM 'gen_metadata' LIMIT 5")
    for r in c.fetchall():
        print(r)
