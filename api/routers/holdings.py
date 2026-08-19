from fastapi import APIRouter, Depends, HTTPException, Query

from dependencies import get_repository
from repositories.snowflake_repository import SnowflakeRepository
from services.holding_service import HoldingService
from services.portfolio_service import PortfolioService
from schemas.holding import HoldingListResponse

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
        le=1000
    ),
    repository: SnowflakeRepository = Depends(get_repository)
):

    portfolio_service = PortfolioService(repository)

    portfolio = portfolio_service.get_portfolio(
        portfolio_id
    )

    if portfolio is None:
        raise HTTPException(
            status_code=404,
            detail={
                "code": "PORTFOLIO_NOT_FOUND",
                "message": (
                    f"Portfolio {portfolio_id} was not found"
                )
            }
        )

    holding_service = HoldingService(repository)

    return holding_service.get_holdings(
        portfolio_id=portfolio_id,
        page=page,
        page_size=page_size
    )