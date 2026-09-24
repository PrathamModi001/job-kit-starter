async (page) => {
  // 1. Phone Country
  try {
    const country = page.locator('#country');
    await country.click();
    await country.pressSequentially('India', { delay: 80 });
    await page.waitForTimeout(600);
    // Find option that says India
    const inOpt = page.locator('[role="option"]').filter({ hasText: /India/i }).first();
    if (await inOpt.isVisible()) {
      await inOpt.click();
    } else {
      await page.keyboard.press('Enter');
    }
  } catch (e) {}

  // 2. Candidate Location
  try {
    const loc = page.locator('#candidate-location');
    await loc.click();
    await loc.pressSequentially('Bengaluru', { delay: 80 });
    await page.waitForTimeout(1000); // wait for geocoding
    const locOpt = page.locator('[role="option"]').first();
    if (await locOpt.isVisible()) {
      await locOpt.click();
    } else {
      await page.keyboard.press('ArrowDown');
      await page.keyboard.press('Enter');
    }
  } catch (e) {}

  await page.waitForTimeout(1000);

  // Return values
  return await page.evaluate(() => {
    return {
      country: document.querySelector('#country')?.closest('.select__control')?.innerText,
      location: document.querySelector('#candidate-location')?.closest('.select__control')?.innerText
    };
  });
}
