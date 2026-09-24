async (page) => {
  // Fill email
  const emailInput = page.locator('input[data-automation-id="email"]');
  await emailInput.fill('prathammodi001@gmail.com');

  // Fill password
  const passInput = page.locator('input[data-automation-id="password"]');
  await passInput.fill('NCRApply#2026PM');

  // Fill verify password
  const verifyPassInput = page.locator('input[data-automation-id="verifyPassword"]');
  await verifyPassInput.fill('NCRApply#2026PM');

  // Check terms checkbox
  const checkbox = page.locator('input[data-automation-id="createAccountCheckbox"]');
  await checkbox.check({ force: true });

  await page.waitForTimeout(1000);

  // Click submit button / filter
  const submitTarget = page.locator('div[aria-label="Create Account"][role="button"]');
  if (await submitTarget.count() > 0) {
    await submitTarget.click({ force: true });
  } else {
    await page.locator('button[data-automation-id="createAccountSubmitButton"]').click({ force: true });
  }

  // Wait 5 seconds for response
  await page.waitForTimeout(5000);

  return {
    url: page.url(),
    title: await page.title(),
    headings: await page.locator('h1, h2, h3').allInnerTexts(),
    bodySnippet: (await page.locator('body').innerText()).slice(0, 400)
  };
}