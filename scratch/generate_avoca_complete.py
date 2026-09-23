import base64

pdf_path = 'job-kit-starter/output/Avoca - Deployment Engineer/Pratham_Modi_Resume.pdf'
with open(pdf_path, 'rb') as f:
    b64 = base64.b64encode(f.read()).decode('utf-8')

js_code = f'''async (page) => {{
  try {{
    if (!page.url().includes('jobs.ashbyhq.com/avoca')) {{
      await page.goto('https://jobs.ashbyhq.com/avoca/6758ee84-51b4-4d0d-a3a6-d40ec164de49/application');
      await page.waitForTimeout(3000);
    }}
    
    const b64 = "{b64}";
    
    // Fill all form fields and attach resume via evaluate
    const fillResult = await page.evaluate((b64Data) => {{
      // 1. Name
      const nameInput = document.getElementById('_systemfield_name');
      if (nameInput) {{
        nameInput.value = 'Pratham Modi';
        nameInput.dispatchEvent(new Event('input', {{ bubbles: true }}));
        nameInput.dispatchEvent(new Event('change', {{ bubbles: true }}));
      }}
      
      // 2. Email
      const emailInput = document.getElementById('_systemfield_email');
      if (emailInput) {{
        emailInput.value = 'prathammodi001@gmail.com';
        emailInput.dispatchEvent(new Event('input', {{ bubbles: true }}));
        emailInput.dispatchEvent(new Event('change', {{ bubbles: true }}));
      }}
      
      // 3. Phone
      const phoneInput = document.querySelector('input[type="tel"]');
      if (phoneInput) {{
        phoneInput.value = '+919033393729';
        phoneInput.dispatchEvent(new Event('input', {{ bubbles: true }}));
        phoneInput.dispatchEvent(new Event('change', {{ bubbles: true }}));
      }}
      
      // 4. LinkedIn
      const linkedinInput = document.querySelector('input[type="url"]');
      if (linkedinInput) {{
        linkedinInput.value = 'https://www.linkedin.com/in/prathammodii001/';
        linkedinInput.dispatchEvent(new Event('input', {{ bubbles: true }}));
        linkedinInput.dispatchEvent(new Event('change', {{ bubbles: true }}));
      }}
      
      // 5. Radios
      const genderRadios = Array.from(document.querySelectorAll('input[name*="eeoc_gender"]'));
      if (genderRadios[0]) genderRadios[0].click();
      
      const raceRadios = Array.from(document.querySelectorAll('input[name*="eeoc_race"]'));
      // Find Asian radio
      const asianRadio = raceRadios.find(r => {{
        const label = document.querySelector(`label[for="${{r.id}}"]`) || r.parentElement;
        return label && label.innerText.includes('Asian');
      }}) || raceRadios[4];
      if (asianRadio) asianRadio.click();
      
      const vetRadios = Array.from(document.querySelectorAll('input[name*="eeoc_veteran_status"]'));
      const vetRadio = vetRadios.find(r => {{
        const label = document.querySelector(`label[for="${{r.id}}"]`) || r.parentElement;
        return label && label.innerText.includes('not a protected veteran');
      }}) || vetRadios[1];
      if (vetRadio) vetRadio.click();
      
      // 6. Resume Upload via DataTransfer
      const resumeInput = document.getElementById('_systemfield_resume');
      if (!resumeInput) return {{ success: false, error: 'resume input not found' }};
      
      const binary = atob(b64Data);
      const array = new Uint8Array(binary.length);
      for (let i = 0; i < binary.length; i++) {{
        array[i] = binary.charCodeAt(i);
      }}
      const file = new File([array], "Pratham_Modi_Resume.pdf", {{ type: "application/pdf" }});
      const dt = new DataTransfer();
      dt.items.add(file);
      
      resumeInput.files = dt.files;
      resumeInput.dispatchEvent(new Event('input', {{ bubbles: true }}));
      resumeInput.dispatchEvent(new Event('change', {{ bubbles: true }}));
      
      return {{
        success: true,
        name: nameInput?.value,
        email: emailInput?.value,
        phone: phoneInput?.value,
        linkedin: linkedinInput?.value,
        resumeName: resumeInput.files[0]?.name
      }};
    }}, b64);
    
    await page.waitForTimeout(3000);
    
    // Check if resume is attached and submit button is available
    const bodyText = await page.innerText('body');
    const hasResumeAttached = bodyText.includes('Pratham_Modi_Resume.pdf');
    
    // Click Submit Application
    const submitBtn = await page.$('button:has-text("Submit Application")');
    let submitted = false;
    if (submitBtn) {{
      await submitBtn.click();
      submitted = true;
      await page.waitForTimeout(6000);
    }}
    
    return {{
      fillResult,
      hasResumeAttached,
      submitted,
      finalUrl: page.url(),
      finalTitle: await page.title(),
      confirmationText: (await page.innerText('body')).slice(0, 1000)
    }};
  }} catch (e) {{
    return {{ error: e.message, stack: e.stack }};
  }}
}}
'''

with open('scratch/apply_avoca_complete.js', 'w') as f:
    f.write(js_code)

print('Generated scratch/apply_avoca_complete.js successfully')
