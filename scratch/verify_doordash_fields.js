async (page) => {
  return await page.evaluate(() => {
    const requiredInputs = [];
    document.querySelectorAll('[aria-required="true"], input[required], select[required], textarea[required]').forEach(el => {
      const id = el.id || el.name || el.getAttribute('aria-label');
      const val = el.value || el.innerText || (el.closest('.select__control') ? el.closest('.select__control').innerText : '');
      requiredInputs.push({
        id: id,
        tag: el.tagName,
        ariaLabel: el.getAttribute('aria-label'),
        value: val.replace(/\n/g, ' ')
      });
    });
    return requiredInputs;
  });
}
