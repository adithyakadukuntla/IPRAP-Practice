from repositories.snowflake_repository import SnowflakeRepository


class RiskService:

    def __init__(self, repository: SnowflakeRepository):
        self.repository = repository

    def get_risk(self, portfolio_id: str):

        risk = self.repository.get_risk(
            portfolio_id
        )

        return risk