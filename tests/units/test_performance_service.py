from unittest.mock import Mock

from api.services.performance_service import PerformanceService


def test_get_performance_returns_expected_structure():
    repository = Mock()

    repository.get_performance.return_value = [
        {
            "performance_id": "PERF001",
            "portfolio_id": "P10001",
            "return_amount": 1000.0,
            "return_percent": 5.0,
        }
    ]

    service = PerformanceService(repository)

    result = service.get_performance(
        portfolio_id="P10001",
        interval="monthly"
    )

    assert result["portfolio_id"] == "P10001"
    assert result["interval"] == "monthly"
    assert len(result["items"]) == 1


def test_performance_interval_is_normalized():
    repository = Mock()
    repository.get_performance.return_value = []

    service = PerformanceService(repository)

    result = service.get_performance(
        portfolio_id="P10001",
        interval="MONTHLY"
    )

    assert result["interval"] == "monthly"


def test_invalid_performance_interval():
    repository = Mock()

    service = PerformanceService(repository)

    try:
        service.get_performance(
            portfolio_id="P10001",
            interval="yearly"
        )
        assert False
    except ValueError:
        assert True