import React from 'react';
import { AlertCircle } from 'lucide-react';

interface ErrorAlertProps {
  title?: string;
  message: string;
  onDismiss?: () => void;
  statusCode?: number;
}

export const ErrorAlert: React.FC<ErrorAlertProps> = ({
  title,
  message,
  onDismiss,
  statusCode,
}) => {
  let displayTitle = title;

  if (!displayTitle && statusCode) {
    switch (statusCode) {
      case 404:
        displayTitle = 'Not Found';
        break;
      case 500:
        displayTitle = 'Server Error';
        break;
      case 503:
        displayTitle = 'Service Unavailable';
        break;
      default:
        displayTitle = 'Error';
    }
  }

  return (
    <div className="rounded-lg bg-red-50 p-4">
      <div className="flex">
        <div className="flex-shrink-0">
          <AlertCircle className="h-5 w-5 text-red-400" />
        </div>
        <div className="ml-3">
          {displayTitle && <h3 className="text-sm font-medium text-red-800">{displayTitle}</h3>}
          <div className="mt-2 text-sm text-red-700">{message}</div>
        </div>
        {onDismiss && (
          <button
            onClick={onDismiss}
            className="ml-auto inline-flex text-red-400 hover:text-red-500"
          >
            <span className="sr-only">Close</span>
            <svg className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
              <path
                fillRule="evenodd"
                d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
                clipRule="evenodd"
              />
            </svg>
          </button>
        )}
      </div>
    </div>
  );
};
