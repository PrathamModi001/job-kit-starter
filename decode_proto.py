import sqlite3
import os

db_path = os.path.expanduser('~/.gemini/antigravity-cli/conversations/cba11062-f2b2-490d-8a2e-c46131def99c.db')
conn = sqlite3.connect(db_path)
c = conn.cursor()
c.execute('SELECT idx, data FROM gen_metadata')
rows = c.fetchall()

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

# Let's inspect subfields of Field 1 in several records
print("Inspecting Field 1 in records:")
for idx, data in rows[:5]:
    parsed = decode_varints(data)
    for f in parsed:
        if f[0] == 1 and f[1] == "bytes":
            sf = decode_varints(f[2])
            print(f"Record {idx} Field 1:")
            for s in sf:
                if s[1] == "varint":
                    print(f"   field {s[0]} = {s[2]}")
                elif s[1] == "bytes":
                    try:
                        print(f"   field {s[0]} str = {s[2].decode('utf-8')[:60]}")
                    except:
                        # nested?
                        nested = decode_varints(s[2])
                        print(f"   field {s[0]} nested ({len(nested)} items): {[n[0] for n in nested]}")
                        for n in nested:
                            if n[1] == "varint":
                                print(f"       n{n[0]} = {n[2]}")
                            elif n[1] == "bytes":
                                try:
                                    print(f"       n{n[0]} str = {n[2].decode('utf-8')[:40]}")
                                except:
                                    pass
