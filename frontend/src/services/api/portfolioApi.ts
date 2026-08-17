import type { Portfolio, DashboardKPIs } from '../../types';
import { mockPortfolios, mockDashboardKPIs } from '../mock/mockData';
import { apiClient } from './apiClient';

const USE_MOCK_API = import.meta.env.VITE_USE_MOCK_API === 'true' || false; // Toggle via env

export const portfolioApi = {
  // Get all portfolios with optional pagination and filters
  async getPortfolios(params?: {
    page?: number;
    limit?: number;
    search?: string;
    riskProfile?: string;
    status?: string;
    type?: string;
  }): Promise<Portfolio[]> {
    if (USE_MOCK_API) {
      // Simulate pagination and filtering
      let filtered = [...mockPortfolios];

      if (params?.search) {
        filtered = filtered.filter(p =>
          p.name.toLowerCase().includes(params.search!.toLowerCase()) ||
          p.id.toLowerCase().includes(params.search!.toLowerCase())
        );
      }

      if (params?.riskProfile) {
        filtered = filtered.filter(p => p.riskProfile === params.riskProfile);
      }

      if (params?.status) {
        filtered = filtered.filter(p => p.status === params.status);
      }

      if (params?.type) {
        filtered = filtered.filter(p => p.type === params.type);
      }

      return filtered;
    }

    // Sanitize params for backend: map camelCase to snake_case, remove undefined,
    // and enforce page_size limit. Backend expects `page` and `page_size`.
    const cleanParams: Record<string, any> = {};

    if (params) {
      // Page and limit/page_size
      if (params.page !== undefined) cleanParams.page = params.page;
      if (params.limit !== undefined) cleanParams.page_size = params.limit;
      if ((params as any).page_size !== undefined) cleanParams.page_size = (params as any).page_size;

      // Filters: map frontend camelCase keys to backend snake_case
      if ((params as any).riskProfile) cleanParams.risk_profile = (params as any).riskProfile;
      if ((params as any).clientId) cleanParams.client_id = (params as any).clientId;
      if (params.status) cleanParams.status = params.status;
      if ((params as any).type) cleanParams.type = (params as any).type;
      if ((params as any).search) cleanParams.search = (params as any).search;
    }

    // Remove undefined or literal 'undefined' values
    Object.keys(cleanParams).forEach((k) => {
      if (cleanParams[k] === undefined || cleanParams[k] === 'undefined') {
        delete cleanParams[k];
      }
    });

    // Cap page_size to 100 per backend validation
    if (cleanParams.page_size && Number(cleanParams.page_size) > 100) {
      cleanParams.page_size = 100;
    }

    const response = await apiClient.get('/portfolios', { params: cleanParams });

    // Backend returns a paginated response { items, page, page_size, total_items, total_pages }
    const data = response.data;
    const items = data?.items ?? [];

    // Map backend snake_case fields to frontend camelCase `Portfolio` shape
    const map = (p: any): Portfolio => ({
      id: p.portfolio_id || p.id,
      name: p.portfolio_name || p.name,
      clientId: p.client_id || p.clientId,
      type: p.portfolio_type || p.type,
      riskProfile: (p.risk_profile || p.riskProfile || '').toLowerCase(),
      baseCurrency: p.base_currency || p.baseCurrency,
      currentValue: p.current_value ?? p.currentValue ?? 0,
      initialValue: p.initial_value ?? p.initialValue ?? 0,
      return: p.return_amount ?? p.return ?? 0,
      returnPercentage: p.return_percent ?? p.returnPercentage ?? 0,
      status: (p.status || p.status) ? (p.status || p.status).toLowerCase() : 'active',
      holdingCount: p.holding_count ?? p.holdingCount ?? 0,
      asOfDate: p.latest_performance_date || p.as_of_date || p.asOfDate || '',
    });

    return items.map(map);
  },

  // Get single portfolio by ID
  async getPortfolio(portfolioId: string): Promise<Portfolio> {
    if (USE_MOCK_API) {
      const portfolio = mockPortfolios.find(p => p.id === portfolioId);
      if (!portfolio) {
        throw new Error(`Portfolio ${portfolioId} not found`);
      }
      return portfolio;
    }

    const response = await apiClient.get(`/portfolios/${portfolioId}`);
    const p = response.data;
    if (!p) throw new Error('Portfolio not found');

    return {
      id: p.portfolio_id || p.id,
      name: p.portfolio_name || p.name,
      clientId: p.client_id || p.clientId,
      type: p.portfolio_type || p.type,
      riskProfile: (p.risk_profile || p.riskProfile || '').toLowerCase(),
      baseCurrency: p.base_currency || p.baseCurrency,
      currentValue: p.current_value ?? p.currentValue ?? 0,
      initialValue: p.initial_value ?? p.initialValue ?? 0,
      return: p.return_amount ?? p.return ?? 0,
      returnPercentage: p.return_percent ?? p.returnPercentage ?? 0,
      status: (p.status || p.status) ? (p.status || p.status).toLowerCase() : 'active',
      holdingCount: p.holding_count ?? p.holdingCount ?? 0,
      asOfDate: p.latest_performance_date || p.as_of_date || p.asOfDate || '',
    };
  },

  // Get dashboard KPIs
  async getDashboardKPIs(): Promise<DashboardKPIs> {
    if (USE_MOCK_API) {
      return mockDashboardKPIs;
    }

    const response = await apiClient.get('/dashboard/kpis');
    const d = response.data || {};

    return {
      totalPortfolioValue: d.total_portfolio_value ?? d.totalPortfolioValue ?? 0,
      activePortfolios: d.active_portfolios ?? d.activePortfolios ?? 0,
      averageReturn: d.average_return ?? d.averageReturn ?? 0,
      highRiskPortfolios: d.high_risk_portfolios ?? d.highRiskPortfolios ?? 0,
      totalHoldings: d.total_holdings ?? d.totalHoldings ?? 0,
    } as DashboardKPIs;
  },
};
