async (page) => {
  const pitch = `Hi Surya,

I came across WarpBuild's mission to supercharge CI and developer loops with 10x faster runners, and I'd love to contribute as your GTM / Developer Platform Engineer.

Why I'm a strong technical & product fit:
1. Hands-on Developer Tooling & GitOps: Built DeployMind (https://github.com/PrathamModi001/DeployMind), an automated GitOps platform containerizing applications to Kubernetes and EC2 via dynamic Docker daemon sandboxes with canary deployments and automated rollback.
2. Distributed Production Systems: At C3iHub (IIT Kanpur), I architected backend infrastructure serving 50K+ users (10K+ concurrent WebSocket connections), deployed OpenTelemetry distributed tracing across 15+ microservices, and reduced cloud storage costs by 60%.
3. Technical Communication & Customer Growth: Experienced in writing deep technical documentation, architectural walkthroughs, and developer-facing tooling that turns complex infrastructure into intuitive experiences.

Bonus poem from the job description:
"Pipelines green and runners swift,
Containers spin, the branches shift.
From commit hash to cluster node,
We build the rails that ship the code."

I'd love to chat about scaling developer adoption and automating customer growth at WarpBuild!

Best regards,
Pratham Modi
prathammodi001@gmail.com | +91-9033393729
https://github.com/PrathamModi001 | https://linkedin.com/in/prathammodii001`;

  const textarea = page.locator('textarea');
  await textarea.fill(pitch);
  await page.waitForTimeout(1000);
  const sendBtn = page.getByRole('button', { name: 'Send' });
  await sendBtn.click();
  await page.waitForTimeout(3000);
  return 'submitted';
}
