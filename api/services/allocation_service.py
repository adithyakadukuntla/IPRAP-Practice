from repositories.snowflake_repository import SnowflakeRepository


class AllocationService:

    def __init__(self, repository: SnowflakeRepository):
        self.repository = repository

    def get_allocation(
        self,
        portfolio_id: str,
        dimension: str,
    ):
        dimension = dimension.lower()

        valid_dimensions = {
            "security",
            "sector",
            "country",
        }

        if dimension not in valid_dimensions:
            raise ValueError(
                "Invalid allocation dimension"
            )

        items = self.repository.get_allocation(
            portfolio_id=portfolio_id,
            dimension=dimension,
        )

        return {
            "items": items,
            "dimension": dimension,
        }