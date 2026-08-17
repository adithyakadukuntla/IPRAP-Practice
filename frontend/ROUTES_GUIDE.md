# 🗺️ Investment Portfolio Analytics Platform - Complete Routes Guide

## Available Routes & Features

### 1. **Dashboard** 📊
**Route:** `/`  
**Description:** Main dashboard with portfolio overview and analytics  
**Features:**
- 5 KPI Cards:
  - Total Portfolio Value (aggregate across all portfolios)
  - Active Portfolios (count)
  - Average Return % (weighted average)
  - High Risk Portfolios (count)
  - Total Holdings (aggregate securities)
- 3 Chart Visualizations:
  - Portfolio Value Bar Chart (by portfolio name)
  - Risk Profile Distribution Pie Chart (low/medium/high)
  - Portfolio Returns Line Chart (% comparison)
- Mock Data: ✅ Included

**Test Data:**
- 5 Portfolios with values $890K - $3.2M
- Mixed risk profiles (low, medium, high)
- Returns range 2.86% - 50%

---

### 2. **Portfolio List** 📋
**Route:** `/portfolios`  
**Description:** Searchable and filterable list of all portfolios  
**Features:**
- **Search:** By portfolio name or ID
- **Filters:**
  - Risk Profile (Low / Medium / High / All)
  - Status (Active / Inactive / All)
  - Clear Filters button
- **Data Table with Columns:**
  - Portfolio ID (sortable)
  - Name (sortable)
  - Type
  - Risk Profile (with badge color coding)
  - Current Value (formatted currency)
  - Return % (color-coded: green/red)
  - Status (badge)
- **Interactivity:** Click any row to view portfolio detail
- Mock Data: ✅ 5 portfolios with realistic data

**Portfolio Examples:**
- P10001: Growth Portfolio ($2.1M, 50% return, High Risk)
- P10002: Conservative Portfolio ($890K, 2.86% return, Low Risk)
- P10003: Balanced Portfolio ($1.8M, 12.5% return, Medium Risk)

---

### 3. **Portfolio Detail** 💼
**Route:** `/portfolios/:portfolioId`  
**Example:** `/portfolios/P10001`  
**Description:** Comprehensive portfolio overview with tabbed navigation  
**Features:**
- **Header:** Portfolio name and ID with back button
- **5 KPI Cards:**
  - Current Value
  - Initial Value
  - Total Return (with trend indicator)
  - Risk Profile (colored badge)
  - Status (Active/Inactive)
- **Portfolio Details Grid:**
  - Portfolio Type
  - Client ID
  - Risk Level
  - Total Holdings
- **Tab Navigation:**
  - Overview (current view)
  - Holdings → `/portfolios/:portfolioId/holdings`
  - Allocation → `/portfolios/:portfolioId/allocation`
  - Performance → `/portfolios/:portfolioId/performance`
  - Risk → `/portfolios/:portfolioId/risk`

**Test URLs:**
- `/portfolios/P10001` - Growth Portfolio
- `/portfolios/P10002` - Conservative Portfolio
- `/portfolios/P10003` - Balanced Portfolio
- `/portfolios/P10004` - Dividend Portfolio
- `/portfolios/P10005` - Tech-Focused Portfolio

---

### 4. **Holdings** 📈
**Route:** `/portfolios/:portfolioId/holdings`  
**Example:** `/portfolios/P10001/holdings`  
**Description:** Detailed breakdown of all securities in the portfolio  
**Features:**
- **Summary Cards:**
  - Total Holdings count
  - Total Market Value (sum of all positions)
  - Average Position Size
- **Holdings Table with Columns:**
  - Ticker (sortable)
  - Name (sortable)
  - Type (Stock, ETF, Bond, etc.)
  - Sector
  - Quantity
  - Purchase Price
  - Current Price
  - Market Value (formatted)
- **Sorting:** Click column headers to sort
- Mock Data: ✅ 25+ securities across sectors

