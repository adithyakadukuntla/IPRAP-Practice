"""
TC-API-022 to TC-API-026: Allocation API Tests
Requirements: Section 15-17 - Allocation Endpoints
"""

from test_case_template import TestCase, TEST_STATUS


class TC_API_022_GetAllocation(TestCase):
    """Get allocation breakdown for portfolio"""

    def __init__(self):
        super().__init__(
            test_id="TC-API-022",
            requirement_id="REQ-API-022",
            title="Get Portfolio Allocation",
            preconditions=[
                "Portfolio P10001 exists",
                "Holdings data available"
            ],
            test_data={"portfolio_id": "P10001"},
            steps=[
                "Send GET /portfolios/P10001/allocation",
                "Validate status 200",
                "Validate response structure",
                "Check allocation percentages",
                "Verify total = 100%"
            ],
            expected_result=(
                "Status 200 with allocation items containing "
                "security_id, security_name, security_market_value "
                "and security_allocation_percent"
            )
        )

    def execute(self, api_client, auth_headers):
        try:
            response = api_client.get(
                "/portfolios/P10001/allocation",
                headers=auth_headers
            )

            assert response.status_code == 200

            data = response.json()

            assert "items" in data
            assert "dimension" in data
            assert data["dimension"] == "security"

            allocations = data["items"]

            assert allocations, "Allocation items should not be empty"

            total_pct = sum(
                float(a["security_allocation_percent"])
                for a in allocations
            )

            assert abs(total_pct - 100.0) < 0.1, (
                f"Total allocation {total_pct}% should equal 100%"
            )

            for allocation in allocations:
                assert "security_id" in allocation
                assert "security_name" in allocation
                assert "security_market_value" in allocation
                assert "security_allocation_percent" in allocation

            self.actual_result = (
                f"Status 200: {len(allocations)} allocations "
                f"sum to {total_pct}%"
            )
            self.status = TEST_STATUS["PASS"]
            return True

        except Exception as e:
            self.actual_result = str(e)
            self.status = TEST_STATUS["FAIL"]
            return False


class TC_API_023_AllocationByType(TestCase):
    """Get allocation grouped by sector"""

    def __init__(self):
        super().__init__(
            test_id="TC-API-023",
            requirement_id="REQ-API-023",
            title="Allocation Grouped by Sector",
            preconditions=["Portfolio P10001 exists"],
            test_data={
                "portfolio_id": "P10001",
                "dimension": "sector"
            },
            steps=[
                "Send GET /portfolios/P10001/allocation?dimension=sector",
                "Validate status 200",
                "Validate dimension",
                "Check sector allocation breakdown"
            ],
            expected_result=(
                "Status 200 with allocation items containing "
                "sector and sector_allocation_percent"
            )
        )

    def execute(self, api_client, auth_headers):
        try:
            response = api_client.get(
                "/portfolios/P10001/allocation",
                params={"dimension": "sector"},
                headers=auth_headers
            )

            assert response.status_code == 200

            data = response.json()

            assert data["dimension"] == "sector"
            assert "items" in data
            assert data["items"]

            for allocation in data["items"]:
                assert "sector" in allocation
                assert "sector_allocation_percent" in allocation

            self.actual_result = (
                f"Status 200: {len(data['items'])} "
                "sector allocation items retrieved"
            )
            self.status = TEST_STATUS["PASS"]
            return True

        except Exception as e:
            self.actual_result = str(e)
            self.status = TEST_STATUS["FAIL"]
            return False


class TC_API_024_InvalidGroupBy(TestCase):
    """Invalid allocation dimension returns 400"""

    def __init__(self):
        super().__init__(
            test_id="TC-API-024",
            requirement_id="REQ-API-024",
            title="Invalid Allocation Dimension",
            preconditions=["Portfolio P10001 exists"],
            test_data={
                "portfolio_id": "P10001",
                "dimension": "invalid"
            },
            steps=[
                "Send GET with invalid dimension",
                "Validate status 400",
                "Validate error code"
            ],
            expected_result=(
                "Status 400 with INVALID_DIMENSION error"
            )
        )

    def execute(self, api_client, auth_headers):
        try:
            response = api_client.get(
                "/portfolios/P10001/allocation",
                params={"dimension": "invalid"},
                headers=auth_headers
            )

            assert response.status_code == 400

            data = response.json()

            assert data["detail"]["code"] == "INVALID_DIMENSION"

            self.actual_result = (
                "Status 400: Invalid allocation dimension rejected"
            )
            self.status = TEST_STATUS["PASS"]
            return True

        except Exception as e:
            self.actual_result = str(e)
            self.status = TEST_STATUS["FAIL"]
            return False


def test_get_allocation(api_client, auth_headers):
    """TC-API-022: Get portfolio allocation"""
    tc = TC_API_022_GetAllocation()
    result = tc.execute(api_client, auth_headers)
    assert result, tc.actual_result


def test_allocation_by_type(api_client, auth_headers):
    """TC-API-023: Allocation by sector"""
    tc = TC_API_023_AllocationByType()
    result = tc.execute(api_client, auth_headers)
    assert result, tc.actual_result


def test_invalid_group_by(api_client, auth_headers):
    """TC-API-024: Invalid allocation dimension"""
    tc = TC_API_024_InvalidGroupBy()
    result = tc.execute(api_client, auth_headers)
    assert result, tc.actual_result


def test_allocation_totals_100_percent(api_client, auth_headers):
    """TC-API-025: Allocation percentages sum to 100%"""

    response = api_client.get(
        "/portfolios/P10001/allocation",
        headers=auth_headers
    )

    assert response.status_code == 200

    data = response.json()

    assert "items" in data

    allocations = data["items"]

    total = sum(
        float(a["security_allocation_percent"])
        for a in allocations
    )

    assert abs(total - 100.0) < 0.5, (
        f"Allocations sum to {total}%, should be ~100%"
    )


def test_allocation_values_positive(api_client, auth_headers):
    """TC-API-026: All allocation percentages positive"""

    response = api_client.get(
        "/portfolios/P10001/allocation",
        headers=auth_headers
    )

    assert response.status_code == 200

    data = response.json()

    assert "items" in data

    for alloc in data["items"]:
        percentage = float(
            alloc["security_allocation_percent"]
        )

        market_value = float(
            alloc["security_market_value"]
        )

        assert percentage >= 0, (
            f"Negative allocation found: {percentage}"
        )

        assert market_value >= 0, (
            f"Negative market value found: {market_value}"
        )