# Investment Portfolio Risk & Analytics Platform

## Participant 3 - Snowflake Data Engineering

### Overview
This module builds the trusted enterprise data layer in Snowflake for the Investment Portfolio Risk & Analytics Platform.

### Responsibilities
- Create Snowflake database (IPRA_DB) with RAW, STAGING, CORE, ANALYTICS schemas
- Create staging tables for data loading
- Create CORE tables (CLIENT, PORTFOLIO, SECURITY, HOLDING, PERFORMANCE)
- Load clean data from Participant 2 into Snowflake
- Create analytics views for downstream consumers
- Provide API data contract to Participant 4

### Setup

#### Prerequisites
- Snowflake account
- Python 3.8+
- Clean data from Participant 2

#### Environment Setup
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

#### Snowflake Connection
Create .env file with:
SNOWFLAKE_ACCOUNT=HCOOYHA-DS63251
SNOWFLAKE_USER=KATTABHAVANA
SNOWFLAKE_PASSWORD=Password@010405
SNOWFLAKE_WAREHOUSE=COMPUTE_WH
SNOWFLAKE_DATABASE=IPRA_DB
SNOWFLAKE_SCHEMA=CORE
SNOWFLAKE_ROLE=ACCOUNTADMIN

### Data Model

#### CORE Tables
- CLIENT - Client master data
- PORTFOLIO - Portfolio master data
- SECURITY - Security master data
- HOLDING - Portfolio security positions
- PORTFOLIO_PERFORMANCE - Historical portfolio performance

#### STAGING Tables
- CLIENT_STAGE - Staging for client data
- PORTFOLIO_STAGE - Staging for portfolio data
- SECURITY_STAGE - Staging for security data
- HOLDING_STAGE - Staging for holding data
- PERFORMANCE_STAGE - Staging for performance data

### Analytics Views
- V_PORTFOLIO_SUMMARY - Portfolio summary with value, return, risk (One row per portfolio)
- V_PORTFOLIO_HOLDINGS - Portfolio holdings with security details (One row per holding)
- V_PORTFOLIO_ALLOCATION - Security, sector, geographic allocation (One row per security per portfolio)
- V_PORTFOLIO_PERFORMANCE - Historical performance (One row per performance record)
- V_PORTFOLIO_RISK - Risk indicators with concentration (One row per portfolio)
- V_CLIENT_PORTFOLIO_SUMMARY - Client-level portfolio summary (One row per client)

### Data Loading
python scripts/load_data.py

### Handoff to Participant 4
All analytics views are available in IPRA_DB.ANALYTICS schema.

Snowflake Account: HCOOYHA-DS63251

### SQL Scripts
All SQL scripts are organized in sql/ folder:
- sql/ddl/ - Database and table creation
- sql/staging/ - Staging table creation
- sql/transformations/ - MERGE scripts
- sql/analytics/ - Analytics views
- sql/validation/ - Validation queries

### Testing
Run validation queries from sql/validation/ folder to verify data quality.

### Git Branch
feature/participant-03-snowflake

### Related Work
- Upstream: Participant 2 - Data Quality & Standardization
- Downstream: Participant 4 - REST API / MuleSoft Integration