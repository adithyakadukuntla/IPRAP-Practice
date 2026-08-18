# QUICK START: Run All Tests

## Prerequisites
```powershell
cd C:\Users\Administrator\Desktop\IPRAP-Practice

# Install dependencies
pip install -r tests/requirements.txt
```

## Run All Tests (Recommended)
```powershell
pytest tests/ -v --tb=short --html=tests/reports/report.html
```

## Run by Category

### API Tests (Primary)
```powershell
pytest tests/automation/api/ -v
```

### Data Quality & Reconciliation
```powershell
pytest tests/automation/data/ -v
```

### UI Tests (Requires React running on :3000)
```powershell
pytest tests/automation/ui/ -v -m asyncio
```

## Run Specific Test Suites
```powershell
# Health check
pytest tests/automation/api/test_api_health.py -v

# Portfolio operations
pytest tests/automation/api/test_api_contract.py -v

# Holdings
pytest tests/automation/api/test_api_holdings.py -v

# Risk metrics
pytest tests/automation/api/test_api_risk.py -v

# Performance data
pytest tests/automation/api/test_api_performance.py -v

# Allocation breakdown
pytest tests/automation/api/test_api_allocation.py -v

# Dashboard KPIs
pytest tests/automation/api/test_api_dashboard.py -v

# Security validation
pytest tests/automation/api/test_security.py -v

# Error handling
pytest tests/automation/api/test_negative_scenarios.py -v

# Performance baselines
pytest tests/automation/api/test_performance.py -v

# Data reconciliation
pytest tests/automation/data/test_data_reconciliation.py -v

# Data quality
pytest tests/automation/data/test_data_quality.py -v
```

## View Reports
```powershell
# Open HTML report (after test run)
start tests/reports/report.html

# View coverage
start tests/reports/coverage/index.html
```

## Test Summary
- **82 total test cases** across all categories
- **API Tests**: 38 test cases (health, contract, holdings, risk, performance, allocation, dashboard, error, security)
- **Data Tests**: 10 test cases (reconciliation, quality)
- **UI Tests**: 8 test cases (navigation, search, detail, charts, dashboard)
- **Performance Tests**: 7 test cases (latency baselines)

## Expected Outcomes
✓ All endpoints responding correctly  
✓ Data reconciliation passing  
✓ No security vulnerabilities  
✓ Performance within baselines  
✓ 80%+ code coverage  

---
**Status**: Ready to Execute  
**Version**: 1.0
