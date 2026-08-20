def test_uat_dashboard_loads(api_client):
    response = api_client.get("/dashboard")

    assert response.status_code == 200

    data = response.json()

    assert "total_portfolio_value" in data
    assert "active_portfolios" in data
    assert "average_return" in data
    assert "high_risk_portfolios" in data
    assert "total_holdings" in data


def test_uat_dashboard_has_valid_business_values(api_client):
    response = api_client.get("/dashboard")

    assert response.status_code == 200

    data = response.json()

    assert data["total_portfolio_value"] >= 0
    assert data["active_portfolios"] >= 0
    assert data["total_holdings"] >= 0