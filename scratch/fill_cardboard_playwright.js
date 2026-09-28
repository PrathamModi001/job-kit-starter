async (page) => {
  const fields = [
    { sel: '#_systemfield_name', val: 'Pratham Modi' },
    { sel: '#_systemfield_email', val: 'prathammodi001@gmail.com' },
    { sel: '[name="82ba5c30-ce3f-4948-82c3-271f3fe4f563"]', val: 'https://www.linkedin.com/in/prathammodii001/' },
    { sel: '[name="31e3978d-5437-44e4-be2a-5f794493ad0c"]', val: 'https://github.com/PrathamModi001' },
    { sel: '[name="db066833-07d9-4e74-be58-c1e7e65255c7"]', val: 'https://prathammodi.dev' },
    { sel: '[name="b3231537-d95c-40dd-868c-6989ee814d99"]', val: '1.5 years experience, 2024 graduate (B.Tech in Computer Science)' },
    { sel: '[name="9a698396-b84b-44ea-83ca-3158a9e87f59"]', val: 'Linear, because of its uncompromising keyboard-first ergonomics, instant local-first optimistic updates, and rock-solid sync architecture.' },
    { sel: '[name="faa800a4-8136-45f2-bc62-fdd6676f2ce0"]', val: 'Built and deployed an automated GitOps container deployment platform (DeployMind) orchestrating isolated Docker build sandboxes, WebSocket log streaming, and zero-downtime microservice rollouts.' }
  ];

  for (const f of fields) {
    const loc = page.locator(f.sel);
    await loc.click();
    await loc.fill(f.val);
  }

  await page.waitForTimeout(1000);

  // Check if errors disappeared
  const errorText = await page.evaluate(() => {
    const err = document.querySelector('[class*="error"], [class*="alert"], [class*="banner"]');
    return err ? err.innerText : 'none';
  });

  return { filled: true, errorText };
}
