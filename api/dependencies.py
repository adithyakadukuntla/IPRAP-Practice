from repositories.snowflake_repository import SnowflakeRepository
from repositories.mock_repository import MockRepository
from config import settings


def get_repository():
    """Return a repository implementation.

    Use the real Snowflake repository when `SNOWFLAKE_ACCOUNT` is configured.
    Otherwise fall back to the `MockRepository` so the API remains usable in
    local development without Snowflake credentials.
    """
    if settings.SNOWFLAKE_ACCOUNT:
        return SnowflakeRepository()

    return MockRepository()