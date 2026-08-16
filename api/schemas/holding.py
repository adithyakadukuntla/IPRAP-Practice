from datetime import date
from typing import List

from pydantic import BaseModel


class Holding(BaseModel):
    holding_id: str
    portfolio_id: str
    security_id: str
    ticker_symbol: str
    security_name: str
    security_type: str
    sector: str
    security_country: str
    security_currency: str

    quantity: float
    purchase_price: float
    current_price: float
    market_value: float

    as_of_date: date

    portfolio_name: str
    client_id: str
    client_name: str


class HoldingListResponse(BaseModel):
    items: List[Holding]
    page: int
    page_size: int
    total_items: int
    total_pages: int