import React, { useState, useCallback } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useAsync } from '../hooks/useAsync';
import { portfolioApi } from '../services/api/portfolioApi';
import { LoadingSpinner } from '../components/common/LoadingSpinner';
import { ErrorAlert } from '../components/common/ErrorAlert';
import { KPICard } from '../components/common/KPICard';
import { RiskBadge } from '../components/common/RiskBadge';
import { formatCurrency, formatPercentage, formatDate } from '../utils/formatters';
import { ChevronRight, ArrowLeft } from 'lucide-react';

export const PortfolioDetailPage: React.FC = () => {
  const { portfolioId } = useParams<{ portfolioId: string }>();
  const navigate = useNavigate();
  const [dismissError, setDismissError] = useState(false);

  const fetchPortfolio = useCallback(
    () => portfolioApi.getPortfolio(portfolioId || ''),
    [portfolioId]
  );

  const { data: portfolio, loading, error } = useAsync(fetchPortfolio, !!portfolioId);

  if (loading) {
    return <LoadingSpinner fullScreen />;
  }

  if (!dismissError && error) {
    return (
      <div className="min-h-screen bg-gray-50 p-6">
        <ErrorAlert
          title="Portfolio Not Found"
          message={error.message}
          onDismiss={() => {
            setDismissError(true);
            navigate('/portfolios');
          }}
          statusCode={404}
        />
      </div>
    );
  }

  if (!portfolio) {
    return (
      <div className="min-h-screen bg-gray-50 p-6">
        <ErrorAlert
          title="Portfolio Not Found"
          message="The requested portfolio could not be found."
          statusCode={404}
        />
      </div>
    );
  }

  const tabs = [
    { label: 'Overview', href: '#' },
    { label: 'Holdings', href: `/portfolios/${portfolioId}/holdings` },
    { label: 'Allocation', href: `/portfolios/${portfolioId}/allocation` },
    { label: 'Performance', href: `/portfolios/${portfolioId}/performance` },
    { label: 'Risk', href: `/portfolios/${portfolioId}/risk` },
  ];

  return (
    <div className="bg-slate-50/70 py-8">
      <div className="mx-auto max-w-5xl px-4 sm:px-6 lg:px-8">
        {/* Header with Back Button */}
        <div className="mb-6 flex items-center gap-4">
          <button
            onClick={() => {
              try {
                if (window.history.length > 1) {
                  navigate(-1);
                } else {
                  navigate('/portfolios');
                }
              } catch (err) {
                navigate('/portfolios');
              }
            }}
            className="inline-flex items-center gap-2 rounded-xl border border-slate-200 bg-white px-4 py-2.5 text-sm font-medium text-slate-700 shadow-sm transition hover:border-slate-300 hover:bg-slate-50"
          >
            <ArrowLeft className="h-4 w-4" />
            Back
          </button>
          <div>
            <p className="text-xs font-semibold uppercase tracking-[0.18em] text-slate-500">Portfolio overview</p>
            <h1 className="mt-2 text-3xl font-bold text-slate-900">{portfolio.name}</h1>
            <p className="mt-1 text-sm text-slate-500">Portfolio ID: {portfolio.id}</p>
          </div>
        </div>

        {/* Portfolio Summary Cards */}
        <div className="mb-8 grid grid-cols-1 gap-4 md:grid-cols-3 lg:grid-cols-5">
          <KPICard
            title="Current Value"
            value={formatCurrency(portfolio.currentValue, portfolio.baseCurrency)}
            subtitle={portfolio.baseCurrency}
            wide
          />
          <KPICard
            title="Initial Value"
            value={formatCurrency(portfolio.initialValue, portfolio.baseCurrency)}
            subtitle={portfolio.baseCurrency}
            wide
          />
          <KPICard
            title="Total Return"
            value={formatCurrency(portfolio.return, portfolio.baseCurrency)}
            subtitle={formatPercentage(portfolio.returnPercentage)}
            trend={{ value: portfolio.returnPercentage, direction: portfolio.returnPercentage >= 0 ? 'up' : 'down' }}
            wide
          />
          <KPICard
            title="Risk Profile"
            value={portfolio.riskProfile.toUpperCase()}
            subtitle={`${portfolio.holdingCount} Holdings`}
          />
          <KPICard
            title="Status"
            value={portfolio.status.toUpperCase()}
            subtitle={`As of ${formatDate(portfolio.asOfDate)}`}
          />
        </div>

        {/* Portfolio Details Grid */}
        <div className="glass-card mb-8 rounded-2xl p-6">
          <h2 className="mb-6 text-lg font-semibold text-slate-900">Portfolio Details</h2>
          <div className="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-4">
            <div>
              <p className="text-sm font-medium text-gray-600">Portfolio Type</p>
              <p className="mt-2 text-lg text-gray-900">{portfolio.type}</p>
            </div>
            <div>
              <p className="text-sm font-medium text-gray-600">Client ID</p>
              <p className="mt-2 text-lg text-gray-900">{portfolio.clientId}</p>
            </div>
            <div>
              <p className="text-sm font-medium text-gray-600">Risk Level</p>
              <p className="mt-2">
                <RiskBadge level={portfolio.riskProfile as 'low' | 'medium' | 'high'} />
              </p>
            </div>
            <div>
              <p className="text-sm font-medium text-gray-600">Total Holdings</p>
              <p className="mt-2 text-lg text-gray-900">{portfolio.holdingCount}</p>
            </div>
          </div>
        </div>

        {/* Navigation Tabs */}
        <div className="glass-card overflow-hidden rounded-2xl">
          <div className="border-b border-slate-200/80 bg-white/50">
            <nav className="flex flex-wrap gap-2 px-5" aria-label="Tabs">
              {tabs.map((tab, idx) => (
                <button
                  key={idx}
                  onClick={() => {
                    if (tab.href !== '#') {
                      navigate(tab.href);
                    }
                  }}
                  className={`flex items-center gap-2 rounded-t-xl border-b-2 px-3 py-3.5 text-sm font-medium transition ${
                    tab.href === '#'
                      ? 'border-sky-600 text-sky-700 bg-sky-50/80'
                      : 'border-transparent text-slate-600 hover:border-slate-300 hover:text-slate-900'
                  }`}
                >
                  {tab.label}
                  {tab.href !== '#' && <ChevronRight className="h-4 w-4" />}
                </button>
              ))}
            </nav>
          </div>

          {/* Overview Content */}
          <div className="p-6">
            <h3 className="mb-4 text-lg font-semibold text-gray-900">Performance Summary</h3>
            <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
              <div className="rounded-lg bg-gray-50 p-4">
                <p className="text-sm text-gray-600">Absolute Return</p>
                <p className={`mt-2 text-2xl font-bold ${portfolio.return >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                  {formatCurrency(portfolio.return, portfolio.baseCurrency)}
                </p>
              </div>
              <div className="rounded-lg bg-gray-50 p-4">
                <p className="text-sm text-gray-600">Return Percentage</p>
                <p className={`mt-2 text-2xl font-bold ${portfolio.returnPercentage >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                  {formatPercentage(portfolio.returnPercentage)}
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
