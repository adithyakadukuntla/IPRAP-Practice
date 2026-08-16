# API Data Contract - Snowflake Analytics Views

## Views Available

### V_PORTFOLIO_SUMMARY
**Grain:** One row per portfolio
**Key:** PORTFOLIO_ID
**Purpose:** Portfolio summary with value, return, and risk attributes

| Column | Type | Description |
|--------|------|-------------|
| PORTFOLIO_ID | VARCHAR(20) | Unique portfolio identifier |
| CLIENT_ID | VARCHAR(20) | Owner client identifier |
| PORTFOLIO_NAME | VARCHAR(200) | Portfolio name |
| PORTFOLIO_TYPE | VARCHAR(50) | Portfolio type |
| BASE_CURRENCY | VARCHAR(10) | Currency |
| RISK_PROFILE | VARCHAR(20) | Risk profile |
| INITIAL_VALUE | NUMBER(18,2) | Starting value |
| CURRENT_VALUE | NUMBER(18,2) | Current value |
| RETURN_AMOUNT | NUMBER(18,2) | Return amount |
| RETURN_PERCENT | NUMBER(12,4) | Return percentage |
| TOTAL_MARKET_VALUE | NUMBER(18,2) | Total market value |
| HOLDING_COUNT | NUMBER | Number of holdings |

### V_PORTFOLIO_HOLDINGS
**Grain:** One row per holding
**Key:** HOLDING_ID
**Purpose:** Portfolio holdings with security details

### V_PORTFOLIO_ALLOCATION
**Grain:** One row per security per portfolio
**Purpose:** Security, sector, and geographic allocation percentages

### V_PORTFOLIO_PERFORMANCE
**Grain:** One row per performance record
**Purpose:** Historical portfolio performance

### V_PORTFOLIO_RISK
**Grain:** One row per portfolio
**Purpose:** Risk indicators including concentration risk

### V_CLIENT_PORTFOLIO_SUMMARY
**Grain:** One row per client
**Purpose:** Client-level portfolio summary