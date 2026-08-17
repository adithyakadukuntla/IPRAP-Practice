from fastapi import APIRouter, Depends, HTTPException, Query

from dependencies import get_repository
from repositories.snowflake_repository import SnowflakeRepository
from schemas.portfolio import PortfolioSummary
from schemas.portfolio_list import PortfolioListResponse
from services.portfolio_service import PortfolioService


router = APIRouter(
    prefix="/api/v1/portfolios",
    tags=["Portfolios"]
)


@router.get(
    "",
    response_model=PortfolioListResponse
)
def get_portfolios(
    page: int = Query(
        default=1,
        ge=1
    ),
    page_size: int = Query(
        default=20,
        ge=1,
        le=100
    ),
    client_id: str | None = None,
    risk_profile: str | None = None,
    status: str | None = None,
    search: str | None = None,
    repository: SnowflakeRepository = Depends(get_repository)
):
    service = PortfolioService(repository)

    return service.get_portfolios(
        page=page,
        page_size=page_size,
        client_id=client_id,
        risk_profile=risk_profile,
        status=status,
        search=search,
    )


@router.get(
    "/{portfolio_id}",
    response_model=PortfolioSummary
)
def get_portfolio(
    portfolio_id: str,
    repository: SnowflakeRepository = Depends(get_repository)
):
    service = PortfolioService(repository)

    portfolio = service.get_portfolio(portfolio_id)

    if portfolio is None:
        raise HTTPException(
            status_code=404,
            detail={
                "code": "PORTFOLIO_NOT_FOUND",
                "message": f"Portfolio {portfolio_id} was not found"
            }
        )

    return portfolio