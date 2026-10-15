import json, os

BASE = r"E:\Extra\job-kit-starter"
with open(os.path.join(BASE, 'job-kit-starter', 'drafts_payload.json'), 'r', encoding='utf-8') as f:
    items = json.load(f)

# Note: item 0 (GovStar) was already sent!
remaining = items[1:]  # items 1 to 19 (19 items)

chunks = [
    remaining[0:4],    # 1..4 (Irash Tech, Sendery, Komodo Health, Willow Education)
    remaining[4:9],    # 5..9 (neoshare, Estuary, Silkline, Steg.AI, Quill)
    remaining[9:14],   # 10..14 (Pango, Catalyst Wayfare AI, Biobase, Lucia, Noricum)
    remaining[14:19]   # 15..19 (Senzing, Privy.pro, SKIES, Cascade Space, Tecuity)
]

for idx, chunk in enumerate(chunks):
    fname = os.path.join(BASE, 'scratch', f'send_chunk_{idx}.js')
    chunk_json = json.dumps(chunk, ensure_ascii=False)

    code = f"""async (page) => {{
  const targets = {chunk_json};
  const results = [];

  for (let i = 0; i < targets.length; i++) {{
    const item = targets[i];
    const searchUrl = 'https://mail.google.com/mail/u/0/#search/in%3Adrafts+' + encodeURIComponent(item.email);

    try {{
      await page.goto(searchUrl, {{ waitUntil: 'load', timeout: 30000 }});
      await page.waitForTimeout(2500);

      // Find and click the draft row
      const clicked = await page.evaluate((targetComp) => {{
        const rows = Array.from(document.querySelectorAll("tr[role='row']"));
        const row = rows.find(r => r.innerText.toLowerCase().includes(targetComp.toLowerCase())) || rows[0];
        if (row) {{
          row.click();
          return true;
        }}
        return false;
      }}, item.company);

      if (!clicked) {{
        results.push({{ company: item.company, email: item.email, status: 'Error: Draft row not found' }});
        continue;
      }}

      await page.waitForTimeout(2000);

      // Click Send
      const sendResult = await page.evaluate(() => {{
        const sendBtn = document.querySelector("div[role='button'][aria-label*='Send'], div[data-tooltip*='Send']");
        if (sendBtn) {{
          sendBtn.click();
          return true;
        }}
        return false;
      }});

      await page.waitForTimeout(3000);

      const check = await page.evaluate(() => {{
        const text = document.body.innerText;
        const dialog = document.querySelector("[role='dialog']");
        return {{
          sent: text.includes('Message sent') || text.includes('Sending') || !dialog,
          dialogOpen: !!dialog
        }};
      }});

      results.push({{
        company: item.company,
        email: item.email,
        status: check.sent ? 'Sent' : 'Send_Unconfirmed',
        details: check
      }});
    }} catch (e) {{
      results.push({{
        company: item.company,
        email: item.email,
        status: 'Error: ' + e.message
      }});
    }}
  }}

  return results;
}}"""
    with open(fname, 'w', encoding='utf-8') as out:
        out.write(code)
    print(f"Wrote {fname} with {len(chunk)} items: {[c['company'] for c in chunk]}")
