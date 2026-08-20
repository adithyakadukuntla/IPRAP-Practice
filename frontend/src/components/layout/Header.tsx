import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { BarChart3, Menu, ShieldCheck, X } from 'lucide-react';

export const Header: React.FC = () => {
  const [mobileMenuOpen, setMobileMenuOpen] = React.useState(false);
  const location = useLocation();

  const navItems = [
    { label: 'Dashboard', href: '/' },
    { label: 'Portfolios', href: '/portfolios' },
    { label: 'Clients', href: '/clients' },
  ];

  const isActive = (path: string) => {
    if (path === '/') {
      return location.pathname === '/';
    }

    return location.pathname === path || location.pathname.startsWith(`${path}/`);
  };

  return (
    <header className="sticky top-0 z-50 border-b border-slate-200/70 bg-slate-950/90 shadow-[0_12px_30px_rgba(15,23,42,0.18)] backdrop-blur-xl">
      <nav className="mx-auto flex max-w-7xl items-center justify-between px-4 py-4 sm:px-6 lg:px-8">
        <Link to="/" className="flex items-center gap-3">
          <div className="flex h-11 w-11 items-center justify-center rounded-2xl bg-gradient-to-br from-blue-500 via-cyan-400 to-indigo-600 shadow-lg shadow-blue-500/30 ring-2 ring-white/10">
            <BarChart3 className="h-5 w-5 text-white" />
          </div>
          <div className="leading-none">
            <div className="text-[0.7rem] font-semibold uppercase tracking-[0.34em] text-blue-200/90">
              Portfolio
            </div>
            <div className="mt-1 text-xl font-black tracking-tight text-white">IPRAP</div>
          </div>
        </Link>

        <div className="hidden flex-1 items-center justify-center gap-2 md:flex md:pl-10">
          {navItems.map((item) => (
            <Link
              key={item.href}
              to={item.href}
              className={`rounded-full px-4 py-2 text-sm font-semibold transition-all duration-200 ${
                isActive(item.href)
                  ? 'bg-white text-slate-900 shadow-md shadow-slate-900/10'
                  : 'text-slate-200 hover:bg-slate-800 hover:text-white'
              }`}
            >
              {item.label}
            </Link>
          ))}
        </div>

        <div className="hidden items-center gap-3 md:flex">
          <div className="inline-flex items-center gap-2 rounded-full border border-blue-400/30 bg-blue-500/10 px-3 py-2 text-xs font-semibold uppercase tracking-[0.2em] text-blue-100">
            <ShieldCheck className="h-3.5 w-3.5" />
            Secure
          </div>
        </div>

        <button
          onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          className="inline-flex items-center justify-center rounded-xl border border-slate-700 bg-slate-900 p-2 text-slate-200 transition hover:border-slate-500 hover:text-white md:hidden"
          aria-label="Toggle navigation"
        >
          {mobileMenuOpen ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
        </button>
      </nav>

      {mobileMenuOpen && (
        <div className="border-t border-slate-800 bg-slate-950/95 md:hidden">
          <div className="space-y-1 px-3 py-3">
            {navItems.map((item) => (
              <Link
                key={item.href}
                to={item.href}
                className={`block rounded-xl px-3 py-2.5 text-base font-medium ${
                  isActive(item.href)
                    ? 'bg-white text-slate-900'
                    : 'text-slate-200 hover:bg-slate-800 hover:text-white'
                }`}
                onClick={() => setMobileMenuOpen(false)}
              >
                {item.label}
              </Link>
            ))}
          </div>
        </div>
      )}
    </header>
  );
};
