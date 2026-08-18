"""
TC-API-007 to TC-API-011: Holdings API Tests
Requirements: Section 15-17 - API Contract & Holdings Endpoints
"""

from test_case_template import TestCase, TEST_STATUS


class TC_API_007_GetHoldings(TestCase):
    """Get holdings for portfolio"""

    def __init__(self):
        super().__init__(
            test_id="TC-API-007",
            requirement_id="REQ-API-007",
            title="Get Holdings for Portfolio",
            preconditions=[
                "Portfolio P10001 exists",
                "Holdings exist"
            ],
            test_data={"portfolio_id": "P10001"},
            steps=[
                "Send GET /portfolios/P10001/holdings",
                "Validate status 200",
                "Validate response structure",
                "Verify required holding fields"
            ],
            expected_result=(
                "Status 200 with holdings items containing "
                "security_id, quantity and market_value"
            )
        )

    def execute(self, api_client, auth_headers):
        try:
            response = api_client.get(
                "/portfolios/P10001/holdings",
                headers=auth_headers
            )

            assert response.status_code == 200, (
                f"Expected 200, got {response.status_code}"
            )

            data = response.json()

            assert "items" in data
            assert isinstance(data["items"], list)

            holdings = data["items"]

            assert len(holdings) > 0, (
                "No holdings returned"
            )

            for holding in holdings:
                assert "security_id" in holding
                assert "quantity" in holding
                assert "market_value" in holding

            self.actual_result = (
                f"Status 200: {len(holdings)} holdings retrieved"
            )

            self.status = TEST_STATUS["PASS"]
            return True

        except Exception as e:
            self.actual_result = str(e)
            self.status = TEST_STATUS["FAIL"]
            return False


class TC_API_008_HoldingDetails(TestCase):
    """
    Validate individual holding details from the holdings collection.

    The current API does not expose /holdings/{holding_id}.
    """

    def __init__(self):
        super().__init__(
            test_id="TC-API-008",
            requirement_id="REQ-API-008",
            title="Validate Holding Details",
            preconditions=[
                "Portfolio P10001 exists",
                "Holdings exist"
            ],
            test_data={"portfolio_id": "P10001"},
            steps=[
                "Send GET /portfolios/P10001/holdings",
                "Validate status 200",
                "Validate holding fields",
                "Validate holding numeric values"
            ],
            expected_result=(
                "Status 200 with valid holding records"
            )
        )

    def execute(self, api_client, auth_headers):
        try:
            response = api_client.get(
                "/portfolios/P10001/holdings",
                headers=auth_headers
            )

            assert response.status_code == 200

            data = response.json()

            assert "items" in data

            holdings = data["items"]

            assert holdings

            for holding in holdings:
                assert "security_id" in holding
                assert "quantity" in holding
                assert "market_value" in holding

                assert float(holding["quantity"]) >= 0
                assert float(holding["market_value"]) >= 0

            self.actual_result = (
                f"Status 200: {len(holdings)} holding records validated"
            )

            self.status = TEST_STATUS["PASS"]
            return True

        except Exception as e:
            self.actual_result = str(e)
            self.status = TEST_STATUS["FAIL"]
            return False


class TC_API_009_EmptyHoldings(TestCase):
    """Portfolio with no holdings returns empty items"""

    def __init__(self):
        super().__init__(
            test_id="TC-API-009",
            requirement_id="REQ-API-009",
            title="Portfolio with No Holdings",
            preconditions=[
                "Portfolio with no holdings exists"
            ],
            test_data={"portfolio_id": "P10005"},
            steps=[
                "Send GET /portfolios/P10005/holdings",
                "Validate response",
                "Check items array"
            ],
            expected_result=(
                "Status 200 with empty items array "
                "when portfolio has no holdings"
            )
        )

    def execute(self, api_client, auth_headers):
        try:
            response = api_client.get(
                "/portfolios/P10005/holdings",
                headers=auth_headers
            )

            assert response.status_code == 200

            data = response.json()

            assert "items" in data
            assert isinstance(data["items"], list)

            assert len(data["items"]) == 0, (
                f"Expected empty holdings, "
                f"got {len(data['items'])}"
            )

            self.actual_result = (
                "Status 200: Empty holdings array returned"
            )

            self.status = TEST_STATUS["PASS"]
            return True

        except Exception as e:
            self.actual_result = str(e)
            self.status = TEST_STATUS["FAIL"]
            return False


def test_get_holdings(api_client, auth_headers):
    """TC-API-007: Get holdings for portfolio"""

    tc = TC_API_007_GetHoldings()

    result = tc.execute(
        api_client,
        auth_headers
    )

    assert result, tc.actual_result


def test_holding_details(api_client, auth_headers):
    """TC-API-008: Validate holding details"""

    tc = TC_API_008_HoldingDetails()

    result = tc.execute(
        api_client,
        auth_headers
    )

    assert result, tc.actual_result


def test_empty_holdings(api_client):
    """Portfolio with no holdings returns empty array"""

    response = api_client.get("/portfolios/PXXXX/holdings")

    assert response.status_code == 200

    data = response.json()

    assert data["items"] == []
    assert data["total_items"] == 0
    assert data["total_pages"] == 0


def test_invalid_portfolio_holdings(api_client):
    """Unknown portfolio returns empty holdings result"""

    response = api_client.get("/portfolios/PXXXX/holdings")

    assert response.status_code == 200

    data = response.json()

    assert data["items"] == []
    assert data["total_items"] == 0


def test_holdings_pagination(api_client, auth_headers):
    """TC-API-011: Holdings pagination"""

    response = api_client.get(
        "/portfolios/P10001/holdings",
        params={
            "page": 1,
            "page_size": 2
        },
        headers=auth_headers
    )

    assert response.status_code == 200

    data = response.json()

    assert "items" in data
    assert isinstance(data["items"], list)

    assert len(data["items"]) <= 2

    if "page" in data:
        assert data["page"] == 1

    if "page_size" in data:
        assert data["page_size"] == 2