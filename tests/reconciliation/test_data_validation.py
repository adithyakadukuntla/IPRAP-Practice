"""
Data Validation and Reconciliation Tests

Validates consistency between:
    Portfolio API
    Holdings API
    Performance API
    Risk API
    Allocation API
    Dashboard API
"""

import requests


BASE_URL = "http://127.0.0.1:8000/api/v1"


def get(endpoint, **params):
    response = requests.get(
        f"{BASE_URL}{endpoint}",
        params=params
    )

    assert response.status_code == 200, (
        f"GET {endpoint} failed: "
        f"{response.status_code} - {response.text}"
    )

    return response.json()


# ------------------------------------------------------------------
# Portfolio ↔ Holdings
# ------------------------------------------------------------------

def test_portfolio_holding_count_consistency():
    """
    Verify portfolio.holding_count matches the number
    of holdings returned by the holdings API.
    """

    portfolio = get("/portfolios/P10001")

    holdings = get(
        "/portfolios/P10001/holdings",
        page=1,
        page_size=1000
    )

    expected_count = portfolio.get("holding_count")
    actual_count = len(holdings.get("items", []))

    assert expected_count == actual_count, (
        f"Holding count mismatch: "
        f"portfolio={expected_count}, "
        f"holdings={actual_count}"
    )


def test_portfolio_market_value_matches_holdings():
    """
    Verify portfolio total market value is consistent
    with the sum of holding market values.
    """

    portfolio = get("/portfolios/P10001")

    holdings = get(
        "/portfolios/P10001/holdings",
        page=1,
        page_size=1000
    )

    calculated_value = sum(
        float(h.get("market_value") or 0)
        for h in holdings.get("items", [])
    )

    portfolio_value = float(
        portfolio.get("total_market_value") or 0
    )

    assert abs(calculated_value - portfolio_value) < 1.0, (
        f"Market value mismatch: "
        f"calculated={calculated_value}, "
        f"portfolio={portfolio_value}"
    )


# ------------------------------------------------------------------
# Portfolio ↔ Performance
# ------------------------------------------------------------------

def test_performance_portfolio_consistency():
    """
    Verify performance records belong to the requested portfolio.
    """

    portfolio_id = "P10001"

    data = get(
        f"/portfolios/{portfolio_id}/performance",
        interval="monthly"
    )

    for item in data.get("items", []):
        assert item["portfolio_id"] == portfolio_id


def test_performance_return_calculation():
    """
    Verify:

        return_amount =
        ending_value - beginning_value

    """

    data = get(
        "/portfolios/P10001/performance",
        interval="monthly"
    )

    for item in data.get("items", []):

        beginning = float(
            item.get("beginning_value") or 0
        )

        ending = float(
            item.get("ending_value") or 0
        )

        return_amount = float(
            item.get("return_amount") or 0
        )

        calculated = ending - beginning

        assert abs(calculated - return_amount) < 1.0, (
            f"Return calculation mismatch for "
            f"{item.get('performance_id')}: "
            f"calculated={calculated}, "
            f"reported={return_amount}"
        )


# ------------------------------------------------------------------
# Portfolio ↔ Risk
# ------------------------------------------------------------------

def test_risk_portfolio_consistency():
    """
    Verify risk response belongs to the requested portfolio.
    """

    portfolio_id = "P10001"

    portfolio = get(
        f"/portfolios/{portfolio_id}"
    )

    risk = get(
        f"/portfolios/{portfolio_id}/risk"
    )

    assert risk["portfolio_id"] == portfolio["portfolio_id"]

    assert risk["client_id"] == portfolio["client_id"]

    assert risk["portfolio_name"] == portfolio["portfolio_name"]


def test_risk_market_value_consistency():
    """
    Verify risk total market value matches portfolio data.
    """

    portfolio_id = "P10001"

    portfolio = get(
        f"/portfolios/{portfolio_id}"
    )

    risk = get(
        f"/portfolios/{portfolio_id}/risk"
    )

    portfolio_value = float(
        portfolio.get("total_market_value") or 0
    )

    risk_value = float(
        risk.get("total_market_value") or 0
    )

    assert abs(portfolio_value - risk_value) < 1.0, (
        f"Risk market value mismatch: "
        f"portfolio={portfolio_value}, "
        f"risk={risk_value}"
    )


# ------------------------------------------------------------------
# Portfolio ↔ Allocation
# ------------------------------------------------------------------

def test_allocation_total_consistency():
    """
    Verify allocation percentages add up to approximately 100%.
    """

    data = get(
        "/portfolios/P10001/allocation",
        group_by="security"
    )

    items = data.get("items", [])

    if not items:
        return

    total_percentage = sum(
        float(
            item.get("security_allocation_percent") or 0
        )
        for item in items
    )

    assert 99.0 <= total_percentage <= 101.0, (
        f"Allocation total is {total_percentage}%"
    )


# ------------------------------------------------------------------
# Holdings data validation
# ------------------------------------------------------------------

def test_holding_market_value_calculation():
    """
    Verify:

        market_value ≈ quantity × current_price
    """

    data = get(
        "/portfolios/P10001/holdings",
        page=1,
        page_size=1000
    )

    for holding in data.get("items", []):

        quantity = float(
            holding.get("quantity") or 0
        )

        current_price = float(
            holding.get("current_price") or 0
        )

        market_value = float(
            holding.get("market_value") or 0
        )

        calculated = quantity * current_price

        # Allow rounding differences.
        assert abs(calculated - market_value) < 2.0, (
            f"Market value mismatch for "
            f"{holding.get('holding_id')}: "
            f"calculated={calculated}, "
            f"reported={market_value}"
        )


def test_holding_values_non_negative():
    """
    Verify financial values are not unexpectedly negative.
    """

    data = get(
        "/portfolios/P10001/holdings",
        page=1,
        page_size=1000
    )

    for holding in data.get("items", []):

        assert holding["quantity"] >= 0

        assert holding["purchase_price"] >= 0

        assert holding["current_price"] >= 0

        assert holding["market_value"] >= 0


# ------------------------------------------------------------------
# General schema/data integrity
# ------------------------------------------------------------------

def test_portfolio_ids_are_unique():
    """
    Verify portfolio listing does not contain duplicate IDs.
    """

    data = get(
        "/portfolios",
        page=1,
        page_size=1000
    )

    items = data.get("items", [])

    ids = [
        item["portfolio_id"]
        for item in items
    ]

    assert len(ids) == len(set(ids)), (
        "Duplicate portfolio IDs detected"
    )


def test_required_portfolio_fields_not_null():
    """
    Verify important portfolio fields are populated.
    """

    data = get(
        "/portfolios",
        page=1,
        page_size=1000
    )

    required_fields = [
        "portfolio_id",
        "client_id",
        "portfolio_name",
        "portfolio_type",
        "base_currency",
        "risk_profile",
        "initial_value",
        "current_value",
        "status",
        "inception_date",
    ]

    for portfolio in data.get("items", []):

        for field in required_fields:

            assert field in portfolio, (
                f"Missing field {field} "
                f"in portfolio {portfolio.get('portfolio_id')}"
            )

            assert portfolio[field] is not None, (
                f"Null field {field} "
                f"in portfolio {portfolio.get('portfolio_id')}"
            )