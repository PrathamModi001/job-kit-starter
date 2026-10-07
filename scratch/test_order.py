from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('https://job-boards.greenhouse.io/embed/job_app?for=observeai&token=5432596008')
    page.wait_for_selector('#first_name', timeout=10000)

    # 1. Upload Resume FIRST
    pdf_path = r'E:\Extra\job-kit-starter\job-kit-starter\output\Observe.ai - AI Agent Engineer\Pratham_Modi_Resume.pdf'
    print("Uploading resume first...")
    page.set_input_files('#resume', pdf_path)
    page.wait_for_timeout(3000)

    # 2. Check if first_name / last_name were touched
    print("first_name before filling:", page.locator('#first_name').input_value())
    print("last_name before filling:", page.locator('#last_name').input_value())

    # 3. Fill first_name, last_name, email, phone
    def set_react_input(locator, value):
        locator.click()
        locator.fill("")
        locator.type(value, delay=30)
        locator.evaluate('el => el.dispatchEvent(new Event("change", { bubbles: true }))')

    set_react_input(page.locator('#first_name'), "Pratham")
    set_react_input(page.locator('#last_name'), "Modi")
    set_react_input(page.locator('#email'), "prathammodi001@gmail.com")

    print("first_name after filling:", page.locator('#first_name').input_value())
    print("last_name after filling:", page.locator('#last_name').input_value())
    print("email after filling:", page.locator('#email').input_value())

    browser.close()
