from datetime import date
from typing import Optional

from pydantic import BaseModel


class PortfolioSummary(BaseModel):
    portfolio_id: str
    client_id: str
    portfolio_name: str
    portfolio_type: str
    base_currency: str
    risk_profile: str

    initial_value: float
    current_value: float

    return_amount: Optional[float] = None
    return_percent: Optional[float] = None

    total_market_value: Optional[float] = None
    holding_count: Optional[int] = None

    latest_performance_date: Optional[date] = None

    status: str
    inception_date: date