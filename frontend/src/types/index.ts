export interface Portfolio {
  id: string;
  name: string;
  clientId: string;
  type: string;
  riskProfile: 'low' | 'medium' | 'high';
  baseCurrency: string;
  currentValue: number;
  initialValue: number;
  return: number;
  returnPercentage: number;
  status: 'active' | 'inactive';
  holdingCount: number;
  asOfDate: string;
}

export interface Holding {
  id: string;
  securityId: string;
  ticker: string;
  name: string;
  type: string;
  sector: string;
  quantity: number;
  purchasePrice: number;
  currentPrice: number;
  marketValue: number;
  asOfDate: string;
}

export interface AllocationData {
  dimension: 'sector' | 'security' | 'country';
  items: {
    name: string;
    value: number;
    percentage: number;
  }[];
  asOfDate: string;
}

export interface PerformanceData {
  date: string;
  portfolioValue: number;
  returnPercentage: number;
}

export interface RiskData {
  riskProfile: string;
  concentrationRisk: number;
  highestSecurityWeight: number;
  riskStatus: 'low' | 'medium' | 'high';
  message: string;
}

export interface Client {
  id: string;
  name: string;
  email: string;
  type: string;
}

export interface DashboardKPIs {
  totalPortfolioValue: number;
  activePortfolios: number;
  averageReturn: number;
  highRiskPortfolios: number;
  totalHoldings: number;
}

export interface ApiResponse<T> {
  success: boolean;
  data: T;
  error?: string;
}
