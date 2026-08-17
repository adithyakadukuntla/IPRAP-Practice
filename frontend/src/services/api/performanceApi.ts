import type { PerformanceData } from '../../types';
import { mockPerformanceData } from '../mock/mockData';
import { apiClient } from './apiClient';

const USE_MOCK_API = import.meta.env.VITE_USE_MOCK_API === 'true' || false;

export const performanceApi = {
  // Get performance data for a portfolio
  async getPerformance(portfolioId: string, params?: {
    startDate?: string;
    endDate?: string;
  }): Promise<PerformanceData[]> {
    if (USE_MOCK_API) {
      return mockPerformanceData[portfolioId] || [];
    }

    const response = await apiClient.get(`/portfolios/${portfolioId}/performance`, { params });
    const data = response.data;
    const items = data?.items ?? [];

    // Map backend performance fields to frontend `PerformanceData`
    return items.map((p: any) => ({
      date: p.as_of_date || p.date || '',
      portfolioValue: p.ending_value ?? p.portfolio_value ?? 0,
      returnPercentage: p.return_percent ?? p.returnPercentage ?? 0,
    }));
  },
};
