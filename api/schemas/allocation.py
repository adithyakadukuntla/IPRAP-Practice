from datetime import date
from typing import List, Optional

from pydantic import BaseModel


class Allocation(BaseModel):
    portfolio_id: str
    security_id: str
    security_name: str
    sector: str
    security_country: str

    security_market_value: float

    security_allocation_percent: Optional[float] = None
    sector_allocation_percent: Optional[float] = None
    country_allocation_percent: Optional[float] = None

    portfolio_total_value: float
    as_of_date: date


class AllocationListResponse(BaseModel):
    items: List[Allocation]
    dimension: str