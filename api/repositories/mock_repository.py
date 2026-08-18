from typing import Any, List, Tuple


class MockRepository:
    """A minimal mock repository used when Snowflake is not configured.

    Returns empty datasets or None so the API can run in development without Snowflake.
    """

    def check_connection(self) -> bool:
        return True

    def get_portfolio(self, portfolio_id: str) -> Any:
        return None

    def get_portfolios(
        self,
        page: int = 1,
        page_size: int = 20,
        client_id: str | None = None,
        risk_profile: str | None = None,
        status: str | None = None,
    ) -> Tuple[List[Any], int]:
        return [], 0

    def get_holdings(self, portfolio_id: str, page: int = 1, page_size: int = 20) -> Tuple[List[Any], int]:
        return [], 0

    def get_allocation(self, portfolio_id: str, dimension: str) -> List[Any]:
        return []

    def get_performance(self, portfolio_id: str, from_date=None, to_date=None, interval: str = "monthly") -> List[Any]:
        return []

    def get_risk(self, portfolio_id: str) -> Any:
        return None

    def get_client_portfolios(self, client_id: str) -> List[Any]:
        return []

    def get_clients(self) -> List[Any]:
        # Minimal client list used by the frontend client list view
        return []
