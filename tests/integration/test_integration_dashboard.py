"""
Integration Tests - Dashboard

Validates:
Dashboard → Portfolio Service → Repository → Database
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


def test_dashboard_portfolio_value_consistency(
    api_client
):
    """
    Verify dashboard total portfolio value is consistent
    with portfolio API data.
    """

    dashboard_response = api_client.get(
        "/dashboard"
    )

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