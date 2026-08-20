import React from 'react';

export const Footer: React.FC = () => {
  return (
    <footer className="border-t border-slate-200 bg-slate-950 text-slate-200">
      <div className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
        <div className="flex flex-col items-center justify-between gap-5 md:flex-row">
          <div className="text-sm text-slate-300">
            © 2026 <span className="font-semibold text-white">IPRAP</span> Investment Portfolio Risk & Analytics Platform.
          </div>
          <div className="flex flex-wrap items-center justify-center gap-5 text-sm text-slate-300">
            <a href="#" className="transition hover:text-white">Privacy Policy</a>
            <a href="#" className="transition hover:text-white">Terms of Service</a>
            <a href="#" className="transition hover:text-white">Contact</a>
          </div>
          <div className="rounded-full border border-blue-400/30 bg-blue-500/10 px-3 py-1 text-[0.65rem] font-semibold uppercase tracking-[0.2em] text-blue-100">
            v1.0.0
          </div>
        </div>
      </div>
    </footer>
  );
};
