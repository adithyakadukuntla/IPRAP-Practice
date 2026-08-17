import React, { useState, useCallback, useMemo } from 'react';
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
import {
  PieChart,
  Pie,
  Cell,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts';
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

  const COLORS = ['#0ea5e9', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899', '#14b8a6', '#f97316'];

  return (
    <div className="bg-gray-50 py-8">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="mb-8 flex items-center gap-4">
          <button
            onClick={() => navigate(`/portfolios/${portfolioId}`)}
            className="inline-flex items-center gap-2 rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50"
          >
            <ArrowLeft className="h-4 w-4" />
            Back
          </button>
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Asset Allocation</h1>
            <p className="mt-2 text-gray-600">{portfolio?.name}</p>
          </div>
        </div>

        {/* Dimension Selector */}
        <div className="mb-6 flex gap-4">
          {(['sector', 'security', 'country'] as const).map((dim) => (
            <button
              key={dim}
              onClick={() => setDimension(dim)}
              className={`rounded-md px-4 py-2 text-sm font-medium transition-colors ${
                dimension === dim
                  ? 'bg-primary-600 text-white'
                  : 'border border-gray-300 bg-white text-gray-700 hover:bg-gray-50'
              }`}
            >
              By {dim.charAt(0).toUpperCase() + dim.slice(1)}
            </button>
          ))}
        </div>

        {/* Charts - Disabled due to Recharts re-render issues, table below shows data */}
        {allocation && allocation.items.length > 0 ? (
          <>
            {/* Hidden charts for now - keeping for future Recharts upgrade */}

            {/* Allocation Table */}
            <div className="rounded-lg bg-white shadow-sm">
              <div className="border-b border-gray-200 px-6 py-4">
                <h3 className="text-lg font-semibold text-gray-900">Detailed Allocation ({dimension})</h3>
                <p className="mt-1 text-sm text-gray-600">As of {formatDate(allocation.asOfDate)}</p>
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
