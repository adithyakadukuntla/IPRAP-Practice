def test_uat_portfolio_holdings(api_client):
    response = api_client.get(
        "/portfolios/P10001/holdings"
    )

    assert response.status_code == 200

    data = response.json()

    assert "items" in data

    for holding in data["items"]:
        assert holding["holding_id"]
        assert holding["security_id"]
        assert holding["security_name"]
        assert holding["quantity"] >= 0
        assert holding["market_value"] >= 0