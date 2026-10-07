from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('https://job-boards.greenhouse.io/embed/job_app?for=observeai&token=5432596008')
    page.wait_for_selector('button[type="submit"]', timeout=10000)
    
    # Click submit on empty form
    page.locator('button[type="submit"]').click()
    page.wait_for_timeout(1000)
    
    errors = page.locator('[id*="error"]').all()
    print('Errors on empty submit:')
    for err in errors:
        print(' -', err.get_attribute('id'), ':', err.inner_text())

    browser.close()
