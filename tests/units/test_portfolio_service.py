from unittest.mock import Mock

from api.services.portfolio_service import PortfolioService


def test_get_portfolio():
    repository = Mock()

    repository.get_portfolio.return_value = {
        "portfolio_id": "P10001",
        "client_id": "C10001",
        "portfolio_name": "Equity Growth Portfolio",
    }

    service = PortfolioService(repository)

    result = service.get_portfolio("P10001")

    assert result is not None
    assert result["portfolio_id"] == "P10001"

    repository.get_portfolio.assert_called_once_with(
        "P10001"
    )


def test_get_invalid_portfolio():
    repository = Mock()

    repository.get_portfolio.return_value = None

    service = PortfolioService(repository)

    result = service.get_portfolio("PXXXX")

    assert result is None


def test_get_portfolios():
    repository = Mock()

    repository.get_portfolios.return_value = {
        "items": [],
        "page": 1,
        "page_size": 20,
        "total_items": 0,
        "total_pages": 0,
    }

    service = PortfolioService(repository)

    result = service.get_portfolios(
        page=1,
        page_size=20
    )

    assert result["page"] == 1
    assert result["page_size"] == 20
    assert "items" in result