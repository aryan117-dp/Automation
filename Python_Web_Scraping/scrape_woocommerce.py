import asyncio
import json
import csv
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto("https://amundsensports.com/sweater-women/")
        await page.wait_for_selector("li.product")

        products = await page.query_selector_all("li.product")
        results = []

        for product in products:
            title = await (await product.query_selector(".woocommerce-loop-product__title")).inner_text()
            gender = await (await product.query_selector(".woocommerce-loop-product__gender")).inner_text()
            price = await (await product.query_selector(".price .amount")).inner_text()
            link = await (await product.query_selector("a.woocommerce-loop-product__link")).get_attribute("href")

            color_elements = await product.query_selector_all(".color-variable-item")
            size_elements = await product.query_selector_all(".button-variable-item")

            colors = [await el.get_attribute("title") for el in color_elements]
            sizes = [await el.get_attribute("title") for el in size_elements]

            results.append({
                "title": title,
                "gender": gender,
                "price": price,
                "link": link,
                "colors": colors,
                "sizes": sizes
            })

        with open("products.json", "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)

        with open("products.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["title", "gender", "price", "link", "colors", "sizes"])
            writer.writeheader()
            for item in results:
                writer.writerow({
                    "title": item["title"],
                    "gender": item["gender"],
                    "price": item["price"],
                    "link": item["link"],
                    "colors": ", ".join(item["colors"]),
                    "sizes": ", ".join(item["sizes"]),
                })

asyncio.run(main())