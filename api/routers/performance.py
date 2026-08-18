from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query

from dependencies import get_repository
from repositories.snowflake_repository import SnowflakeRepository
from schemas.performance import PerformanceResponse
from services.performance_service import PerformanceService


router = APIRouter(
    prefix="/api/v1/portfolios",
    tags=["Performance"]
)


@router.get(
    "/{portfolio_id}/performance",
    response_model=PerformanceResponse
)
def get_performance(
    portfolio_id: str,
    from_date: date | None = Query(
        default=None,
        alias="from"
    ),
    to_date: date | None = Query(
        default=None,
        alias="to"
    ),
    interval: str = Query(
        default="monthly"
    ),
    repository: SnowflakeRepository = Depends(
        get_repository
    )
):
    interval = interval.lower()

    valid_intervals = {
        "daily",
        "weekly",
        "monthly",
    }

    if interval not in valid_intervals:
        raise HTTPException(
            status_code=400,
            detail={
                "code": "INVALID_INTERVAL",
                "message": (
                    "interval must be one of: "
                    "daily, weekly, monthly"
                )
            }
        )

    if from_date and to_date and from_date > to_date:
        raise HTTPException(
            status_code=400,
            detail={
                "code": "INVALID_DATE_RANGE",
                "message": (
                    "'from' date cannot be after "
                    "'to' date"
                )
            }
        )

    service = PerformanceService(repository)

    return service.get_performance(
        portfolio_id=portfolio_id,
        from_date=from_date,
        to_date=to_date,
        interval=interval,
    )