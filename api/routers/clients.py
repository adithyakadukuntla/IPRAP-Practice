from fastapi import APIRouter, Depends, HTTPException

from dependencies import get_repository
from repositories.snowflake_repository import SnowflakeRepository
from schemas.client import ClientPortfolioSummary
from services.client_service import ClientService


router = APIRouter(
    prefix="/api/v1/clients",
    tags=["Clients"]
)


@router.get(
    "/{client_id}/portfolios",
    response_model=ClientPortfolioSummary
)
def get_client_portfolios(
    client_id: str,
    repository: SnowflakeRepository = Depends(
        get_repository
    )
):
    service = ClientService(repository)

    result = service.get_client_portfolios(
        client_id
    )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail={
                "code": "CLIENT_NOT_FOUND",
                "message": (
                    f"Client {client_id} "
                    f"was not found"
                )
            }
        )

    return result