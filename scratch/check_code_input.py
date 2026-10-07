from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('https://job-boards.greenhouse.io/embed/job_app?for=observeai&token=5432596008')
    page.wait_for_selector('#first_name', timeout=10000)
    pdf_path = r'E:\Extra\job-kit-starter\job-kit-starter\output\Observe.ai - AI Agent Engineer\Pratham_Modi_Resume.pdf'
    page.set_input_files('#resume', pdf_path)
    page.wait_for_timeout(2000)
    
    def set_input(locator, value):
        locator.click()
        locator.fill("")
        locator.type(value, delay=20)
        locator.evaluate('el => { el.dispatchEvent(new Event("input", { bubbles: true })); el.dispatchEvent(new Event("change", { bubbles: true })); }')

    set_input(page.locator('#first_name'), 'Pratham')
    set_input(page.locator('#last_name'), 'Modi')
    set_input(page.locator('#email'), 'prathammodi001@gmail.com')
    ctrl = page.locator('#country').locator('xpath=ancestor::div[contains(@class, "select__control")]')
    ctrl.click()
    page.wait_for_timeout(300)
    page.keyboard.type('India')
    page.wait_for_timeout(500)
    for opt in page.locator('[id*="react-select"][id*="-option-"]').all():
        if 'India +91' in opt.inner_text():
            opt.click()
            break
    set_input(page.locator('#phone'), '9033393729')
    page.locator('#candidate-location').focus()
    page.keyboard.type('Hyderabad')
    page.wait_for_timeout(1000)
    for opt in page.locator('[id*="react-select"][id*="-option-"]').all():
        if 'Hyderabad, Telangana, India' in opt.inner_text():
            opt.click()
            break
    set_input(page.locator('#question_18769800008'), 'https://www.linkedin.com/in/prathammodii001/')
    set_input(page.locator('#question_18769801008'), 'https://prathammodi001.github.io/prathammodi/')
    
    page.locator('button[type="submit"]').click()
    page.wait_for_timeout(5000)

    # Inspect code input
    inputs = page.locator('input').all()
    for inp in inputs:
        id_attr = inp.get_attribute('id')
        name_attr = inp.get_attribute('name')
        aria_label = inp.get_attribute('aria-label')
        placeholder = inp.get_attribute('placeholder')
        if any(x in str(id_attr or '').lower() or x in str(name_attr or '').lower() or x in str(aria_label or '').lower() for x in ['code', 'security', 'verify', 'token']):
            print('Code input found:', id_attr, name_attr, aria_label, placeholder)
            print('Outer HTML:', inp.evaluate('el => el.outerHTML'))

    browser.close()
