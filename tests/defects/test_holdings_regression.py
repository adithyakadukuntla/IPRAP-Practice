"""
Holdings Defect Regression Tests
"""


def test_holdings_endpoint_exists(api_client):
    response = api_client.get(
        "/portfolios/P10001/holdings"
    )

    assert response.status_code == 200


def test_holdings_pagination(api_client):
    response = api_client.get(
        "/portfolios/P10001/holdings",
        params={
            "page": 1,
            "page_size": 20,
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "items" in data
    assert "page" in data
    assert "page_size" in data
    assert "total_items" in data
    assert "total_pages" in data


def test_holdings_large_reconciliation_page(api_client):
    response = api_client.get(
        "/portfolios/P10001/holdings",
        params={
            "page": 1,
            "page_size": 1000,
        }
    )

    assert response.status_code == 200


def test_invalid_holdings_portfolio(api_client):
    response = api_client.get(
        "/portfolios/PXXXX/holdings"
    )

    assert response.status_code == 404