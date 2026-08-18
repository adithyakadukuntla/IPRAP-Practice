"""
TC-API-002 to TC-API-006
API Contract & Response Validation
"""

from tests.api.test_case_template import TestCase, TEST_STATUS


class TC_API_002_GetPortfolio(TestCase):

    def __init__(self):
        super().__init__(
            test_id="TC-API-002",
            requirement_id="REQ-API-002",
            title="Get Portfolio By ID",
            preconditions=[
                "API server running",
                "Portfolio P10001 exists"
            ],
            test_data={"portfolio_id": "P10001"},
            steps=[
                "Send GET /portfolios/P10001",
                "Validate status 200",
                "Validate response schema",
                "Validate required fields",
                "Validate data types"
            ],
            expected_result="Status 200 with valid portfolio object"
        )

    def execute(self, api_client, auth_headers, portfolio_data=None):
        try:
            response = api_client.get(
                "/portfolios/P10001",
                headers=auth_headers
            )

            assert response.status_code == 200

            data = response.json()

            required_fields = [
                "portfolio_id",
                "client_id",
                "portfolio_name",
                "portfolio_type",
                "base_currency",
                "risk_profile",
                "initial_value",
                "current_value",
                "return_amount",
                "return_percent",
                "total_market_value",
                "holding_count",
                "status",
                "inception_date"
            ]

            for field in required_fields:
                assert field in data, f"Missing required field: {field}"

            assert isinstance(data["portfolio_id"], str)
            assert isinstance(data["client_id"], str)
            assert isinstance(data["portfolio_name"], str)
            assert isinstance(data["portfolio_type"], str)
            assert isinstance(data["base_currency"], str)
            assert isinstance(data["risk_profile"], str)
            assert isinstance(data["initial_value"], (int, float))
            assert isinstance(data["current_value"], (int, float))
            assert isinstance(data["return_amount"], (int, float))
            assert isinstance(data["return_percent"], (int, float))
            assert isinstance(data["holding_count"], int)

            self.actual_result = (
                f"Status 200: Portfolio "
                f"{data['portfolio_id']} retrieved"
            )
            self.status = TEST_STATUS["PASS"]
            return True

        except Exception as e:
            self.actual_result = str(e)
            self.status = TEST_STATUS["FAIL"]
            return False


class TC_API_003_UnknownPortfolio(TestCase):

    def __init__(self):
        super().__init__(
            test_id="TC-API-003",
            requirement_id="REQ-API-003",
            title="Get Unknown Portfolio",
            preconditions=["API server running"],
            test_data={"portfolio_id": "PXXXX"},
            steps=[
                "Send GET /portfolios/PXXXX",
                "Validate status 404",
                "Validate error response"
            ],
            expected_result="Status 404 with portfolio not found error"
        )

    def execute(self, api_client, auth_headers):
        try:
            response = api_client.get(
                "/portfolios/PXXXX",
                headers=auth_headers
            )

            assert response.status_code == 404

            data = response.json()

            # Current API uses detail instead of error
            assert "detail" in data

            detail = data["detail"]

            if isinstance(detail, dict):
                assert detail.get("code") == "PORTFOLIO_NOT_FOUND"

            self.actual_result = "Status 404: Portfolio not found"
            self.status = TEST_STATUS["PASS"]
            return True

        except Exception as e:
            self.actual_result = str(e)
            self.status = TEST_STATUS["FAIL"]
            return False


class TC_API_004_PortfolioList(TestCase):

    def __init__(self):
        super().__init__(
            test_id="TC-API-004",
            requirement_id="REQ-API-004",
            title="List Portfolios with Pagination",
            preconditions=[
                "API server running",
                "At least 5 portfolios exist"
            ],
            test_data={
                "page": 1,
                "page_size": 10
            },
            steps=[
                "Send GET /portfolios?page=1&page_size=10",
                "Validate status 200",
                "Validate items array",
                "Validate pagination metadata",
                "Validate item count"
            ],
            expected_result="Status 200 with paginated portfolio response"
        )

    def execute(self, api_client, auth_headers):
        try:
            response = api_client.get(
                "/portfolios",
                params={
                    "page": 1,
                    "page_size": 10
                },
                headers=auth_headers
            )

            assert response.status_code == 200

            data = response.json()

            assert "items" in data
            assert isinstance(data["items"], list)

            assert "page" in data
            assert "page_size" in data
            assert "total_items" in data
            assert "total_pages" in data

            assert data["page"] == 1
            assert data["page_size"] == 10
            assert len(data["items"]) <= 10
            assert data["total_items"] >= len(data["items"])

            self.actual_result = (
                f"Status 200: Retrieved "
                f"{len(data['items'])} portfolios"
            )
            self.status = TEST_STATUS["PASS"]
            return True

        except Exception as e:
            self.actual_result = str(e)
            self.status = TEST_STATUS["FAIL"]
            return False


def test_get_portfolio(api_client, auth_headers, portfolio_data):
    tc = TC_API_002_GetPortfolio()
    result = tc.execute(
        api_client,
        auth_headers,
        portfolio_data
    )
    assert result, tc.actual_result


def test_unknown_portfolio(api_client, auth_headers):
    tc = TC_API_003_UnknownPortfolio()
    result = tc.execute(
        api_client,
        auth_headers
    )
    assert result, tc.actual_result


def test_portfolio_list(api_client, auth_headers):
    tc = TC_API_004_PortfolioList()
    result = tc.execute(
        api_client,
        auth_headers
    )
    assert result, tc.actual_result


def test_invalid_page_size(api_client, auth_headers):
    response = api_client.get(
        "/portfolios",
        params={
            "page": 1,
            "page_size": 10000
        },
        headers=auth_headers
    )

    assert response.status_code == 422