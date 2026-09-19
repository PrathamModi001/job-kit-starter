async (page) => {
  const pitch = `Hi Suraj,

I saw Uniprep's opening for a Java Developer and wanted to reach out directly.

At C3iHub, IIT Kanpur, I architected core microservices serving 50K+ users with 99.9% uptime at 10,000+ concurrent connections. My background spans building resilient RESTful APIs and microservices in Java and Python, optimizing database queries (cutting p99 latency from 450ms to 135ms via indexing and Redis caching), and managing event-driven pipelines handling 75K+ daily events via Kafka.

I'm very comfortable designing clean data models, optimizing backend throughput, and maintaining scalable production services. I would love to contribute to Uniprep's backend infrastructure.

Best regards,
Pratham Modi
prathammodi001@gmail.com | +91-9033393729`;

  const textarea = page.locator('textarea');
  await textarea.fill(pitch);
  await page.waitForTimeout(1000);
  return 'Filled pitch';
}
