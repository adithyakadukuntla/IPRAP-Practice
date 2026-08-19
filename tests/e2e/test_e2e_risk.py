"""
E2E Tests - Risk

Validates:

Portfolio
    ↓
Holdings
    ↓
Risk analysis
"""


def test_risk_end_to_end(api_client):
    """
    E2E-005:
    Validate risk analysis against portfolio holdings.
    """

    portfolio_id = "P10001"

    # ---------------------------------------------------------
    # Portfolio
    # ---------------------------------------------------------

    portfolio_response = api_client.get(
        f"/portfolios/{portfolio_id}"
    )

    assert portfolio_response.status_code == 200

    portfolio = portfolio_response.json()

    # ---------------------------------------------------------
    # Holdings
    # ---------------------------------------------------------

    holdings_response = api_client.get(
        f"/portfolios/{portfolio_id}/holdings"
    )

    assert holdings_response.status_code == 200

    holdings = holdings_response.json()["items"]

    # ---------------------------------------------------------
    # Risk
    # ---------------------------------------------------------

    risk_response = api_client.get(
        f"/portfolios/{portfolio_id}/risk"
    )

    assert risk_response.status_code == 200

    risk = risk_response.json()

    assert risk["portfolio_id"] == portfolio_id

    # ---------------------------------------------------------
    # Basic risk fields
    # ---------------------------------------------------------

    assert risk.get("portfolio_name")

    assert risk.get("client_id")

    assert risk.get("risk_status")

    assert risk.get("concentration_risk")

    # ---------------------------------------------------------
    # Holdings consistency
    # ---------------------------------------------------------

    if "holding_count" in risk:

        assert risk["holding_count"] == len(holdings)

    # ---------------------------------------------------------
    # Risk values
    # ---------------------------------------------------------

    if risk.get("highest_holding_value") is not None:

        assert float(
            risk["highest_holding_value"]
        ) >= 0

    if risk.get("highest_weight_percent") is not None:

        weight = float(
            risk["highest_weight_percent"]
        )

        assert 0 <= weight <= 100

    if risk.get("current_value") is not None:

        assert float(
            risk["current_value"]
        ) >= 0

    if risk.get("total_market_value") is not None:

        assert float(
            risk["total_market_value"]
        ) >= 0