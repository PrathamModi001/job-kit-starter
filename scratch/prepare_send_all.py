import json
import os

targets_map = {
    "CoinSwitch": "ashish@coinswitch.co",
    "Yellow.ai": "raghu@yellow.ai",
    "Gupshup": "beerud@gupshup.io",
    "Park+": "amit@myparkplus.com",
    "Ultrahuman": "mohit@ultrahuman.com",
    "Captain Fresh": "utham@captainfresh.com",
    "Curefoods": "ankit@curefoods.in",
    "Rebel Foods": "jaydeep@rebelfoods.com",
    "Pocket FM": "rohan@pocketfm.com",
    "Plum": "abhishek@plumhq.com",
    "Axiom": "neil@axiom.co",
    "K-Scale": "ben@kscale.ai",
    "Cursor": "michael@anysphere.co",
    "Reflex": "nikhil@reflex.dev",
    "Baserow": "bram@baserow.io",
    "Starbridge": "recruiting@starbridge.ai",
    "Fazeshift": "chris.zehner@fazeshift.com",
    "Sidekick Labs": "hn@sidekicklabs.com",
    "Pairio": "hello@pairio.app",
    "PAGNOS": "recruiting@pagnos.com",
    "Blockchain Security": "jobs@chainsecurity.com",
    "Trackerbot": "dobrev.d10@gmail.com",
    "Full-Stack Developer": "dobrev.d10@gmail.com"
}

js_script = f"""async (page) => {{
  const targetsMap = {json.dumps(targets_map)};
  const sentLogs = [];

  for (let loop = 0; loop < 25; loop++) {{
    // 1. Get first row in main table
    const rowSubject = await page.evaluate(() => {{
      const main = document.querySelector('div[role="main"]');
      if (!main) return null;
      const rows = Array.from(main.querySelectorAll('tr[role="row"]'));
      if (rows.length === 0) return null;
      const r = rows[0];
      const text = r.innerText.replace(/\\n+/g, ' | ');
      r.click();
      return text;
    }});

    if (!rowSubject) {{
      console.log("No more draft rows found in main drafts view.");
      break;
    }}

    console.log(`[Step ${{loop + 1}}] Opening row: ${{rowSubject.slice(0, 60)}}`);
    await page.waitForTimeout(2000);

    // 2. Identify email based on subject in dialog
    const subjectInDialog = await page.evaluate(() => {{
      const dialog = document.querySelector('div[role="dialog"]');
      if (!dialog) return '';
      const subj = dialog.querySelector('input[name="subjectbox"]');
      return subj ? subj.value : '';
    }});

    let matchedEmail = null;
    for (const [key, email] of Object.entries(targetsMap)) {{
      if (subjectInDialog.includes(key) || rowSubject.includes(key)) {{
        matchedEmail = email;
        break;
      }}
    }}

    console.log(`Matched email: ${{matchedEmail}} for subject: ${{subjectInDialog}}`);

    // 3. Check if recipient chip exists, if not fill it
    if (matchedEmail) {{
      const hasChip = await page.evaluate((email) => {{
        const dialog = document.querySelector('div[role="dialog"]');
        if (!dialog) return false;
        return dialog.innerText.includes(email);
      }}, matchedEmail);

      if (!hasChip) {{
        console.log(`Adding recipient ${{matchedEmail}} to To field...`);
        const toInput = page.locator('div[role="dialog"] input[peoplekit-id], div[role="dialog"] input[aria-label="To recipients"]').first();
        if (await toInput.isVisible()) {{
          await toInput.fill(matchedEmail);
          await page.keyboard.press('Enter');
          await page.waitForTimeout(1000);
        }}
      }}
    }}

    // 4. Send via Ctrl+Enter
    console.log("Pressing Ctrl+Enter to send...");
    await page.keyboard.press('Control+Enter');
    await page.waitForTimeout(3000);

    // 5. Verify dialog closed
    const isClosed = await page.evaluate(() => {{
      const dialogs = document.querySelectorAll('div[role="dialog"]');
      return dialogs.length === 0;
    }});

    if (!isClosed) {{
      console.log("Dialog still open, clicking Send button directly via DOM");
      await page.evaluate(() => {{
        const dialog = document.querySelector('div[role="dialog"]');
        if (dialog) {{
          const sendBtn = dialog.querySelector('div[role="button"][data-tooltip*="Send"]') || dialog.querySelector('div[role="button"][aria-label*="Send"]');
          if (sendBtn) sendBtn.click();
        }}
      }});
      await page.waitForTimeout(2500);
    }}

    sentLogs.push({{ loop: loop + 1, subject: subjectInDialog || rowSubject.slice(0, 50), email: matchedEmail }});
  }}

  return {{ totalProcessed: sentLogs.length, details: sentLogs }};
}}
"""

out_file = r'E:\Extra\job-kit-starter\scratch\send_all_robust.js'
with open(out_file, 'w', encoding='utf-8') as f:
    f.write(js_script)

print("Generated scratch/send_all_robust.js")
