from unittest.mock import Mock

from api.services.holding_service import HoldingService


def test_get_holdings():
    repository = Mock()

    repository.get_holdings.return_value = {
        "items": [],
        "page": 1,
        "page_size": 20,
        "total_items": 0,
        "total_pages": 0,
    }

    service = HoldingService(repository)

    result = service.get_holdings(
        portfolio_id="P10001",
        page=1,
        page_size=20
    )

    assert result["page"] == 1
    assert result["page_size"] == 20
    assert "items" in result


def test_get_holdings_passes_parameters():
    repository = Mock()

    repository.get_holdings.return_value = {
        "items": [],
        "page": 2,
        "page_size": 50,
        "total_items": 100,
        "total_pages": 2,
    }

    service = HoldingService(repository)

    service.get_holdings(
        portfolio_id="P10001",
        page=2,
        page_size=50
    )

    repository.get_holdings.assert_called_once_with(
        portfolio_id="P10001",
        page=2,
        page_size=50,
    )


def test_empty_holdings():
    repository = Mock()

    repository.get_holdings.return_value = {
        "items": [],
        "page": 1,
        "page_size": 20,
        "total_items": 0,
        "total_pages": 0,
    }

    service = HoldingService(repository)

    result = service.get_holdings(
        portfolio_id="P10001",
        page=1,
        page_size=20
    )

    assert result["items"] == []
    assert result["total_items"] == 0