async (page) => {
  const sent = [];
  const MAX_PER_BATCH = 25; // Can send all remaining drafts
  
  for (let i = 0; i < MAX_PER_BATCH; i++) {
    // Check how many drafts remain
    const draftText = await page.evaluate(() => {
      const rows = Array.from(document.querySelectorAll('div[role="main"] tr[role="row"]'));
      if (rows.length === 0) return null;
      const r = rows[0];
      const text = r.innerText.replace(/\n+/g, ' | ');
      // Click row to open compose modal
      r.click();
      return text;
    });

    if (!draftText) {
      console.log("No more draft rows found in main table.");
      break;
    }

    console.log(`[Draft ${i+1}] Opened: ${draftText.slice(0, 70)}`);
    await page.waitForTimeout(2000);

    // Click Send
    const clicked = await page.evaluate(() => {
      const dialog = document.querySelector('div[role="dialog"]');
      if (dialog) {
        const sendBtns = Array.from(dialog.querySelectorAll('div[role="button"]')).filter(b => {
          const label = (b.getAttribute("aria-label") || "") + " " + (b.getAttribute("data-tooltip") || "") + " " + b.innerText;
          return label.includes("Send") && !label.includes("options") && !label.includes("Schedule");
        });
        if (sendBtns.length > 0) {
          sendBtns[sendBtns.length - 1].click();
          return true;
        }
      }
      // Fallback to document query
      const sendBtns = Array.from(document.querySelectorAll('div[role="button"]')).filter(b => {
        const label = (b.getAttribute("aria-label") || "") + " " + (b.getAttribute("data-tooltip") || "") + " " + b.innerText;
        return label.includes("Send") && !label.includes("options") && !label.includes("Schedule");
      });
      if (sendBtns.length > 0) {
        sendBtns[sendBtns.length - 1].click();
        return true;
      }
      return false;
    });

    if (!clicked) {
      console.log("Clicking Send button failed, using Ctrl+Enter");
      await page.keyboard.press("Control+Enter");
    }

    // Wait for email to send and draft row to be removed
    await page.waitForTimeout(2500);
    sent.push(draftText.slice(0, 90));
  }

  return { totalSent: sent.length, sent };
}
