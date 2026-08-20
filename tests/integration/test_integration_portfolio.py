"""
Integration Tests - Portfolio

Validates integration between:

API
 ↓
Portfolio Service
 ↓
Repository
 ↓
Database/Data Source

The tests also validate:
- Portfolio retrieval
- Portfolio listing
- Required fields
- Portfolio/holdings consistency
- Pagination
- Unknown portfolio handling
"""

import pytest


def test_portfolio_api_repository_integration(api_client):
    """
    Verify that portfolio data returned by the API
    is successfully retrieved through the
    service/repository layer.
    """

    portfolio_id = "P10001"

    response = api_client.get(
        f"/portfolios/{portfolio_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data is not None
    assert isinstance(data, dict)

    required_fields = [
        "portfolio_id",
        "portfolio_name",
        "client_id",
    ]

    for field in required_fields:
        assert field in data, (
            f"Missing portfolio field: {field}"
        )

    assert data["portfolio_id"] == portfolio_id


def test_portfolio_list_repository_integration(
    api_client
):
    """
    Verify that portfolio listing successfully retrieves
    multiple records through the backend layers.
    """

    response = api_client.get(
        "/portfolios?page=1&page_size=100"
    )

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


def test_portfolio_pagination_integration(
    api_client
):
    """
    Verify that portfolio pagination works correctly
    through the API/service/repository layers.
    """

    response = api_client.get(
        "/portfolios?page=1&page_size=10"
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, dict)

    assert "items" in data
    assert "page" in data
    assert "page_size" in data
    assert "total_items" in data
    assert "total_pages" in data

    assert isinstance(data["items"], list)

    assert data["page"] == 1
    assert data["page_size"] == 10

    assert data["total_items"] >= 0
    assert data["total_pages"] >= 0

    assert len(data["items"]) <= data["page_size"]


def test_portfolio_holdings_count_integration(
    api_client
):
    """
    Verify that the holding_count reported by the
    portfolio API is consistent with the holdings API.
    """

    portfolio_id = "P10001"

    portfolio_response = api_client.get(
        f"/portfolios/{portfolio_id}"
    )

    holdings_response = api_client.get(
        f"/portfolios/{portfolio_id}/holdings"
        "?page=1&page_size=100"
    )

    assert portfolio_response.status_code == 200
    assert holdings_response.status_code == 200

    portfolio = portfolio_response.json()
    holdings = holdings_response.json()

    assert "holding_count" in portfolio
    assert "total_items" in holdings

    portfolio_count = int(
        portfolio["holding_count"]
    )

    holdings_count = int(
        holdings["total_items"]
    )

    assert portfolio_count == holdings_count, (
        f"Holding count mismatch for {portfolio_id}: "
        f"portfolio reports {portfolio_count}, "
        f"but holdings API reports {holdings_count}"
    )


def test_unknown_portfolio_integration(
    api_client
):
    """
    Verify that requesting an unknown portfolio
    returns the expected error response.
    """

    response = api_client.get(
        "/portfolios/PXXXX"
    )

    assert response.status_code == 404

    data = response.json()

    assert isinstance(data, dict)
    assert "detail" in data


def test_portfolio_id_uniqueness_integration(
    api_client
):
    """
    Verify that the portfolio listing does not
    contain duplicate portfolio IDs.
    """

    response = api_client.get(
        "/portfolios?page=1&page_size=100"
    )

    assert response.status_code == 200

    data = response.json()

    portfolios = data["items"]

    portfolio_ids = [
        portfolio["portfolio_id"]
        for portfolio in portfolios
    ]

    assert len(portfolio_ids) == len(
        set(portfolio_ids)
    ), (
        "Duplicate portfolio IDs found "
        "in portfolio listing"
    )