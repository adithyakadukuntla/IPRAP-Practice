import os
import pytest
import requests


BASE_URL = os.getenv(
    "API_BASE_URL",
    "http://127.0.0.1:8000/api/v1"
)


class APIClient:
    """
    Simple HTTP client used by API and integration tests.
    """

    def __init__(self, base_url):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()

    def _url(self, endpoint):
        endpoint = endpoint.lstrip("/")

        # Health endpoint is outside /api/v1
        if endpoint == "health":
            return "http://127.0.0.1:8000/api/v1/health"

        return f"{self.base_url}/{endpoint}"

    def get(self, endpoint, **kwargs):
        return self.session.get(
            self._url(endpoint),
            **kwargs
        )

    def post(self, endpoint, **kwargs):
        return self.session.post(
            self._url(endpoint),
            **kwargs
        )

    def put(self, endpoint, **kwargs):
        return self.session.put(
            self._url(endpoint),
            **kwargs
        )

    def delete(self, endpoint, **kwargs):
        return self.session.delete(
            self._url(endpoint),
            **kwargs
        )

    def patch(self, endpoint, **kwargs):
        return self.session.patch(
            self._url(endpoint),
            **kwargs
        )


@pytest.fixture
def api_client():
    """
    Shared API client for API and integration tests.
    """
    return APIClient(BASE_URL)