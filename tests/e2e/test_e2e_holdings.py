"""
E2E Tests - Holdings

Validates:

Portfolio
    ↓
Holdings
    ↓
Holding values
    ↓
Portfolio consistency
"""


def test_holdings_end_to_end(api_client):
    """
    E2E-003:
    Validate holdings belong to the selected portfolio
    and contain valid financial values.
    """

    portfolio_id = "P10001"

    portfolio_response = api_client.get(
        f"/portfolios/{portfolio_id}"
    )

    assert portfolio_response.status_code == 200

    portfolio = portfolio_response.json()

    holdings_response = api_client.get(
        f"/portfolios/{portfolio_id}/holdings"
    )

    assert holdings_response.status_code == 200

    holdings_data = holdings_response.json()

    assert "items" in holdings_data

    holdings = holdings_data["items"]

    # ---------------------------------------------------------
    # Validate ownership
    # ---------------------------------------------------------

    for holding in holdings:

        assert holding["portfolio_id"] == portfolio_id

        assert holding.get("holding_id")

        assert holding.get("security_id")

        assert holding.get("ticker_symbol")

    # ---------------------------------------------------------
    # Validate financial values
    # ---------------------------------------------------------

    for holding in holdings:

        assert float(
            holding["quantity"]
        ) >= 0

        assert float(
            holding["purchase_price"]
        ) >= 0

        assert float(
            holding["current_price"]
        ) >= 0

        assert float(
            holding["market_value"]
        ) >= 0

    # ---------------------------------------------------------
    # Validate count
    # ---------------------------------------------------------

    assert len(holdings) == portfolio["holding_count"]