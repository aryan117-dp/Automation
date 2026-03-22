import json
from playwright.sync_api import sync_playwright

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto('https://www.amazon.com/b?node=283155')
        page.wait_for_selector('.a-column')

        product_data = []
        products = page.query_selector_all('.a-column')

        for product in products:
            title = product.query_selector('.p13n-sc-truncate-desktop-type2')
            if title:
                rating = product.query_selector('.a-icon-alt')
                reviews_count = product.query_selector('.a-size-small')
                image = product.query_selector('img')

                product_data.append({
                    'title': title.inner_text() if title else None,
                    'rating': rating.inner_text() if rating else None,
                    'reviews_count': reviews_count.inner_text() if reviews_count else None,
                    'image_url': image.get_attribute('src') if image else None
                })

        with open('product_data.json', 'w', encoding='utf-8') as f:
            json.dump(product_data, f, ensure_ascii=False, indent=2)

        browser.close()

if __name__ == "__main__":
    main()
