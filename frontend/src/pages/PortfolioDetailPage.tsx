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
    <div className="bg-gray-50 py-8">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        {/* Header with Back Button */}
        <div className="mb-8 flex items-center gap-4">
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
            className="inline-flex items-center gap-2 rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50"
          >
            <ArrowLeft className="h-4 w-4" />
            Back
          </button>
          <div>
            <h1 className="text-3xl font-bold text-gray-900">{portfolio.name}</h1>
            <p className="mt-2 text-gray-600">Portfolio ID: {portfolio.id}</p>
          </div>
        </div>

        {/* Portfolio Summary Cards */}
        <div className="mb-8 grid grid-cols-1 gap-4 md:grid-cols-3 lg:grid-cols-5">
          <KPICard
            title="Current Value"
            value={formatCurrency(portfolio.currentValue, portfolio.baseCurrency)}
            subtitle={portfolio.baseCurrency}
          />
          <KPICard
            title="Initial Value"
            value={formatCurrency(portfolio.initialValue, portfolio.baseCurrency)}
            subtitle={portfolio.baseCurrency}
          />
          <KPICard
            title="Total Return"
            value={formatCurrency(portfolio.return, portfolio.baseCurrency)}
            subtitle={formatPercentage(portfolio.returnPercentage)}
            trend={{ value: portfolio.returnPercentage, direction: portfolio.returnPercentage >= 0 ? 'up' : 'down' }}
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
        <div className="mb-8 rounded-lg border border-gray-200 bg-white p-6 shadow-sm">
          <h2 className="mb-6 text-lg font-semibold text-gray-900">Portfolio Details</h2>
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
        <div className="rounded-lg border border-gray-200 bg-white shadow-sm">
          <div className="border-b border-gray-200">
            <nav className="flex flex-wrap gap-4 px-6" aria-label="Tabs">
              {tabs.map((tab, idx) => (
                <button
                  key={idx}
                  onClick={() => {
                    if (tab.href !== '#') {
                      navigate(tab.href);
                    }
                  }}
                  className={`flex items-center gap-2 border-b-2 py-4 px-1 text-sm font-medium ${
                    tab.href === '#'
                      ? 'border-primary-500 text-primary-600'
                      : 'border-transparent text-gray-600 hover:border-gray-300 hover:text-gray-900'
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
