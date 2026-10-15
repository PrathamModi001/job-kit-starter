async (page) => {
  const fixDates = await page.evaluate(() => {
    // Checkbox for Currently working here
    const cws = Array.from(document.querySelectorAll('input[type="checkbox"]'));
    // If not checked or if we can click it to disable end date
    // Let's check the date selects for work experience
    const selects = Array.from(document.querySelectorAll('select'));
    // In Webbtree's bug: "2024-11" vs "2025-6", it thinks November 2024 > June 2025 because string comparison "11" > "6"!
    // If "Currently working here" is checked, does End Date get hidden/disabled?
    // Let's check the currently working checkbox:
    const workingHereLabel = Array.from(document.querySelectorAll('label, div, span')).find(el => el.innerText && el.innerText.trim() === 'Currently working here');
    if (workingHereLabel) {
      workingHereLabel.click();
    }
    const chk = document.querySelector('input[value="iscurrent"]');
    if (chk && !chk.checked) {
      chk.click();
      chk.dispatchEvent(new Event('change', { bubbles: true }));
    }

    // Also if start date is Jul 2025 (current role at C3iHub), let's set company = C3iHub, IIT Kanpur
    const comp = document.querySelector('input[placeholder*="company" i]');
    if (comp) {
      comp.value = 'C3iHub, IIT Kanpur';
      comp.dispatchEvent(new Event('input', { bubbles: true }));
      comp.dispatchEvent(new Event('change', { bubbles: true }));
    }

    return {
      chkChecked: chk ? chk.checked : false
    };
  });

  await page.waitForTimeout(1000);
  return fixDates;
}
