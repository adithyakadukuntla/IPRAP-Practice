import pytest
from test_case_template import TestCase, TEST_STATUS


class TC_API_027_DashboardKPIs(TestCase):
    """Get dashboard KPIs"""

    def __init__(self):
        super().__init__(
            test_id="TC-API-027",
            requirement_id="REQ-DASHBOARD-001",
            title="Dashboard KPI Endpoints",
            preconditions=["API server running", "All portfolios loaded"],
            test_data={},
            steps=[
                "Send GET /dashboard/kpis",
                "Validate status 200",
                "Check executive KPI values",
                "Verify data types"
            ],
            expected_result=(
                "Status 200 with: total_portfolio_value, "
                "active_portfolios, average_return, "
                "high_risk_portfolios, total_holdings"
            )
        )

    def execute(self, api_client, auth_headers):
        try:
            response = api_client.get("/dashboard/kpis")

            assert response.status_code == 200, (
                f"Expected 200, got {response.status_code}"
            )

            data = response.json()

            required_kpis = [
                "total_portfolio_value",
                "active_portfolios",
                "average_return",
                "high_risk_portfolios",
                "total_holdings"
            ]

            for kpi in required_kpis:
                assert kpi in data, f"Missing KPI: {kpi}"

            assert isinstance(
                data["total_portfolio_value"], (int, float)
            )

            assert isinstance(
                data["active_portfolios"], int
            )

            assert isinstance(
                data["average_return"], (int, float)
            )

            assert isinstance(
                data["high_risk_portfolios"], int
            )

            assert isinstance(
                data["total_holdings"], int
            )

            self.actual_result = (
                f"Status 200: "
                f"Portfolio Value={data['total_portfolio_value']}, "
                f"Active Portfolios={data['active_portfolios']}"
            )

            self.status = TEST_STATUS["PASS"]
            return True

        except Exception as e:
            self.actual_result = str(e)
            self.status = TEST_STATUS["FAIL"]
            return False


def test_dashboard_kpis(api_client, auth_headers):
    """TC-API-027: Dashboard KPIs"""

    tc = TC_API_027_DashboardKPIs()
    result = tc.execute(api_client, auth_headers)

    assert result, tc.actual_result


def test_kpi_values_positive(api_client, auth_headers):
    """TC-API-030: All KPI values positive or zero"""

    response = api_client.get("/dashboard/kpis")

    assert response.status_code == 200

    data = response.json()

    assert data["total_portfolio_value"] >= 0
    assert data["active_portfolios"] >= 0
    assert data["average_return"] >= 0
    assert data["high_risk_portfolios"] >= 0
    assert data["total_holdings"] >= 0