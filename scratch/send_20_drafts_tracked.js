async (page) => {
  const sentResults = [];
  const maxSends = 20;

  for (let i = 0; i < maxSends; i++) {
    // Check if any draft row exists in the table
    const rowInfo = await page.evaluate(() => {
      const row = document.querySelector('tr[role="row"]');
      if (!row) return null;
      const text = row.innerText.replace(/\s+/g, ' ').trim();
      row.click();
      return text;
    });

    if (!rowInfo) {
      break;
    }

    // Wait for compose dialog to appear
    await page.waitForTimeout(2000);

    // Click Send button and extract recipient/subject
    const result = await page.evaluate((info) => {
      const dialog = document.querySelector('div[role="dialog"]') || document;
      const sendBtn = Array.from(dialog.querySelectorAll('div[role="button"]')).find(b => b.innerText && b.innerText.trim() === 'Send');
      
      const subjectInput = dialog.querySelector('input[name="subjectbox"]');
      const subject = subjectInput ? subjectInput.value : '';

      if (sendBtn) {
        sendBtn.click();
        return { success: true, text: info, subject: subject };
      }
      
      // Close if send button not found to prevent hanging
      const closeBtn = document.querySelector('img[aria-label="Save & close"], [aria-label="Save & close"]');
      if (closeBtn) closeBtn.click();
      return { success: false, text: info, error: 'Send button not found' };
    }, rowInfo);

    sentResults.push(result);
    if (!result.success) break;

    // Pace sends ~3 seconds apart
    await page.waitForTimeout(3000);
  }

  return sentResults;
}
