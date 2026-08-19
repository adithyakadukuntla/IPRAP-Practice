import pytest
from playwright.sync_api import expect


BASE_URL = "http://localhost:5173"


def test_dashboard_page_loads(page):
    page.goto(f"{BASE_URL}/dashboard")

    expect(page).to_have_url(f"{BASE_URL}/dashboard")


def test_dashboard_has_content(page):
    page.goto(f"{BASE_URL}/dashboard")

    expect(page.locator("body")).to_be_visible()

    assert page.locator("body").inner_text().strip() != ""


def test_dashboard_displays_kpis(page):
    page.goto(f"{BASE_URL}/dashboard")

    page.wait_for_load_state("networkidle")

    body_text = page.locator("body").inner_text().lower()

    expected_terms = [
        "portfolio",
        "return",
        "risk",
    ]

    matches = sum(
        term in body_text
        for term in expected_terms
    )

    assert matches >= 2


def test_dashboard_no_error(page):
    page.goto(f"{BASE_URL}/dashboard")

    page.wait_for_load_state("networkidle")

    body_text = page.locator("body").inner_text().lower()

    assert "internal server error" not in body_text
    assert "application error" not in body_text