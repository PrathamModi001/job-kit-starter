async (page) => {
  // Click the label for No
  const noLabel = page.locator('label:has-text("No")');
  await noLabel.click({ force: true });

  // Resume upload via setInputFiles
  const resumePath = '/home/modi/Work/job-kit-starter/job-kit-starter/output/Anyscale - Software Engineer, Platform Infrastructure/Pratham_Modi_Resume.pdf';
  await page.locator('#_systemfield_resume').setInputFiles(resumePath);

  // Wait 3 seconds for upload processing
  await page.waitForTimeout(3000);

  const radioNo = page.locator('input[id*="labeled-radio-1"]');
  return {
    radioChecked: await radioNo.isChecked(),
    uploadedFileText: await page.locator('div:has-text("Pratham_Modi_Resume.pdf")').count()
  };
}