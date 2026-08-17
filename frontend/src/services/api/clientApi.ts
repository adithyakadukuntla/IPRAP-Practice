import type { Client, Portfolio } from '../../types';
import { mockClients, mockPortfolios } from '../mock/mockData';
import { apiClient } from './apiClient';

const USE_MOCK_API = import.meta.env.VITE_USE_MOCK_API === 'true' || false;

export const clientApi = {
  // Get all clients
  async getClients(): Promise<Client[]> {
    if (USE_MOCK_API) {
      return mockClients;
    }

    const response = await apiClient.get('/clients');
    const data = response.data || [];

    // Map backend fields to frontend Client type
    return (data || []).map((c: any) => ({
      id: c.client_id || c.id || '',
      name: c.client_name || c.name || '',
      email: c.email || '',
      type: c.client_type || c.type || '',
    }));
  },

  // Get single client by ID
  async getClient(clientId: string): Promise<Client> {
    if (USE_MOCK_API) {
      const client = mockClients.find(c => c.id === clientId);
      if (!client) {
        throw new Error(`Client ${clientId} not found`);
      }
      return client;
    }

    const response = await apiClient.get(`/clients/${clientId}`);
    const c = response.data;
    if (!c) throw new Error('Client not found');

    return {
      id: c.client_id || c.id || '',
      name: c.client_name || c.name || '',
      email: c.email || '',
      type: c.client_type || c.type || '',
    };
  },

  // Get portfolios for a client
  async getClientPortfolios(clientId: string): Promise<Portfolio[]> {
    if (USE_MOCK_API) {
      return mockPortfolios.filter(p => p.clientId === clientId);
    }

    const response = await apiClient.get<Portfolio[]>(
      `/clients/${clientId}/portfolios`
    );
    return response.data;
  },
};
