from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("https://example.com")
    images = page.eval_on_selector_all("img", "els => els.map(el => el.src)")
    print(images)
    browser.close()
