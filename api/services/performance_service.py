from repositories.snowflake_repository import SnowflakeRepository


class PerformanceService:

    def __init__(self, repository: SnowflakeRepository):
        self.repository = repository

    def get_performance(
        self,
        portfolio_id: str,
        from_date=None,
        to_date=None,
        interval: str = "monthly",
    ):
        interval = interval.lower()

        valid_intervals = {
            "daily",
            "weekly",
            "monthly",
        }

        if interval not in valid_intervals:
            raise ValueError(
                "Invalid performance interval"
            )

        items = self.repository.get_performance(
            portfolio_id=portfolio_id,
            from_date=from_date,
            to_date=to_date,
            interval=interval,
        )

        return {
            "items": items,
            "portfolio_id": portfolio_id,
            "interval": interval,
        }