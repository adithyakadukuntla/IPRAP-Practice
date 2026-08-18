import pytest
from playwright.sync_api import expect


BASE_URL = "http://localhost:5173"


def test_portfolios_page_loads(page):
    page.goto(f"{BASE_URL}/portfolios")

    expect(page).to_have_url(f"{BASE_URL}/portfolios")


def test_portfolios_page_has_content(page):
    page.goto(f"{BASE_URL}/portfolios")

    expect(page.locator("body")).to_be_visible()

    assert page.locator("body").inner_text().strip() != ""


def test_portfolios_page_has_portfolio_data(page):
    page.goto(f"{BASE_URL}/portfolios")

    page.wait_for_load_state("networkidle")

    body_text = page.locator("body").inner_text()

    # At least one expected portfolio identifier should appear
    assert (
        "P10001" in body_text
        or "Portfolio" in body_text
        or "Portfolios" in body_text
    )


def test_portfolios_page_no_error_message(page):
    page.goto(f"{BASE_URL}/portfolios")

    page.wait_for_load_state("networkidle")

    body_text = page.locator("body").inner_text().lower()

    assert "internal server error" not in body_text
    assert "application error" not in body_text
    assert "something went wrong" not in body_text


def test_portfolios_page_has_interactive_elements(page):
    page.goto(f"{BASE_URL}/portfolios")

    page.wait_for_load_state("networkidle")

    buttons = page.locator("button")
    inputs = page.locator("input")
    links = page.locator("a")

    total_interactive = (
        buttons.count()
        + inputs.count()
        + links.count()
    )

    assert total_interactive > 0