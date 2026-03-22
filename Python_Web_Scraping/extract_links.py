from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("https://example.com")
    links = page.eval_on_selector_all("a", "els => els.map(el => el.href)")
    print(links)
    browser.close()
