"""
UI Tests - Performance
"""

from playwright.sync_api import Page, expect


def test_performance_page_loads(open_app: Page):
    """
    Performance page should load successfully.
    """

    page = open_app

    page.goto(
        "http://localhost:5173/portfolios/P10001/performance",
        wait_until="domcontentloaded"
    )

    expect(page.locator("body")).to_be_visible()


def test_performance_page_contains_performance_data(
    open_app: Page
):
    """
    Performance page should display performance information.
    """

    page = open_app

    page.goto(
        "http://localhost:5173/portfolios/P10001/performance",
        wait_until="domcontentloaded"
    )

    body = page.locator("body")

    expect(body).to_contain_text(
        "Performance",
        timeout=10000
    )


def test_performance_page_no_server_error(open_app: Page):
    """
    Performance page should not display server errors.
    """

    page = open_app

    page.goto(
        "http://localhost:5173/portfolios/P10001/performance",
        wait_until="domcontentloaded"
    )

    body_text = page.locator("body").inner_text().lower()

    assert "internal server error" not in body_text
    assert "500 internal" not in body_text