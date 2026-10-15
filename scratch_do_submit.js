async (page) => {
  const res = await page.evaluate(() => {
    const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.includes('Submit application'));
    if (btn) {
      btn.scrollIntoView({ behavior: 'instant', block: 'center' });
      btn.click();
      return { clicked: true };
    }
    return { clicked: false };
  });
  await page.waitForTimeout(5000);
  const postSubmit = await page.evaluate(() => {
    return {
      url: window.location.href,
      bodyTextSnippet: document.body.innerText.slice(0, 1000),
      hasSuccess: /thank you|success|submitted|received/i.test(document.body.innerText)
    };
  });
  return { res, postSubmit };
}
