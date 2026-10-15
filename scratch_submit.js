async (page) => {
  const submitBtn = page.getByRole("button", { name: "Submit application" });
  if (await submitBtn.count() > 0) {
    await submitBtn.click();
    await page.waitForTimeout(5000);
    return { clicked: true, url: page.url() };
  }
  return { clicked: false, error: "Submit button not found" };
}
