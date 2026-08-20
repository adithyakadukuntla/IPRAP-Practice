"""
Integration Tests - Holdings

Validates:

Portfolio
    ↓
Holdings API
    ↓
Service
    ↓
Repository
    ↓
Database/Data Source

The tests also validate:
- Portfolio/holding relationships
- Required holding fields
- Market value calculations
- Pagination
- Holding count consistency
- Unknown portfolio behavior
"""


def test_portfolio_holdings_integration(api_client):
    """
    Verify that holdings retrieved for a portfolio
    belong to the requested portfolio.
    """

    portfolio_id = "P10001"

    response = api_client.get(
        f"/portfolios/{portfolio_id}/holdings"
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, dict)
    assert "items" in data

    holdings = data["items"]

    assert isinstance(holdings, list)
    assert len(holdings) > 0

    for holding in holdings:

        assert "holding_id" in holding
        assert "portfolio_id" in holding
        assert "security_id" in holding
        assert "quantity" in holding
        assert "current_price" in holding
        assert "market_value" in holding

        # Integration consistency check
        assert holding["portfolio_id"] == portfolio_id


def test_holding_value_integration(api_client):
    """
    Verify that holding market value is consistent
    with quantity and current price.
    """

    response = api_client.get(
        "/portfolios/P10001/holdings"
    )

    assert response.status_code == 200

    data = response.json()

    holdings = data["items"]

    assert isinstance(holdings, list)
    assert len(holdings) > 0

    for holding in holdings:

        quantity = float(
            holding["quantity"]
        )

        current_price = float(
            holding["current_price"]
        )

        market_value = float(
            holding["market_value"]
        )

        expected_value = (
            quantity * current_price
        )

        assert abs(
            market_value - expected_value
        ) < 1.0, (
            f"Market value mismatch for "
            f"{holding['holding_id']}: "
            f"expected {expected_value}, "
            f"actual {market_value}"
        )


def test_holdings_pagination_integration(api_client):
    """
    Verify that holdings API pagination returns
    a valid paginated response.
    """

    response = api_client.get(
        "/portfolios/P10001/holdings"
        "?page=1&page_size=10"
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


def test_holding_count_consistency(api_client):
    """
    Verify that the portfolio holding_count is
    consistent with the holdings API total_items.
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

    portfolio_holding_count = int(
        portfolio["holding_count"]
    )

    actual_holding_count = int(
        holdings["total_items"]
    )

    assert portfolio_holding_count == actual_holding_count, (
        f"Holding count mismatch for {portfolio_id}: "
        f"portfolio reports "
        f"{portfolio_holding_count}, "
        f"but holdings API reports "
        f"{actual_holding_count}"
    )


def test_unknown_portfolio_holdings_integration(
    api_client
):
    """
    Verify that requesting holdings for an unknown
    portfolio returns the expected error response.
    """

    response = api_client.get(
        "/portfolios/PXXXX/holdings"
    )

    assert response.status_code == 404

    data = response.json()

    assert isinstance(data, dict)

    assert "detail" in data