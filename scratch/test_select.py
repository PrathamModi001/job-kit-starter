from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('https://job-boards.greenhouse.io/embed/job_app?for=observeai&token=5432596008', wait_until='networkidle')
    
    # 1. Country
    page.locator('#country').focus()
    page.keyboard.type('India')
    page.wait_for_timeout(500)
    page.keyboard.press('Enter')
    page.wait_for_timeout(500)
    country_val = page.locator('#country').evaluate('el => el.closest(".select__control").innerText')
    print('Country container text:', repr(country_val))
    
    # 2. Location
    page.locator('#candidate-location').focus()
    page.keyboard.type('Bengaluru')
    page.wait_for_timeout(1000)
    opts = page.locator('[id*="react-select"][id*="-option-"]').all()
    print('Location options for Bengaluru:', [o.inner_text() for o in opts])
    if opts:
        opts[0].click()
    page.wait_for_timeout(500)
    loc_val = page.locator('#candidate-location').evaluate('el => el.closest(".select__control").innerText')
    print('Location container text:', repr(loc_val))

    # 3. Resume upload
    resume_input = page.locator('#resume')
    print('Resume input exists:', resume_input.count())

    browser.close()
