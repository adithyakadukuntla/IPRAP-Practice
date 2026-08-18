from datetime import date
from typing import Optional, List

from pydantic import BaseModel


class Performance(BaseModel):
    performance_id: str
    portfolio_id: str
    as_of_date: date

    beginning_value: float
    ending_value: float

    return_amount: float
    return_percent: float

    previous_value: Optional[float] = None
    period_over_period_return: Optional[float] = None

    portfolio_name: str
    client_id: str


class PerformanceResponse(BaseModel):
    items: List[Performance]
    portfolio_id: str
    interval: str