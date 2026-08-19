# IPRAP Test Execution Guide - Participant 8

## Overview
Comprehensive test suite for Investment Portfolio Risk & Analytics Platform (IPRAP) covering:
- API Contract & Endpoint Validation
- Data Reconciliation & Quality
- Security Validation
- Performance Baselines
- Negative/Error Scenarios

## Test Framework Setup

### 1. Install Dependencies
```powershell
cd C:\Users\Administrator\Desktop\IPRAP-Practice
pip install -r tests/requirements.txt
```

### 2. Configure Environment
Create `.env` file in `tests/` directory:
```env
API_BASE_URL=http://localhost:8000
AUTH_TOKEN=your-test-token-here
SNOWFLAKE_ACCOUNT=your-account
SNOWFLAKE_USER=your-user
SNOWFLAKE_PASSWORD=your-password
SNOWFLAKE_DATABASE=IPRAP_DEV
SNOWFLAKE_SCHEMA=PUBLIC
```

## Test Suite Structure

### API Tests (tests/automation/api/)
| Test File | Test IDs | Coverage |
|-----------|----------|----------|
| test_api_health.py | TC-API-001 | Health check, response schema |
| test_api_contract.py | TC-API-002 to TC-API-006 | Portfolio retrieval, 404s, pagination |
| test_api_holdings.py | TC-API-007 to TC-API-011 | Holdings endpoints, cost basis |
| test_api_risk.py | TC-API-012 to TC-API-016 | Risk metrics, dimensions, HIGH/LOW portfolios |
| test_api_performance.py | TC-API-017 to TC-API-021 | Performance metrics, history, calculations |
| test_api_allocation.py | TC-API-022 to TC-API-026 | Allocation breakdown, grouping, validation |
| test_api_dashboard.py | TC-API-027 to TC-API-031 | KPIs, filtering, sorting, consistency |
| test_negative_scenarios.py | TC-API-032 to TC-API-038 | Invalid inputs, edge cases, error handling |
| test_security.py | TC-SEC-001 to TC-SEC-008 | Auth, credentials, stack traces, CORS |
| test_performance.py | TC-PERF-001 to TC-PERF-007 | Latency baselines, p50, p95 |

### Data Tests (tests/automation/data/)
| Test File | Test IDs | Coverage |
|-----------|----------|----------|
| test_data_reconciliation.py | TC-DATA-001 to TC-DATA-005 | Portfolio count, AUM, holdings, allocation |
| test_data_quality.py | TC-DATA-006 to TC-DATA-010 | Nulls, negatives, dates, duplicates, risk levels |

## Execution Commands

### Quick Start (Smoke Tests)
```powershell
# Run health check only
pytest tests/automation/api/test_api_health.py -v

# Run data quality checks
pytest tests/automation/data/test_data_quality.py -v
```

### Run All API Tests
```powershell
pytest tests/automation/api/ -v --tb=short
```

### Run All Data Tests
```powershell
pytest tests/automation/data/ -v --tb=short
```

### Run All Tests with Coverage
```powershell
pytest tests/ -v --cov=tests --cov-report=html
```

### Run Specific Test Suite
```powershell
# API health checks
pytest tests/automation/api/test_api_health.py -v

# Portfolio contract tests
pytest tests/automation/api/test_api_contract.py -v

# Data reconciliation
pytest tests/automation/data/test_data_reconciliation.py -v

# Security validation
pytest tests/automation/api/test_security.py -v

# Performance baselines
pytest tests/automation/api/test_performance.py -v
```

### Run by Test ID
```powershell
# Run specific test by ID
pytest -k "TC_API_001" -v

# Run all API tests
pytest -k "TC_API" -v

# Run all data tests
pytest -k "TC_DATA" -v

# Run all security tests
pytest -k "TC_SEC" -v

# Run all performance tests
pytest -k "TC_PERF" -v
```

### Run by Marker
```powershell
# Smoke tests
pytest -m smoke -v

# Security validation
pytest -m security -v

# Performance tests
pytest -m performance -v
```

### Generate Reports
```powershell
# HTML report
pytest tests/ -v --html=tests/reports/report.html --self-contained-html

# JUnit XML report
pytest tests/ -v --junit-xml=tests/reports/junit.xml

# Coverage report
pytest tests/ -v --cov=tests --cov-report=html:tests/reports/coverage
```

### Run Test Runner Script
```powershell
# Run all test suites
python tests/run_tests.py

# Run specific test file
python tests/run_tests.py tests/automation/api/test_api_health.py
```

## Test Data

### Test Portfolio Configuration (tests/test-cases/test_data.json)
- **P10001** (Growth, HIGH risk): 4 holdings - AAPL concentrated
- **P10002** (Balanced, MEDIUM risk): 1 holding - diversified
- **P10003** (Conservative, LOW risk): 1 holding - bonds only
- **P10004** (Growth, HIGH risk): 1 holding - single security
- **P10005** (Growth, LOW risk): 0 holdings - empty portfolio

