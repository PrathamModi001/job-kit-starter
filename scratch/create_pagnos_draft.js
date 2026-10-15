async (page) => {
  const filePath = 'E:\\Extra\\job-kit-starter\\job-kit-starter\\output\\Pratham_Modi_Base_Resume.pdf';
  
  // 1. Click Compose button via DOM
  await page.evaluate(() => {
    const btn = Array.from(document.querySelectorAll('div[role="button"]')).find(b => b.innerText.includes('Compose'));
    if (btn) btn.click();
  });
  await page.waitForTimeout(2000);

  // 2. Fill To
  const toInput = page.locator('div[role="dialog"] input[aria-label="To recipients"], div[role="dialog"] input[peoplekit-id]').first();
  await toInput.fill('recruiting@pagnos.com');
  await page.keyboard.press('Enter');
  await page.waitForTimeout(500);

  // 3. Fill Subject
  const subjectInput = page.locator('div[role="dialog"] input[name="subjectbox"]').first();
  await subjectInput.fill('Serverless backends & Kafka telemetry for PAGNOS');
  await page.waitForTimeout(500);

  // 4. Fill Body
  const body = `Hi Team,

Saw PAGNOS scaling AWS serverless architectures and distributed cloud pipelines on HN.

At C3iHub (IIT Kanpur), I engineered event-driven pipelines handling 75k daily Kafka events at 99.5% delivery reliability with automated dead-letter queues. At Playpower Labs, I built microservices supporting 500+ concurrent WebSocket connections with sub-100ms response times.

Resume attached. GitHub's github.com/PrathamModi001 if you want to poke around the code. Open to chatting if there's a fit.

Pratham`;

  const bodyInput = page.locator('div[role="dialog"] div[role="textbox"][aria-label*="Message Body"]').first();
  await bodyInput.fill(body);
  await page.waitForTimeout(500);

  // 5. Attach file
  await page.setInputFiles('input[type="file"][name="Filedata"]', filePath);
  await page.waitForTimeout(4000); // wait for upload

  // 6. Close and save draft
  await page.evaluate(() => {
    const closeBtn = document.querySelector('div[role="dialog"] img[aria-label*="Save & close"]') || document.querySelector('div[role="dialog"] [aria-label*="Save & close"]');
    if (closeBtn) closeBtn.click();
  });
  await page.waitForTimeout(2000);

  return 'PAGNOS draft created with attachment and saved';
}
