"""
TC-API-001: Health Check Endpoint
Requirements: Section 15 - API Mandatory Scenarios
"""

import time
from tests.api.test_case_template import TestCase, TEST_STATUS


class TC_API_001(TestCase):
    """Health check endpoint returns 200 with system status"""

    def __init__(self):
        super().__init__(
            test_id="TC-API-001",
            requirement_id="REQ-API-001",
            title="Health Check Endpoint",
            preconditions=[
                "API server is running",
                "Network connectivity exists"
            ],
            test_data={"endpoint": "/health"},
            steps=[
                "Send GET request to /health endpoint",
                "Capture HTTP status code",
                "Validate response schema",
                "Verify status value",
                "Verify service and version"
            ],
            expected_result=(
                "Status 200 with status UP, service ipra-api "
                "and version 1.0.0"
            )
        )

    def execute(self, api_client, auth_headers):
        try:
            response = api_client.get(
                "/health",
                headers=auth_headers
            )

            assert response.status_code == 200, (
                f"Expected 200, got {response.status_code}"
            )

            data = response.json()

            assert isinstance(data, dict)

            assert data["status"] == "UP"
            assert data["service"] == "ipra-api"
            assert data["version"] == "1.0.0"

            self.actual_result = (
                f"Status 200: {data}"
            )

            self.status = TEST_STATUS["PASS"]
            return True

        except Exception as e:
            self.actual_result = str(e)
            self.status = TEST_STATUS["FAIL"]
            return False


def test_health_check(api_client, auth_headers):
    """TC-API-001: Health check endpoint"""

    tc = TC_API_001()

    result = tc.execute(
        api_client,
        auth_headers
    )

    assert result, tc.actual_result
    assert tc.status == TEST_STATUS["PASS"]


def test_health_response_schema(api_client, auth_headers):
    """TC-API-001.1: Health response schema"""

    response = api_client.get(
        "/health",
        headers=auth_headers
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, dict)
    assert "status" in data
    assert "service" in data
    assert "version" in data

    assert isinstance(data["status"], str)
    assert isinstance(data["service"], str)
    assert isinstance(data["version"], str)


def test_health_status(api_client, auth_headers):
    """TC-API-001.2: Health status is UP"""

    response = api_client.get(
        "/health",
        headers=auth_headers
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "UP"


def test_health_performance(api_client):
    """TC-API-001.2: Health check response time < 3000ms"""
    import time

    start = time.perf_counter()
    response = api_client.get("/health")
    elapsed_ms = (time.perf_counter() - start) * 1000

    assert response.status_code == 200

    assert elapsed_ms < 3000, (
        f"Response time {elapsed_ms:.2f}ms exceeds 3000ms threshold"
    )