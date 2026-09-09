from playwright.sync_api import sync_playwright

def automate_login():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        print("__new page opend background browser__")
        
        page.goto("http://quotes.toscrape.com/login")
        print("__page loaded__")
        page.wait_for_selector("#username")
        page.locator("#username").fill("admin")
        page.wait_for_selector("#password")
        page.locator("#password").fill("securepassword")
        page.wait_for_selector("input[type='submit']")  
        page.locator("input[type='submit']").click()
        
        print("__login button clicked__")
        
        if page.locator("text=Logout").is_visible():
            print("__login successful__")
automate_login()