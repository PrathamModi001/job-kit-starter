async (page) => {
  const result = await page.evaluate(() => {
    // Select elements
    const selects = Array.from(document.querySelectorAll('select'));
    const selectLogs = [];

    // Let's set each select appropriately
    // 0: Job start month (July)
    // 1: Job start year (2025)
    // 2: Job end month (leave or select)
    // 3: Job end year
    // 4: Edu start month (July or August)
    // 5: Edu start year (2021)
    // 6: Edu end month (May or June)
    // 7: Edu end year (2025)

    const setSelectByText = (sel, text) => {
      if (!sel) return false;
      for (let i = 0; i < sel.options.length; i++) {
        if (sel.options[i].text.toLowerCase() === text.toLowerCase()) {
          sel.selectedIndex = i;
          sel.dispatchEvent(new Event('change', { bubbles: true }));
          return true;
        }
      }
      return false;
    };

    selects.forEach((s, idx) => {
      selectLogs.push({ idx, name: s.name, id: s.id, current: s.value, optionsCount: s.options.length });
    });

    if (selects.length >= 2) {
      setSelectByText(selects[0], 'July');
      setSelectByText(selects[1], '2025');
    }
    if (selects.length >= 6) {
      setSelectByText(selects[selects.length - 4], 'July');
      setSelectByText(selects[selects.length - 3], '2021');
      setSelectByText(selects[selects.length - 2], 'May');
      setSelectByText(selects[selects.length - 1], '2025');
    }

    return { selectCount: selects.length, selectLogs };
  });

  return result;
}
