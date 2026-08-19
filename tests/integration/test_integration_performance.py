"""
Integration Tests - Performance

Validates:
Portfolio → Performance Service → Repository → Database
"""


def test_performance_integration(api_client):
    """
    Verify performance data is correctly retrieved
    for a portfolio.
    """

    portfolio_id = "P10001"

    response = api_client.get(
        f"/portfolios/{portfolio_id}/performance"
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, dict)

    assert "items" in data
    assert "portfolio_id" in data
    assert "interval" in data

    assert data["portfolio_id"] == portfolio_id

    performance = data["items"]

    assert isinstance(performance, list)
    assert len(performance) > 0

    for item in performance:

        assert item["portfolio_id"] == portfolio_id

        assert "beginning_value" in item
        assert "ending_value" in item
        assert "return_amount" in item
        assert "return_percent" in item


def test_performance_calculation_integration(api_client):
    """
    Verify that performance calculations remain consistent
    across the repository/service/API layers.
    """

    response = api_client.get(
        "/portfolios/P10001/performance"
    )

    assert response.status_code == 200

    data = response.json()

    for item in data["items"]:

        beginning = float(
            item["beginning_value"]
        )

        ending = float(
            item["ending_value"]
        )

        return_amount = float(
            item["return_amount"]
        )

        expected_return = (
            ending - beginning
        )

        assert abs(
            return_amount - expected_return
        ) < 1.0