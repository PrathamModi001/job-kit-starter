async (page) => {
  const fields = [
    { id: '_systemfield_name', val: 'Pratham Modi', key: 'Name' },
    { id: '_systemfield_email', val: 'prathammodi001@gmail.com', key: 'Email' },
    { id: '6f9c9903-0146-41b7-b6eb-35575104087b', val: '+91-9033393729', key: 'Phone' },
    { id: '21ee1315-088b-47f1-bfe9-091e141792f3', val: 'https://www.linkedin.com/in/prathammodii001/', key: 'LinkedIn' },
    { id: '54de20b6-3976-4b62-a281-dddf833950aa', val: 'https://github.com/PrathamModi001', key: 'GitHub' },
    { id: '3880a764-8b4d-40e0-a580-338c758111d9', val: "I am deeply inspired by Sarvam AI's mission to build full-stack sovereign AI infrastructure for India. Having engineered high-throughput distributed backends (50K+ users, 10K+ concurrent connections, Kafka/Redis Streams) at C3iHub and low-latency vector retrieval / RAG microservices at Playpower Labs, I love building robust, containerized backend systems and MCP/agentic pipelines that run reliably in constrained, production enterprise environments.", key: 'WhySarvam' }
  ];

  const results = await page.evaluate((fieldsList) => {
    const filled = [];
    for (const f of fieldsList) {
      const el = document.getElementById(f.id);
      if (el) {
        el.focus();
        const proto = el.tagName === 'TEXTAREA' ? window.HTMLTextAreaElement.prototype : window.HTMLInputElement.prototype;
        const nativeSetter = Object.getOwnPropertyDescriptor(proto, 'value')?.set;
        if (nativeSetter) {
          nativeSetter.call(el, f.val);
        } else {
          el.value = f.val;
        }
        el.dispatchEvent(new Event('input', { bubbles: true }));
        el.dispatchEvent(new Event('change', { bubbles: true }));
        el.blur();
        filled.push(f.key + '=' + el.value);
      } else {
        filled.push(f.key + '=MISSING');
      }
    }
    return filled;
  }, fields);

  return results;
}