"""
TC-API-017 to TC-API-021: Performance API Tests

Matches the actual Performance API contract:

GET /api/v1/portfolios/{portfolio_id}/performance

Response:
{
    "items": [...],
    "portfolio_id": "P10001",
    "interval": "monthly"
}

Query parameters:
    from
    to
    interval
"""

import pytest
from test_case_template import TestCase, TEST_STATUS


class TC_API_017_GetPerformance(TestCase):
    """Get performance metrics for portfolio"""

    def __init__(self):
        super().__init__(
            test_id="TC-API-017",
            requirement_id="REQ-API-017",
            title="Get Performance Metrics",
            preconditions=[
                "Portfolio P10001 exists",
                "Performance data calculated"
            ],
            test_data={
                "portfolio_id": "P10001"
            },
            steps=[
                "Send GET /portfolios/P10001/performance",
                "Validate status 200",
                "Check response structure",
                "Check performance items",
                "Verify required performance fields"
            ],
            expected_result=(
                "Status 200 with items array, portfolio_id "
                "and interval"
            )
        )

    def execute(self, api_client, auth_headers):
        try:
            response = api_client.get(
                "/portfolios/P10001/performance",
                headers=auth_headers
            )

            assert response.status_code == 200, (
                f"Expected 200, got {response.status_code}"
            )

            data = response.json()

            # Validate top-level response
            assert isinstance(data, dict), (
                "Response should be an object"
            )

            assert "items" in data, (
                "Missing 'items' field"
            )

            assert "portfolio_id" in data, (
                "Missing 'portfolio_id' field"
            )

            assert "interval" in data, (
                "Missing 'interval' field"
            )

            # Validate types
            assert isinstance(data["items"], list), (
                "'items' should be a list"
            )

            assert data["portfolio_id"] == "P10001"

            assert data["interval"] in [
                "daily",
                "weekly",
                "monthly"
            ]

            # Validate individual performance records
            required_fields = [
                "performance_id",
                "portfolio_id",
                "as_of_date",
                "beginning_value",
                "ending_value",
                "return_amount",
                "return_percent",
                "portfolio_name",
                "client_id"
            ]

            for item in data["items"]:
                for field in required_fields:
                    assert field in item, (
                        f"Missing performance field: {field}"
                    )

            self.actual_result = (
                f"Status 200: "
                f"{len(data['items'])} performance records retrieved"
            )

            self.status = TEST_STATUS["PASS"]
            return True

        except Exception as e:
            self.actual_result = str(e)
            self.status = TEST_STATUS["FAIL"]
            return False


class TC_API_018_PerformanceHistory(TestCase):
    """Get performance history for date range"""

    def __init__(self):
        super().__init__(
            test_id="TC-API-018",
            requirement_id="REQ-API-018",
            title="Performance History by Date Range",
            preconditions=[
                "Portfolio P10001 exists",
                "Historical performance data available"
            ],
            test_data={
                "portfolio_id": "P10001",
                "from": "2026-01-01",
                "to": "2026-08-18"
            },
            steps=[
                "Send GET with from and to dates",
                "Validate status 200",
                "Verify response structure",
                "Check portfolio ID",
                "Check returned performance records"
            ],
            expected_result=(
                "Status 200 with performance records "
                "for requested date range"
            )
        )

    def execute(self, api_client, auth_headers):
        try:
            params = {
                "from": "2026-01-01",
                "to": "2026-08-18",
                "interval": "monthly"
            }

            response = api_client.get(
                "/portfolios/P10001/performance",
                params=params,
                headers=auth_headers
            )

            assert response.status_code == 200, (
                f"Expected 200, got {response.status_code}"
            )

            data = response.json()

            assert isinstance(data, dict)
            assert "items" in data
            assert "portfolio_id" in data
            assert "interval" in data

            assert data["portfolio_id"] == "P10001"
            assert isinstance(data["items"], list)

            self.actual_result = (
                f"Status 200: "
                f"{len(data['items'])} historical records retrieved"
            )

            self.status = TEST_STATUS["PASS"]
            return True

        except Exception as e:
            self.actual_result = str(e)
            self.status = TEST_STATUS["FAIL"]
            return False


class TC_API_019_InvalidDateRange(TestCase):
    """Invalid date range returns 400"""

    def __init__(self):
        super().__init__(
            test_id="TC-API-019",
            requirement_id="REQ-API-019",
            title="Invalid Date Range",
            preconditions=[
                "Portfolio P10001 exists"
            ],
            test_data={
                "portfolio_id": "P10001",
                "from": "2026-08-18",
                "to": "2026-01-01"
            },
            steps=[
                "Send GET with from date after to date",
                "Validate status 400"
            ],
            expected_result=(
                "Status 400 for invalid date range"
            )
        )

    def execute(self, api_client, auth_headers):
        try:
            params = {
                "from": "2026-08-18",
                "to": "2026-01-01"
            }

            response = api_client.get(
                "/portfolios/P10001/performance",
                params=params,
                headers=auth_headers
            )

            assert response.status_code == 400, (
                f"Expected 400, got {response.status_code}"
            )

            self.actual_result = (
                "Status 400: Invalid date range rejected"
            )

            self.status = TEST_STATUS["PASS"]
            return True

        except Exception as e:
            self.actual_result = str(e)
            self.status = TEST_STATUS["FAIL"]
            return False


def test_get_performance(api_client, auth_headers):
    """TC-API-017: Get performance metrics"""

    tc = TC_API_017_GetPerformance()

    result = tc.execute(
        api_client,
        auth_headers
    )

    assert result, tc.actual_result


def test_performance_history(api_client, auth_headers):
    """TC-API-018: Performance history"""

    tc = TC_API_018_PerformanceHistory()

    result = tc.execute(
        api_client,
        auth_headers
    )

    assert result, tc.actual_result


def test_invalid_date_range(api_client, auth_headers):
    """TC-API-019: Invalid date range"""

    tc = TC_API_019_InvalidDateRange()

    result = tc.execute(
        api_client,
        auth_headers
    )

    assert result, tc.actual_result


def test_positive_return(api_client, auth_headers):
    """TC-API-020: At least one positive performance record"""

    response = api_client.get(
        "/portfolios/P10001/performance",
        params={"interval": "monthly"},
        headers=auth_headers
    )

    assert response.status_code == 200

    data = response.json()

    assert "items" in data

    items = data["items"]

    # If there is no historical data, don't fail because of
    # an unsupported assumption about the dataset.
    if not items:
        pytest.skip(
            "No performance records available for P10001"
        )

    positive_returns = [
        item["return_percent"]
        for item in items
        if item.get("return_percent") is not None
    ]

    assert positive_returns, (
        "No return_percent values found"
    )

    assert any(
        value > 0 for value in positive_returns
    ), (
        "Expected at least one positive performance return"
    )


def test_return_calculation_accuracy(api_client, auth_headers):
    """TC-API-021: Return amount calculation accuracy"""

    response = api_client.get(
        "/portfolios/P10001/performance",
        params={"interval": "monthly"},
        headers=auth_headers
    )

    assert response.status_code == 200

    data = response.json()

    assert "items" in data

    items = data["items"]

    if not items:
        pytest.skip(
            "No performance records available for P10001"
        )

    for item in items:

        beginning = item["beginning_value"]
        ending = item["ending_value"]
        return_amount = item["return_amount"]

        calculated_return = ending - beginning

        assert abs(
            return_amount - calculated_return
        ) < 1.0, (
            f"Return amount incorrect for "
            f"{item.get('performance_id')}: "
            f"expected {calculated_return}, "
            f"got {return_amount}"
        )