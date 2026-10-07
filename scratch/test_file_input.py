from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('https://job-boards.greenhouse.io/embed/job_app?for=observeai&token=5432596008')
    page.wait_for_selector('input[type="file"]', timeout=10000)
    print('Current URL:', page.url)
    inputs = page.locator('input[type="file"]').all()
    for inp in inputs:
        print('File input id:', inp.get_attribute('id'), 'aria-label:', inp.get_attribute('aria-label'))
    browser.close()
