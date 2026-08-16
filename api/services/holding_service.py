from repositories.snowflake_repository import SnowflakeRepository


class HoldingService:

    def __init__(self, repository: SnowflakeRepository):
        self.repository = repository

    def get_holdings(
        self,
        portfolio_id: str,
        page: int = 1,
        page_size: int = 20,
    ):
        items, total_items = self.repository.get_holdings(
            portfolio_id=portfolio_id,
            page=page,
            page_size=page_size,
        )

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