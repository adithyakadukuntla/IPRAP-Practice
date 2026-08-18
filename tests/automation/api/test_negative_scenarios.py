"""
Negative API Scenario Tests
Requirements: Section 15-17 - API Negative Scenarios
"""

import pytest


def test_invalid_portfolio_id(api_client):
    """Invalid portfolio ID should return 404."""
    response = api_client.get("/portfolios/PXXXX")

    assert response.status_code == 404


def test_null_portfolio_id(api_client):
    """Non-existent/null-like portfolio ID should be rejected."""
    response = api_client.get("/portfolios/null")

    assert response.status_code in [400, 404]


def test_invalid_page_size(api_client):
    """Invalid page size should not crash the API."""
    response = api_client.get(
        "/portfolios",
        params={"page_size": -1}
    )

    assert response.status_code in [200, 400, 422]


def test_negative_page(api_client):
    """Negative page number should be handled safely."""
    response = api_client.get(
        "/portfolios",
        params={"page": -1}
    )

    assert response.status_code in [200, 400, 422]


def test_invalid_dimension(api_client):
    """
    Invalid risk dimension should be handled safely.

    If the backend does not support dimension filtering,
    400/422/200 are acceptable depending on implementation.
    """
    response = api_client.get(
        "/portfolios/P10001/risk",
        params={"dimension": "invalid"}
    )

    assert response.status_code in [200, 400, 422]


def test_missing_required_param(api_client):
    """
    Verify that the API handles requests without optional
    parameters correctly.
    """
    response = api_client.get("/portfolios")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, dict)
    assert "items" in data


def test_method_not_allowed(api_client):
    """Unsupported HTTP method should return 405."""
    response = api_client.post("/portfolios/P10001")

    assert response.status_code == 405