### Securities
- AAPL (Equity, Technology): $200/share
- MSFT (Equity, Technology): $450/share
- JPM (Equity, Financials): $180/share
- US10Y (Bond, Fixed Income): $100/share

## Test Execution Checklist

### Pre-Execution
- [ ] API server running on `http://localhost:8000`
- [ ] Test database seeded with test data
- [ ] `.env` configured with correct credentials
- [ ] Dependencies installed: `pip install -r tests/requirements.txt`

### API Tests
```powershell
# Phase 1: Smoke Tests
pytest tests/automation/api/test_api_health.py -v
pytest tests/automation/api/test_api_contract.py -v

# Phase 2: Core Functionality
pytest tests/automation/api/test_api_holdings.py -v
pytest tests/automation/api/test_api_risk.py -v
pytest tests/automation/api/test_api_performance.py -v
pytest tests/automation/api/test_api_allocation.py -v
pytest tests/automation/api/test_api_dashboard.py -v

# Phase 3: Error Handling & Security
pytest tests/automation/api/test_negative_scenarios.py -v
pytest tests/automation/api/test_security.py -v

# Phase 4: Performance
pytest tests/automation/api/test_performance.py -v
```

### Data Tests
```powershell
# Phase 1: Data Quality
pytest tests/automation/data/test_data_quality.py -v

# Phase 2: Reconciliation
pytest tests/automation/data/test_data_reconciliation.py -v
```

## Test Results Interpretation

### Pass Criteria
- HTTP status codes match expected values
- Response schemas contain all required fields
- Data calculations are accurate (tolerance: $1.00 for AUM, 0.01% for percentages)
- API response times meet p50 thresholds (health: <100ms, portfolio: <500ms)
- No null values in required fields
- No duplicate primary keys
- Allocation percentages sum to 100% (±0.1%)

### Failure Handling
1. **API Failures**: Check server logs, verify endpoints are implemented
2. **Data Failures**: Validate test data loaded correctly, check Snowflake connection
3. **Performance Failures**: Check server load, database query performance
4. **Security Failures**: Review configuration, check authentication implementation

## Coverage Summary

### Test Types Implemented
- **Functional Tests**: 35 test cases (portfolio, holdings, risk, performance, allocation)
- **API Contract Tests**: 15 test cases (schemas, status codes, pagination)
- **Data Reconciliation Tests**: 5 test cases (count, value, calculations)
- **Data Quality Tests**: 5 test cases (nulls, negatives, formats, duplicates)
- **Security Tests**: 8 test cases (auth, credentials, errors, CORS)
- **Performance Tests**: 7 test cases (p50, p95 baselines)
- **Negative/Error Tests**: 7 test cases (invalid inputs, edge cases)

**Total: 82 test cases across all categories**

## Continuous Integration

### GitHub Actions Setup
See `.github/workflows/test.yml` for CI/CD pipeline configuration.

Run tests automatically on:
- Pull requests to main/dev branches
- Commits to dev branch
- Manual workflow dispatch

### Quality Gates
- ✓ All tests must pass
- ✓ Code coverage ≥ 80%
- ✓ No performance regressions
- ✓ Security checks pass

## Troubleshooting

### Common Issues

**ImportError: No module named 'tests'**
```powershell
# Add current directory to PYTHONPATH
$env:PYTHONPATH = "."
pytest tests/
```

**Connection refused to localhost:8000**
```powershell
# Ensure API server is running
# Update API_BASE_URL in .env if using different port
```

**Snowflake connection fails**
```powershell
# Verify credentials in .env
# Test connection: python -c "from snowflake.connector import connect; connect(...)"
```

**Performance tests fail with high latency**
- Check system load and available resources
- May be normal in dev environment
- Establish baseline before regression testing

## Next Steps

1. **Execute Smoke Tests**: Verify basic connectivity and health
2. **Run API Tests**: Validate all endpoints and contracts
3. **Run Data Tests**: Verify reconciliation and quality
4. **Generate Reports**: Review coverage and results
5. **Fix Defects**: Log failures in defect tracking system
6. **Document Evidence**: Capture screenshots/logs for traceability

## Related Documentation

- [Participant 8 PDF](./docs/Participant_08_Requirements.pdf) - Full requirements (47 sections)
- [Test Case Matrix](./tests/requirements/traceability-matrix.csv) - REQ to TC mapping
- [API Documentation](./docs/API_SPEC.md) - Endpoint specifications
- [Test Reports](./tests/reports/) - Execution results and artifacts

---
**Version**: 1.0  
**Last Updated**: 2026-08-18  
**Status**: Ready for Execution
