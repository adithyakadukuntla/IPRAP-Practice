def test_uat_portfolio_allocation(api_client):
    response = api_client.get(
        "/portfolios/P10001/allocation"
    )

    assert response.status_code == 200

    data = response.json()

    assert "items" in data
    assert "dimension" in data

    for item in data["items"]:
        assert item["portfolio_id"] == "P10001"
        assert item["security_id"]
        assert item["security_name"]