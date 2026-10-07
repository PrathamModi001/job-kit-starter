from playwright.sync_api import sync_playwright
import time
import os

with sync_playwright() as p:
    # Launch browser
    browser = p.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()

    responses = []
    page.on('response', lambda res: responses.append((res.status, res.url)))

    url = 'https://job-boards.greenhouse.io/embed/job_app?for=observeai&token=5432596008'
    print(f"Navigating to {url}...")
    page.goto(url)
    page.wait_for_selector('#first_name', timeout=15000)

    # 1. First Name & Last Name
    page.locator('#first_name').fill("Pratham")
    page.locator('#last_name').fill("Modi")

    # 2. Email
    page.locator('#email').fill("prathammodi001@gmail.com")

    # 3. Country (+91)
    ctrl = page.locator('#country').locator('xpath=ancestor::div[contains(@class, "select__control")]')
    ctrl.click()
    page.wait_for_timeout(300)
    page.keyboard.type('India')
    page.wait_for_timeout(500)
    for opt in page.locator('[id*="react-select"][id*="-option-"]').all():
        if 'India +91' in opt.inner_text():
            opt.click()
            break
    page.wait_for_timeout(300)

    # 4. Phone
    page.locator('#phone').fill("9033393729")

    # 5. Location
    page.locator('#candidate-location').focus()
    page.keyboard.type('Hyderabad')
    page.wait_for_timeout(1000)
    for opt in page.locator('[id*="react-select"][id*="-option-"]').all():
        if 'Hyderabad, Telangana, India' in opt.inner_text():
            opt.click()
            break
    page.wait_for_timeout(300)

    # 6. Resume
    pdf_path = r'E:\Extra\job-kit-starter\job-kit-starter\output\Observe.ai - AI Agent Engineer\Pratham_Modi_Resume.pdf'
    page.set_input_files('#resume', pdf_path)
    page.wait_for_timeout(500)

    # 7. Questions
    page.locator('#question_18769800008').fill("https://www.linkedin.com/in/prathammodii001/")
    page.locator('#question_18769801008').fill("https://prathammodi001.github.io/prathammodi/")

    page.wait_for_timeout(1000)

    # Click Submit application
    print("Clicking Submit application...")
    submit_btn = page.locator('button[type="submit"]')
    submit_btn.click()

    # Wait for submission network activity or navigation
    print("Waiting 10 seconds for post-submit state...")
    page.wait_for_timeout(10000)

    print("Post-submit URL:", page.url)
    print("Post-submit title:", page.title())

    # Check for confirmation or error text
    body_text = page.locator('body').inner_text()
    out_dir = r'E:\Extra\job-kit-starter\job-kit-starter\output\Observe.ai - AI Agent Engineer'
    post_screenshot = os.path.join(out_dir, 'post_submit_screen.png')
    page.screenshot(path=post_screenshot, full_page=True)
    print(f"Screenshot saved to {post_screenshot}")

    with open(os.path.join(out_dir, 'post_submit_text.txt'), 'w', encoding='utf-8') as f:
        f.write(f"URL: {page.url}\nTitle: {page.title()}\n\nBody:\n{body_text}")

    print("\nRecent Responses:")
    for status, res_url in responses[-15:]:
        print(f"  {status} {res_url}")

    browser.close()
