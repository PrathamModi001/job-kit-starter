async (page) => {
  const sentResults = [];
  const maxSends = 20;

  for (let i = 0; i < maxSends; i++) {
    // Find a draft row (one that contains 'Draft')
    const clickedInfo = await page.evaluate(() => {
      const rows = Array.from(document.querySelectorAll('tr[role="row"]'));
      const draftRow = rows.find(r => r.innerText && r.innerText.includes('Draft'));
      if (!draftRow) return null;
      const text = draftRow.innerText.replace(/\s+/g, ' ').slice(0, 80);
      draftRow.click();
      return text;
    });

    if (!clickedInfo) {
      console.log('No more draft rows found.');
      break;
    }

    // Wait for compose dialog to appear
    await page.waitForTimeout(2500);

    // Click Send inside the compose dialog
    const sendResult = await page.evaluate((info) => {
      const dialog = document.querySelector('div[role="dialog"]') || document;
      const sendBtn = Array.from(dialog.querySelectorAll('div[role="button"]')).find(b => b.innerText && b.innerText.trim() === 'Send');
      const subjectInput = dialog.querySelector('input[name="subjectbox"]');
      const subject = subjectInput ? subjectInput.value : '';

      if (sendBtn) {
        sendBtn.click();
        return { success: true, text: info, subject: subject };
      }

      // Close if not found
      const closeBtn = document.querySelector('img[aria-label="Save & close"], [aria-label="Save & close"]');
      if (closeBtn) closeBtn.click();
      return { success: false, text: info, error: 'Send button not found' };
    }, clickedInfo);

    sentResults.push(sendResult);
    if (!sendResult.success) {
      break;
    }

    // Pace sends ~3.5 seconds apart to ensure clean dispatch and network throughput
    await page.waitForTimeout(3500);
  }

  return sentResults;
}
