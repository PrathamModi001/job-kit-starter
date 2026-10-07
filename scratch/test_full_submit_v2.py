from playwright.sync_api import sync_playwright
import time
import os

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()

    responses = []
    page.on('response', lambda res: responses.append((res.status, res.url)))

    url = 'https://job-boards.greenhouse.io/embed/job_app?for=observeai&token=5432596008'
    print(f"Navigating to {url}...")
    page.goto(url)
    page.wait_for_selector('#first_name', timeout=15000)

    # 1. Upload Resume FIRST
    pdf_path = r'E:\Extra\job-kit-starter\job-kit-starter\output\Observe.ai - AI Agent Engineer\Pratham_Modi_Resume.pdf'
    print("Uploading resume first...")
    page.set_input_files('#resume', pdf_path)
    page.wait_for_timeout(3000)

    def set_input(locator, value):
        locator.click()
        locator.fill("")
        locator.type(value, delay=20)
        locator.evaluate('el => { el.dispatchEvent(new Event("input", { bubbles: true })); el.dispatchEvent(new Event("change", { bubbles: true })); }')

    # 2. First Name & Last Name
    set_input(page.locator('#first_name'), "Pratham")
    set_input(page.locator('#last_name'), "Modi")

    # 3. Email
    set_input(page.locator('#email'), "prathammodi001@gmail.com")

    # 4. Country (+91)
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

    # 5. Phone
    set_input(page.locator('#phone'), "9033393729")

    # 6. Location
    page.locator('#candidate-location').focus()
    page.keyboard.type('Hyderabad')
    page.wait_for_timeout(1000)
    for opt in page.locator('[id*="react-select"][id*="-option-"]').all():
        if 'Hyderabad, Telangana, India' in opt.inner_text():
            opt.click()
            break
    page.wait_for_timeout(300)

    # 7. Questions
    set_input(page.locator('#question_18769800008'), "https://www.linkedin.com/in/prathammodii001/")
    set_input(page.locator('#question_18769801008'), "https://prathammodi001.github.io/prathammodi/")

    page.wait_for_timeout(1000)

    print("Verifying values before submit:")
    print(" - First Name:", page.locator('#first_name').input_value())
    print(" - Last Name:", page.locator('#last_name').input_value())
    print(" - Email:", page.locator('#email').input_value())
    print(" - Phone:", page.locator('#phone').input_value())
    print(" - LinkedIn:", page.locator('#question_18769800008').input_value())
    print(" - Website:", page.locator('#question_18769801008').input_value())
    
    invalids = page.locator(':invalid, [aria-invalid="true"]').all()
    print(" - Invalids count:", len(invalids))

    out_dir = r'E:\Extra\job-kit-starter\job-kit-starter\output\Observe.ai - AI Agent Engineer'
    pre_submit = os.path.join(out_dir, 'pre_submit_v2.png')
    page.screenshot(path=pre_submit, full_page=True)

    # Submit!
    print("Clicking Submit application...")
    submit_btn = page.locator('button[type="submit"]')
    submit_btn.click()

    # Wait for submission
    print("Waiting 15 seconds for post-submit state...")
    page.wait_for_timeout(15000)

    print("Post-submit URL:", page.url)
    print("Post-submit title:", page.title())

    body_text = page.locator('body').inner_text()
    post_screenshot = os.path.join(out_dir, 'post_submit_v2.png')
    page.screenshot(path=post_screenshot, full_page=True)
    print(f"Screenshot saved to {post_screenshot}")

    with open(os.path.join(out_dir, 'post_submit_v2_text.txt'), 'w', encoding='utf-8') as f:
        f.write(f"URL: {page.url}\nTitle: {page.title()}\n\nBody:\n{body_text}")

    print("\nRecent Responses:")
    for status, res_url in responses[-15:]:
        print(f"  {status} {res_url}")

    browser.close()
