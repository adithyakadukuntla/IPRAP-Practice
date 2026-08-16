# API Data Contract - Snowflake Analytics Views

Database: IPRA_DB
Schema: ANALYTICS

---

## 1. V_PORTFOLIO_SUMMARY

Grain: One row per portfolio
Key: PORTFOLIO_ID

Columns:
- PORTFOLIO_ID (VARCHAR(20)) - Unique portfolio identifier
- CLIENT_ID (VARCHAR(20)) - Owner client identifier
- PORTFOLIO_NAME (VARCHAR(200)) - Portfolio name
- PORTFOLIO_TYPE (VARCHAR(50)) - Portfolio type
- BASE_CURRENCY (VARCHAR(10)) - Currency
- RISK_PROFILE (VARCHAR(20)) - Risk profile
- INITIAL_VALUE (NUMBER(18,2)) - Starting value
- CURRENT_VALUE (NUMBER(18,2)) - Current value
- RETURN_AMOUNT (NUMBER(18,2)) - Return amount
- RETURN_PERCENT (NUMBER(12,4)) - Return percentage
- TOTAL_MARKET_VALUE (NUMBER(18,2)) - Total market value
- HOLDING_COUNT (NUMBER) - Number of holdings

---

## 2. V_PORTFOLIO_HOLDINGS

Grain: One row per holding
Key: HOLDING_ID

Columns:
- HOLDING_ID (VARCHAR(30)) - Unique holding identifier
- PORTFOLIO_ID (VARCHAR(20)) - Portfolio identifier
- SECURITY_ID (VARCHAR(20)) - Security identifier
- TICKER_SYMBOL (VARCHAR(30)) - Security ticker
- SECURITY_NAME (VARCHAR(200)) - Security name
- SECURITY_TYPE (VARCHAR(30)) - EQUITY, BOND, ETF
- SECTOR (VARCHAR(100)) - Industry sector
- SECURITY_COUNTRY (VARCHAR(10)) - Security country
- QUANTITY (NUMBER(20,4)) - Number of units held
- PURCHASE_PRICE (NUMBER(18,4)) - Original purchase price
- CURRENT_PRICE (NUMBER(18,4)) - Current market price
- MARKET_VALUE (NUMBER(18,2)) - Current holding value
- AS_OF_DATE (DATE) - Valuation date

---

## 3. V_PORTFOLIO_ALLOCATION

Grain: One row per security per portfolio

Columns:
- PORTFOLIO_ID (VARCHAR(20)) - Portfolio identifier
- SECURITY_ID (VARCHAR(20)) - Security identifier
- SECURITY_NAME (VARCHAR(200)) - Security name
- SECTOR (VARCHAR(100)) - Industry sector
- SECURITY_COUNTRY (VARCHAR(10)) - Security country
- SECURITY_MARKET_VALUE (NUMBER(18,2)) - Security market value
- SECURITY_ALLOCATION_PERCENT (NUMBER(10,2)) - Security allocation %
- SECTOR_ALLOCATION_PERCENT (NUMBER(10,2)) - Sector allocation %
- COUNTRY_ALLOCATION_PERCENT (NUMBER(10,2)) - Geographic allocation %
- PORTFOLIO_TOTAL_VALUE (NUMBER(18,2)) - Total portfolio value

---

## 4. V_PORTFOLIO_PERFORMANCE

Grain: One row per performance record

Columns:
- PERFORMANCE_ID (VARCHAR(30)) - Unique performance identifier
- PORTFOLIO_ID (VARCHAR(20)) - Portfolio identifier
- AS_OF_DATE (DATE) - Performance measurement date
- BEGINNING_VALUE (NUMBER(18,2)) - Value at period start
- ENDING_VALUE (NUMBER(18,2)) - Value at period end
- RETURN_AMOUNT (NUMBER(18,2)) - Gain/loss amount
- RETURN_PERCENT (NUMBER(12,4)) - Return percentage
- PREVIOUS_VALUE (NUMBER(18,2)) - Previous period value
- PERIOD_OVER_PERIOD_RETURN (NUMBER(12,4)) - Period-over-period return %

---

## 5. V_PORTFOLIO_RISK

Grain: One row per portfolio

Columns:
- PORTFOLIO_ID (VARCHAR(20)) - Portfolio identifier
- CLIENT_ID (VARCHAR(20)) - Client identifier
- PORTFOLIO_NAME (VARCHAR(200)) - Portfolio name
- PORTFOLIO_RISK_PROFILE (VARCHAR(20)) - Portfolio risk profile
- HIGHEST_HOLDING_SECURITY_ID (VARCHAR(20)) - Highest weight security
- HIGHEST_HOLDING_VALUE (NUMBER(18,2)) - Highest holding value
- HIGHEST_WEIGHT_PERCENT (NUMBER(10,2)) - Highest security weight %
- CONCENTRATION_RISK (VARCHAR(10)) - HIGH (>40%), MEDIUM (>25%), LOW
- RISK_STATUS (VARCHAR(10)) - CRITICAL, REVIEW, NORMAL
- RISK_EXPLANATION (VARCHAR(500)) - Human-readable risk explanation

Risk Rules:
IF highest_security_weight > 40% THEN CONCENTRATION_RISK = HIGH
ELSE IF highest_security_weight > 25% THEN CONCENTRATION_RISK = MEDIUM
ELSE CONCENTRATION_RISK = LOW

---

## 6. V_CLIENT_PORTFOLIO_SUMMARY

Grain: One row per client

Columns:
- CLIENT_ID (VARCHAR(20)) - Client identifier
- CLIENT_NAME (VARCHAR(200)) - Client name
- CLIENT_TYPE (VARCHAR(30)) - INDIVIDUAL, INSTITUTIONAL
- CLIENT_COUNTRY (VARCHAR(10)) - Client country
- CLIENT_RISK_PROFILE (VARCHAR(20)) - Client risk profile
- PORTFOLIO_COUNT (NUMBER) - Number of portfolios
- TOTAL_PORTFOLIO_VALUE (NUMBER(18,2)) - Total portfolio value
- AVERAGE_RETURN_PERCENT (NUMBER(12,4)) - Average return
- HIGH_RISK_PORTFOLIO_COUNT (NUMBER) - Count of HIGH risk portfolios
- MEDIUM_RISK_PORTFOLIO_COUNT (NUMBER) - Count of MEDIUM risk portfolios
- LOW_RISK_PORTFOLIO_COUNT (NUMBER) - Count of LOW risk portfolios

---

## API Endpoint Mapping

GET /api/v1/portfolios - V_PORTFOLIO_SUMMARY
GET /api/v1/portfolios/{id} - V_PORTFOLIO_SUMMARY
GET /api/v1/portfolios/{id}/holdings - V_PORTFOLIO_HOLDINGS
GET /api/v1/portfolios/{id}/allocation - V_PORTFOLIO_ALLOCATION
GET /api/v1/portfolios/{id}/performance - V_PORTFOLIO_PERFORMANCE
GET /api/v1/portfolios/{id}/risk - V_PORTFOLIO_RISK
GET /api/v1/clients/{id}/portfolios - V_CLIENT_PORTFOLIO_SUMMARY

## Connection Details
Snowflake Account: HCOOYHA-DS63251
Database: IPRA_DB
Schema: ANALYTICS