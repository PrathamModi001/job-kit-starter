async (page) => {
  const sent = [];
  
  for (let i = 0; i < 10; i++) {
    // 1. Find the top draft row
    const rowExists = await page.evaluate(() => {
      const rows = Array.from(document.querySelectorAll('div[role="main"] tr[role="row"]'));
      if (rows.length === 0) return false;
      const r = rows[0];
      const subject = r.querySelector('.y6')?.innerText || r.innerText.slice(0, 50);
      r.click();
      return subject;
    });

    if (!rowExists) {
      console.log("No more draft rows found");
      break;
    }

    console.log(`Opened draft: ${rowExists}`);
    await page.waitForTimeout(2000);

    // 2. Click Send in the open composer
    const clickedSend = await page.evaluate(() => {
      const sendBtns = Array.from(document.querySelectorAll('div[role="button"]')).filter(b => {
        const label = (b.getAttribute("aria-label") || "") + " " + (b.getAttribute("data-tooltip") || "") + " " + b.innerText;
        return label.includes("Send") && !label.includes("options");
      });
      if (sendBtns.length > 0) {
        sendBtns[sendBtns.length - 1].click();
        return true;
      }
      return false;
    });

    if (!clickedSend) {
      console.log("Send button not found via click, trying keyboard Ctrl+Enter");
      await page.keyboard.press("Control+Enter");
    }

    // 3. Wait for send to complete and draft list to refresh
    await page.waitForTimeout(3000);
    sent.push(rowExists);
  }

  return sent;
}