def test_uat_portfolio_list(api_client):
    response = api_client.get(
        "/portfolios",
        params={
            "page": 1,
            "page_size": 20
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "items" in data
    assert "page" in data
    assert "page_size" in data
    assert "total_items" in data
    assert "total_pages" in data


def test_uat_portfolio_details(api_client):
    response = api_client.get(
        "/portfolios/P10001"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["portfolio_id"] == "P10001"
    assert data["portfolio_name"]
    assert data["current_value"] >= 0
    assert data["status"]