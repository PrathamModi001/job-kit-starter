async (page) => {
  return await page.evaluate(async () => {
    async function selectOption(inputSelector, textToType, targetRegex) {
      const el = document.querySelector(inputSelector);
      if (!el) return 'Element not found: ' + inputSelector;
      el.focus();
      el.value = textToType;
      el.dispatchEvent(new Event('input', { bubbles: true }));
      el.dispatchEvent(new Event('change', { bubbles: true }));

      const control = el.closest('.select__control');
      const btn = control ? control.querySelector('button[aria-label="Toggle flyout"]') : null;
      if (btn) {
        btn.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true }));
        btn.dispatchEvent(new MouseEvent('mousedown', { bubbles: true }));
        btn.dispatchEvent(new MouseEvent('mouseup', { bubbles: true }));
        btn.dispatchEvent(new MouseEvent('click', { bubbles: true }));
      }

      await new Promise(r => setTimeout(r, 200));

      const options = Array.from(document.querySelectorAll('[role="option"], [class*="option"], [id*="option"]'))
        .filter(o => !o.id.startsWith('iti-0'));

      const match = options.find(o => targetRegex.test(o.innerText)) || options[0];
      if (match) {
        match.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true }));
        match.dispatchEvent(new MouseEvent('mousedown', { bubbles: true }));
        match.dispatchEvent(new MouseEvent('mouseup', { bubbles: true }));
        match.dispatchEvent(new MouseEvent('click', { bubbles: true }));
        return match.innerText.trim();
      }
      return 'None';
    }

    const school = await selectOption('#school--0', 'Pandit', /Pandit|Other/i);
    const degree = await selectOption('#degree--0', 'Bachelor', /Bachelor/i);
    return { school, degree };
  });
}
