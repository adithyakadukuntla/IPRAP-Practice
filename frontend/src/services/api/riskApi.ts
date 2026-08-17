import type { RiskData } from '../../types';
import { mockRiskData } from '../mock/mockData';
import { apiClient } from './apiClient';

const USE_MOCK_API = import.meta.env.VITE_USE_MOCK_API === 'true' || false;

export const riskApi = {
  // Get risk data for a portfolio
  async getRisk(portfolioId: string): Promise<RiskData> {
    if (USE_MOCK_API) {
      const risk = mockRiskData[portfolioId];
      if (!risk) {
        throw new Error(`Risk data for portfolio ${portfolioId} not found`);
      }
      return risk;
    }

    const response = await apiClient.get(`/portfolios/${portfolioId}/risk`);
    const r:any = response.data;
    if (!r) throw new Error('Risk data not found');

    return {
      riskProfile: (r.portfolio_risk_profile || r.risk_profile || '').toLowerCase(),
      // The API returns a categorical `concentration_risk` (e.g. 'HIGH') and
      // a numeric `highest_weight_percent`. Use the numeric highest weight
      // as the concentration percentage shown in the UI.
      concentrationRisk: Number(r.highest_weight_percent) || 0,
      highestSecurityWeight: Number(r.highest_weight_percent) || 0,
      riskStatus: (r.risk_status || '').toLowerCase(),
      message: r.risk_explanation || r.riskExplanation || '',
    } as RiskData;
  },
};
