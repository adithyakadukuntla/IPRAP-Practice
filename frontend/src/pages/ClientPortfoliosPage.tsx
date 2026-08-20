import React, { useEffect, useState } from 'react';
import { ArrowUpRight, BriefcaseBusiness } from 'lucide-react';
import { useParams, Link } from 'react-router-dom';
import { portfolioApi } from '../services/api/portfolioApi';
import { RiskBadge } from '../components/common/RiskBadge';
import { formatCurrency, formatPercentage } from '../utils/formatters';
import type { Portfolio } from '../types';

export const ClientPortfoliosPage: React.FC = () => {
  const { clientId } = useParams();
  const [portfolios, setPortfolios] = useState<Portfolio[] | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!clientId) return;
    let mounted = true;
    setLoading(true);
    portfolioApi
      .getPortfolios({ page: 1, page_size: 100, client_id: clientId })
      .then((data) => mounted && setPortfolios(data))
      .catch((err) => mounted && setError(err?.message || 'Failed to load'))
      .finally(() => mounted && setLoading(false));

    return () => {
      mounted = false;
    };
  }, [clientId]);

  if (loading) return <div className="mx-auto max-w-5xl px-4 py-10 text-slate-600">Loading portfolios…</div>;
  if (error) return <div className="mx-auto max-w-5xl px-4 py-10 text-red-600">{error}</div>;
  if (!portfolios || portfolios.length === 0)
    return <div className="mx-auto max-w-5xl px-4 py-10 text-slate-600">No portfolios available for this client.</div>;

  return (
    <div className="bg-slate-50/70 py-8">
      <div className="mx-auto max-w-5xl px-4 sm:px-6 lg:px-8">
        <div className="mb-6 flex items-center gap-3">
          <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-slate-900 text-white shadow-lg shadow-slate-900/20">
            <BriefcaseBusiness className="h-5 w-5" />
          </div>
          <div>
            <p className="text-xs font-semibold uppercase tracking-[0.18em] text-slate-500">Client</p>
            <h1 className="text-3xl font-bold text-slate-900">Client Portfolios</h1>
          </div>
        </div>

        <div className="space-y-4">
          {portfolios.map((p) => (
            <Link
              key={p.id}
              to={`/portfolios/${p.id}`}
              className="group block rounded-2xl border border-slate-200/80 bg-white/85 p-5 shadow-[0_20px_45px_-28px_rgba(15,23,42,0.45)] backdrop-blur-sm transition-all duration-200 hover:-translate-y-0.5 hover:border-sky-200 hover:shadow-[0_24px_55px_-30px_rgba(14,165,233,0.55)]"
            >
              <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
                <div className="flex items-start gap-4">
                  <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-sky-100 text-sky-700">
                    <BriefcaseBusiness className="h-5 w-5" />
                  </div>
                  <div>
                    <div className="text-lg font-semibold text-slate-900 group-hover:text-sky-700">{p.name}</div>
                    <div className="mt-1 text-sm text-slate-500">{p.id}</div>
                    <div className="mt-2 flex flex-wrap items-center gap-2 text-xs text-slate-600">
                      <span className="rounded-full bg-slate-100 px-2.5 py-1 font-medium">{p.type}</span>
                      <span className="rounded-full bg-slate-100 px-2.5 py-1 font-medium">{p.status}</span>
                    </div>
                  </div>
                </div>

                <div className="flex flex-col items-start gap-3 md:items-end">
                  <RiskBadge level={p.riskProfile as 'low' | 'medium' | 'high'} />
                  <div className="text-right">
                    <div className="text-xl font-bold text-slate-900">{formatCurrency(p.currentValue, p.baseCurrency)}</div>
                    <div className={`text-sm font-medium ${p.returnPercentage >= 0 ? 'text-emerald-600' : 'text-rose-600'}`}>
                      {formatPercentage(p.returnPercentage)}
                    </div>
                  </div>
                  <div className="inline-flex items-center gap-2 text-sm font-medium text-sky-700">
                    View portfolio
                    <ArrowUpRight className="h-4 w-4 transition-transform group-hover:translate-x-0.5 group-hover:-translate-y-0.5" />
                  </div>
                </div>
              </div>
            </Link>
          ))}
        </div>
      </div>
    </div>
  );
};

export default ClientPortfoliosPage;
