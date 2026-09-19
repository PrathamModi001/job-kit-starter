async (page) => {
  const filePath = '/home/modi/Work/job-kit-starter/job-kit-starter/output/base_resume/Pratham_Modi_Resume.pdf';
  
  // 1. Fill To
  const toInput = page.locator('input[aria-label="To recipients"], input[peoplekit-id]').first();
  await toInput.fill('surya@warpbuild.com');
  await page.keyboard.press('Enter');
  await page.waitForTimeout(500);

  // 2. Fill Subject
  const subjectInput = page.locator('input[name="subjectbox"]');
  await subjectInput.fill('Accelerating developer loops and CI runners for WarpBuild');
  await page.waitForTimeout(500);

  // 3. Fill Body
  const body = `Hi Surya,

I've been following WarpBuild's mission to eliminate CI bottlenecks with 10x faster GitHub Actions runners, and I'd love to contribute as an early Developer Platform / GTM Engineer.

Why I can hit the ground running:
- Developer Platforms & GitOps: Built DeployMind (https://github.com/PrathamModi001/DeployMind), an automated GitOps platform containerizing applications via dynamic Docker daemon sandboxes to Kubernetes/EC2 with automated canary rollouts.
- High-Throughput Production Systems: At C3iHub (IIT Kanpur), I architected distributed services serving 50K+ users (10,000+ concurrent connections), deployed OpenTelemetry distributed tracing across 15+ microservices, and cut cloud storage costs 60%.
- Technical Communication: Passionate about writing deep technical docs, architectural walkthroughs, and building developer-facing tooling that turns infrastructure into intuitive workflows.

Attached is my base resume and pinned GitHub (https://github.com/PrathamModi001). Would love to chat about scaling runner adoption and automating customer growth at WarpBuild!

Best regards,
Pratham Modi
prathammodi001@gmail.com | +91-9033393729
https://linkedin.com/in/prathammodii001`;

  const bodyInput = page.locator('div[role="textbox"][aria-label*="Message Body"]');
  await bodyInput.fill(body);
  await page.waitForTimeout(500);

  // 4. Attach file
  await page.setInputFiles('input[type="file"][name="Filedata"]', filePath);
  await page.waitForTimeout(3000); // wait for upload to complete

  // 5. Close and save draft
  const closeBtn = page.locator('[aria-label="Save & close"]').first();
  await closeBtn.click();
  await page.waitForTimeout(1000);

  return 'Draft 1 created with attachment and saved';
}
