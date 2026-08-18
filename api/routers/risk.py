from fastapi import APIRouter, Depends, HTTPException

from dependencies import get_repository
from repositories.snowflake_repository import SnowflakeRepository
from schemas.risk import PortfolioRisk
from services.risk_service import RiskService


router = APIRouter(
    prefix="/api/v1/portfolios",
    tags=["Risk"]
)


@router.get(
    "/{portfolio_id}/risk",
    response_model=PortfolioRisk
)
def get_risk(
    portfolio_id: str,
    repository: SnowflakeRepository = Depends(
        get_repository
    )
):
    service = RiskService(repository)

    risk = service.get_risk(
        portfolio_id
    )

    if risk is None:
        raise HTTPException(
            status_code=404,
            detail={
                "code": "RISK_NOT_FOUND",
                "message": (
                    f"Risk information for "
                    f"portfolio {portfolio_id} "
                    f"was not found"
                )
            }
        )

    return risk