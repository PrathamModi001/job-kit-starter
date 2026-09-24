async (page) => {
  return await page.evaluate(async () => {
    async function selectOption(inputSelector, textToType, targetTextRegex) {
      const el = document.querySelector(inputSelector);
      if (!el) return 'Element not found: ' + inputSelector;
      
      const control = el.closest('.select__control');
      if (!control) return 'No control';
      
      const btn = control.querySelector('button[aria-label="Toggle flyout"]');
      if (btn) {
        btn.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true }));
        btn.dispatchEvent(new MouseEvent('mousedown', { bubbles: true }));
        btn.dispatchEvent(new MouseEvent('mouseup', { bubbles: true }));
        btn.dispatchEvent(new MouseEvent('click', { bubbles: true }));
      } else {
        el.focus();
      }

      if (textToType) {
        el.value = textToType;
        el.dispatchEvent(new Event('input', { bubbles: true }));
        el.dispatchEvent(new Event('change', { bubbles: true }));
      }

      await new Promise(r => setTimeout(r, 400));

      const options = Array.from(document.querySelectorAll('[role="option"], [class*="option"], [id*="option"]'))
        .filter(o => !o.id.startsWith('iti-0'));

      const match = options.find(o => targetTextRegex.test(o.innerText)) || options[0];
      if (match) {
        match.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true }));
        match.dispatchEvent(new MouseEvent('mousedown', { bubbles: true }));
        match.dispatchEvent(new MouseEvent('mouseup', { bubbles: true }));
        match.dispatchEvent(new MouseEvent('click', { bubbles: true }));
        return match.innerText.trim();
      }
      return 'No match among ' + options.map(o => o.innerText).join(' | ');
    }

    const countryRes = await selectOption('#country', 'India', /^India$/i);
    const locRes = await selectOption('#candidate-location', 'Bengaluru', /Bengaluru|Bangalore/i);

    return { countryRes, locRes };
  });
}
