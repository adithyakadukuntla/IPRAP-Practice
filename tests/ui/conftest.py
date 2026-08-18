import pytest
from playwright.sync_api import Page


FRONTEND_URL = "http://localhost:5173"


@pytest.fixture
def frontend_url():
    return FRONTEND_URL


@pytest.fixture
def open_app(page: Page, frontend_url):
    page.goto(
        frontend_url,
        wait_until="domcontentloaded"
    )

    return page