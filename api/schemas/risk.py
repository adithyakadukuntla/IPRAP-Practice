from datetime import datetime

from pydantic import BaseModel


class PortfolioRisk(BaseModel):
    portfolio_id: str
    client_id: str
    portfolio_name: str

    portfolio_risk_profile: str

    highest_holding_security_id: str
    highest_holding_value: float
    highest_weight_percent: float

    concentration_risk: str
    risk_status: str
    risk_explanation: str

    current_value: float
    total_market_value: float
    holding_count: int

    analyzed_at: datetime