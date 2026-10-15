async (page) => {
  const info = await page.evaluate(() => {
    const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.includes('Submit application'));
    if (!btn) return { found: false };
    const rect = btn.getBoundingClientRect();
    const style = window.getComputedStyle(btn);
    return {
      found: true,
      text: btn.innerText,
      disabled: btn.disabled,
      rect: { top: rect.top, left: rect.left, width: rect.width, height: rect.height },
      style: {
        display: style.display,
        visibility: style.visibility,
        opacity: style.opacity,
        pointerEvents: style.pointerEvents
      }
    };
  });
  return info;
}
