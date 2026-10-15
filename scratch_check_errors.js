async (page) => {
  const formValidation = await page.evaluate(() => {
    const invalidInputs = Array.from(document.querySelectorAll('input:invalid, select:invalid, textarea:invalid')).map(el => ({
      tag: el.tagName,
      placeholder: el.placeholder,
      name: el.name,
      validationMessage: el.validationMessage
    }));

    // Also look for error text or red labels
    const errorEls = Array.from(document.querySelectorAll('.error, .invalid-feedback, .text-danger, [class*="error" i]')).map(el => el.innerText.trim()).filter(Boolean);

    return { invalidInputs, errorEls };
  });

  return formValidation;
}
