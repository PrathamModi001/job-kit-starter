async (page) => {
  const sent = [];

  for (let i = 0; i < 5; i++) {
    // 1. Check if dialog is open
    let dialogOpen = await page.evaluate(() => {
      const dialog = document.querySelector('div[role="dialog"]');
      return !!dialog;
    });

    if (!dialogOpen) {
      const opened = await page.evaluate(() => {
        const rows = Array.from(document.querySelectorAll('div[role="main"] tr[role="row"]'));
        if (rows.length === 0) return null;
        rows[0].click();
        return true;
      });

      if (!opened) {
        sent.push({ error: 'No more draft rows' });
        break;
      }
      await page.waitForTimeout(2500);
    }

    // 2. Extract info and click Send
    const sendResult = await page.evaluate(() => {
      const dialog = document.querySelector('div[role="dialog"]');
      if (!dialog) return { error: 'No dialog found' };

      const to = dialog.querySelector('span[email]')?.getAttribute('email') || 
                 dialog.querySelector('input[aria-label*="To"], input[peoplekit-id]')?.value || 
                 dialog.querySelector('.vR .vN')?.innerText || 'unknown';
      const subject = dialog.querySelector('input[name="subjectbox"]')?.value || 'unknown';
      const attachment = dialog.querySelector('.aV3')?.innerText || 'none';

      const sendBtn = dialog.querySelector('.aoO.v7, div[role="button"][data-tooltip*="Send"], [aria-label*="Send"]');
      if (sendBtn) {
        sendBtn.click();
        return { status: 'sent', to, subject, attachment };
      }
      return { error: 'Send button not found', to, subject, attachment };
    });

    if (sendResult.error === 'Send button not found') {
      await page.keyboard.press('Control+Enter');
      sendResult.status = 'sent_via_hotkey';
    }

    sent.push(sendResult);
    await page.waitForTimeout(4000);
  }

  return sent;
}