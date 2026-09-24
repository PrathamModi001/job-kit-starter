async (page) => {
  return await page.evaluate(async () => {
    // 1. Focus location input and type
    const locInput = document.querySelector('#candidate-location');
    locInput.focus();
    locInput.value = 'Bengaluru';
    locInput.dispatchEvent(new Event('input', { bubbles: true }));
    locInput.dispatchEvent(new Event('change', { bubbles: true }));

    // Wait for dropdown
    await new Promise(r => setTimeout(r, 1200));

    // List all visible options in DOM
    const opts = Array.from(document.querySelectorAll('[role="option"], [id*="option"], .select__option')).map(o => ({
      id: o.id,
      text: o.innerText
    }));

    return opts;
  });
}
