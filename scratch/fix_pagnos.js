async (page) => {
  const filePath = 'E:\\Extra\\job-kit-starter\\job-kit-starter\\output\\Pratham_Modi_Base_Resume.pdf';
  
  // 1. Let's discard this broken draft if it exists
  const discardBtn = page.locator('div[role="dialog"] div[aria-label*="Discard draft"], div[role="dialog"] div[data-tooltip*="Discard draft"]').first();
  if (await discardBtn.isVisible()) {
    await discardBtn.click();
    await page.waitForTimeout(1500);
  }

  // 2. Click Compose
  await page.locator('div[role="button"]:has-text("Compose")').first().click();
  await page.waitForTimeout(1500);

  // 3. Fill To
  const toInput = page.locator('div[role="dialog"] input[aria-label="To recipients"], div[role="dialog"] input[peoplekit-id]').first();
  await toInput.fill('recruiting@pagnos.com');
  await page.keyboard.press('Enter');
  await page.waitForTimeout(500);

  // 4. Fill Subject
  const subjectInput = page.locator('div[role="dialog"] input[name="subjectbox"]').first();
  await subjectInput.fill('Serverless backends & Kafka telemetry for PAGNOS');
  await page.waitForTimeout(500);

  // 5. Fill Body
  const body = `Hi Team,

Saw PAGNOS scaling AWS serverless architectures and distributed cloud pipelines on HN.

At C3iHub (IIT Kanpur), I engineered event-driven pipelines handling 75k daily Kafka events at 99.5% delivery reliability with automated dead-letter queues. At Playpower Labs, I built microservices supporting 500+ concurrent WebSocket connections with sub-100ms response times.

Resume attached. GitHub's github.com/PrathamModi001 if you want to poke around the code. Open to chatting if there's a fit.

Pratham`;

  const bodyInput = page.locator('div[role="dialog"] div[role="textbox"][aria-label*="Message Body"]').first();
  await bodyInput.fill(body);
  await page.waitForTimeout(500);

  // 6. Attach file
  await page.setInputFiles('input[type="file"][name="Filedata"]', filePath);
  await page.waitForTimeout(3500); // wait for upload to complete

  // 7. Save and close draft
  const closeBtn = page.locator('div[role="dialog"] [aria-label="Save & close"]').first();
  if (await closeBtn.isVisible()) {
    await closeBtn.click();
    await page.waitForTimeout(1000);
  }

  return 'PAGNOS draft fixed and saved with attachment';
}
