async (page) => {
  const submitBtn = page.locator('button:has-text("Submit Application")');
  await submitBtn.click();

  // Wait up to 10 seconds for navigation or confirmation message
  await page.waitForTimeout(5000);

  return {
    url: page.url(),
    title: await page.title(),
    headings: await page.locator('h1, h2, h3').allInnerTexts(),
    bodySnippet: (await page.locator('body').innerText()).slice(0, 500)
  };
}