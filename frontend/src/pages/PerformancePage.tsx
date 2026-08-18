import React, { useState, useCallback } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useAsync } from '../hooks/useAsync';
import { performanceApi } from '../services/api/performanceApi';
import { portfolioApi } from '../services/api/portfolioApi';
import { LoadingSpinner } from '../components/common/LoadingSpinner';
import { ErrorAlert } from '../components/common/ErrorAlert';
import { EmptyState } from '../components/common/EmptyState';
import { formatCurrency, formatPercentage, formatDate } from '../utils/formatters';
import {
  Line,
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  ComposedChart,
} from 'recharts';
import { ArrowLeft } from 'lucide-react';

export const PerformancePage: React.FC = () => {
  const { portfolioId } = useParams<{ portfolioId: string }>();
  const navigate = useNavigate();
  const [dismissError, setDismissError] = useState(false);

  const fetchPortfolio = useCallback(
    () => portfolioApi.getPortfolio(portfolioId || ''),
    [portfolioId]
  );

  const fetchPerformance = useCallback(
    () => performanceApi.getPerformance(portfolioId || ''),
    [portfolioId]
  );

  const { data: portfolio } = useAsync(fetchPortfolio, !!portfolioId);
  const { data: performance, loading, error } = useAsync(fetchPerformance, !!portfolioId);

  if (loading) {
    return <LoadingSpinner fullScreen />;
  }

  if (!dismissError && error) {
    return (
      <div className="min-h-screen bg-gray-50 p-6">
        <ErrorAlert
          title="Failed to load performance data"
          message={error.message}
          onDismiss={() => setDismissError(true)}
          statusCode={500}
        />
      </div>
    );
  }

  const latestData = performance && performance.length > 0 ? performance[performance.length - 1] : null;
  const earliestData = performance && performance.length > 0 ? performance[0] : null;

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
            <h1 className="text-3xl font-bold text-gray-900">Performance</h1>
            <p className="mt-2 text-gray-600">{portfolio?.name}</p>
          </div>
        </div>

        {/* Performance Summary Cards */}
        {latestData && earliestData && (
          <div className="mb-6 grid grid-cols-1 gap-4 md:grid-cols-3">
            <div className="rounded-lg border border-gray-200 bg-white p-6 shadow-sm">
              <p className="text-sm font-medium text-gray-600">Beginning Value</p>
              <p className="mt-2 text-3xl font-bold text-gray-900">
                {formatCurrency(earliestData.portfolioValue, portfolio?.baseCurrency)}
              </p>
            </div>
            <div className="rounded-lg border border-gray-200 bg-white p-6 shadow-sm">
              <p className="text-sm font-medium text-gray-600">Ending Value</p>
              <p className="mt-2 text-3xl font-bold text-gray-900">
                {formatCurrency(latestData.portfolioValue, portfolio?.baseCurrency)}
              </p>
            </div>
            <div className="rounded-lg border border-gray-200 bg-white p-6 shadow-sm">
              <p className="text-sm font-medium text-gray-600">Total Return</p>
              <p
                className={`mt-2 text-3xl font-bold ${
                  latestData.returnPercentage >= 0 ? 'text-green-600' : 'text-red-600'
                }`}
              >
                {formatPercentage(latestData.returnPercentage)}
              </p>
            </div>
          </div>
        )}

        {/* Charts */}
        {performance && performance.length > 0 ? (
          <>
            {/* Portfolio Value Chart */}
            <div className="mb-6 rounded-lg border border-gray-200 bg-white p-6 shadow-sm">
              <h3 className="mb-4 text-lg font-semibold text-gray-900">Portfolio Value Over Time</h3>
              <ResponsiveContainer width="100%" height={400}>
                <AreaChart data={performance}>
                  <defs>
                    <linearGradient id="colorValue" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#0ea5e9" stopOpacity={0.8} />
                      <stop offset="95%" stopColor="#0ea5e9" stopOpacity={0} />
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="date" />
                  <YAxis />
                  <Tooltip
                    formatter={(value) => formatCurrency(value as number, portfolio?.baseCurrency)}
                    labelFormatter={(label) => formatDate(String(label))}
                  />
                  <Area
                    type="monotone"
                    dataKey="portfolioValue"
                    stroke="#0ea5e9"
                    fillOpacity={1}
                    fill="url(#colorValue)"
                    name="Portfolio Value"
                  />
                </AreaChart>
              </ResponsiveContainer>
            </div>

            {/* Combined Chart: Value and Return */}
            <div className="rounded-lg border border-gray-200 bg-white p-6 shadow-sm">
              <h3 className="mb-4 text-lg font-semibold text-gray-900">Value & Return Performance</h3>
              <ResponsiveContainer width="100%" height={400}>
                <ComposedChart data={performance}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="date" />
                  <YAxis yAxisId="left" />
                  <YAxis yAxisId="right" orientation="right" />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: '#ffffff',
                      border: '1px solid #e5e7eb',
                      borderRadius: '0.5rem',
                    }}
                    formatter={(value, name) => {
                      const seriesName = String(name || '').toLowerCase();
                      // If the series name includes 'value' treat it as currency
                      if (seriesName.includes('value')) {
                        return [formatCurrency(value as number, portfolio?.baseCurrency), 'Value'];
                      }
                      // Otherwise show percentage for returns
                      return [`${(value as number).toFixed(2)}%`, 'Return %'];
                    }}
                    labelFormatter={(label) => formatDate(String(label))}
                  />
                  <Legend />
                  <Line
                    yAxisId="left"
                    type="monotone"
                    dataKey="portfolioValue"
                    stroke="#0ea5e9"
                    strokeWidth={2}
                    dot={false}
                    name="Portfolio Value"
                  />
                  <Line
                    yAxisId="right"
                    type="monotone"
                    dataKey="returnPercentage"
                    stroke="#10b981"
                    strokeWidth={2}
                    dot={false}
                    name="Return %"
                  />
                </ComposedChart>
              </ResponsiveContainer>
            </div>
          </>
        ) : (
          <EmptyState
            title="No performance data available"
            description="There is no historical performance data for this portfolio."
          />
        )}
      </div>
    </div>
  );
};
