"""
Performance Defect Regression Tests
"""


def test_health_endpoint_exists(api_client):
    response = api_client.get("/health")

    assert response.status_code == 200


def test_health_response_schema(api_client):
    response = api_client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert "status" in data
    assert "service" in data
    assert "version" in data


def test_performance_endpoint_exists(api_client):
    response = api_client.get(
        "/portfolios/P10001/performance"
    )

    assert response.status_code == 200


def test_performance_invalid_range(api_client):
    response = api_client.get(
        "/portfolios/P10001/performance",
        params={
            "from": "2026-08-20",
            "to": "2026-08-01",
        }
    )

    assert response.status_code == 400