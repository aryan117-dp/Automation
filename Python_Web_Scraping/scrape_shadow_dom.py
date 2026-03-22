from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("https://shop.polymer-project.org/")
    shadow_text = page.eval_on_selector("shop-app", '''
        el => el.shadowRoot.querySelector("shop-home").shadowRoot.querySelector("h2").textContent
    ''')
    print(shadow_text)
    browser.close()
