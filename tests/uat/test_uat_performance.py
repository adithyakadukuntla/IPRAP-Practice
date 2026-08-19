def test_uat_portfolio_performance(api_client):
    response = api_client.get(
        "/portfolios/P10001/performance"
    )

    assert response.status_code == 200

    data = response.json()

    assert "items" in data
    assert "portfolio_id" in data
    assert "interval" in data

    assert data["portfolio_id"] == "P10001"