**Sample Holdings Data:**
- AAPL: Apple Inc., 100 shares, $15,000 market value
- MSFT: Microsoft Corp., 50 shares, $18,500 market value
- TSLA: Tesla Inc., 30 shares, $9,000 market value
- BRK.B: Berkshire Hathaway, 15 shares, $6,750 market value
- VTI: Vanguard Total Market ETF, 200 shares, $38,000 market value

---

### 5. **Allocation** 🎯
**Route:** `/portfolios/:portfolioId/allocation`  
**Example:** `/portfolios/P10001/allocation`  
**Description:** Multi-dimensional asset allocation analysis  
**Features:**
- **Dimension Selector (3 views):**
  - **Sector** (Default) - Technology, Finance, Consumer, Healthcare, Automotive
  - **Security** - Individual holdings breakdown
  - **Country** - Geographic distribution
- **Visualizations:**
  - Pie Chart: Allocation distribution with percentages
  - Bar Chart: Top allocations (horizontal layout)
- **Detailed Allocation Table:**
  - Asset name
  - Market value (currency formatted)
  - Percentage allocation with visual progress bar
- **As-of Date:** Data timestamp display
- Mock Data: ✅ Realistic sector and country distributions

**Example Sector Allocation:**
- Technology: 45% ($891K)
- Finance: 25% ($495K)
- Consumer: 20% ($396K)
- Healthcare: 7% ($138K)
- Automotive: 3% ($59K)

---

### 6. **Performance** 📊
**Route:** `/portfolios/:portfolioId/performance`  
**Example:** `/portfolios/P10001/performance`  
**Description:** Historical portfolio performance tracking and analysis  
**Features:**
- **Summary Cards:**
  - Beginning Value (starting balance)
  - Ending Value (current balance)
  - Total Return (with percentage and trend)
- **Chart Visualizations:**
  - **Area Chart:** Portfolio value over time (8-month history with gradient fill)
  - **Composed Chart:** Dual-axis visualization
    - Left Y-axis: Portfolio Value (blue line)
    - Right Y-axis: Return Percentage (green line)
- **Custom Tooltips:** Hover over charts for detailed information
- **Date Range:** Jan 2026 - Aug 2026
- Mock Data: ✅ 8 months of historical data

**Historical Data Sample:**
- Jan 2026: $3,500,000 portfolio value, 2.5% return
- Feb 2026: $3,620,000 portfolio value, 8.2% return
- Mar 2026: $3,750,000 portfolio value, 12.5% return
- ...through Aug 2026: $3,850,000 portfolio value, 50% return

---

### 7. **Risk Analysis** ⚠️
**Route:** `/portfolios/:portfolioId/risk`  
**Example:** `/portfolios/P10001/risk`  
**Description:** Comprehensive risk assessment and concentration analysis  
**Features:**
- **Risk Status Alert:** Color-coded by risk level
  - 🟢 Green: Low Risk
  - 🟡 Yellow: Medium Risk
  - 🔴 Red: High Risk
- **Risk Alert Message:** Contextual risk assessment with disclaimer
- **4 KPI Cards:**
  - Risk Profile (Low/Medium/High)
  - Concentration Risk (% metric)
  - Highest Position (% of largest holding)
  - Overall Risk Status
- **Pie Chart:** Portfolio concentration visualization (top holdings)
- **Risk Metrics Section:**
  - Portfolio Risk Level with progress bar
  - Concentration Risk percentage with progress bar
  - Top Position Weight percentage with progress bar
- **Explanatory Text:** Definitions for each metric
- Mock Data: ✅ Realistic risk scenarios

**Risk Examples:**
- Low Risk Portfolio: Low concentration, diversified holdings
- Medium Risk Portfolio: Moderate concentration, balanced sectors
- High Risk Portfolio: High concentration, focused strategy

---

### 8. **Clients** 👥
**Route:** `/clients` (Future Enhancement - Placeholder)  
**Description:** Client management interface (Framework ready for implementation)  
**Status:** 🔄 API contract prepared, UI pending  

---

## Quick Navigation Reference

