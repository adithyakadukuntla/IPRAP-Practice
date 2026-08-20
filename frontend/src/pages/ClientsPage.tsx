import React, { useEffect, useState } from 'react';
import { ArrowRight, BriefcaseBusiness, Mail, UserRound } from 'lucide-react';
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

  if (loading)
    return (
      <div className="rounded-[2rem] border border-slate-200/80 bg-white/80 p-8 text-center shadow-lg shadow-slate-200/40">
        <div className="text-lg font-semibold text-slate-700">Loading clients…</div>
      </div>
    );

  if (error)
    return (
      <div className="mx-auto max-w-6xl rounded-[2rem] border border-red-200 bg-red-50 p-8 text-red-700 shadow-sm">
        {error}
      </div>
    );

  if (!clients || clients.length === 0)
    return (
      <div className="mx-auto max-w-6xl rounded-[2rem] border border-slate-200 bg-white/80 p-10 text-center shadow-lg shadow-slate-200/40">
        <div className="text-xl font-bold text-slate-900">No clients available.</div>
      </div>
    );

  return (
    <div className="mx-auto max-w-7xl">
      <div className="mb-8 flex flex-col gap-3 md:flex-row md:items-end md:justify-between">
        <div>
          <p className="text-xs font-semibold uppercase tracking-[0.28em] text-blue-600">Client Network</p>
          <h1 className="mt-2 text-4xl font-black tracking-tight text-slate-900">Clients</h1>
        </div>
        <div className="rounded-full border border-slate-200 bg-white/80 px-4 py-2 text-sm font-medium text-slate-600 shadow-sm">
          {clients.length} active client{clients.length > 1 ? 's' : ''}
        </div>
      </div>

      <div className="grid gap-5 lg:grid-cols-2 xl:grid-cols-3">
        {clients.map((c) => (
          <div
            key={c.id}
            className="group rounded-[1.75rem] border border-slate-200/80 bg-white/85 p-5 shadow-[0_22px_50px_-28px_rgba(15,23,42,0.45)] backdrop-blur-sm transition-all duration-300 hover:-translate-y-1 hover:shadow-[0_30px_65px_-30px_rgba(37,99,235,0.35)]"
          >
            <div className="flex items-start justify-between gap-4">
              <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-gradient-to-br from-slate-900 to-blue-600 text-white shadow-md shadow-blue-500/20">
                <UserRound className="h-5 w-5" />
              </div>

              {c.id ? (
                <Link
                  to={`/clients/${c.id}/portfolios`}
                  className="inline-flex items-center gap-2 rounded-full border border-blue-200 bg-blue-50 px-3 py-1.5 text-xs font-bold uppercase tracking-[0.12em] text-blue-700 transition hover:border-blue-300 hover:bg-blue-100"
                >
                  View
                  <ArrowRight className="h-3.5 w-3.5" />
                </Link>
              ) : (
                <span className="rounded-full bg-slate-100 px-3 py-1 text-xs font-semibold text-slate-500">
                  No portfolios
                </span>
              )}
            </div>

            <div className="mt-5">
              <div className="flex items-center gap-2 text-xl font-black text-slate-900">
                <BriefcaseBusiness className="h-4 w-4 text-blue-600" />
                {c.name}
              </div>
              <div className="mt-4 flex items-center gap-2 text-sm text-slate-600">
                <Mail className="h-4 w-4 text-slate-400" />
                <span className="truncate">{c.email}</span>
              </div>
            </div>

            <div className="mt-5 rounded-2xl bg-slate-50 p-3 text-sm text-slate-600">
              Client ID: <span className="font-semibold text-slate-800">{c.id}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ClientsPage;
