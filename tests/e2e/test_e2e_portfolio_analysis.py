"""
E2E Tests - Complete Portfolio Analysis

Validates the complete flow:

Portfolio
    ↓
Holdings
    ↓
Performance
    ↓
Risk
    ↓
Cross-component consistency
"""


def test_complete_portfolio_analysis(api_client):
    """
    E2E-001:
    Validate that a portfolio can be retrieved and analyzed
    through holdings, performance, and risk APIs.
    """

    portfolio_id = "P10001"

    # ---------------------------------------------------------
    # Step 1: Get portfolio
    # ---------------------------------------------------------

    portfolio_response = api_client.get(
        f"/portfolios/{portfolio_id}"
    )

    assert portfolio_response.status_code == 200

    portfolio = portfolio_response.json()

    assert portfolio["portfolio_id"] == portfolio_id

    # ---------------------------------------------------------
    # Step 2: Get holdings
    # ---------------------------------------------------------

    holdings_response = api_client.get(
        f"/portfolios/{portfolio_id}/holdings"
    )

    assert holdings_response.status_code == 200

    holdings_data = holdings_response.json()

    assert "items" in holdings_data

    holdings = holdings_data["items"]

    # Every holding must belong to the requested portfolio
    for holding in holdings:
        assert holding["portfolio_id"] == portfolio_id

    # ---------------------------------------------------------
    # Step 3: Get performance
    # ---------------------------------------------------------

    performance_response = api_client.get(
        f"/portfolios/{portfolio_id}/performance"
    )

    assert performance_response.status_code == 200

    performance_data = performance_response.json()

    assert performance_data["portfolio_id"] == portfolio_id
    assert "items" in performance_data

    # ---------------------------------------------------------
    # Step 4: Get risk
    # ---------------------------------------------------------

    risk_response = api_client.get(
        f"/portfolios/{portfolio_id}/risk"
    )

    assert risk_response.status_code == 200

    risk_data = risk_response.json()

    assert risk_data["portfolio_id"] == portfolio_id

    # ---------------------------------------------------------
    # Step 5: Validate portfolio → holdings consistency
    # ---------------------------------------------------------

    if holdings:

        holding_count = len(holdings)

        assert holding_count == portfolio["holding_count"], (
            f"Holding count mismatch: "
            f"portfolio={portfolio['holding_count']}, "
            f"actual={holding_count}"
        )

    # ---------------------------------------------------------
    # Step 6: Validate portfolio values
    # ---------------------------------------------------------

    assert float(portfolio["current_value"]) >= 0
    assert float(portfolio["total_market_value"]) >= 0

    # ---------------------------------------------------------
    # Step 7: Validate risk references same portfolio
    # ---------------------------------------------------------

    assert risk_data["portfolio_id"] == portfolio_id

    # ---------------------------------------------------------
    # Final E2E validation
    # ---------------------------------------------------------

    assert portfolio is not None
    assert holdings_data is not None
    assert performance_data is not None
    assert risk_data is not None