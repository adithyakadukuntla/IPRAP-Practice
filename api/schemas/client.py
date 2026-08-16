from datetime import date

from pydantic import BaseModel


class ClientPortfolioSummary(BaseModel):
    client_id: str
    client_name: str
    client_type: str
    client_country: str
    client_risk_profile: str

    portfolio_count: int
    total_portfolio_value: float
    average_return_percent: float

    high_risk_portfolio_count: int
    medium_risk_portfolio_count: int
    low_risk_portfolio_count: int

    client_status: str
    created_date: date