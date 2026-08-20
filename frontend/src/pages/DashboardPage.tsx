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
    <div className="py-6 md:py-8">
      <div className="mx-auto max-w-7xl">
        <div className="mb-8 flex flex-col gap-3 md:flex-row md:items-end md:justify-between">
          <div>
            <p className="text-xs font-semibold uppercase tracking-[0.28em] text-blue-600">Overview</p>
            <h1 className="mt-2 text-4xl font-black tracking-tight text-slate-900">Dashboard</h1>
          </div>
          <div className="rounded-full border border-slate-200 bg-white/80 px-4 py-2 text-sm font-medium text-slate-600 shadow-sm">
            Investment Analytics Platform
          </div>
        </div>

        <div className="mb-8 grid grid-cols-1 gap-4 md:grid-cols-2 xl:grid-cols-5">
          {kpis && (
            <>
              <KPICard
                title="Total Portfolio Value"
                value={formatCurrency(kpis.totalPortfolioValue)}
                icon={DollarSign}
                wide
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

        {portfolios && portfolios.length > 0 ? (
          <div className="grid grid-cols-1 gap-6 xl:grid-cols-2">
            <div className="glass-card rounded-[1.75rem] p-5 md:p-6">
              <div className="mb-4 flex items-center justify-between">
                <h3 className="text-xl font-bold text-slate-900">Portfolio Value</h3>
                <span className="rounded-full bg-blue-50 px-2.5 py-1 text-xs font-semibold uppercase tracking-[0.15em] text-blue-700">
                  Value
                </span>
              </div>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={portfolioValueData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#cbd5e1" vertical={false} />
                  <XAxis dataKey="name" angle={-45} textAnchor="end" height={80} tick={{ fill: '#475569', fontSize: 12 }} />
                  <YAxis tick={{ fill: '#475569', fontSize: 12 }} />
                  <Tooltip formatter={(value) => formatCurrency(value as number)} contentStyle={{ borderRadius: 14, border: '1px solid #dbeafe' }} />
                  <Bar dataKey="value" fill="#2563eb" radius={[10, 10, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>

            <div className="glass-card rounded-[1.75rem] p-5 md:p-6">
              <div className="mb-4 flex items-center justify-between">
                <h3 className="text-xl font-bold text-slate-900">Risk Profile Distribution</h3>
                <span className="rounded-full bg-violet-50 px-2.5 py-1 text-xs font-semibold uppercase tracking-[0.15em] text-violet-700">
                  Mix
                </span>
              </div>
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

            <div className="glass-card rounded-[1.75rem] p-5 md:p-6 xl:col-span-2">
              <div className="mb-4 flex items-center justify-between">
                <h3 className="text-xl font-bold text-slate-900">Portfolio Returns</h3>
                <span className="rounded-full bg-emerald-50 px-2.5 py-1 text-xs font-semibold uppercase tracking-[0.15em] text-emerald-700">
                  Returns
                </span>
              </div>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={returnData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#cbd5e1" vertical={false} />
                  <XAxis dataKey="name" tick={{ fill: '#475569', fontSize: 12 }} />
                  <YAxis tick={{ fill: '#475569', fontSize: 12 }} />
                  <Tooltip formatter={(value) => `${value}%`} contentStyle={{ borderRadius: 14, border: '1px solid #dbeafe' }} />
                  <Legend />
                  <Line
                    type="monotone"
                    dataKey="return"
                    stroke="#0ea5e9"
                    strokeWidth={3}
                    dot={{ fill: '#0ea5e9', r: 4 }}
                    activeDot={{ r: 7 }}
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
