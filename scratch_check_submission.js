async (page) => {
  const check = await page.evaluate(() => {
    // Check if form is still there or if there's a modal/alert/toast
    const toasts = Array.from(document.querySelectorAll('.toast, .alert, .modal, [class*="success" i], [class*="message" i]')).map(el => el.innerText.trim()).filter(Boolean);
    const formHeading = document.querySelector('h6');
    const submitBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.includes('Submit application'));
    return {
      toasts,
      formHeadingText: formHeading?.innerText,
      submitBtnPresent: !!submitBtn,
      bodyTextFullLength: document.body.innerText.length
    };
  });
  return check;
}
