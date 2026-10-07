from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('https://job-boards.greenhouse.io/embed/job_app?for=observeai&token=5432596008', wait_until='networkidle')
    
    print('PAGE TITLE:', page.title())
    
    # Check all labels and their associated inputs
    labels = page.locator('label').all()
    for l in labels:
        txt = l.inner_text().strip().replace('\n', ' ')
        for_attr = l.get_attribute('for')
        print(f"Label: '{txt}' -> for: '{for_attr}'")
        
    print("\n--- ALL INPUTS ---")
    inputs = page.locator('input, textarea, select, button').all()
    for el in inputs:
        tag = el.evaluate('el => el.tagName.toLowerCase()')
        id_attr = el.get_attribute('id')
        name_attr = el.get_attribute('name')
        type_attr = el.get_attribute('type')
        aria_label = el.get_attribute('aria-label')
        text = el.inner_text().strip() if tag == 'button' else ''
        print(f"Tag: {tag}, id: {id_attr}, name: {name_attr}, type: {type_attr}, aria-label: {aria_label}, text: {text}")

    browser.close()
