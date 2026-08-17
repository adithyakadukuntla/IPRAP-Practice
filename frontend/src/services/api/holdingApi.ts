import type { Holding } from '../../types';
import { mockHoldings } from '../mock/mockData';
import { apiClient } from './apiClient';

const USE_MOCK_API = import.meta.env.VITE_USE_MOCK_API === 'true' || false;

export const holdingApi = {
  // Get holdings for a portfolio
  async getHoldings(portfolioId: string, params?: {
    page?: number;
    limit?: number;
    sortBy?: string;
  }): Promise<Holding[]> {
    if (USE_MOCK_API) {
      return mockHoldings[portfolioId] || [];
    }

    const response = await apiClient.get(`/portfolios/${portfolioId}/holdings`, { params });
    const data = response.data;
    const items = data?.items ?? [];

    const map = (h: any): Holding => ({
      id: h.holding_id || h.id,
      securityId: h.security_id || h.securityId,
      ticker: h.ticker_symbol || h.ticker || '',
      name: h.security_name || h.name || '',
      type: h.security_type || h.type || '',
      sector: h.sector || '',
      quantity: h.quantity ?? 0,
      purchasePrice: h.purchase_price ?? h.purchasePrice ?? 0,
      currentPrice: h.current_price ?? h.currentPrice ?? 0,
      marketValue: h.market_value ?? h.marketValue ?? 0,
      asOfDate: h.as_of_date || h.asOfDate || '',
    });

    return items.map(map);
  },

  // Get single holding by ID
  async getHolding(portfolioId: string, holdingId: string): Promise<Holding> {
    if (USE_MOCK_API) {
      const holding = (mockHoldings[portfolioId] || []).find(h => h.id === holdingId);
      if (!holding) {
        throw new Error(`Holding ${holdingId} not found`);
      }
      return holding;
    }

    const response = await apiClient.get(`/portfolios/${portfolioId}/holdings/${holdingId}`);
    const h = response.data;
    if (!h) throw new Error('Holding not found');

    return {
      id: h.holding_id || h.id,
      securityId: h.security_id || h.securityId,
      ticker: h.ticker_symbol || h.ticker || '',
      name: h.security_name || h.name || '',
      type: h.security_type || h.type || '',
      sector: h.sector || '',
      quantity: h.quantity ?? 0,
      purchasePrice: h.purchase_price ?? h.purchasePrice ?? 0,
      currentPrice: h.current_price ?? h.currentPrice ?? 0,
      marketValue: h.market_value ?? h.marketValue ?? 0,
      asOfDate: h.as_of_date || h.asOfDate || '',
    };
  },
};
