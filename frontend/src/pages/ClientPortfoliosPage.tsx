// import React, { useEffect, useState } from 'react';
// import { useParams, Link } from 'react-router-dom';
// import { portfolioApi } from '../services/api/portfolioApi';
// import type { Portfolio } from '../types';

// export const ClientPortfoliosPage: React.FC = () => {
//   const { clientId } = useParams();
//   const [portfolios, setPortfolios] = useState<Portfolio[] | null>(null);
//   const [loading, setLoading] = useState(true);
//   const [error, setError] = useState<string | null>(null);

//   useEffect(() => {
//     if (!clientId) return;
//     let mounted = true;
//     setLoading(true);
//     portfolioApi
//       .getPortfolios({ page: 1, page_size: 100, client_id: clientId })
//       .then((data) => mounted && setPortfolios(data))
//       .catch((err) => mounted && setError(err?.message || 'Failed to load'))
//       .finally(() => mounted && setLoading(false));

//     return () => {
//       mounted = false;
//     };
//   }, [clientId]);

//   if (loading) return <div className="p-6">Loading portfolios…</div>;
//   if (error) return <div className="p-6 text-red-600">{error}</div>;
//   if (!portfolios || portfolios.length === 0)
//     return <div className="p-6">No portfolios available for this client.</div>;

//   return (
//     <div className="p-6">
//       <h1 className="text-2xl font-semibold mb-4">Client Portfolios</h1>
//       <ul className="space-y-2">
//         {portfolios.map((p) => (
//           <li key={p.id} className="border rounded p-3">
//             <div className="flex items-center justify-between">
//               <div>
//                 <div className="font-medium">{p.name}</div>
//                 <div className="text-sm text-gray-500">{p.id}</div>
//               </div>
//               <div>
//                 <Link to={`/portfolios/${p.id}`} className="text-primary-600 hover:underline">
//                   View details
//                 </Link>
//               </div>
//             </div>
//           </li>
//         ))}
//       </ul>
//     </div>
//   );
// };

// export default ClientPortfoliosPage;




import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { portfolioApi } from '../services/api/portfolioApi';
import type { Portfolio } from '../types';

export const ClientPortfoliosPage: React.FC = () => {
  const { clientId } = useParams<{ clientId: string }>();

  const [portfolios, setPortfolios] = useState<Portfolio[] | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!clientId) {
      setError('Client ID is missing');
      setLoading(false);
      return;
    }

    let mounted = true;

    setLoading(true);
    setError(null);

    portfolioApi
      .getPortfolios({
        page: 1,
        limit: 100,
      })
      .then((data) => {
        if (!mounted) return;

        const clientPortfolios = data.filter(
          (portfolio) => portfolio.clientId === clientId
        );

        setPortfolios(clientPortfolios);
      })
      .catch((err) => {
        if (!mounted) return;

        setError(err?.message || 'Failed to load portfolios');
      })
      .finally(() => {
        if (!mounted) return;

        setLoading(false);
      });

    return () => {
      mounted = false;
    };
  }, [clientId]);

  if (loading) {
    return <div className="p-6">Loading portfolios…</div>;
  }

  if (error) {
    return <div className="p-6 text-red-600">{error}</div>;
  }

  if (!portfolios || portfolios.length === 0) {
    return (
      <div className="p-6">
        No portfolios available for this client.
      </div>
    );
  }

  return (
    <div className="p-6">
      <h1 className="text-2xl font-semibold mb-4">
        Client Portfolios
      </h1>

      <ul className="space-y-2">
        {portfolios.map((portfolio) => (
          <li
            key={portfolio.id}
            className="border rounded p-3"
          >
            <div className="flex items-center justify-between">
              <div>
                <div className="font-medium">
                  {portfolio.name}
                </div>

                <div className="text-sm text-gray-500">
                  {portfolio.id}
                </div>
              </div>

              <div>
                <Link
                  to={`/portfolios/${portfolio.id}`}
                  className="text-primary-600 hover:underline"
                >
                  View details
                </Link>
              </div>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default ClientPortfoliosPage;