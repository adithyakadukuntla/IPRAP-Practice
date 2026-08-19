from unittest.mock import Mock

from api.services.risk_service import RiskService


def test_get_risk():
    repository = Mock()

    repository.get_risk.return_value = {
        "portfolio_id": "P10001",
        "client_id": "C10001",
        "portfolio_name": "Equity Growth Portfolio",
        "risk_status": "CRITICAL",
        "concentration_risk": "MEDIUM",
        "highest_weight_percent": 36.47,
    }

    service = RiskService(repository)

    result = service.get_risk("P10001")

    assert result is not None
    assert result["portfolio_id"] == "P10001"
    assert result["risk_status"] == "CRITICAL"


def test_risk_repository_called():
    repository = Mock()
    repository.get_risk.return_value = {}

    service = RiskService(repository)

    service.get_risk("P10001")

    repository.get_risk.assert_called_once_with(
        "P10001"
    )


def test_high_risk_result():
    repository = Mock()

    repository.get_risk.return_value = {
        "portfolio_id": "P10001",
        "risk_status": "CRITICAL",
        "concentration_risk": "HIGH",
    }

    service = RiskService(repository)

    result = service.get_risk("P10001")

    assert result["risk_status"] == "CRITICAL"
    assert result["concentration_risk"] == "HIGH"