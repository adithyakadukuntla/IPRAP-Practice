import React from 'react';
import type { LucideIcon } from 'lucide-react';

interface KPICardProps {
  title: string;
  value: string | number;
  subtitle?: string;
  icon?: LucideIcon;
  trend?: {
    value: number;
    direction: 'up' | 'down';
  };
  onClick?: () => void;
  className?: string;
  wide?: boolean;
}

export const KPICard: React.FC<KPICardProps> = ({
  title,
  value,
  subtitle,
  icon: Icon,
  trend,
  onClick,
  className = '',
  wide = false,
}) => {
  return (
    <div
      onClick={onClick}
      className={`glass-card group min-w-0 rounded-[1.75rem] p-5 transition-all duration-300 hover:-translate-y-1 hover:shadow-[0_28px_45px_-30px_rgba(15,23,42,0.42)] ${
        onClick ? 'cursor-pointer' : ''
      } ${wide ? 'md:col-span-2 xl:col-span-2' : ''} ${className}`}
    >
      <div className="flex min-w-0 items-start justify-between gap-3">
        <div className="min-w-0 flex-1 overflow-hidden">
          <p className="text-sm font-semibold uppercase tracking-[0.14em] text-slate-500">{title}</p>
          <p className="mt-3 min-w-0 break-words text-[clamp(1.5rem,2vw,2.4rem)] font-black leading-none tracking-[-0.06em] text-slate-900">
            {value}
          </p>
          {subtitle && <p className="mt-2 text-sm text-slate-500">{subtitle}</p>}
        </div>

        {Icon && (
          <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-2xl bg-gradient-to-br from-blue-600 to-cyan-500 text-white shadow-lg shadow-blue-500/20">
            <Icon className="h-5 w-5" />
          </div>
        )}
      </div>

      {trend && (
        <div className="mt-4 flex items-center">
          <span
            className={`inline-flex items-center rounded-full px-2.5 py-1 text-xs font-bold ${
              trend.direction === 'up'
                ? 'bg-emerald-100 text-emerald-700'
                : 'bg-red-100 text-red-700'
            }`}
          >
            {trend.direction === 'up' ? '↑' : '↓'} {Math.abs(trend.value).toFixed(2)}%
          </span>
        </div>
      )}
    </div>
  );
};
