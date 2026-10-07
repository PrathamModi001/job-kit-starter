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

    # 5. Location: Hyderabad, Telangana, India
    page.locator('#candidate-location').focus()
    page.keyboard.type('Hyderabad')
    page.wait_for_timeout(1000)
    for opt in page.locator('[id*="react-select"][id*="-option-"]').all():
        if 'Hyderabad, Telangana, India' in opt.inner_text():
            opt.click()
            break
    page.wait_for_timeout(300)

    # 6. Resume
    pdf_path = r'E:\Extra\job-kit-starter\job-kit-starter\output\Observe.ai - AI Agent Engineer\Pratham_Modi_Resume.pdf'
    page.set_input_files('#resume', pdf_path)
    page.wait_for_timeout(500)

    # 7. Questions
    page.locator('#question_18769800008').fill("https://www.linkedin.com/in/prathammodii001/")
    page.locator('#question_18769801008').fill("https://prathammodi001.github.io/prathammodi/")

    # Screenshot the form before submit
    screenshot_path = r'E:\Extra\job-kit-starter\job-kit-starter\output\Observe.ai - AI Agent Engineer\form_filled_preview.png'
    page.screenshot(path=screenshot_path, full_page=True)
    print("Screenshot saved to", screenshot_path)

    # Let's inspect submit button
    submit_btn = page.locator('button[type="submit"]')
    print("Submit button text:", submit_btn.inner_text())
    print("Submit button disabled:", submit_btn.is_disabled())

    browser.close()
