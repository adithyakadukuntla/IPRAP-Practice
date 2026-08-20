import React from 'react';
import { Outlet } from 'react-router-dom';
import { Header } from '../components/layout/Header';
import { Footer } from '../components/layout/Footer';

const Layout: React.FC = () => {
  return (
    <div className="flex min-h-screen flex-col bg-transparent text-slate-900">
      <Header />
      <main className="flex-1">
        <div className="mx-auto w-full max-w-[1600px] px-4 py-6 sm:px-6 lg:px-8">
          <Outlet />
        </div>
      </main>
      <Footer />
    </div>
  );
};

export default Layout;
