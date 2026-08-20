"""
Dashboard Defect Regression Tests
"""


def test_dashboard_endpoint_exists(api_client):
    response = api_client.get("/dashboard")

    assert response.status_code == 200


def test_dashboard_kpis_present(api_client):
    response = api_client.get("/dashboard")

    assert response.status_code == 200

    data = response.json()

    required_fields = [
        "total_portfolio_value",
        "active_portfolios",
        "average_return",
        "high_risk_portfolios",
        "total_holdings",
    ]

    for field in required_fields:
        assert field in data


def test_dashboard_values_non_negative(api_client):
    response = api_client.get("/dashboard")

    assert response.status_code == 200

    data = response.json()

    assert data["total_portfolio_value"] >= 0
    assert data["active_portfolios"] >= 0
    assert data["high_risk_portfolios"] >= 0
    assert data["total_holdings"] >= 0


def test_dashboard_matches_portfolios(api_client):
    dashboard_response = api_client.get(
        "/dashboard"
    )

    portfolio_response = api_client.get(
        "/portfolios",
        params={
            "page": 1,
            "page_size": 100
        }
    )

    assert dashboard_response.status_code == 200
    assert portfolio_response.status_code == 200

    dashboard = dashboard_response.json()
    portfolios = portfolio_response.json()

    calculated_total = sum(
        float(p.get("current_value") or 0)
        for p in portfolios["items"]
    )

    dashboard_total = float(
        dashboard["total_portfolio_value"]
    )

    assert abs(
        calculated_total - dashboard_total
    ) < 1.0