"""
Integration Tests - Risk

Validates:

Portfolio
    ↓
Risk API
    ↓
Risk Service
    ↓
Repository
    ↓
Database/Data Source

The tests also validate:
- Risk response structure
- Portfolio/risk relationship
- Risk/holdings consistency
- Market value consistency
- Holding count consistency
- Portfolio risk profile consistency
- Unknown portfolio handling
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
    holdings and reports a valid holding count and value.
    """

    portfolio_id = "P10001"

    holdings_response = api_client.get(
        f"/portfolios/{portfolio_id}/holdings"
        "?page=1&page_size=100"
    )

    risk_response = api_client.get(
        f"/portfolios/{portfolio_id}/risk"
    )

    assert holdings_response.status_code == 200
    assert risk_response.status_code == 200

    holdings_data = holdings_response.json()
    risk_data = risk_response.json()

    holdings = holdings_data["items"]

    assert isinstance(holdings, list)

    assert risk_data["holding_count"] == len(holdings), (
        "Risk holding count does not match "
        "holdings API"
    )

    calculated_total = sum(
        float(holding["market_value"] or 0)
        for holding in holdings
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


def test_risk_portfolio_consistency(api_client):
    """
    Verify that the risk response belongs to the
    requested portfolio.
    """

    portfolio_id = "P10001"

    response = api_client.get(
        f"/portfolios/{portfolio_id}/risk"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["portfolio_id"] == portfolio_id


def test_risk_profile_consistency(api_client):
    """
    Verify that the risk analysis uses the same
    risk profile reported by the portfolio API.
    """

    portfolio_id = "P10001"

    portfolio_response = api_client.get(
        f"/portfolios/{portfolio_id}"
    )

    risk_response = api_client.get(
        f"/portfolios/{portfolio_id}/risk"
    )

    assert portfolio_response.status_code == 200
    assert risk_response.status_code == 200

    portfolio = portfolio_response.json()
    risk = risk_response.json()

    assert "risk_profile" in portfolio
    assert "portfolio_risk_profile" in risk

    assert (
        portfolio["risk_profile"]
        == risk["portfolio_risk_profile"]
    ), (
        "Risk profile reported by risk API does not "
        "match portfolio API"
    )


def test_unknown_portfolio_risk_integration(
    api_client
):
    """
    Verify that requesting risk information for
    an unknown portfolio returns the expected error.
    """

    response = api_client.get(
        "/portfolios/PXXXX/risk"
    )

    assert response.status_code == 404

    data = response.json()

    assert isinstance(data, dict)
    assert "detail" in data