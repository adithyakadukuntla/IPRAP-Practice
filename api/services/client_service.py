from repositories.snowflake_repository import SnowflakeRepository


class ClientService:

    def __init__(self, repository: SnowflakeRepository):
        self.repository = repository

    def get_client_portfolios(
        self,
        client_id: str
    ):
        return self.repository.get_client_portfolios(
            client_id
        )