from fastapi import APIRouter, Depends, HTTPException

from dependencies import get_repository
from repositories.snowflake_repository import SnowflakeRepository


router = APIRouter(
    prefix="/api/v1/health",
    tags=["Health"]
)


@router.get("")
def health():
    return {
        "status": "UP",
        "service": "ipra-api",
        "version": "1.0.0"
    }


@router.get("/ready")
def readiness(
    repository: SnowflakeRepository = Depends(get_repository)
):
    try:
        if not repository.check_connection():
            raise HTTPException(
                status_code=503,
                detail="Data source unavailable"
            )

        return {
            "status": "READY",
            "service": "ipra-api"
        }

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=503,
            detail="Data source unavailable"
        )