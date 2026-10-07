from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.on('request', lambda req: print('REQ:', req.method, req.url))
    page.goto('https://job-boards.greenhouse.io/embed/job_app?for=observeai&token=5432596008')
    page.wait_for_selector('#first_name', timeout=10000)
    pdf_path = r'E:\Extra\job-kit-starter\job-kit-starter\output\Observe.ai - AI Agent Engineer\Pratham_Modi_Resume.pdf'

    print("--- Setting input files on #resume ---")
    page.set_input_files('#resume', pdf_path)
    page.wait_for_timeout(2000)

    # Let's see all buttons and labels in the page
    btns = page.locator('button').all()
    print("All buttons:", [b.inner_text() for b in btns])
    
    browser.close()
