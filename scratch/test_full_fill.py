from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('https://job-boards.greenhouse.io/embed/job_app?for=observeai&token=5432596008')
    page.wait_for_selector('#first_name', timeout=10000)

    # 1. First Name & Last Name
    page.locator('#first_name').fill("Pratham")
    page.locator('#last_name').fill("Modi")

    # 2. Email
    page.locator('#email').fill("prathammodi001@gmail.com")

    # 3. Country (phone dial code)
    ctrl = page.locator('#country').locator('xpath=ancestor::div[contains(@class, "select__control")]')
    ctrl.click()
    page.wait_for_timeout(300)
    page.keyboard.type('India')
    page.wait_for_timeout(500)
    for opt in page.locator('[id*="react-select"][id*="-option-"]').all():
        if 'India +91' in opt.inner_text():
            opt.click()
            break
    page.wait_for_timeout(300)

    # 4. Phone
    page.locator('#phone').fill("9033393729")

    # 5. Location
    page.locator('#candidate-location').focus()
    page.keyboard.type('Hyderabad')
    page.wait_for_timeout(1000)
    opts = page.locator('[id*="react-select"][id*="-option-"]').all()
    print('Location options for Hyderabad:', [o.inner_text() for o in opts])
    if opts:
        opts[0].click()
    else:
        # try Bengaluru if Hyderabad not in dropdown
        page.locator('#candidate-location').focus()
        page.keyboard.type('Bengaluru')
        page.wait_for_timeout(1000)
        opts_b = page.locator('[id*="react-select"][id*="-option-"]').all()
        print('Location options for Bengaluru:', [o.inner_text() for o in opts_b])
        if opts_b:
            opts_b[0].click()
    page.wait_for_timeout(300)

    # 6. Resume
    pdf_path = r'E:\Extra\job-kit-starter\job-kit-starter\output\Observe.ai - AI Agent Engineer\Pratham_Modi_Resume.pdf'
    page.set_input_files('#resume', pdf_path)
    page.wait_for_timeout(500)

    # 7. Questions
    page.locator('#question_18769800008').fill("https://www.linkedin.com/in/prathammodii001/")
    page.locator('#question_18769801008').fill("https://prathammodi001.github.io/prathammodi/")

    # Check values of all filled inputs
    vals = page.evaluate('''() => {
        return {
            first_name: document.getElementById('first_name').value,
            last_name: document.getElementById('last_name').value,
            email: document.getElementById('email').value,
            phone: document.getElementById('phone').value,
            linkedin: document.getElementById('question_18769800008').value,
            website: document.getElementById('question_18769801008').value,
            resume_files: document.getElementById('resume').files.length,
            resume_file_name: document.getElementById('resume').files[0] ? document.getElementById('resume').files[0].name : null,
            candidate_location: document.getElementById('candidate-location').value || document.querySelector('#candidate-location').closest('.select__control').innerText.trim()
        };
    }''')
    print('Filled form values:', vals)

    browser.close()
