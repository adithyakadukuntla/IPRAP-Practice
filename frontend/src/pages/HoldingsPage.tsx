import React, { useState, useCallback } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useAsync } from '../hooks/useAsync';
import { holdingApi } from '../services/api/holdingApi';
import { portfolioApi } from '../services/api/portfolioApi';
import type { Holding } from '../types';
import { LoadingSpinner } from '../components/common/LoadingSpinner';
import { ErrorAlert } from '../components/common/ErrorAlert';
import { EmptyState } from '../components/common/EmptyState';
import { DataTable } from '../components/common/DataTable';
import type { TableColumn } from '../components/common/DataTable';
import { formatCurrency, formatNumber } from '../utils/formatters';
import { ArrowLeft } from 'lucide-react';

export const HoldingsPage: React.FC = () => {
  const { portfolioId } = useParams<{ portfolioId: string }>();
  const navigate = useNavigate();
  const [dismissError, setDismissError] = useState(false);

  const fetchPortfolio = useCallback(
    () => portfolioApi.getPortfolio(portfolioId || ''),
    [portfolioId]
  );

  const fetchHoldings = useCallback(
    () => holdingApi.getHoldings(portfolioId || ''),
    [portfolioId]
  );

  const { data: portfolio } = useAsync(fetchPortfolio, !!portfolioId);
  const { data: holdings, loading, error } = useAsync(fetchHoldings, !!portfolioId);

  const columns: TableColumn<Holding>[] = [
    {
      key: 'ticker',
      label: 'Ticker',
      sortable: true,
    },
    {
      key: 'name',
      label: 'Security Name',
      sortable: true,
    },
    {
      key: 'type',
      label: 'Type',
    },
    {
      key: 'sector',
      label: 'Sector',
    },
    {
      key: 'quantity',
      label: 'Quantity',
      render: (value: number) => formatNumber(value),
    },
    {
      key: 'purchasePrice',
      label: 'Purchase Price',
      render: (value: number) => formatCurrency(value),
    },
    {
      key: 'currentPrice',
      label: 'Current Price',
      render: (value: number) => formatCurrency(value),
    },
    {
      key: 'marketValue',
      label: 'Market Value',
      render: (value: number) => formatCurrency(value),
    },
  ];

  if (loading) {
    return <LoadingSpinner fullScreen />;
  }

  if (!dismissError && error) {
    return (
      <div className="min-h-screen bg-gray-50 p-6">
        <ErrorAlert
          title="Failed to load holdings"
          message={error.message}
          onDismiss={() => setDismissError(true)}
          statusCode={500}
        />
      </div>
    );
  }

  const totalMarketValue = holdings?.reduce((sum, h) => sum + h.marketValue, 0) || 0;

  return (
    <div className="bg-slate-50/70 py-8">
      <div className="mx-auto max-w-5xl px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="mb-6 flex items-center gap-4">
          <button
            onClick={() => navigate(`/portfolios/${portfolioId}`)}
            className="inline-flex items-center gap-2 rounded-xl border border-slate-200 bg-white px-4 py-2.5 text-sm font-medium text-slate-700 shadow-sm transition hover:border-slate-300 hover:bg-slate-50"
          >
            <ArrowLeft className="h-4 w-4" />
            Back
          </button>
          <div>
            <p className="text-xs font-semibold uppercase tracking-[0.18em] text-slate-500">Portfolio holdings</p>
            <h1 className="mt-2 text-3xl font-bold text-slate-900">Holdings</h1>
            <p className="mt-1 text-sm text-slate-500">{portfolio?.name}</p>
          </div>
        </div>

        {/* Summary Card */}
        <div className="mb-6 grid grid-cols-1 gap-4 md:grid-cols-3">
          <div className="glass-card rounded-2xl p-6">
            <p className="text-sm font-medium text-gray-600">Total Holdings</p>
            <p className="mt-2 text-3xl font-bold text-gray-900">{holdings?.length || 0}</p>
          </div>
          <div className="rounded-lg border border-gray-200 bg-white p-6 shadow-sm">
            <p className="text-sm font-medium text-gray-600">Total Market Value</p>
            <p className="mt-2 text-3xl font-bold text-gray-900">
              {formatCurrency(totalMarketValue, portfolio?.baseCurrency)}
            </p>
          </div>
          <div className="rounded-lg border border-gray-200 bg-white p-6 shadow-sm">
            <p className="text-sm font-medium text-gray-600">Average Position Size</p>
            <p className="mt-2 text-3xl font-bold text-gray-900">
              {holdings && holdings.length > 0
                ? formatCurrency(totalMarketValue / holdings.length, portfolio?.baseCurrency)
                : formatCurrency(0, portfolio?.baseCurrency)}
            </p>
          </div>
        </div>

        {/* Table */}
        {holdings && holdings.length > 0 ? (
          <div className="glass-card overflow-hidden rounded-2xl">
            <DataTable
              columns={columns}
              data={holdings}
              rowKey="id"
            />
          </div>
        ) : (
          <EmptyState
            title="No holdings found"
            description="This portfolio does not have any holdings at the moment."
          />
        )}
      </div>
    </div>
  );
};
