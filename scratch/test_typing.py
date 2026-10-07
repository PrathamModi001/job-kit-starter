from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('https://job-boards.greenhouse.io/embed/job_app?for=observeai&token=5432596008')
    page.wait_for_selector('#first_name', timeout=10000)

    # Sequential typing
    fn = page.locator('#first_name')
    fn.click()
    fn.press_sequentially('Pratham', delay=50)
    
    ln = page.locator('#last_name')
    ln.click()
    ln.press_sequentially('Modi', delay=50)

    em = page.locator('#email')
    em.click()
    em.press_sequentially('prathammodi001@gmail.com', delay=50)

    print('Values after sequential typing:')
    print('First Name:', fn.input_value())
    print('Last Name:', ln.input_value())
    print('Email:', em.input_value())

    # Click body to blur
    page.locator('body').click()
    page.wait_for_timeout(500)

    print('After blur:')
    print('First Name:', fn.input_value())
    errs = [e.inner_text() for e in page.locator('[id*="error"]').all() if e.is_visible()]
    print('Errors on page:', errs)

    browser.close()
