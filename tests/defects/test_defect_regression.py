"""
Defect Regression Tests

Verifies that previously identified API defects remain fixed.
"""

def test_invalid_portfolio_returns_404(api_client):
    response = api_client.get(
        "/portfolios/PXXXX"
    )

    assert response.status_code == 404


def test_invalid_portfolio_holdings_returns_404(api_client):
    response = api_client.get(
        "/portfolios/PXXXX/holdings"
    )

    assert response.status_code == 404


def test_invalid_portfolio_risk_returns_404(api_client):
    response = api_client.get(
        "/portfolios/PXXXX/risk"
    )

    assert response.status_code == 404


def test_invalid_date_range_returns_400(api_client):
    response = api_client.get(
        "/portfolios/P10001/performance",
        params={
            "from": "2026-08-20",
            "to": "2026-08-01",
        }
    )

    assert response.status_code == 400


def test_invalid_performance_interval_returns_400(api_client):
    response = api_client.get(
        "/portfolios/P10001/performance",
        params={
            "interval": "invalid"
        }
    )

    assert response.status_code == 400


def test_invalid_page_returns_422(api_client):
    response = api_client.get(
        "/portfolios",
        params={
            "page": 0
        }
    )

    assert response.status_code == 422


def test_invalid_page_size_returns_422(api_client):
    response = api_client.get(
        "/portfolios",
        params={
            "page_size": 0
        }
    )

    assert response.status_code == 422


def test_large_portfolio_page_size_rejected(api_client):
    response = api_client.get(
        "/portfolios",
        params={
            "page_size": 1001
        }
    )

    assert response.status_code == 422


def test_invalid_holdings_page_size_rejected(api_client):
    response = api_client.get(
        "/portfolios/P10001/holdings",
        params={
            "page_size": 1001
        }
    )

    assert response.status_code == 422