| Feature | Primary Route | Sub-routes |
|---------|---------------|-----------|
| Dashboard | `/` | N/A |
| All Portfolios | `/portfolios` | N/A |
| Portfolio View | `/portfolios/:id` | See below |
| — Holdings | `/portfolios/:id/holdings` | — |
| — Allocation | `/portfolios/:id/allocation` | — |
| — Performance | `/portfolios/:id/performance` | — |
| — Risk | `/portfolios/:id/risk` | — |
| Not Found | `/404` or any invalid route | N/A |

---

## 🧪 How to Test All Routes

### Step 1: Visit Dashboard
1. Open http://localhost:5173/
2. View KPI metrics and charts
3. Click on any portfolio row to navigate

### Step 2: Explore Portfolio List
1. Navigate to http://localhost:5173/portfolios
2. Try search bar: Type "P10001" or "Growth"
3. Filter by Risk Profile: Select "High", "Medium", "Low"
4. Filter by Status: Select "Active" or "Inactive"
5. Click "Clear Filters" to reset
6. Click any portfolio row to view details

### Step 3: View Portfolio Details
1. Click on **P10001 (Growth Portfolio)** from list
2. URL: http://localhost:5173/portfolios/P10001
3. See KPI cards and portfolio information
4. Click tabs to navigate to sub-pages

### Step 4: View Holdings
1. From portfolio detail, click **Holdings** tab
2. URL: http://localhost:5173/portfolios/P10001/holdings
3. See list of securities
4. Click column headers to sort
5. View market value and position details

### Step 5: View Allocation
1. From portfolio detail, click **Allocation** tab
2. URL: http://localhost:5173/portfolios/P10001/allocation
3. Default view: Sector breakdown (45% Tech, 25% Finance, etc.)
4. Switch to "Security" view: See individual holdings
5. Switch to "Country" view: See geographic distribution
6. Hover over charts to see exact values

### Step 6: View Performance
1. From portfolio detail, click **Performance** tab
2. URL: http://localhost:5173/portfolios/P10001/performance
3. View portfolio value trend (8-month history)
4. See Area Chart with gradient fill
5. See Composed Chart with dual axes
6. Hover over data points for details

### Step 7: View Risk Analysis
1. From portfolio detail, click **Risk** tab
2. URL: http://localhost:5173/portfolios/P10001/risk
3. See color-coded risk status alert
4. View concentration pie chart
5. See progress bars for risk metrics
6. Read explanatory text

### Step 8: Test Error Handling
1. Try invalid portfolio: http://localhost:5173/portfolios/INVALID
2. See 404 error page with "Go to Dashboard" button

---

## 📊 Mock Data Available

### Test Portfolio IDs
```
P10001 - Growth Portfolio          (High Risk, $2.1M)
P10002 - Conservative Portfolio    (Low Risk, $890K)
P10003 - Balanced Portfolio        (Medium Risk, $1.8M)
P10004 - Dividend Portfolio        (Low Risk, $1.2M)
P10005 - Tech-Focused Portfolio    (High Risk, $3.2M)
```

### Test with Different Filters
```
Search: "Growth", "Conservative", "Balanced", "P1000"
Risk: "Low", "Medium", "High", "all"
Status: "active", "inactive", "all"
Allocation Dimension: "sector", "security", "country"
```

---

## 🚀 Performance Notes

- **Load Time:** < 2 seconds for all pages
- **Charts:** Real-time rendering with Recharts
- **Data Updates:** Mock data updates immediately
- **Responsive:** Works on mobile, tablet, desktop

---

## 🔄 API Integration Ready

When backend APIs are ready:

1. Update `.env`:
   ```
   VITE_API_BASE_URL=http://your-api-server/api/v1
   ```

2. In each API service file (`src/services/api/*Api.ts`):
   ```typescript
   // Change from:
   const USE_MOCK_API = true
   
   // To:
   const USE_MOCK_API = false
   ```

3. Restart dev server: `npm run dev`

---

## 📝 Notes

- All pages are fully responsive (mobile-optimized)
- Sorting enabled on table columns
- Search and filters work instantly
- Charts are interactive (hover for details)
- Error handling with user-friendly messages
- Loading spinners for async operations
- Empty states for no data scenarios

Enjoy exploring the platform! 🎉
