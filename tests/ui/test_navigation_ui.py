from playwright.sync_api import expect


BASE_URL = "http://localhost:5173"


def test_portfolios_navigation(page):
    page.goto(f"{BASE_URL}/portfolios")

    page.wait_for_load_state("networkidle")

    links = page.locator("a")

    assert links.count() > 0


def test_page_has_no_broken_navigation(page):
    page.goto(f"{BASE_URL}/portfolios")

    page.wait_for_load_state("networkidle")

    for link in page.locator("a").all():
        href = link.get_attribute("href")

        if href and href.startswith("/"):
            assert not href.startswith("//")