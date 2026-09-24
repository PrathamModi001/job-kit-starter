async (page) => {
  const ans1 = "I would build an autonomous software reliability engine—an agentic platform that doesn't just surface alerts and distributed traces, but autonomously diagnoses distributed system failures, synthesizes deterministic rollback and remediation PRs, verifies them in isolated ephemeral container sandboxes, and executes canary rollouts with formal safety proofs. Having built DeployMind (automated container sandboxes) and instrumented OpenTelemetry across 15+ microservices at C3iHub (IIT Kanpur), I've seen how much high-leverage engineering bandwidth is burned fighting distributed state drift and flaky pipelines. Making cloud infrastructure self-healing and deterministic at global scale is the problem I think about constantly.";

  const ans2 = "Architecting the distributed event-driven LMS backend at C3iHub (IIT Kanpur) to sustain 10,000+ concurrent connections and 75K+ daily events with 99.9% uptime: slashing MongoDB p99 latency from 450ms to 135ms through horizontal sharding and compound indexes, implementing BullMQ/Kafka queues with consumer deduplication and DLQs, and deploying OpenTelemetry across 15+ microservices to reduce incident MTTR by 85%.";

  await page.locator("textarea").fill(ans1);
  await page.waitForTimeout(500);

  await page.locator("input[type='text']").fill(ans2);
  await page.waitForTimeout(500);

  await page.getByRole("button", { name: "Submit" }).click();
  await page.waitForTimeout(3000);

  return "submitted";
}