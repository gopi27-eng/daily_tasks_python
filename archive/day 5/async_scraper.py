from playwright.sync_api import sync_playwright

def scrape_dynamic_site():
    print("--- Booting Headless Browser ---\n")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        print("Navigating to JS-rendered site...")
        page.goto("http://quotes.toscrape.com/js/")

        print("Waiting for JavaScript to render...")
        page.wait_for_selector(".text")

        first_quote = page.locator(".text").first.inner_text()
        print(f"Extracted: {first_quote}")

        browser.close()

scrape_dynamic_site()
