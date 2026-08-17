import type { AllocationData } from '../../types';
import { mockAllocationData } from '../mock/mockData';
import { apiClient } from './apiClient';

const USE_MOCK_API = import.meta.env.VITE_USE_MOCK_API === 'true' || false;

export const allocationApi = {
  // Get allocation data for a portfolio
  async getAllocation(
    portfolioId: string,
    params?: {
      dimension?: 'sector' | 'security' | 'country';
    }
  ): Promise<AllocationData> {
    if (USE_MOCK_API) {
      const data = mockAllocationData[portfolioId];
      if (!data) {
        // Return a default allocation if not found
        return {
          dimension: params?.dimension || 'sector',
          items: [],
          asOfDate: new Date().toISOString().split('T')[0],
        };
      }
      return data;
    }

    const response = await apiClient.get(`/portfolios/${portfolioId}/allocation`, { params });
    const data = response.data || { items: [], dimension: params?.dimension || 'sector' };

    // Map backend allocation items into frontend-friendly shape and handle aggregated field names
    const mappedItems = (data.items || []).map((it: any) => {
      const name = it.security_name || it.sector || it.security_country || it.security_id || '';

      const rawValue = it.security_market_value ?? it.sector_market_value ?? it.country_market_value ?? it.portfolio_total_value ?? 0;
      const rawPercentage = (params?.dimension === 'sector'
        ? it.sector_allocation_percent
        : params?.dimension === 'country'
        ? it.country_allocation_percent
        : it.security_allocation_percent) ?? 0;

      const value = Number(rawValue) || 0;
      const percentage = Number(rawPercentage) || 0;

      return {
        name,
        value,
        percentage,
      };
    });

    return {
      dimension: data.dimension || params?.dimension || 'sector',
      items: mappedItems,
      asOfDate: data.items && data.items.length > 0 ? (data.items[0].as_of_date || data.items[0].as_of_date || '') : new Date().toISOString().split('T')[0],
    } as AllocationData;
  },
};
