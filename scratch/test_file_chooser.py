from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('https://job-boards.greenhouse.io/embed/job_app?for=observeai&token=5432596008')
    page.wait_for_selector('#first_name', timeout=10000)
    pdf_path = r'E:\Extra\job-kit-starter\job-kit-starter\output\Observe.ai - AI Agent Engineer\Pratham_Modi_Resume.pdf'

    # Trigger via file chooser
    with page.expect_file_chooser() as fc_info:
        # First Attach button is for resume
        page.locator('button:has-text("Attach")').first.click()
    file_chooser = fc_info.value
    file_chooser.set_files(pdf_path)
    
    page.wait_for_timeout(3000)

    # Let's see what is inside resume container now
    container = page.locator('#resume').locator('xpath=ancestor::div[3]')
    print('Resume container text after file chooser:', container.inner_text())

    browser.close()
