from playwright import sync_api as sa


with sa.sync_playwright() as d:
    browser = d.firefox.launch(headless=False)
    print(type(browser))
    page = browser.new_page()
    print(type(page))
    # page.goto("https://splash.ironwifi.com/api/pages/2034/?mac=17:22:33:44:55:66&url=https://www.ironwifi.com&iwr=91d3cf2d9d95069ab2ca75180f1d7b3469b85b47&iwt=1723705876")
    # page.locator('input[name="plan37_quantity"]').fill("press_something")
    # time.sleep(20)

# Works

# from playwright import sync_api as sa
# import time

# with sa.sync_playwright() as d:
#     browser = d.firefox.launch(headless=False)
#     page = browser.new_page()
#     page.goto("https://splash.ironwifi.com/api/pages/r-xqkwo-rcwhu-xcrkv/?mac=08:22:33:44:55:66&url=https://www.ironwifi.com&iwr=716ed9ad8edebb8f6da172de469e0014dc0f5944&iwt=1723677920")
#     page.locator("#localaccount_login").click()
#     time.sleep(20)
