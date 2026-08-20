"""
Integration Tests - Performance

Validates:

Portfolio
    ↓
Performance API
    ↓
Performance Service
    ↓
Repository
    ↓
Database/Data Source

The tests also validate:
- Portfolio/performance relationships
- Required performance fields
- Return amount calculation
- Return percentage calculation
- Chronological ordering
- Performance response structure
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
    Verify that performance return amounts remain
    consistent across the repository/service/API layers.
    """

    response = api_client.get(
        "/portfolios/P10001/performance"
    )

    assert response.status_code == 200

    data = response.json()

    performance = data["items"]

    assert isinstance(performance, list)
    assert len(performance) > 0

    for item in performance:

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
        ) < 1.0, (
            f"Return amount mismatch for "
            f"portfolio {item['portfolio_id']}"
        )


def test_performance_percentage_integration(
    api_client
):
    """
    Verify that return percentage is consistent
    with beginning and ending portfolio values.
    """

    response = api_client.get(
        "/portfolios/P10001/performance"
    )

    assert response.status_code == 200

    data = response.json()

    performance = data["items"]

    assert isinstance(performance, list)
    assert len(performance) > 0

    for item in performance:

        beginning = float(
            item["beginning_value"]
        )

        ending = float(
            item["ending_value"]
        )

        return_percent = float(
            item["return_percent"]
        )

        # Avoid division by zero
        if beginning == 0:
            continue

        expected_percent = (
            (ending - beginning) / beginning
        ) * 100

        assert abs(
            return_percent - expected_percent
        ) < 0.01, (
            f"Return percentage mismatch for "
            f"portfolio {item['portfolio_id']}"
        )


def test_performance_portfolio_consistency(
    api_client
):
    """
    Verify every performance record belongs to
    the requested portfolio.
    """

    portfolio_id = "P10001"

    response = api_client.get(
        f"/portfolios/{portfolio_id}/performance"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["portfolio_id"] == portfolio_id

    for item in data["items"]:

        assert item["portfolio_id"] == portfolio_id


def test_performance_chronological_order(
    api_client
):
    """
    Verify performance records are returned in
    chronological order when a performance date
    field is available.
    """

    response = api_client.get(
        "/portfolios/P10001/performance"
    )

    assert response.status_code == 200

    data = response.json()

    performance = data["items"]

    if len(performance) < 2:
        return

    # Use the first available supported date field.
    date_field = None

    for candidate in [
        "date",
        "performance_date",
        "as_of_date",
    ]:
        if candidate in performance[0]:
            date_field = candidate
            break

    # If the API does not expose a date field,
    # this check is not applicable.
    if date_field is None:
        return

    dates = [
        item[date_field]
        for item in performance
    ]

    assert dates == sorted(dates), (
        "Performance records are not in "
        "chronological order"
    )