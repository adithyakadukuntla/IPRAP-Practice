import { format, parseISO } from 'date-fns';

export const formatCurrency = (value: number, currency: string = 'USD'): string => {
  const formatter = new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: currency,
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  });
  return formatter.format(value);
};

export const formatNumber = (value: number): string => {
  return new Intl.NumberFormat('en-US', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(value);
};

export const formatPercentage = (value: number): string => {
  return `${value.toFixed(2)}%`;
};

export const formatDate = (dateString: string): string => {
  try {
    const date = parseISO(dateString);
    return format(date, 'dd MMM yyyy');
  } catch {
    return dateString;
  }
};

export const formatDatetime = (dateString: string): string => {
  try {
    const date = parseISO(dateString);
    return format(date, 'dd MMM yyyy HH:mm');
  } catch {
    return dateString;
  }
};

export const getStatusColor = (status: string): string => {
  switch (status.toLowerCase()) {
    case 'low':
      return 'text-success';
    case 'medium':
      return 'text-warning';
    case 'high':
      return 'text-danger';
    case 'active':
      return 'text-success';
    case 'inactive':
      return 'text-secondary-500';
    default:
      return 'text-secondary-600';
  }
};

export const getRiskBgColor = (risk: string): string => {
  switch (risk.toLowerCase()) {
    case 'low':
      return 'bg-green-100';
    case 'medium':
      return 'bg-yellow-100';
    case 'high':
      return 'bg-red-100';
    default:
      return 'bg-gray-100';
  }
};

export const getRiskTextColor = (risk: string): string => {
  switch (risk.toLowerCase()) {
    case 'low':
      return 'text-green-700';
    case 'medium':
      return 'text-yellow-700';
    case 'high':
      return 'text-red-700';
    default:
      return 'text-gray-700';
  }
};
