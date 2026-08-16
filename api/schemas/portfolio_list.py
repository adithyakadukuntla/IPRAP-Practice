from typing import List

from pydantic import BaseModel

from schemas.portfolio import PortfolioSummary


class PortfolioListResponse(BaseModel):
    items: List[PortfolioSummary]
    page: int
    page_size: int
    total_items: int
    total_pages: int