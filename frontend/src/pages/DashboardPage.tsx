import React, { useState, useCallback } from 'react';
import { useAsync } from '../hooks/useAsync';
import { portfolioApi } from '../services/api/portfolioApi';
import { LoadingSpinner } from '../components/common/LoadingSpinner';
import { ErrorAlert } from '../components/common/ErrorAlert';
import { KPICard } from '../components/common/KPICard';
import { EmptyState } from '../components/common/EmptyState';
import {
  BarChart,
  Bar,
  LineChart,
  Line,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';
import { formatCurrency, formatPercentage } from '../utils/formatters';
import {
  TrendingUp,
  DollarSign,
  Briefcase,
  AlertTriangle,
  Package,
} from 'lucide-react';

export const DashboardPage: React.FC = () => {
  const [dismissError, setDismissError] = useState(false);

  const fetchKPIs = useCallback(() => portfolioApi.getDashboardKPIs(), []);
  // Request up to 100 portfolios so charts reflect the full set
  const fetchPortfolios = useCallback(() => portfolioApi.getPortfolios({ limit: 100 }), []);

  const { data: kpis, loading: kpisLoading, error: kpisError } = useAsync(fetchKPIs, true);
  const { data: portfolios, loading: portfoliosLoading, error: portfoliosError } = useAsync(
    fetchPortfolios,
    true
  );

  if (kpisLoading || portfoliosLoading) {
    return (
      <div className="min-h-screen bg-gray-50">
        <LoadingSpinner fullScreen />
      </div>
    );
  }

  if (!dismissError && (kpisError || portfoliosError)) {
    return (
      <div className="min-h-screen bg-gray-50 p-6">
        <ErrorAlert
          title="Failed to load dashboard"
          message={kpisError?.message || portfoliosError?.message || 'An error occurred'}
          onDismiss={() => setDismissError(true)}
          statusCode={500}
        />
      </div>
    );
  }

  // Prepare chart data
  const portfolioValueData = portfolios?.map(p => ({
    name: p.name,
    value: p.currentValue,
  })) || [];

  const riskProfileData = portfolios?.reduce((acc, p) => {
    const existing = acc.find(item => item.name === p.riskProfile);
    if (existing) {
      existing.value += 1;
    } else {
      acc.push({ name: p.riskProfile, value: 1 });
    }
    return acc;
  }, [] as { name: string; value: number }[]) || [];

  const returnData = portfolios?.map(p => ({
    name: p.name.substring(0, 10),
    return: parseFloat(p.returnPercentage.toFixed(2)),
  })) || [];

  const COLORS = ['#0ea5e9', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6'];

  return (
    <div className="bg-gray-50 py-8">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        {/* Page Title */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
          <p className="mt-2 text-gray-600">Welcome to the Investment Analytics Platform</p>
        </div>

        {/* KPI Cards */}
        <div className="mb-8 grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-5">
          {kpis && (
            <>
              <KPICard
                title="Total Portfolio Value"
                value={formatCurrency(kpis.totalPortfolioValue)}
                icon={DollarSign}
              />
              <KPICard
                title="Active Portfolios"
                value={kpis.activePortfolios}
                icon={Briefcase}
              />
              <KPICard
                title="Average Return"
                value={formatPercentage(kpis.averageReturn)}
                icon={TrendingUp}
                trend={{ value: kpis.averageReturn, direction: 'up' }}
              />
              <KPICard
                title="High Risk Portfolios"
                value={kpis.highRiskPortfolios}
                icon={AlertTriangle}
              />
              <KPICard
                title="Total Holdings"
                value={kpis.totalHoldings}
                icon={Package}
              />
            </>
          )}
        </div>

        {/* Charts Grid */}
        {portfolios && portfolios.length > 0 ? (
          <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
            {/* Portfolio Value Chart */}
            <div className="rounded-lg border border-gray-200 bg-white p-6 shadow-sm">
              <h3 className="mb-4 text-lg font-semibold text-gray-900">Portfolio Value</h3>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={portfolioValueData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" angle={-45} textAnchor="end" height={80} />
                  <YAxis />
                  <Tooltip formatter={(value) => formatCurrency(value as number)} />
                  <Bar dataKey="value" fill="#0ea5e9" />
                </BarChart>
              </ResponsiveContainer>
            </div>

            {/* Risk Profile Distribution */}
            <div className="rounded-lg border border-gray-200 bg-white p-6 shadow-sm">
              <h3 className="mb-4 text-lg font-semibold text-gray-900">Risk Profile Distribution</h3>
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie
                    data={riskProfileData}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    label={({ name, value }) => `${name}: ${value}`}
                    outerRadius={100}
                    fill="#8884d8"
                    dataKey="value"
                  >
                    {riskProfileData.map((_, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            </div>

            {/* Portfolio Returns */}
            <div className="rounded-lg border border-gray-200 bg-white p-6 shadow-sm lg:col-span-2">
              <h3 className="mb-4 text-lg font-semibold text-gray-900">Portfolio Returns</h3>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={returnData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis />
                  <Tooltip formatter={(value) => `${value}%`} />
                  <Legend />
                  <Line
                    type="monotone"
                    dataKey="return"
                    stroke="#0ea5e9"
                    strokeWidth={2}
                    dot={{ fill: '#0ea5e9' }}
                    name="Return %"
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>
        ) : (
          <EmptyState
            title="No portfolios found"
            description="There are no portfolios to display at the moment."
          />
        )}
      </div>
    </div>
  );
};
