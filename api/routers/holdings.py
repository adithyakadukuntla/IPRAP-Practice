from fastapi import APIRouter, Depends, Query

from dependencies import get_repository
from repositories.snowflake_repository import SnowflakeRepository
from schemas.holding import HoldingListResponse
from services.holding_service import HoldingService


router = APIRouter(
    prefix="/api/v1/portfolios",
    tags=["Holdings"]
)


@router.get(
    "/{portfolio_id}/holdings",
    response_model=HoldingListResponse
)
def get_holdings(
    portfolio_id: str,
    page: int = Query(
        default=1,
        ge=1
    ),
    page_size: int = Query(
        default=20,
        ge=1,
        le=100
    ),
    repository: SnowflakeRepository = Depends(get_repository)
):
    service = HoldingService(repository)

    return service.get_holdings(
        portfolio_id=portfolio_id,
        page=page,
        page_size=page_size,
    )