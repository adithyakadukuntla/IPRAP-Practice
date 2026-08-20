import React, { useState, useCallback } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useAsync } from '../hooks/useAsync';
import { allocationApi } from '../services/api/allocationApi';
import { portfolioApi } from '../services/api/portfolioApi';
import { LoadingSpinner } from '../components/common/LoadingSpinner';
import { ErrorAlert } from '../components/common/ErrorAlert';
import { EmptyState } from '../components/common/EmptyState';
import { DataTable } from '../components/common/DataTable';
import type { TableColumn } from '../components/common/DataTable';
import { formatCurrency, formatPercentage, formatDate } from '../utils/formatters';
import { ArrowLeft } from 'lucide-react';

interface AllocationItem {
  name: string;
  value: number;
  percentage: number;
}

export const AllocationPage: React.FC = () => {
  const { portfolioId } = useParams<{ portfolioId: string }>();
  const navigate = useNavigate();
  const [dimension, setDimension] = useState<'sector' | 'security' | 'country'>('sector');
  const [dismissError, setDismissError] = useState(false);

  const fetchPortfolio = useCallback(() => portfolioApi.getPortfolio(portfolioId || ''), [portfolioId]);
  const { data: portfolio } = useAsync(fetchPortfolio, !!portfolioId);

  const fetchAllocation = useCallback(
    () => allocationApi.getAllocation(portfolioId || '', { dimension }),
    [portfolioId, dimension]
  );

  const { data: allocation, loading, error } = useAsync(fetchAllocation, !!(portfolioId && dimension));

  const columns: TableColumn<AllocationItem>[] = [
    {
      key: 'name',
      label: dimension.charAt(0).toUpperCase() + dimension.slice(1),
      sortable: true,
    },
    {
      key: 'value',
      label: 'Market Value',
      render: (value: number) => formatCurrency(value, portfolio?.baseCurrency),
    },
    {
      key: 'percentage',
      label: 'Allocation %',
      render: (value: number) => (
        <div className="flex items-center gap-2">
          <div className="h-2 w-32 rounded-full bg-gray-200">
            <div
              className="h-2 rounded-full bg-primary-500"
              style={{ width: `${value}%` }}
            />
          </div>
          <span>{formatPercentage(value)}</span>
        </div>
      ),
    },
  ];

  if (loading) {
    return <LoadingSpinner fullScreen />;
  }

  if (!dismissError && error) {
    return (
      <div className="min-h-screen bg-gray-50 p-6">
        <ErrorAlert
          title="Failed to load allocation data"
          message={error.message}
          onDismiss={() => setDismissError(true)}
          statusCode={500}
        />
      </div>
    );
  }

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
            <p className="text-xs font-semibold uppercase tracking-[0.18em] text-slate-500">Allocation</p>
            <h1 className="mt-2 text-3xl font-bold text-slate-900">Asset Allocation</h1>
            <p className="mt-1 text-sm text-slate-500">{portfolio?.name}</p>
          </div>
        </div>

        <div className="glass-card mb-6 rounded-2xl p-4">
          <div className="flex flex-wrap gap-3">
            {(['sector', 'security', 'country'] as const).map((dim) => (
              <button
                key={dim}
                onClick={() => setDimension(dim)}
                className={`rounded-xl px-4 py-2.5 text-sm font-medium transition-all ${
                  dimension === dim
                    ? 'bg-slate-900 text-white shadow-lg shadow-slate-900/20'
                    : 'border border-slate-200 bg-white text-slate-700 hover:border-slate-300 hover:bg-slate-50'
                }`}
              >
                By {dim.charAt(0).toUpperCase() + dim.slice(1)}
              </button>
            ))}
          </div>
        </div>

        {/* Charts - Disabled due to Recharts re-render issues, table below shows data */}
        {allocation && allocation.items.length > 0 ? (
          <>
            {/* Hidden charts for now - keeping for future Recharts upgrade */}

            {/* Allocation Table */}
            <div className="glass-card overflow-hidden rounded-2xl">
              <div className="border-b border-slate-200/80 bg-white/60 px-6 py-4">
                <h3 className="text-lg font-semibold text-slate-900">Detailed Allocation ({dimension})</h3>
                <p className="mt-1 text-sm text-slate-600">As of {formatDate(allocation.asOfDate)}</p>
              </div>
              <DataTable
                columns={columns}
                data={allocation.items}
                rowKey="name"
              />
            </div>
          </>
        ) : (
          <EmptyState
            title="No allocation data available"
            description="There is no allocation data for this portfolio."
          />
        )}
      </div>
    </div>
  );
};
