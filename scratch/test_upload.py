from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('https://job-boards.greenhouse.io/embed/job_app?for=observeai&token=5432596008', wait_until='networkidle')
    
    pdf_path = r'E:\Extra\job-kit-starter\job-kit-starter\output\Observe.ai - AI Agent Engineer\Pratham_Modi_Resume.pdf'
    page.set_input_files('#resume', pdf_path)
    page.wait_for_timeout(2000)
    
    # Check if file uploaded and shown
    resume_div = page.locator('#resume').locator('xpath=ancestor::div[contains(@class, "field")]')
    print('Resume field text:', resume_div.inner_text())

    browser.close()
