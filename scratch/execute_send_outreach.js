async (page) => {
  const sent = [];

  for (let i = 0; i < 10; i++) {
    // Check if dialog is currently open
    let dialogOpen = await page.evaluate(() => {
      const dialog = document.querySelector('div[role="dialog"]');
      return !!dialog;
    });

    if (!dialogOpen) {
      // Click the first draft row in drafts view
      const rowInfo = await page.evaluate(() => {
        const rows = Array.from(document.querySelectorAll('div[role="main"] tr[role="row"]'));
        if (rows.length === 0) return null;
        const text = rows[0].innerText.replace(/\n+/g, ' ');
        rows[0].click();
        return text.slice(0, 80);
      });

      if (!rowInfo) {
        console.log("No more draft rows found");
        break;
      }
      await page.waitForTimeout(2500);
    }

    // Now send the open dialog
    const res = await page.evaluate(() => {
      const dialog = document.querySelector('div[role="dialog"]');
      if (!dialog) return { error: 'no dialog' };
      const to = dialog.querySelector('input[aria-label="To recipients"], input[peoplekit-id]')?.value || dialog.querySelector('span[email]')?.getAttribute('email') || 'unknown';
      const subject = dialog.querySelector('input[name="subjectbox"]')?.value || 'unknown';
      const sendBtn = dialog.querySelector('.aoO.v7, div[role="button"][data-tooltip*="Send"]');
      if (sendBtn) {
        sendBtn.click();
        return { status: 'sent', to, subject };
      }
      return { error: 'no send button', to, subject };
    });

    sent.push(res);
    await page.waitForTimeout(3500);
  }

  return sent;
}
