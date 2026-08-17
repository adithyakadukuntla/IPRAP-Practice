from pydantic import BaseModel


class DashboardKPIs(BaseModel):
    total_portfolio_value: float
    active_portfolios: int
    average_return: float
    high_risk_portfolios: int
    total_holdings: int
