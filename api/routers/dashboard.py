from fastapi import APIRouter, Depends

from dependencies import get_repository
from repositories.snowflake_repository import SnowflakeRepository
from services.portfolio_service import PortfolioService
from schemas.dashboard import DashboardKPIs


router = APIRouter(
    prefix="/api/v1/dashboard",
    tags=["Dashboard"]
)


@router.get("/kpis", response_model=DashboardKPIs)
def get_kpis(repository: SnowflakeRepository = Depends(get_repository)):
    service = PortfolioService(repository)

    # Attempt to retrieve all portfolios in one request (large page_size)
    result = service.get_portfolios(page=1, page_size=1000)
    items = result.get("items", [])

    total_portfolio_value = 0.0
    active_portfolios = 0
    total_return = 0.0
    count_for_return = 0
    high_risk_portfolios = 0
    total_holdings = 0

    for p in items:
        try:
            total_portfolio_value += float(p.get("current_value") or 0)
            if p.get("status", "").lower() == "active":
                active_portfolios += 1
            if p.get("risk_profile", "").lower() == "high":
                high_risk_portfolios += 1
            if p.get("return_percent") is not None:
                total_return += float(p.get("return_percent") or 0)
                count_for_return += 1
            total_holdings += int(p.get("holding_count") or 0)
        except Exception:
            continue

    average_return = (total_return / count_for_return) if count_for_return > 0 else 0.0

    return DashboardKPIs(
        total_portfolio_value=total_portfolio_value,
        active_portfolios=active_portfolios,
        average_return=average_return,
        high_risk_portfolios=high_risk_portfolios,
        total_holdings=total_holdings,
    )
