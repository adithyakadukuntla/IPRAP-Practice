from repositories.snowflake_repository import SnowflakeRepository


class PortfolioService:

    def __init__(self, repository: SnowflakeRepository):
        self.repository = repository

    def get_portfolio(self, portfolio_id: str):
        return self.repository.get_portfolio(portfolio_id)

    def get_portfolios(
        self,
        page: int = 1,
        page_size: int = 20,
        client_id=None,
        risk_profile=None,
        status=None,
        search=None,
    ):
        result = self.repository.get_portfolios(
            page=page,
            page_size=page_size,
            client_id=client_id,
            risk_profile=risk_profile,
            status=status,
            search=search,
        )

        if isinstance(result, tuple):
            items = result[0]
            total_items = result[-1]
        else:
            items = result
            total_items = len(items)

        total_pages = (
            (total_items + page_size - 1) // page_size
            if total_items > 0
            else 0
        )

        return {
            "items": items,
            "page": page,
            "page_size": page_size,
            "total_items": total_items,
            "total_pages": total_pages,
        }