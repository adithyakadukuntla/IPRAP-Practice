"""
Integration Tests - Dashboard

Validates:

Dashboard API
    ↓
Portfolio Service
    ↓
Repository
    ↓
Database/Data Source

The tests also perform reconciliation between
dashboard KPIs and portfolio API data.
"""


def test_dashboard_integration(api_client):
    """
    Verify dashboard KPI data is successfully generated
    from portfolio data.
    """

    response = api_client.get("/dashboard")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, dict)

    required_fields = [
        "total_portfolio_value",
        "active_portfolios",
        "average_return",
        "high_risk_portfolios",
        "total_holdings",
    ]

    for field in required_fields:
        assert field in data, (
            f"Missing dashboard KPI: {field}"
        )


def test_dashboard_portfolio_value_consistency(api_client):
    """
    Verify dashboard total portfolio value is consistent
    with portfolio API data.
    """

    dashboard_response = api_client.get("/dashboard")

    portfolio_response = api_client.get(
        "/portfolios?page=1&page_size=100"
    )

    assert dashboard_response.status_code == 200
    assert portfolio_response.status_code == 200

    dashboard = dashboard_response.json()
    portfolios = portfolio_response.json()

    items = portfolios["items"]

    calculated_total = sum(
        float(p.get("current_value") or 0)
        for p in items
    )

    dashboard_total = float(
        dashboard["total_portfolio_value"]
    )

    assert abs(
        calculated_total - dashboard_total
    ) < 1.0, (
        "Dashboard portfolio value does not match "
        "portfolio data"
    )


def test_dashboard_active_portfolio_count_consistency(
    api_client
):
    """
    Verify dashboard active portfolio count is
    consistent with portfolio API data.
    """

    dashboard_response = api_client.get("/dashboard")

    portfolio_response = api_client.get(
        "/portfolios?page=1&page_size=100"
    )

    assert dashboard_response.status_code == 200
    assert portfolio_response.status_code == 200

    dashboard = dashboard_response.json()
    portfolios = portfolio_response.json()

    items = portfolios["items"]

    calculated_active = sum(
        1
        for portfolio in items
        if str(
            portfolio.get("status", "")
        ).upper() == "ACTIVE"
    )

    dashboard_active = int(
        dashboard["active_portfolios"]
    )

    assert calculated_active == dashboard_active, (
        "Dashboard active portfolio count does not "
        "match portfolio data"
    )


def test_dashboard_average_return_consistency(
    api_client
):
    """
    Verify dashboard average return is consistent
    with portfolio API data.
    """

    dashboard_response = api_client.get("/dashboard")

    portfolio_response = api_client.get(
        "/portfolios?page=1&page_size=100"
    )

    assert dashboard_response.status_code == 200
    assert portfolio_response.status_code == 200

    dashboard = dashboard_response.json()
    portfolios = portfolio_response.json()

    items = portfolios["items"]

    returns = [
        float(portfolio["return_percent"])
        for portfolio in items
        if portfolio.get("return_percent") is not None
    ]

    assert returns, (
        "No portfolio return data available "
        "for average calculation"
    )

    calculated_average = (
        sum(returns) / len(returns)
    )

    dashboard_average = float(
        dashboard["average_return"]
    )

    assert abs(
        calculated_average - dashboard_average
    ) < 0.01, (
        "Dashboard average return does not match "
        "portfolio data"
    )


def test_dashboard_high_risk_count_consistency(
    api_client
):
    """
    Verify dashboard high-risk portfolio count is
    consistent with portfolio API data.

    This assumes the dashboard defines a high-risk
    portfolio using risk_profile == 'HIGH'.
    """

    dashboard_response = api_client.get("/dashboard")

    portfolio_response = api_client.get(
        "/portfolios?page=1&page_size=100"
    )

    assert dashboard_response.status_code == 200
    assert portfolio_response.status_code == 200

    dashboard = dashboard_response.json()
    portfolios = portfolio_response.json()

    items = portfolios["items"]

    calculated_high_risk = sum(
        1
        for portfolio in items
        if str(
            portfolio.get("risk_profile", "")
        ).upper() == "HIGH"
    )

    dashboard_high_risk = int(
        dashboard["high_risk_portfolios"]
    )

    assert calculated_high_risk == dashboard_high_risk, (
        "Dashboard high-risk portfolio count does not "
        "match portfolio data"
    )


def test_dashboard_total_holdings_consistency(
    api_client
):
    """
    Verify dashboard total holdings is consistent
    with portfolio holding_count values.

    This assumes portfolio holding_count represents
    the number of holdings belonging to that portfolio.
    """

    dashboard_response = api_client.get("/dashboard")

    portfolio_response = api_client.get(
        "/portfolios?page=1&page_size=100"
    )

    assert dashboard_response.status_code == 200
    assert portfolio_response.status_code == 200

    dashboard = dashboard_response.json()
    portfolios = portfolio_response.json()

    items = portfolios["items"]

    calculated_holdings = sum(
        int(portfolio.get("holding_count") or 0)
        for portfolio in items
    )

    dashboard_holdings = int(
        dashboard["total_holdings"]
    )

    assert calculated_holdings == dashboard_holdings, (
        "Dashboard total holdings does not match "
        "portfolio data"
    )