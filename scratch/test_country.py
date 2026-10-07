from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('https://job-boards.greenhouse.io/embed/job_app?for=observeai&token=5432596008', wait_until='networkidle')
    
    # Click on the country control
    ctrl = page.locator('#country').locator('xpath=ancestor::div[contains(@class, "select__control")]')
    ctrl.click()
    page.wait_for_timeout(500)
    page.keyboard.type('India')
    page.wait_for_timeout(500)
    
    # List options
    opts = page.locator('[id*="react-select"][id*="-option-"]').all()
    print('Options for country:', [o.inner_text() for o in opts])
    if opts:
        for o in opts:
            if o.inner_text().strip() == 'India':
                o.click()
                break
    page.wait_for_timeout(500)
    print('Selected Country text:', ctrl.inner_text())

    browser.close()
