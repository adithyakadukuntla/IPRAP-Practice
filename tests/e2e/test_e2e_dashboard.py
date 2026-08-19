"""
E2E Tests - Dashboard

Validates:

Portfolio API
      ↓
Dashboard API
      ↓
KPI consistency
"""


def test_dashboard_end_to_end(api_client):
    """
    E2E-002:
    Validate dashboard KPIs against portfolio data.
    """

    dashboard_response = api_client.get(
        "/dashboard"
    )

    assert dashboard_response.status_code == 200

    dashboard = dashboard_response.json()

    required_fields = [
        "total_portfolio_value",
        "active_portfolios",
        "average_return",
        "high_risk_portfolios",
        "total_holdings",
    ]

    for field in required_fields:
        assert field in dashboard, (
            f"Dashboard missing field: {field}"
        )

    # Get all portfolios.
    portfolio_response = api_client.get(
        "/portfolios?page=1&page_size=100"
    )

    assert portfolio_response.status_code == 200

    portfolio_data = portfolio_response.json()

    portfolios = portfolio_data.get(
        "items",
        []
    )

    # ---------------------------------------------------------
    # Calculate expected dashboard values
    # ---------------------------------------------------------

    total_value = sum(
        float(p.get("current_value") or 0)
        for p in portfolios
    )

    active_count = sum(
        1
        for p in portfolios
        if str(p.get("status", "")).upper() == "ACTIVE"
    )

    high_risk_count = sum(
        1
        for p in portfolios
        if str(p.get("risk_profile", "")).upper() == "HIGH"
    )

    total_holdings = sum(
        int(p.get("holding_count") or 0)
        for p in portfolios
    )

    returns = [
        float(p["return_percent"])
        for p in portfolios
        if p.get("return_percent") is not None
    ]

    expected_average_return = (
        sum(returns) / len(returns)
        if returns
        else 0
    )

    # ---------------------------------------------------------
    # Validate dashboard
    # ---------------------------------------------------------

    assert abs(
        float(dashboard["total_portfolio_value"])
        - total_value
    ) < 1.0

    assert dashboard["active_portfolios"] == active_count

    assert dashboard["high_risk_portfolios"] == high_risk_count

    assert dashboard["total_holdings"] == total_holdings

    assert abs(
        float(dashboard["average_return"])
        - expected_average_return
    ) < 0.01