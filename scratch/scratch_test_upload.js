// Test setting file via DataTransfer
async (page) => {
  const result = await page.evaluate(() => {
    const input = document.getElementById('_systemfield_resume');
    if (!input) return { success: false, error: 'input not found' };
    
    // Create a dummy PDF file
    const content = '%PDF-1.4\n1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj 2 0 obj<</Type/Pages/Kids[3 0 R]/Count 1>>endobj 3 0 obj<</Type/Page/MediaBox[0 0 612 792]>>endobj\nxref\n0 4\n0000000000 65535 f \n0000000010 00000 n \n0000000060 00000 n \n0000000117 00000 n \ntrailer<</Size 4/Root 1 0 R>>\nstartxref\n178\n%%EOF';
    const blob = new Blob([content], { type: 'application/pdf' });
    const file = new File([blob], 'test_resume.pdf', { type: 'application/pdf' });
    
    const dt = new DataTransfer();
    dt.items.add(file);
    input.files = dt.files;
    input.dispatchEvent(new Event('input', { bubbles: true }));
    input.dispatchEvent(new Event('change', { bubbles: true }));
    
    return {
      success: true,
      filesLength: input.files.length,
      fileName: input.files[0].name
    };
  });
  
  await page.waitForTimeout(2000);
  const text = await page.innerText('body');
  return {
    evalResult: result,
    hasFileNameInBody: text.includes('test_resume.pdf')
  };
}
