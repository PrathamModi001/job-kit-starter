async (page) => {
  const filePath = '/home/modi/Work/job-kit-starter/job-kit-starter/output/REDICA Systems - AI Engineer/Pratham_Modi_Resume.pdf';
  await page.setInputFiles('input[type="file"]', filePath);
  await page.waitForTimeout(3000);
  return 'file set successfully';
}
