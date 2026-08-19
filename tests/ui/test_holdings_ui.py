from playwright.sync_api import expect


BASE_URL = "http://localhost:5173"


def test_holdings_page_loads(page):
    page.goto(f"{BASE_URL}/portfolios/P10001/holdings")

    expect(page).to_have_url(
        f"{BASE_URL}/portfolios/P10001/holdings"
    )


def test_holdings_page_has_content(page):
    page.goto(f"{BASE_URL}/portfolios/P10001/holdings")

    page.wait_for_load_state("networkidle")

    expect(page.locator("body")).to_be_visible()

    assert page.locator("body").inner_text().strip() != ""


def test_holdings_page_no_error(page):
    page.goto(f"{BASE_URL}/portfolios/P10001/holdings")

    page.wait_for_load_state("networkidle")

    body_text = page.locator("body").inner_text().lower()

    assert "internal server error" not in body_text
    assert "application error" not in body_text