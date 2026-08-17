import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { clientApi } from '../services/api/clientApi';
import type { Client } from '../types';

export const ClientsPage: React.FC = () => {
  const [clients, setClients] = useState<Client[] | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let mounted = true;
    setLoading(true);
    clientApi
      .getClients()
      .then((data) => mounted && setClients(data))
      .catch((err) => mounted && setError(err?.message || 'Failed to load'))
      .finally(() => mounted && setLoading(false));

    return () => {
      mounted = false;
    };
  }, []);

  if (loading) return <div className="p-6">Loading clients…</div>;
  if (error) return <div className="p-6 text-red-600">{error}</div>;
  if (!clients || clients.length === 0)
    return <div className="p-6">No clients available.</div>;

  return (
    <div className="p-6">
      <h1 className="text-2xl font-semibold mb-4">Clients</h1>
      <ul className="space-y-2">
        {clients.map((c) => (
          <li key={c.id} className="border rounded p-3">
            <div className="flex items-center justify-between">
              <div>
                <div className="font-medium">{c.name}</div>
                <div className="text-sm text-gray-500">{c.email}</div>
              </div>
              <div>
                {c.id ? (
                  <Link
                    to={`/clients/${c.id}/portfolios`}
                    className="text-primary-600 hover:underline"
                  >
                    View portfolios
                  </Link>
                ) : (
                  <span className="text-gray-400">No portfolios</span>
                )}
              </div>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default ClientsPage;
