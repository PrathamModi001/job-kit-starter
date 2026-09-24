async (page) => {
  // Fill text fields
  await page.locator('#_systemfield_name').fill('Pratham Modi');
  await page.locator('#_systemfield_email').fill('prathammodi001@gmail.com');
  await page.locator('[id="2953e314-ca27-4d2b-8c40-a8197a325a49"]').fill('Bengaluru, Karnataka, India');
  await page.locator('[id="e49092dd-c589-4165-8cb1-4f348dd7b940"]').fill('+919033393729');
  await page.locator('[id="74a9bab8-ba3a-42e8-ab40-876aff50a3ed"]').fill('https://www.linkedin.com/in/prathammodii001/');
  await page.locator('[id="def8cf92-0f00-44d7-9987-57821eb9676c"]').fill('https://github.com/PrathamModi001');
  await page.locator('[id="32178e06-7bfc-41d2-a9d0-96fb5bf6551a"]').fill('https://prathammodi.dev');
  
  // Visa sponsorship radio: No
  const radioNo = page.locator('input[id*="labeled-radio-1"]');
  await radioNo.check();

  // Resume upload via setInputFiles
  const resumePath = '/home/modi/Work/job-kit-starter/job-kit-starter/output/Anyscale - Software Engineer, Platform Infrastructure/Pratham_Modi_Resume.pdf';
  await page.locator('#_systemfield_resume').setInputFiles(resumePath);

  // Wait a bit for upload processing
  await page.waitForTimeout(2000);

  return {
    title: await page.title(),
    name: await page.locator('#_systemfield_name').inputValue(),
    email: await page.locator('#_systemfield_email').inputValue(),
    loc: await page.locator('[id="2953e314-ca27-4d2b-8c40-a8197a325a49"]').inputValue(),
    radio: await radioNo.isChecked()
  };
}