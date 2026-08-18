import React from 'react';
import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import Layout from './Layout';
import { DashboardPage } from '../pages/DashboardPage';
import { PortfolioListPage } from '../pages/PortfolioListPage';
import { PortfolioDetailPage } from '../pages/PortfolioDetailPage';
import { HoldingsPage } from '../pages/HoldingsPage';
import { AllocationPage } from '../pages/AllocationPage';
import { PerformancePage } from '../pages/PerformancePage';
import { RiskPage } from '../pages/RiskPage';
import { NotFoundPage } from '../pages/NotFoundPage';
import { ClientsPage } from '../pages/ClientsPage';
import { ClientPortfoliosPage } from '../pages/ClientPortfoliosPage';

const router = createBrowserRouter([
  {
    path: '/',
    element: <Layout />,
    errorElement: <NotFoundPage />,
    children: [
      {
        index: true,
        element: <DashboardPage />,
      },
      {
        path: 'portfolios',
        element: <PortfolioListPage />,
      },
      {
        path: 'portfolios/:portfolioId',
        element: <PortfolioDetailPage />,
      },
      {
        path: 'portfolios/:portfolioId/holdings',
        element: <HoldingsPage />,
      },
      {
        path: 'portfolios/:portfolioId/allocation',
        element: <AllocationPage />,
      },
      {
        path: 'portfolios/:portfolioId/performance',
        element: <PerformancePage />,
      },
      {
        path: 'portfolios/:portfolioId/risk',
        element: <RiskPage />,
      },
      {
        path: 'clients',
        element: <ClientsPage />,
      },
      {
        path: 'clients/:clientId/portfolios',
        element: <ClientPortfoliosPage />,
      },
      {
        path: '*',
        element: <NotFoundPage />,
      },
    ],
  },
]);

export const App: React.FC = () => {
  return <RouterProvider router={router} />;
};

export default App;
