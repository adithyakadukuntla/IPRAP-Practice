from fastapi import APIRouter, Depends, HTTPException, Query

from dependencies import get_repository
from repositories.snowflake_repository import SnowflakeRepository
from schemas.allocation import AllocationListResponse, AllocationFlexibleResponse
from services.allocation_service import AllocationService


router = APIRouter(
    prefix="/api/v1/portfolios",
    tags=["Allocation"]
)


@router.get(
    "/{portfolio_id}/allocation",
    response_model=AllocationFlexibleResponse
)
def get_allocation(
    portfolio_id: str,
    dimension: str = Query(
        default="security"
    ),
    repository: SnowflakeRepository = Depends(get_repository)
):
    dimension = dimension.lower()

    valid_dimensions = {
        "security",
        "sector",
        "country",
    }

    if dimension not in valid_dimensions:
        raise HTTPException(
            status_code=400,
            detail={
                "code": "INVALID_DIMENSION",
                "message": (
                    "dimension must be one of: "
                    "security, sector, country"
                )
            }
        )

    service = AllocationService(repository)
    try:
        print(f"Allocation request: portfolio={portfolio_id} dimension={dimension}", flush=True)
        result = service.get_allocation(
            portfolio_id=portfolio_id,
            dimension=dimension,
        )
        print(f"Allocation result count={len(result.get('items', [])) if isinstance(result, dict) else 'n/a'}", flush=True)
        return result
    except Exception as exc:
        # Temporary debug: surface exception message in response for troubleshooting
        print(f"Allocation error for {portfolio_id} dimension={dimension}: {exc}", flush=True)
        raise HTTPException(status_code=500, detail={"message": str(exc)})