async (page) => {
  await page.keyboard.press('Escape');
  await page.waitForTimeout(500);

  const res = await page.evaluate(() => {
    function setReactInput(input, val) {
      const proto = window.HTMLInputElement.prototype;
      const setter = Object.getOwnPropertyDescriptor(proto, 'value')?.set;
      if (setter) {
        setter.call(input, val);
      } else {
        input.value = val;
      }
      input.dispatchEvent(new Event('input', { bubbles: true }));
      input.dispatchEvent(new Event('change', { bubbles: true }));
      input.dispatchEvent(new Event('blur', { bubbles: true }));
    }

    const textInputs = Array.from(document.querySelectorAll('input[type="text"].formTextInput'));
    
    // idx 0: Email
    if (textInputs[0]) setReactInput(textInputs[0], 'prathammodi001@gmail.com');
    // idx 1: Contact Number
    if (textInputs[1]) setReactInput(textInputs[1], '+91-9033393729');
    // idx 2: GitHub URL
    if (textInputs[2]) setReactInput(textInputs[2], 'https://github.com/PrathamModi001');
    // idx 3: Current Employer
    if (textInputs[3]) setReactInput(textInputs[3], 'C3iHub, IIT Kanpur');
    // idx 4: Expected CTC
    if (textInputs[4]) setReactInput(textInputs[4], '22 LPA');
    // idx 5: Current Location
    if (textInputs[5]) setReactInput(textInputs[5], 'Koramangala, Bengaluru, Karnataka');
    // idx 6: 10th Percentage
    if (textInputs[6]) setReactInput(textInputs[6], '91');
    // idx 7: 12th Percentage
    if (textInputs[7]) setReactInput(textInputs[7], '89');
    // idx 8: Undergraduate Percentage
    if (textInputs[8]) setReactInput(textInputs[8], '92');
    // idx 9: Postgraduate Percentage
    if (textInputs[9]) setReactInput(textInputs[9], 'NA');
    
    // idx 10: AI build
    const aiBuild = 'Built DeployMind, an autonomous deployment orchestrator that executes multi-stage deployment workflows from repository webhooks to cloud infrastructure. The architecture utilizes a state machine where state transitions are tracked across three autonomous worker processes: security static analysis, container build/image scanning, and cluster deployment. State persistence and distributed locking are managed via Redis key-value stores with conditional branching—triggering automated canary rollbacks upon metric degradation. The system interacts directly with Anthropic Claude 3.5 Sonnet and OpenAI GPT-4o APIs via structured JSON schemas and function calling to evaluate AST vulnerability reports, generate rollback runbooks, and decide execution paths without human intervention.';
    if (textInputs[10]) setReactInput(textInputs[10], aiBuild);

    // idx 11: Non-AI build
    const nonAiBuild = 'At C3iHub, IIT Kanpur, scaled the core LMS backend serving 50,000+ users across microservices handling high-concurrency event bursts. During a pan-India hackathon onboarding 10,000+ simultaneous participants, MongoDB p99 latency spiked past 450ms under heavy read/write contention on the collaborative round engine. Diagnosed unindexed compound queries and write-lock serialization. Implemented horizontal collection sharding and compound indexes on tenant and session IDs, combined with a Redis cluster write-through caching layer and Redis channel groups for race-condition-safe state synchronization. Furthermore, built an event-driven notification pipeline using Kafka consumer groups with consumer-side deduplication and exponential backoff dead-letter queues, dropping p99 database latency from 450ms down to 135ms and maintaining 99.9% uptime across 10,000+ concurrent WebSocket connections.';
    if (textInputs[11]) setReactInput(textInputs[11], nonAiBuild);

    // idx 12: Any Questions for us?
    if (textInputs[12]) setReactInput(textInputs[12], 'What are the primary technical challenges you are currently tackling as you scale DSP API throughput and transition backend components to microservices?');

    // Radios
    // Notice Period: Immediate (<15 Days)
    const radios = Array.from(document.querySelectorAll('input[type="radio"]'));
    for (const r of radios) {
      const label = r.closest('label')?.textContent?.trim();
      if (label === '<15 Days' || label === 'Immediate') {
        r.click();
        break;
      }
    }

    // Years of experience: 2-4 years
    for (const r of radios) {
      const label = r.closest('label')?.textContent?.trim();
      if (label === '2-4 years') {
        r.click();
        break;
      }
    }

    // Checkboxes
    const checkboxes = Array.from(document.querySelectorAll('input[type="checkbox"]'));
    for (const cb of checkboxes) {
      const label = cb.closest('label')?.textContent?.trim();
      if (['Yes', 'Python', 'Django', 'FastAPI', 'Go', 'Others'].includes(label)) {
        if (!cb.checked) cb.click();
      }
    }

    return {
      textInputsFilled: textInputs.length,
      checkedRadios: radios.filter(r => r.checked).map(r => r.closest('label')?.textContent?.trim()),
      checkedBoxes: checkboxes.filter(c => c.checked).map(c => c.closest('label')?.textContent?.trim())
    };
  });

  await page.waitForTimeout(1000);
  return res;
}
