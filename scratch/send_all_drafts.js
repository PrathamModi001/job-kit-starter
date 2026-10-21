async (page) => {
  let count = 0;
  while (true) {
    // Check if any draft row exists
    const hasRow = await page.evaluate(() => {
      const row = document.querySelector('tr[role="row"]');
      return !!row;
    });

    if (!hasRow) {
      console.log('No more drafts found!');
      break;
    }

    // Click the first draft row
    const clickedText = await page.evaluate(() => {
      const row = document.querySelector('tr[role="row"]');
      if (row) {
        row.click();
        return row.innerText.replace(/\n+/g, ' | ').slice(0, 60);
      }
      return null;
    });

    if (!clickedText) break;

    // Wait for compose dialog to appear
    await page.waitForTimeout(2000);

    // Click Send button
    const sent = await page.evaluate(() => {
      const dialog = document.querySelector('div[role="dialog"]');
      if (!dialog) return false;
      const sendBtn = Array.from(dialog.querySelectorAll('div[role="button"]')).find(b => b.innerText && b.innerText.includes('Send'));
      if (sendBtn) {
        sendBtn.click();
        return true;
      }
      return false;
    });

    if (!sent) {
      console.log('Send button not found in dialog for: ' + clickedText);
      // Try closing dialog so we don't get stuck
      await page.evaluate(() => {
        const closeBtn = document.querySelector('img[aria-label="Save & close"], [aria-label="Save & close"]');
        if (closeBtn) closeBtn.click();
      });
      break;
    }

    count++;
    console.log(`[${count}] Sent: ${clickedText}`);
    await page.waitForTimeout(2500);
  }

  return { totalSent: count, pageTitle: await page.title() };
}
