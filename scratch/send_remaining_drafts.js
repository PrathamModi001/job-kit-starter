async (page) => {
  const results = [];
  for (let i = 0; i < 9; i++) {
    // 1. Click first draft row
    const rowInfo = await page.evaluate(() => {
      const rows = Array.from(document.querySelectorAll('tr[role="row"]'));
      if (rows.length === 0) return null;
      const text = rows[0].innerText.replace(/\n+/g, ' ');
      rows[0].click();
      return text.slice(0, 80);
    });

    if (!rowInfo) {
      results.push({ index: i, error: 'no more rows found' });
      break;
    }

    // 2. Wait for composer dialog to open
    await page.waitForTimeout(2500);

    // 3. Click Send
    const sendResult = await page.evaluate(() => {
      const dialog = document.querySelector('div[role="dialog"]');
      if (!dialog) return { error: 'no dialog' };
      const sendBtn = dialog.querySelector('.aoO.v7, div[role="button"][data-tooltip*="Send"]');
      if (!sendBtn) return { error: 'no send button' };
      sendBtn.click();
      return { status: 'sent' };
    });

    results.push({ index: i, draftText: rowInfo, sendResult });

    // 4. Wait for email to send and draft row to be removed
    await page.waitForTimeout(3000);
  }

  const remainingDrafts = await page.evaluate(() => {
    return Array.from(document.querySelectorAll('tr[role="row"]')).map(r => r.innerText.replace(/\n+/g, ' '));
  });

  return { results, remainingDraftsCount: remainingDrafts.length, remainingDrafts };
}
