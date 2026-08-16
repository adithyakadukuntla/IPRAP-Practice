# Participant 3 - Snowflake Data Engineering

## Overview
Builds the Snowflake-based enterprise data layer for the Investment Portfolio Risk & Analytics Platform.

## Responsibilities
- Create Snowflake database (IPRA_DB) with RAW, STAGING, CORE, ANALYTICS schemas
- Create staging tables for data loading
- Create CORE tables (CLIENT, PORTFOLIO, SECURITY, HOLDING, PERFORMANCE)
- Load clean data from Participant 2 into Snowflake
- Create analytics views for downstream consumers
- Provide API data contract to Participant 4

## Setup
1. Copy `.env.example` to `.env`
2. Fill in Snowflake credentials
3. Create virtual environment: `python -m venv .venv`
4. Activate: `source .venv/bin/activate`
5. Install dependencies: `pip install -r requirements.txt`

## Git Branch
`feature/participant-03-snowflake`
