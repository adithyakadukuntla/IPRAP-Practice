"""
Integration Tests - Portfolio

Validates integration between:
API → Portfolio Service → Repository → Database
"""

import pytest


def test_portfolio_api_repository_integration(api_client):
    """
    Verify that portfolio data returned by the API
    is successfully retrieved through the service/repository layer.
    """

    response = api_client.get("/portfolios/P10001")

    assert response.status_code == 200

    data = response.json()

    assert data is not None
    assert isinstance(data, dict)

    # Required portfolio information
    required_fields = [
        "portfolio_id",
        "portfolio_name",
        "client_id",
    ]

    for field in required_fields:
        assert field in data, (
            f"Missing portfolio field: {field}"
        )

    assert data["portfolio_id"] == "P10001"


def test_portfolio_list_repository_integration(api_client):
    """
    Verify that portfolio listing successfully retrieves
    multiple records through the backend layers.
    """

    response = api_client.get("/portfolios")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, dict)

    assert "items" in data

    portfolios = data["items"]

    assert isinstance(portfolios, list)
    assert len(portfolios) > 0

    for portfolio in portfolios:

        assert "portfolio_id" in portfolio
        assert "portfolio_name" in portfolio
        assert "client_id" in portfolio