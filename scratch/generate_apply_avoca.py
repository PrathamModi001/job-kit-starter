import base64

pdf_path = 'job-kit-starter/output/Avoca - Deployment Engineer/Pratham_Modi_Resume.pdf'
with open(pdf_path, 'rb') as f:
    b64 = base64.b64encode(f.read()).decode('utf-8')

js_template = """async (page) => {
  const b64 = "__B64_DATA__";
  
  // 1. Upload Resume via DataTransfer to #_systemfield_resume
  const uploadResult = await page.evaluate((b64Data) => {
    const binary = atob(b64Data);
    const array = new Uint8Array(binary.length);
    for (let i = 0; i < binary.length; i++) {
      array[i] = binary.charCodeAt(i);
    }
    const file = new File([array], "Pratham_Modi_Resume.pdf", { type: "application/pdf" });
    const dt = new DataTransfer();
    dt.items.add(file);
    
    const resumeInput = document.getElementById('_systemfield_resume');
    if (!resumeInput) return { success: false, error: "resume input not found" };
    
    resumeInput.files = dt.files;
    resumeInput.dispatchEvent(new Event('input', { bubbles: true }));
    resumeInput.dispatchEvent(new Event('change', { bubbles: true }));
    
    return { success: true, fileName: resumeInput.files[0]?.name };
  }, b64);
  
  await page.waitForTimeout(2000);
  
  // 2. Fill Name
  await page.fill('#_systemfield_name', 'Pratham Modi');
  
  // 3. Fill Email
  await page.fill('#_systemfield_email', 'prathammodi001@gmail.com');
  
  // 4. Fill Phone
  await page.fill('input[type="tel"]', '+91-9033393729');
  
  // 5. Fill LinkedIn
  await page.fill('input[type="url"]', 'https://www.linkedin.com/in/prathammodii001/');
  
  // 6. EEOC Gender - Male
  const maleInput = await page.locator('input[name*="eeoc_gender"]').first();
  if (maleInput) await maleInput.check();
  
  // 7. EEOC Race - Asian
  const asianRadio = page.locator('label').filter({ hasText: 'Asian' }).locator('input');
  if (await asianRadio.count() > 0) {
    await asianRadio.first().check();
  }
  
  // 8. EEOC Veteran - Not a protected veteran
  const vetRadio = page.locator('label').filter({ hasText: 'I am not a protected veteran' }).locator('input');
  if (await vetRadio.count() > 0) {
    await vetRadio.first().check();
  }
  
  await page.waitForTimeout(1000);
  
  const text = await page.innerText('body');
  return {
    uploadResult,
    hasResumeName: text.includes('Pratham_Modi_Resume.pdf')
  };
}
"""

js_code = js_template.replace('__B64_DATA__', b64)
with open('scratch/apply_avoca.js', 'w') as f:
    f.write(js_code)

print("Generated scratch/apply_avoca.js successfully")
