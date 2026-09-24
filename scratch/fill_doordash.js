async (page) => {
  const resumePath = '/home/modi/Work/job-kit-starter/job-kit-starter/output/DoorDash - Software Engineer, Backend/Pratham_Modi_Resume.pdf';

  // 1. Fill basic text fields
  await page.locator('#first_name').fill('Pratham');
  await page.locator('#last_name').fill('Modi');
  await page.locator('#email').fill('prathammodi001@gmail.com');
  await page.locator('#phone').fill('9033393729');

  // Country select
  try {
    await page.locator('#country').fill('India');
    await page.waitForTimeout(500);
    const indiaOpt = page.locator('[role="option"]').filter({ hasText: 'India' }).first();
    if (await indiaOpt.isVisible()) await indiaOpt.click();
  } catch (e) {}

  // Location
  try {
    await page.locator('#candidate-location').fill('Bengaluru, Karnataka, India');
    await page.waitForTimeout(500);
    const locOpt = page.locator('[role="option"]').first();
    if (await locOpt.isVisible()) await locOpt.click();
  } catch (e) {}

  // 2. Upload tailored resume
  await page.locator('#resume').setInputFiles(resumePath);
  await page.waitForTimeout(1500);

  // 3. Education
  try {
    await page.locator('#school--0').fill('Pandit Deendayal Energy University');
    await page.waitForTimeout(500);
    const schoolOpt = page.locator('[role="option"]').first();
    if (await schoolOpt.isVisible()) await schoolOpt.click();
  } catch (e) {}

  try {
    await page.locator('#degree--0').fill("Bachelor's Degree");
    await page.waitForTimeout(500);
    const degreeOpt = page.locator('[role="option"]').first();
    if (await degreeOpt.isVisible()) await degreeOpt.click();
  } catch (e) {}

  // 4. Custom questions
  await page.locator('#question_46985239').fill('https://www.linkedin.com/in/prathammodii001/');

  // Have you worked at DoorDash?
  try {
    await page.locator('#question_46985241').click();
    await page.locator('#question_46985241').fill('No');
    await page.waitForTimeout(400);
    const noOpt = page.locator('[role="option"]').filter({ hasText: 'No' }).first();
    if (await noOpt.isVisible()) await noOpt.click();
  } catch (e) {}

  // Relocation to Pune
  await page.locator('#question_63930318').fill('Currently based in Bengaluru, Karnataka; fully open and willing to relocate to Pune immediately.');

  // Compensation Expectation
  await page.locator('#question_63930319').fill('20 LPA');

  // Notice Period
  await page.locator('#question_63992617').fill('Immediate');

  // Privacy Acknowledgement
  try {
    await page.locator('#question_46985242').click();
    await page.waitForTimeout(400);
    const ackOpt = page.locator('[role="option"]').first();
    if (await ackOpt.isVisible()) await ackOpt.click();
  } catch (e) {}

  // Survey comboboxes
  const surveySelects = [
    { id: '#\\38 64, [id="864"]', val: 'Male' },
    { id: '#\\31 328, [id="1328"]', val: 'No' },
    { id: '#\\31 332, [id="1332"]', val: 'No' },
    { id: '#\\31 333, [id="1333"]', val: 'Asian' },
    { id: '#\\31 336, [id="1336"]', val: 'not' },
    { id: '#\\31 337, [id="1337"]', val: 'No' }
  ];

  for (const s of surveySelects) {
    try {
      const loc = page.locator(s.id).first();
      if (await loc.isVisible()) {
        await loc.click();
        await page.waitForTimeout(300);
        await loc.fill(s.val);
        await page.waitForTimeout(300);
        const opt = page.locator('[role="option"]').filter({ hasText: new RegExp(s.val, 'i') }).first();
        if (await opt.isVisible()) await opt.click();
      }
    } catch (e) {}
  }

  await page.waitForTimeout(1000);
  return 'Form filled successfully';
}
