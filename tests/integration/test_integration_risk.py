"""
Integration Tests - Risk

Validates:
Portfolio → Risk Service → Repository → Database
"""


def test_risk_integration(api_client):
    """
    Verify that risk analysis successfully integrates
    portfolio and holdings data.
    """

    portfolio_id = "P10001"

    response = api_client.get(
        f"/portfolios/{portfolio_id}/risk"
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, dict)

    required_fields = [
        "portfolio_id",
        "portfolio_risk_profile",
        "concentration_risk",
        "risk_status",
        "total_market_value",
        "holding_count",
    ]

    for field in required_fields:
        assert field in data, (
            f"Missing risk field: {field}"
        )

    assert data["portfolio_id"] == portfolio_id


def test_risk_holdings_consistency(api_client):
    """
    Verify that risk analysis is based on the portfolio's
    holdings and reports a valid holding count/value.
    """

    portfolio_id = "P10001"

    holdings_response = api_client.get(
        f"/portfolios/{portfolio_id}/holdings"
    )

    risk_response = api_client.get(
        f"/portfolios/{portfolio_id}/risk"
    )

    assert holdings_response.status_code == 200
    assert risk_response.status_code == 200

    holdings_data = holdings_response.json()
    risk_data = risk_response.json()

    holdings = holdings_data["items"]

    assert risk_data["holding_count"] == len(holdings)

    calculated_total = sum(
        float(h["market_value"])
        for h in holdings
    )

    reported_total = float(
        risk_data["total_market_value"]
    )

    assert abs(
        calculated_total - reported_total
    ) < 1.0, (
        "Risk total market value does not match "
        "holdings total"
    )