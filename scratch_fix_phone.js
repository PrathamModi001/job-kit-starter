async (page) => {
  const phoneRes = await page.evaluate(() => {
    const ph = document.querySelector('input[placeholder*="contact" i], input[placeholder*="phone" i]');
    if (ph) {
      ph.focus();
      ph.value = '+919033393729';
      ph.dispatchEvent(new Event('input', { bubbles: true }));
      ph.dispatchEvent(new Event('change', { bubbles: true }));
      return { found: true, val: ph.value };
    }
    return { found: false };
  });

  await page.waitForTimeout(500);

  // Check errors again
  const errors = await page.evaluate(() => {
    return Array.from(document.querySelectorAll('.error, .invalid-feedback, .text-danger, [class*="error" i]')).map(el => el.innerText.trim()).filter(Boolean);
  });

  return { phoneRes, errors };
}
