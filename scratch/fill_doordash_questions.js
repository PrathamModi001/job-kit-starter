async (page) => {
  // 1. Education
  try {
    const school = page.locator('#school--0');
    await school.click();
    await school.fill('Pandit Deendayal Energy University');
    await page.waitForTimeout(600);
    const sOpt = page.locator('[role="option"]').first();
    if (await sOpt.isVisible()) await sOpt.click();
    else await page.keyboard.press('Enter');
  } catch (e) {}

  try {
    const deg = page.locator('#degree--0');
    await deg.click();
    await deg.fill("Bachelor's Degree");
    await page.waitForTimeout(600);
    const dOpt = page.locator('[role="option"]').first();
    if (await dOpt.isVisible()) await dOpt.click();
    else await page.keyboard.press('Enter');
  } catch (e) {}

  // 2. LinkedIn Profile
  await page.locator('#question_46985239').fill('https://www.linkedin.com/in/prathammodii001/');

  // 3. Have you worked at DoorDash?
  try {
    const q1 = page.locator('#question_46985241');
    await q1.click();
    await q1.fill('No');
    await page.waitForTimeout(400);
    const noOpt = page.locator('[role="option"]').filter({ hasText: /^No$/i }).first();
    if (await noOpt.isVisible()) await noOpt.click();
    else await page.keyboard.press('Enter');
  } catch (e) {}

  // 4. Current location & relocation to Pune
  await page.locator('#question_63930318').fill('Currently based in Bengaluru, Karnataka; fully open and willing to relocate to Pune immediately.');

  // 5. Compensation Expectation
  await page.locator('#question_63930319').fill('20 LPA');

  // 6. Notice Period
  await page.locator('#question_63992617').fill('Immediate');

  // 7. Privacy Acknowledgement
  try {
    const qAck = page.locator('#question_46985242');
    await qAck.click();
    await page.waitForTimeout(400);
    const ackOpt = page.locator('[role="option"]').first();
    if (await ackOpt.isVisible()) await ackOpt.click();
    else {
      await page.keyboard.press('ArrowDown');
      await page.keyboard.press('Enter');
    }
  } catch (e) {}

  // 8. Voluntary Demographic Survey
  const surveyIds = ['864', '1328', '1332', '1333', '1336', '1337'];
  const surveyVals = ['Male', 'No', 'No', 'Asian', 'not', 'No'];

  for (let i = 0; i < surveyIds.length; i++) {
    try {
      const el = page.locator(`[id="${surveyIds[i]}"]`).first();
      if (await el.isVisible()) {
        await el.click();
        await page.waitForTimeout(300);
        await el.fill(surveyVals[i]);
        await page.waitForTimeout(300);
        const opt = page.locator('[role="option"]').filter({ hasText: new RegExp(surveyVals[i], 'i') }).first();
        if (await opt.isVisible()) await opt.click();
        else {
          await page.keyboard.press('ArrowDown');
          await page.keyboard.press('Enter');
        }
      }
    } catch (e) {}
  }

  await page.waitForTimeout(1000);
  return 'Questions and survey completed';
}
