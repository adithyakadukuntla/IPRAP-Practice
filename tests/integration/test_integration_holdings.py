"""
Integration Tests - Holdings

Validates:
Portfolio → Holdings API → Service → Repository → Database
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
            f"{holding['holding_id']}"
        )