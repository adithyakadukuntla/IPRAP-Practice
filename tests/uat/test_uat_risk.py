def test_uat_portfolio_risk(api_client):
    response = api_client.get(
        "/portfolios/P10001/risk"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["portfolio_id"] == "P10001"
    assert data["portfolio_name"]
    assert data["portfolio_risk_profile"]

    assert data["highest_holding_value"] >= 0
    assert data["highest_weight_percent"] >= 0

    assert data["concentration_risk"]
    assert data["risk_status"]
    assert data["risk_explanation"]