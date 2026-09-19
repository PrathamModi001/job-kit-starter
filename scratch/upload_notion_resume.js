async (page) => {
  const filePath = '/home/modi/Work/job-kit-starter/job-kit-starter/output/AtomicAds - Member of Technical Staff/Pratham_Modi_Resume.pdf';
  const fileChooserPromise = page.waitForEvent('filechooser', { timeout: 10000 });
  await page.getByRole('button', { name: 'Upload' }).click();
  const fileChooser = await fileChooserPromise;
  await fileChooser.setFiles(filePath);
  await page.waitForTimeout(3000);
  return 'File uploaded successfully';
}
