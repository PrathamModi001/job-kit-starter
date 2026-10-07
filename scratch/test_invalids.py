from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('https://job-boards.greenhouse.io/embed/job_app?for=observeai&token=5432596008')
    page.wait_for_selector('button[type="submit"]', timeout=10000)
    page.locator('button[type="submit"]').click()
    page.wait_for_timeout(1000)
    invalids = page.locator(':invalid, [aria-invalid="true"]').all()
    print('Invalid count:', len(invalids))
    for inv in invalids:
        print('Invalid element:', inv.get_attribute('id'), inv.get_attribute('name'), inv.get_attribute('type'))
    # Also print any visible error messages
    err_msgs = page.locator('.error, .error-message, [class*="error"]').all()
    for em in err_msgs:
        if em.is_visible():
            print('Visible error:', em.inner_text())
    browser.close()
