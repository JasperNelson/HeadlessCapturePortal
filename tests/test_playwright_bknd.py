from playwright import sync_api as sa


def test_Playwright_chrome() -> None:
    """
    Test to be used to test if playwright is properly installed and working
    """
    browser = sa.sync_playwright().start().chromium.launch()
    page = browser.new_page()
    page.goto("https://www.scrapethissite.com")
    page.locator('xpath=//*[@id="hero"]/div/div/div/a[1]').click()
    x = page.locator('xpath=//*[@id="pages"]/section/div/div/div/div[1]/p').all_inner_texts()
    assert (x == ['A single page that lists information about all the countries in the world. Good for those just get started with web scraping.'])


 