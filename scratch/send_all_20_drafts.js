async (page) => {
  const sent = [];
  
  for (let i = 0; i < 25; i++) {
    // 1. Check if there are draft rows in the list
    const draftInfo = await page.evaluate(() => {
      const rows = Array.from(document.querySelectorAll('div[role="main"] tr[role="row"]'));
      if (rows.length === 0) return null;
      const r = rows[0];
      const subjectSpan = r.querySelector('.y6') || r.querySelector('span[data-legacy-thread-id]') || r;
      const subject = subjectSpan.innerText.trim();
      r.click();
      return { count: rows.length, subject };
    });

    if (!draftInfo) {
      console.log("No more draft rows found in Drafts folder.");
      break;
    }

    console.log(`[${i+1}] Opened draft: ${draftInfo.subject}`);
    await page.waitForTimeout(2000);

    // 2. Click Send in the open composer
    const sendResult = await page.evaluate(() => {
      const sendBtns = Array.from(document.querySelectorAll('div[role="button"]')).filter(b => {
        const label = ((b.getAttribute("aria-label") || "") + " " + (b.getAttribute("data-tooltip") || "") + " " + (b.innerText || "")).toLowerCase();
        return label.includes("send") && !label.includes("options") && !label.includes("schedule");
      });
      if (sendBtns.length > 0) {
        sendBtns[sendBtns.length - 1].click();
        return "CLICKED_SEND_BUTTON";
      }
      return null;
    });

    if (!sendResult) {
      console.log("Send button not found via selector, pressing Control+Enter");
      await page.keyboard.press("Control+Enter");
    }

    // 3. Wait for send to complete and draft list to refresh
    await page.waitForTimeout(3000);
    sent.push(draftInfo.subject);
  }

  return sent;
}
