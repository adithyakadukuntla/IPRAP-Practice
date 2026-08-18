"""
E2E Tests - Performance

Validates:

Portfolio
    ↓
Performance history
    ↓
Return calculations
"""


def test_performance_end_to_end(api_client):
    """
    E2E-004:
    Validate portfolio performance data end-to-end.
    """

    portfolio_id = "P10001"

    # ---------------------------------------------------------
    # Portfolio
    # ---------------------------------------------------------

    portfolio_response = api_client.get(
        f"/portfolios/{portfolio_id}"
    )

    assert portfolio_response.status_code == 200

    portfolio = portfolio_response.json()

    # ---------------------------------------------------------
    # Performance
    # ---------------------------------------------------------

    performance_response = api_client.get(
        f"/portfolios/{portfolio_id}/performance"
    )

    assert performance_response.status_code == 200

    performance = performance_response.json()

    assert performance["portfolio_id"] == portfolio_id

    assert "items" in performance

    items = performance["items"]

    # ---------------------------------------------------------
    # Validate performance records
    # ---------------------------------------------------------

    for item in items:

        assert item["portfolio_id"] == portfolio_id

        assert item.get("performance_id")

        assert item.get("as_of_date")

        beginning = float(
            item["beginning_value"]
        )

        ending = float(
            item["ending_value"]
        )

        return_amount = float(
            item["return_amount"]
        )

        # Basic calculation consistency
        calculated_return = ending - beginning

        assert abs(
            calculated_return - return_amount
        ) < 1.0

    # ---------------------------------------------------------
    # Validate portfolio return
    # ---------------------------------------------------------

    assert portfolio.get(
        "return_percent"
    ) is not None