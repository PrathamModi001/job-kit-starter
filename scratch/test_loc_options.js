async (page) => {
  // 1. Phone country select via intl-tel-input
  await page.evaluate(() => {
    const itemIn = document.querySelector('#iti-0__item-in');
    if (itemIn) {
      itemIn.dispatchEvent(new MouseEvent('click', { bubbles: true }));
    }
  });

  // 2. Candidate Location: let's test what options appear when typing Bangalore
  const locInput = page.locator('#candidate-location');
  await locInput.click();
  await locInput.fill('Bangalore');
  await page.waitForTimeout(1000);

  return await page.evaluate(() => {
    const opts = Array.from(document.querySelectorAll('[role="option"], [id*="option"], [class*="option"]')).map(o => ({
      id: o.id,
      text: o.innerText
    }));
    return opts.filter(o => !o.id.startsWith('iti-0'));
  });
}
