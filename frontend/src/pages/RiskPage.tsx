import React, { useState, useCallback } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useAsync } from '../hooks/useAsync';
import { riskApi } from '../services/api/riskApi';
import { portfolioApi } from '../services/api/portfolioApi';
import { LoadingSpinner } from '../components/common/LoadingSpinner';
import { ErrorAlert } from '../components/common/ErrorAlert';
import { RiskBadge } from '../components/common/RiskBadge';
import { formatPercentage } from '../utils/formatters';
import { Gauge, AlertTriangle, TrendingUp } from 'lucide-react';
import { ArrowLeft } from 'lucide-react';
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip } from 'recharts';

export const RiskPage: React.FC = () => {
  const { portfolioId } = useParams<{ portfolioId: string }>();
  const navigate = useNavigate();
  const [dismissError, setDismissError] = useState(false);

  const fetchPortfolio = useCallback(
    () => portfolioApi.getPortfolio(portfolioId || ''),
    [portfolioId]
  );

  const fetchRisk = useCallback(
    () => riskApi.getRisk(portfolioId || ''),
    [portfolioId]
  );

  const { data: portfolio } = useAsync(fetchPortfolio, !!portfolioId);
  const { data: riskData, loading, error } = useAsync(fetchRisk, !!portfolioId);

  if (loading) {
    return <LoadingSpinner fullScreen />;
  }

  if (!dismissError && error) {
    return (
      <div className="min-h-screen bg-gray-50 p-6">
        <ErrorAlert
          title="Failed to load risk data"
          message={error.message}
          onDismiss={() => setDismissError(true)}
          statusCode={500}
        />
      </div>
    );
  }

  if (!riskData) {
    return (
      <div className="min-h-screen bg-gray-50 p-6">
        <ErrorAlert title="Risk data not found" message="Could not retrieve risk information for this portfolio." statusCode={404} />
      </div>
    );
  }

  const concentrationChartData = [
    { name: 'Highest Position', value: riskData.highestSecurityWeight },
    { name: 'Other Holdings', value: 100 - riskData.highestSecurityWeight },
  ];

  const COLORS = ['#ef4444', '#e5e7eb'];

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
            <p className="text-xs font-semibold uppercase tracking-[0.18em] text-slate-500">Risk</p>
            <h1 className="mt-2 text-3xl font-bold text-slate-900">Risk Analytics</h1>
            <p className="mt-1 text-sm text-slate-500">{portfolio?.name}</p>
          </div>
        </div>

        {/* Risk Status Alert */}
        <div
          className={`glass-card mb-6 rounded-2xl border p-6 ${
            riskData.riskStatus === 'low'
              ? 'border-green-200 bg-green-50'
              : riskData.riskStatus === 'medium'
                ? 'border-yellow-200 bg-yellow-50'
                : 'border-red-200 bg-red-50'
          }`}
        >
          <div className="flex items-start gap-4">
            <AlertTriangle
              className={`h-6 w-6 flex-shrink-0 ${
                riskData.riskStatus === 'low'
                  ? 'text-green-600'
                  : riskData.riskStatus === 'medium'
                    ? 'text-yellow-600'
                    : 'text-red-600'
              }`}
            />
            <div className="flex-1">
              <h3 className={`text-lg font-semibold ${
                riskData.riskStatus === 'low'
                  ? 'text-green-900'
                  : riskData.riskStatus === 'medium'
                    ? 'text-yellow-900'
                    : 'text-red-900'
              }`}>
                {riskData.message}
              </h3>
              <p className={`mt-2 text-sm ${
                riskData.riskStatus === 'low'
                  ? 'text-green-700'
                  : riskData.riskStatus === 'medium'
                    ? 'text-yellow-700'
                    : 'text-red-700'
              }`}>
                This is a project-defined risk analysis. Please consult with your financial advisor for investment decisions.
              </p>
            </div>
          </div>
        </div>

        {/* Risk KPIs */}
        <div className="mb-6 grid grid-cols-1 gap-4 md:grid-cols-4">
          <div className="glass-card rounded-2xl p-6">
            <div className="flex items-center gap-2">
              <Gauge className="h-5 w-5 text-primary-500" />
              <p className="text-sm font-medium text-gray-600">Risk Profile</p>
            </div>
            <p className="mt-3 text-2xl font-bold text-gray-900">{riskData.riskProfile}</p>
            <p className="mt-2">
              <RiskBadge level={riskData.riskStatus} />
            </p>
          </div>

          <div className="rounded-lg border border-gray-200 bg-white p-6 shadow-sm">
            <div className="flex items-center gap-2">
              <TrendingUp className="h-5 w-5 text-warning" />
              <p className="text-sm font-medium text-gray-600">Concentration Risk</p>
            </div>
            <p className="mt-3 text-2xl font-bold text-gray-900">{formatPercentage(riskData.concentrationRisk)}</p>
            <p className="mt-2 text-sm text-gray-600">
              {riskData.concentrationRisk > 20 ? 'High concentration' : riskData.concentrationRisk > 10 ? 'Moderate concentration' : 'Well diversified'}
            </p>
          </div>

          <div className="rounded-lg border border-gray-200 bg-white p-6 shadow-sm">
            <div className="flex items-center gap-2">
              <AlertTriangle className="h-5 w-5 text-danger" />
              <p className="text-sm font-medium text-gray-600">Highest Position</p>
            </div>
            <p className="mt-3 text-2xl font-bold text-gray-900">{formatPercentage(riskData.highestSecurityWeight)}</p>
            <p className="mt-2 text-sm text-gray-600">Single security weight</p>
          </div>

          <div className="glass-card rounded-2xl p-6">
            <p className="text-sm font-medium text-gray-600">Overall Risk Status</p>
            <p className="mt-3">
              <RiskBadge level={riskData.riskStatus} />
            </p>
            <p className="mt-3 text-sm text-gray-600">
              {riskData.riskStatus === 'low'
                ? 'Conservative'
                : riskData.riskStatus === 'medium'
                  ? 'Balanced'
                  : 'Aggressive'}
            </p>
          </div>
        </div>

        {/* Risk Visualization */}
        <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
          {/* Concentration Chart */}
          <div className="glass-card rounded-2xl p-6">
            <h3 className="mb-4 text-lg font-semibold text-gray-900">Portfolio Concentration</h3>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={concentrationChartData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, value }) => `${name}: ${value.toFixed(1)}%`}
                  outerRadius={100}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {concentrationChartData.map((_, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip formatter={(value) => `${(value as number).toFixed(2)}%`} />
              </PieChart>
            </ResponsiveContainer>
          </div>

          {/* Risk Metrics */}
          <div className="glass-card rounded-2xl p-6">
            <h3 className="mb-4 text-lg font-semibold text-gray-900">Risk Metrics Overview</h3>
            <div className="space-y-4">
              <div>
                <div className="flex items-center justify-between">
                  <p className="text-sm font-medium text-gray-600">Portfolio Risk Level</p>
                  <RiskBadge level={riskData.riskStatus} />
                </div>
                <div className="mt-2 h-2 w-full rounded-full bg-gray-200">
                  <div
                    className={`h-2 rounded-full ${
                      riskData.riskStatus === 'low'
                        ? 'bg-green-500'
                        : riskData.riskStatus === 'medium'
                          ? 'bg-yellow-500'
                          : 'bg-red-500'
                    }`}
                    style={{
                      width: riskData.riskStatus === 'low' ? '33%' : riskData.riskStatus === 'medium' ? '66%' : '100%',
                    }}
                  />
                </div>
              </div>

              <div>
                <p className="text-sm font-medium text-gray-600">Concentration Risk</p>
                <div className="mt-2 h-2 w-full rounded-full bg-gray-200">
                  <div
                    className={`h-2 rounded-full ${
                      riskData.concentrationRisk < 10
                        ? 'bg-green-500'
                        : riskData.concentrationRisk < 20
                          ? 'bg-yellow-500'
                          : 'bg-red-500'
                    }`}
                    style={{
                      width: `${Math.min(riskData.concentrationRisk * 5, 100)}%`,
                    }}
                  />
                </div>
                <p className="mt-1 text-xs text-gray-500">{formatPercentage(riskData.concentrationRisk)}</p>
              </div>

              <div>
                <p className="text-sm font-medium text-gray-600">Top Position Weight</p>
                <div className="mt-2 h-2 w-full rounded-full bg-gray-200">
                  <div
                    className={`h-2 rounded-full ${
                      riskData.highestSecurityWeight < 20
                        ? 'bg-green-500'
                        : riskData.highestSecurityWeight < 35
                          ? 'bg-yellow-500'
                          : 'bg-red-500'
                    }`}
                    style={{
                      width: `${riskData.highestSecurityWeight}%`,
                    }}
                  />
                </div>
                <p className="mt-1 text-xs text-gray-500">{formatPercentage(riskData.highestSecurityWeight)}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
