import requests


BASE_URL = "http://127.0.0.1:8000/api/v1"


def test_api_is_monitorable():
    response = requests.get(
        f"{BASE_URL}/health"
    )

    assert response.status_code == 200


def test_health_response_is_valid():
    response = requests.get(
        f"{BASE_URL}/health"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "UP"
    assert "service" in data
    assert "version" in data


def test_invalid_request_returns_structured_error():
    response = requests.get(
        f"{BASE_URL}/portfolios",
        params={"page": "invalid"}
    )

    assert response.status_code == 422

    data = response.json()

    assert "detail" in data


def test_not_found_error_is_observable():
    response = requests.get(
        f"{BASE_URL}/portfolios/PXXXX"
    )

    assert response.status_code == 404

    data = response.json()

    assert "detail" in data


def test_error_response_does_not_expose_secrets():
    response = requests.get(
        f"{BASE_URL}/portfolios/PXXXX"
    )

    body = response.text.lower()

    forbidden = [
        "password",
        "secret_key",
        "aws_secret",
        "access_key",
        "traceback",
    ]

    for value in forbidden:
        assert value not in body