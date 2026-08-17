import React from 'react';
import { getRiskBgColor, getRiskTextColor } from '../../utils/formatters';

interface RiskBadgeProps {
  level: 'low' | 'medium' | 'high';
  className?: string;
}

export const RiskBadge: React.FC<RiskBadgeProps> = ({ level, className = '' }) => {
  const bgColor = getRiskBgColor(level);
  const textColor = getRiskTextColor(level);

  const label = level.charAt(0).toUpperCase() + level.slice(1);

  return (
    <span
      className={`inline-flex items-center rounded-full px-3 py-1 text-sm font-medium ${bgColor} ${textColor} ${className}`}
    >
      {label}
    </span>
  );
};
