from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('https://job-boards.greenhouse.io/embed/job_app?for=observeai&token=5432596008', wait_until='networkidle')
    
    # Check country input outerHTML
    c_input = page.locator('#country')
    print('Country input HTML:', c_input.evaluate('el => el.outerHTML'))
    print('Country parent HTML:', c_input.evaluate('el => el.parentElement.outerHTML'))
    
    # Check candidate-location input outerHTML
    loc_input = page.locator('#candidate-location')
    print('Location input HTML:', loc_input.evaluate('el => el.outerHTML'))
    print('Location parent HTML:', loc_input.evaluate('el => el.parentElement.outerHTML'))

    # Check phone input outerHTML
    p_input = page.locator('#phone')
    print('Phone input HTML:', p_input.evaluate('el => el.outerHTML'))
    print('Phone parent HTML:', p_input.evaluate('el => el.parentElement.outerHTML'))
    
    browser.close()
