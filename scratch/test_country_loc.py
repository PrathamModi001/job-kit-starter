from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('https://job-boards.greenhouse.io/embed/job_app?for=observeai&token=5432596008', wait_until='networkidle')
    
    # 1. Select Country 'India +91'
    ctrl = page.locator('#country').locator('xpath=ancestor::div[contains(@class, "select__control")]')
    ctrl.click()
    page.wait_for_timeout(300)
    page.keyboard.type('India')
    page.wait_for_timeout(500)
    for opt in page.locator('[id*="react-select"][id*="-option-"]').all():
        if 'India +91' in opt.inner_text():
            opt.click()
            break
    page.wait_for_timeout(500)
    print('Country selected:', ctrl.inner_text())

    # 2. Test candidate-location
    loc_ctrl = page.locator('#candidate-location').locator('xpath=ancestor::div[contains(@class, "select__control")]')
    loc_ctrl.click()
    page.wait_for_timeout(300)
    page.keyboard.type('Bengaluru')
    page.wait_for_timeout(600)
    opts = page.locator('[id*="react-select"][id*="-option-"]').all()
    print('Location opts:', [o.inner_text() for o in opts])
    if opts:
        opts[0].click()
    page.wait_for_timeout(500)
    print('Location selected:', loc_ctrl.inner_text())

    browser.close()
