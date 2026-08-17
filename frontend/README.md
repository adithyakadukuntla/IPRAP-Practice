# Investment Portfolio Risk & Analytics Platform - Frontend

A professional React/TypeScript web application for investment portfolio analytics, featuring real-time portfolio tracking, risk analysis, performance monitoring, and asset allocation visualization.

## Features

### 📊 Dashboard
- **KPI Cards** - Real-time portfolio metrics
- **Visual Charts** - Portfolio value, risk profiles, performance trends
- **Quick Insights** - At-a-glance view of key metrics

### 💼 Portfolio Management
- **Portfolio List** - Searchable, filterable portfolio listing
- **Advanced Filters** - By risk profile, status, type
- **Portfolio Detail** - Comprehensive overview with performance

### 📈 Analytics Screens
- **Holdings** - Security holdings with pricing and allocation
- **Allocation** - Multi-dimensional breakdown (sector, security, country)
- **Performance** - Historical tracking with charts
- **Risk** - Risk metrics, concentration analysis, visual indicators

### 🎨 User Experience
- **Responsive Design** - Desktop, tablet, and mobile optimized
- **Loading States** - Smooth spinners and skeleton screens
- **Error Handling** - User-friendly messages
- **Accessibility** - Semantic HTML and keyboard navigation

## Tech Stack

- React 18+ with TypeScript
- Vite (build tool)
- Tailwind CSS (styling)
- React Router v6 (routing)
- Axios (HTTP client)
- Recharts (charts)
- Lucide React (icons)
- date-fns (date formatting)

## Installation

### Prerequisites
- Node.js 20+ LTS
- npm or yarn

### Setup

```bash
# Install dependencies
npm install

# Create environment file
cp .env.example .env

# Edit .env to set your API URL
# VITE_API_BASE_URL=http://localhost:8000/api/v1
```

## Running the Application

```bash
# Development server
npm run dev

# Production build
npm run build

# Preview production build
npm run preview

# Lint code
npm run lint
```

The dev server runs at `http://localhost:5173/`

## Environment Configuration

```env
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

## Project Structure

```
src/
├── app/                 # Application shell and routing
├── components/          # Reusable React components
│   ├── layout/         # Header, Footer
│   ├── common/         # Shared components
│   ├── portfolio/      # Portfolio components
│   ├── holdings/       # Holdings components
│   ├── allocation/     # Allocation components
│   ├── performance/    # Performance components
│   └── risk/          # Risk components
├── pages/              # Page components (one per route)
├── services/           # API and data services
│   ├── api/           # API client and endpoints
│   └── mock/          # Mock data
├── types/              # TypeScript definitions
├── hooks/              # Custom React hooks
├── utils/              # Utility functions
└── styles/             # Global styles
```

## Routes

- `/` - Dashboard with KPIs and charts
- `/portfolios` - Portfolio list with filtering
- `/portfolios/:id` - Portfolio detail
- `/portfolios/:id/holdings` - Portfolio holdings
- `/portfolios/:id/allocation` - Asset allocation
- `/portfolios/:id/performance` - Historical performance
- `/portfolios/:id/risk` - Risk analysis
- `/404` - Not found page

## Mock Data

The application uses mock data by default for development. Switch to real APIs by modifying `USE_MOCK_API` in API service files.

## API Integration

The application consumes REST APIs following this contract:

```
GET    /api/v1/portfolios
GET    /api/v1/portfolios/{id}
GET    /api/v1/portfolios/{id}/holdings
GET    /api/v1/portfolios/{id}/allocation?dimension=sector
GET    /api/v1/portfolios/{id}/performance
GET    /api/v1/portfolios/{id}/risk
GET    /api/v1/clients/{id}/portfolios
```

## Key Components

### Common Components
- `LoadingSpinner` - Loading indicator
- `ErrorAlert` - Error messages
- `KPICard` - Key metric cards
- `RiskBadge` - Risk level indicators
- `EmptyState` - Empty data states
- `DataTable` - Sortable data table

### Utility Functions
- `formatCurrency()` - Currency formatting
- `formatNumber()` - Number formatting
- `formatPercentage()` - Percentage formatting
- `formatDate()` - Date formatting
- `getRiskBgColor()` - Risk color utilities
- `getRiskTextColor()` - Risk text colors

## Performance Features

- Code splitting with React Router
- Lazy route loading
- Efficient state management
- Optimized chart rendering
- Memoization of expensive computations

## Accessibility

- Semantic HTML structure
- ARIA labels and roles
- Keyboard navigation support
- WCAG AA color contrast
- Focus management
- Meaningful alt text

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Common Issues

**Charts not rendering?**
- Ensure Recharts is installed: `npm install recharts`
- Check that CSS is properly imported

**API errors?**
- Verify `VITE_API_BASE_URL` in `.env`
- Check that backend server is running
- Enable mock mode by setting `USE_MOCK_API = true`

**Styles not applying?**
- Rebuild: `npm run dev`
- Check that Tailwind CSS is configured
- Clear node_modules: `rm -rf node_modules && npm install`

## Future Enhancements

- Real-time data updates (WebSocket)
- User authentication
- Portfolio comparison
- Custom alerts
- Export to PDF/Excel
- Dark mode
- Advanced analytics
- E2E testing

## Development Tips

1. **Mock Data**: Edit `src/services/mock/mockData.ts` for test scenarios
2. **Components**: Build reusable components in `src/components/common/`
3. **API**: Update services in `src/services/api/` when backend is ready
4. **Styling**: Use Tailwind CSS and theme from `tailwind.config.js`
5. **Types**: Keep TypeScript types in `src/types/` updated

## Deployment

### Production Build
```bash
npm run build
# Outputs to dist/ directory
```

### Docker
```dockerfile
FROM node:20-alpine as build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM node:20-alpine
WORKDIR /app
RUN npm install -g serve
COPY --from=build /app/dist ./dist
EXPOSE 3000
CMD ["serve", "-s", "dist", "-l", "3000"]
```

## Testing

Testing infrastructure setup (Vitest + React Testing Library) to be added.

## License

Part of the Investment Portfolio Risk & Analytics Platform capstone project.

---

**Version**: 1.0.0  
**Status**: Development (Mock Data Enabled)  
**Last Updated**: 2026-08-13
