async (page) => {
  return await page.evaluate(async () => {
    async function selectOption(inputSelector, targetTextRegex) {
      const el = document.querySelector(inputSelector);
      if (!el) return 'Element not found: ' + inputSelector;
      const control = el.closest('.select__control');
      if (!control) return 'No control for ' + inputSelector;
      const btn = control.querySelector('button[aria-label="Toggle flyout"]');
      if (!btn) return 'No button for ' + inputSelector;

      btn.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true }));
      btn.dispatchEvent(new MouseEvent('mousedown', { bubbles: true }));
      btn.dispatchEvent(new MouseEvent('mouseup', { bubbles: true }));
      btn.dispatchEvent(new MouseEvent('click', { bubbles: true }));

      await new Promise(r => setTimeout(r, 150));

      const options = Array.from(document.querySelectorAll('[role="option"], [class*="option"], [id*="option"]'))
        .filter(o => !o.id.startsWith('iti-0'));

      const match = options.find(o => targetTextRegex.test(o.innerText));
      if (match) {
        match.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true }));
        match.dispatchEvent(new MouseEvent('mousedown', { bubbles: true }));
        match.dispatchEvent(new MouseEvent('mouseup', { bubbles: true }));
        match.dispatchEvent(new MouseEvent('click', { bubbles: true }));
        return match.innerText.trim();
      }
      return 'No match among ' + options.map(o => o.innerText).join(' | ');
    }

    const results = {};
    results['Privacy'] = await selectOption('#question_46985242', /understand|agree|yes|acknowledge/i);
    results['Gender'] = await selectOption('[id="864"]', /^Male$/i);
    results['Transgender'] = await selectOption('[id="1328"]', /^No$/i);
    results['Hispanic'] = await selectOption('[id="1332"]', /^No$/i);
    results['Race'] = await selectOption('[id="1333"]', /Asian/i);
    results['Veteran'] = await selectOption('[id="1336"]', /not a protected veteran|not/i);
    results['Disability'] = await selectOption('[id="1337"]', /do not have|no/i);

    return results;
  });
}
