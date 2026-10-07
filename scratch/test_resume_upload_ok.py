from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('https://job-boards.greenhouse.io/embed/job_app?for=observeai&token=5432596008')
    page.wait_for_selector('#resume', timeout=10000)
    pdf_path = r'E:\Extra\job-kit-starter\job-kit-starter\output\Observe.ai - AI Agent Engineer\Pratham_Modi_Resume.pdf'
    page.set_input_files('#resume', pdf_path)
    page.wait_for_timeout(2000)
    
    # Check what text appeared around resume
    # Let's see all text in the form
    print("Form content around resume:")
    parent = page.locator('#resume').locator('..')
    print('Parent text:', parent.inner_text())
    print('Grandparent text:', parent.locator('..').inner_text())
    browser.close()
