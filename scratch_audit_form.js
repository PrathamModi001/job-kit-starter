async (page) => {
  const audit = await page.evaluate(() => {
    const inputs = Array.from(document.querySelectorAll('input, select, textarea')).map(el => {
      let label = '';
      if (el.placeholder) label = el.placeholder;
      else if (el.name) label = el.name;
      else if (el.id) label = el.id;
      else {
        let p = el.parentElement;
        while (p && !p.innerText.trim()) p = p.parentElement;
        label = p ? p.innerText.split('\n')[0].trim() : el.tagName;
      }
      return {
        tag: el.tagName,
        type: el.type,
        label,
        value: el.value,
        checked: el.checked
      };
    }).filter(i => i.type !== 'hidden');

    return { inputs };
  });

  return audit;
}
