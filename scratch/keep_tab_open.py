from playwright.sync_api import sync_playwright
import time
import os

print("Launching visible browser to keep Observe.ai application tab open for user...")
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    url = 'https://job-boards.greenhouse.io/embed/job_app?for=observeai&token=5432596008'
    print(f"Navigating to {url}...")
    page.goto(url)
    page.wait_for_selector('#first_name', timeout=15000)

    # 1. Upload Resume
    pdf_path = r'E:\Extra\job-kit-starter\job-kit-starter\output\Observe.ai - AI Agent Engineer\Pratham_Modi_Resume.pdf'
    print("Attaching resume...")
    page.set_input_files('#resume', pdf_path)
    page.wait_for_timeout(3000)

    def set_input(locator, value):
        locator.click()
        locator.fill("")
        locator.type(value, delay=20)
        locator.evaluate('el => { el.dispatchEvent(new Event("input", { bubbles: true })); el.dispatchEvent(new Event("change", { bubbles: true })); }')

    # 2. Personal info
    set_input(page.locator('#first_name'), "Pratham")
    set_input(page.locator('#last_name'), "Modi")
    set_input(page.locator('#email'), "prathammodi001@gmail.com")

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
    set_input(page.locator('#phone'), "9033393729")

    # 5. Location: Hyderabad, Telangana, India
    page.locator('#candidate-location').focus()
    page.keyboard.type('Hyderabad')
    page.wait_for_timeout(1000)
    for opt in page.locator('[id*="react-select"][id*="-option-"]').all():
        if 'Hyderabad, Telangana, India' in opt.inner_text():
            opt.click()
            break
    page.wait_for_timeout(300)

    # 6. Questions
    set_input(page.locator('#question_18769800008'), "https://www.linkedin.com/in/prathammodii001/")
    set_input(page.locator('#question_18769801008'), "https://prathammodi001.github.io/prathammodi/")

    page.wait_for_timeout(1000)

    # 7. Submit to trigger verification
    print("Submitting to bring up security verification code input...")
    page.locator('button[type="submit"]').click()
    page.wait_for_timeout(5000)

    print("Browser tab is now OPEN on desktop with the 8-character verification code prompt!")
    print("Prompt text: A verification code was sent to prathammodi001@gmail.com.")
    print("User can type code directly into browser window.")

    # Keep browser open for user interaction
    while True:
        try:
            # Check if user submitted and navigated away or confirmation appeared
            if page.locator('text=Thank you for applying').count() > 0 or 'confirmation' in page.url.lower():
                print("Application successfully submitted by user!")
                break
            time.sleep(2)
        except Exception:
            break
