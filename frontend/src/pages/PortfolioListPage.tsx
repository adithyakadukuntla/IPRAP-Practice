import React, { useState, useCallback, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAsync } from '../hooks/useAsync';
import { portfolioApi } from '../services/api/portfolioApi';
import type { Portfolio } from '../types';
import { LoadingSpinner } from '../components/common/LoadingSpinner';
import { ErrorAlert } from '../components/common/ErrorAlert';
import { EmptyState } from '../components/common/EmptyState';
import { DataTable } from '../components/common/DataTable';
import type { TableColumn } from '../components/common/DataTable';
import { RiskBadge } from '../components/common/RiskBadge';
import { formatCurrency, formatPercentage } from '../utils/formatters';
import { Search } from 'lucide-react';

export const PortfolioListPage: React.FC = () => {
  const navigate = useNavigate();
  const [search, setSearch] = useState('');
  // `appliedSearch` is the value actually used to query the API.
  // `search` is the live input; changing `search` will not trigger reloads until
  // the user clicks Search or presses Enter (which sets `appliedSearch`).
  const [appliedSearch, setAppliedSearch] = useState('');
  const [riskFilter, setRiskFilter] = useState<string>('');
  const [statusFilter, setStatusFilter] = useState<string>('');
  const [dismissError, setDismissError] = useState(false);

  const fetchPortfolios = useCallback(
    () =>
      portfolioApi.getPortfolios({
        search: appliedSearch || undefined,
        riskProfile: riskFilter || undefined,
        status: statusFilter || undefined,
        limit: 100,
      }),
    [appliedSearch, riskFilter, statusFilter]
  );

  const { data: portfolios, loading, error } = useAsync(fetchPortfolios, true);

  const columns: TableColumn<Portfolio>[] = [
    {
      key: 'id',
      label: 'Portfolio ID',
      sortable: true,
    },
    {
      key: 'name',
      label: 'Name',
      sortable: true,
    },
    {
      key: 'type',
      label: 'Type',
      sortable: true,
    },
    {
      key: 'riskProfile',
      label: 'Risk Profile',
      render: (value: string) => <RiskBadge level={value as 'low' | 'medium' | 'high'} />,
    },
    {
      key: 'currentValue',
      label: 'Current Value',
      sortable: true,
      render: (value: number) => formatCurrency(value),
    },
    {
      key: 'returnPercentage',
      label: 'Return %',
      sortable: true,
      render: (value: number) => (
        <span className={value >= 0 ? 'text-green-600' : 'text-red-600'}>
          {formatPercentage(value)}
        </span>
      ),
    },
    {
      key: 'status',
      label: 'Status',
      render: (value: string) => (
        <span
          className={`inline-flex rounded-full px-3 py-1 text-sm font-medium ${
            value === 'active'
              ? 'bg-green-100 text-green-800'
              : 'bg-gray-100 text-gray-800'
          }`}
        >
          {value.charAt(0).toUpperCase() + value.slice(1)}
        </span>
      ),
    },
  ];

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50">
        <LoadingSpinner fullScreen />
      </div>
    );
  }

  if (!dismissError && error) {
    return (
      <div className="min-h-screen bg-gray-50 p-6">
        <ErrorAlert
          title="Failed to load portfolios"
          message={error.message}
          onDismiss={() => setDismissError(true)}
          statusCode={500}
        />
      </div>
    );
  }

  return (
    <div className="bg-gray-50 py-8">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        {/* Page Title */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Portfolios</h1>
          <p className="mt-2 text-gray-600">Manage and analyze all portfolios</p>
        </div>

        {/* Filters */}
        <div className="mb-6 grid grid-cols-1 gap-4 rounded-lg border border-gray-200 bg-white p-6 md:grid-cols-4">
          {/* Search */}
          <div>
            <label className="block text-sm font-medium text-gray-700">Search</label>
            <div className="mt-1 relative">
              <Search className="absolute left-3 top-3 h-5 w-5 text-gray-400" />
              <input
                type="text"
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                onKeyDown={(e) => {
                  // Apply search when user presses Enter
                  if (e.key === 'Enter') {
                    e.preventDefault();
                    setAppliedSearch(search);
                  }
                }}
                placeholder="Portfolio name or ID"
                className="w-full rounded-md border border-gray-300 py-2 pl-10 pr-4 text-sm focus:border-primary-500 focus:outline-none"
              />
            </div>
          </div>

          {/* Risk Profile Filter */}
          <div>
            <label className="block text-sm font-medium text-gray-700">Risk Profile</label>
            <select
              value={riskFilter}
              onChange={(e) => setRiskFilter(e.target.value)}
              className="mt-1 w-full rounded-md border border-gray-300 py-2 px-4 text-sm focus:border-primary-500 focus:outline-none"
            >
              <option value="">All</option>
              <option value="low">Low</option>
              <option value="medium">Medium</option>
              <option value="high">High</option>
            </select>
          </div>

          {/* Status Filter */}
          <div>
            <label className="block text-sm font-medium text-gray-700">Status</label>
            <select
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
              className="mt-1 w-full rounded-md border border-gray-300 py-2 px-4 text-sm focus:border-primary-500 focus:outline-none"
            >
              <option value="">All</option>
              <option value="active">Active</option>
              <option value="inactive">Inactive</option>
            </select>
          </div>

          {/* Clear Filters */}
          <div className="flex items-end">
            <button
              onClick={() => {
                setSearch('');
                setRiskFilter('');
                setStatusFilter('');
                setAppliedSearch('');
              }}
              className="w-full rounded-md border border-gray-300 bg-white py-2 px-4 text-sm font-medium text-gray-700 hover:bg-gray-50"
            >
              Clear Filters
            </button>
          </div>
        </div>

        {/* Table */}
        {portfolios && portfolios.length > 0 ? (
          <div className="rounded-lg bg-white shadow-sm">
            <DataTable
              columns={columns}
              data={portfolios}
              rowKey="id"
              onRowClick={(portfolio) => navigate(`/portfolios/${portfolio.id}`)}
            />
          </div>
        ) : (
          <EmptyState
            title="No portfolios found"
            description="Try adjusting your filters or add a new portfolio."
          />
        )}
      </div>
    </div>
  );
};
