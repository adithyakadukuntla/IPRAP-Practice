# Comprehensive Test Execution Checklist - Participant 8 IPRAP

**Status**: Ready to Execute  
**Total Test Cases**: 82  
**Execution Phases**: 5  
**Estimated Duration**: 30-45 minutes  

---

## PHASE 0: PRE-EXECUTION SETUP (5 minutes)

### ✓ Environment Setup
- [ ] Verify Python 3.9+ installed: `python --version`
- [ ] Navigate to project: `cd C:\Users\Administrator\Desktop\IPRAP-Practice`
- [ ] Create virtual environment (optional): `python -m venv venv` & activate
- [ ] Install dependencies: `pip install -r tests/requirements.txt`
- [ ] Verify pytest installed: `pytest --version`

### ✓ Configuration
- [ ] Create `.env` file in `tests/` with:
  ```env
  API_BASE_URL=http://localhost:8000
  AUTH_TOKEN=test-token-123
  ```
- [ ] Verify test data loaded: Check `tests/test-cases/test_data.json` exists
- [ ] Verify Snowflake connection (if testing data layer)

### ✓ Start Services
- [ ] **API Server**: Start on `http://localhost:8000`
  ```powershell
  cd api
  python main.py
  ```
- [ ] **Frontend** (optional for UI tests): Start on `http://localhost:3000`
  ```powershell
  cd frontend
  npm start
  ```
- [ ] **Database**: Verify Snowflake/mock DB running
- [ ] **Test Reports Directory**: Create `tests/reports/`
  ```powershell
  mkdir -p tests/reports
  ```

---

## PHASE 1: DATA QUALITY BASELINE (5 minutes)

**Objective**: Verify test data integrity before API testing

### Test Suite: Data Quality & Reconciliation
```powershell
pytest tests/automation/data/test_data_quality.py -v --tb=short
```

**Expected Results**:
- [ ] TC-DATA-006: No Null Required Fields - **PASS**
- [ ] TC-DATA-007: No Negative Values - **PASS**
- [ ] TC-DATA-008: Valid Date Format - **PASS**
- [ ] TC-DATA-009: No Duplicate Keys - **PASS**
- [ ] TC-DATA-010: Valid Risk Levels - **PASS**

### Reconciliation Tests
```powershell
pytest tests/automation/data/test_data_reconciliation.py -v --tb=short
```

**Expected Results**:
- [ ] TC-DATA-001: Portfolio Count Reconciliation - **PASS** (5 portfolios)
- [ ] TC-DATA-002: Total AUM Reconciliation - **PASS** ($2,100,000)
- [ ] TC-DATA-003: Holding Count Reconciliation - **PASS** (7 total)
- [ ] TC-DATA-004: Market Value Reconciliation - **PASS** (calculations accurate)
- [ ] TC-DATA-005: Allocation Total = 100% - **PASS**

**If Any Fail**:
- [ ] Check test data in `tests/test-cases/test_data.json`
- [ ] Verify database seeded with test data
- [ ] Review defect log in `defects/defect-log.csv`

---

## PHASE 2: API CORE FUNCTIONALITY (15 minutes)

**Objective**: Validate all critical API endpoints

### 2.1: Health Check (Critical)
```powershell
pytest tests/automation/api/test_api_health.py -v
```

**Expected Results**:
- [ ] TC-API-001: Health Check Endpoint - **PASS** (Status 200)
- [ ] TC-API-001.1: Response Schema Valid - **PASS** (has status, timestamp)
- [ ] TC-API-001.2: Response Time <100ms - **PASS**

**If Failed**: API server not running or not on correct port

### 2.2: Portfolio Endpoints (Critical)
```powershell
pytest tests/automation/api/test_api_contract.py -v
```

**Expected Results**:
- [ ] TC-API-002: Get Portfolio By ID - **PASS** (Status 200, all fields)
- [ ] TC-API-003: Get Unknown Portfolio - **PASS** (Status 404)
- [ ] TC-API-004: List Portfolios - **PASS** (paginated array)
- [ ] TC-API-005: Invalid Page Size - **PASS** (Status 400)
- [ ] TC-API-006: Missing Auth - **PASS** (Status 401)

### 2.3: Holdings Endpoints (Critical)
```powershell
pytest tests/automation/api/test_api_holdings.py -v
```

**Expected Results**:
- [ ] TC-API-007: Get Holdings - **PASS** (4 for P10001)
- [ ] TC-API-008: Holding Details - **PASS** (cost basis validated)
- [ ] TC-API-009: Empty Holdings - **PASS** (P10005 = [])
- [ ] TC-API-010: Invalid Holding ID - **PASS** (Status 404)
- [ ] TC-API-011: Cost Basis - **PASS** (calculation correct)

### 2.4: Risk Endpoints (Critical)
```powershell
pytest tests/automation/api/test_api_risk.py -v
```

**Expected Results**:
- [ ] TC-API-012: Get Risk Metrics - **PASS** (HIGH/MEDIUM/LOW levels)
- [ ] TC-API-013: Risk by Dimension - **PASS** (sector breakdown)
- [ ] TC-API-014: Invalid Dimension - **PASS** (Status 400)
- [ ] TC-API-015: HIGH Risk Portfolio - **PASS** (P10001 identified)
- [ ] TC-API-016: LOW Risk Portfolio - **PASS** (P10003 identified)

### 2.5: Performance Endpoints (Critical)
```powershell
pytest tests/automation/api/test_api_performance.py -v
```

**Expected Results**:
- [ ] TC-API-017: Get Performance - **PASS** (returns, percentages)
- [ ] TC-API-018: Performance History - **PASS** (date range)
- [ ] TC-API-019: Invalid Date - **PASS** (Status 400)
- [ ] TC-API-020: Positive Return - **PASS** (P10001 > 0%)
- [ ] TC-API-021: Return Accuracy - **PASS** (calculation verified)

### 2.6: Allocation Endpoints (Critical)
```powershell
pytest tests/automation/api/test_api_allocation.py -v
```

**Expected Results**:
- [ ] TC-API-022: Get Allocation - **PASS** (sums to 100%)
- [ ] TC-API-023: Allocation by Type - **PASS** (grouping works)
- [ ] TC-API-024: Invalid GroupBy - **PASS** (Status 400)
- [ ] TC-API-025: Allocation = 100% - **PASS** (validation accurate)
- [ ] TC-API-026: Positive Values - **PASS** (no negatives)

### 2.7: Dashboard Endpoints (Critical)
```powershell
pytest tests/automation/api/test_api_dashboard.py -v
```

**Expected Results**:
- [ ] TC-API-027: Dashboard KPIs - **PASS** (total_aum, client_count, etc)
- [ ] TC-API-028: Portfolio Filtering - **PASS** (risk_profile filter works)
- [ ] TC-API-029: Portfolio Sorting - **PASS** (sorted by AUM desc)
- [ ] TC-API-030: KPI Values Positive - **PASS** (all >= 0)
- [ ] TC-API-031: KPI Consistency - **PASS** (portfolio_count matches)

---

## PHASE 3: ERROR HANDLING & SECURITY (10 minutes)

### 3.1: Negative/Error Scenarios
```powershell
pytest tests/automation/api/test_negative_scenarios.py -v
```

**Expected Results**:
- [ ] TC-API-032: Invalid Portfolio ID - **PASS** (Status 400/404)
- [ ] TC-API-033: Null Portfolio ID - **PASS** (Status 400/404)
- [ ] TC-API-034: Invalid Page Size - **PASS** (Status 400)
- [ ] TC-API-035: Negative Page - **PASS** (Status 400)
- [ ] TC-API-036: Invalid Dimension - **PASS** (Status 400)
- [ ] TC-API-037: Missing Param - **PASS** (Status 400 or validated)
- [ ] TC-API-038: Method Not Allowed - **PASS** (Status 405)

### 3.2: Security Validation
```powershell
pytest tests/automation/api/test_security.py -v
```

**Expected Results**:
- [ ] TC-SEC-001: No Credentials in Repo - **PASS** (no passwords found)
- [ ] TC-SEC-002: Auth Required - **PASS** (Status 401 without token)
- [ ] TC-SEC-003: Invalid Token - **PASS** (Status 401/403)
- [ ] TC-SEC-004: No Stack Traces - **PASS** (error messages clean)
- [ ] TC-SEC-005: No Password Logging - **PASS** (config reviewed)
- [ ] TC-SEC-006: CORS Restrictive - **PASS** (not Allow: *)
- [ ] TC-SEC-007: No Exposed Paths - **PASS** (no /home/, /var/www/)
- [ ] TC-SEC-008: HTTPS Enforced - **PASS** (in production)

---

## PHASE 4: PERFORMANCE BASELINE (5 minutes)

### Performance Tests
```powershell
pytest tests/automation/api/test_performance.py -v
```

**Expected Results**:
- [ ] TC-PERF-001: Health <100ms - **PASS** (baseline p50)
- [ ] TC-PERF-002: Get Portfolio <500ms - **PASS** (baseline p50)
- [ ] TC-PERF-003: List Portfolios <1000ms - **PASS** (baseline p50)
- [ ] TC-PERF-004: Get Holdings <700ms - **PASS** (baseline p50)
- [ ] TC-PERF-005: Get Risk <600ms - **PASS** (baseline p50)
- [ ] TC-PERF-006: Dashboard KPIs <800ms - **PASS** (baseline p50)
- [ ] TC-PERF-007: p95 Latency Baseline - **PASS** (recorded)

**Performance Thresholds**:
| Endpoint | p50 Threshold | Status |
|----------|---------------|--------|
| /health | <100ms | |
| /portfolios/{id} | <500ms | |
| /portfolios | <1000ms | |
| /holdings | <700ms | |
| /risk | <600ms | |
| /dashboard/kpis | <800ms | |

---

## PHASE 5: UI TESTS (Optional, 10 minutes)

### UI Navigation Tests (Requires React running on :3000)
```powershell
pytest tests/automation/ui/test_ui_navigation.py -v -m asyncio
```

**Expected Results**:
- [ ] TC-UI-001: Portfolio List Navigation - **PASS** (page loads)
- [ ] TC-UI-002: Portfolio Search - **PASS** (filters working)
- [ ] TC-UI-003: Portfolio Detail - **PASS** (detail view renders)
- [ ] TC-UI-004: Holdings Table - **PASS** (holdings displayed)
- [ ] TC-UI-005: Allocation Chart - **PASS** (chart rendered)
- [ ] TC-UI-006: Performance Chart - **PASS** (chart rendered)
- [ ] TC-UI-007: Risk Indicator - **PASS** (badge shows HIGH/MEDIUM/LOW)
- [ ] TC-UI-008: Dashboard - **PASS** (KPI cards visible)

---

## COMPREHENSIVE RESULTS SUMMARY

### Run All Tests with Reports
```powershell
pytest tests/ -v --cov=tests --cov-report=html --html=tests/reports/report.html --self-contained-html
```

### Review Results
- [ ] Open `tests/reports/report.html` in browser
- [ ] Review code coverage: `tests/reports/coverage/index.html`
- [ ] Check any failures in test output
- [ ] Log defects in `defects/defect-log.csv`

### Test Metrics
```powershell
# Count passing/failing
pytest tests/ -v --tb=no | Select-String "passed|failed|error"

# Generate JUnit report for CI/CD
pytest tests/ --junit-xml=tests/reports/junit.xml
```

---

## POST-EXECUTION CHECKLIST

### ✓ Results Analysis
- [ ] All Phase 1-4 tests passing (minimum 80%)
- [ ] No critical defects found
- [ ] Performance within baselines
- [ ] Security checks passed
- [ ] Data reconciliation accurate

### ✓ Documentation
- [ ] Test execution results saved: `tests/reports/`
- [ ] Defects logged: `defects/defect-log.csv`
- [ ] Evidence attached (screenshots, logs)
- [ ] Traceability maintained: `tests/requirements/traceability-matrix.csv`

### ✓ Next Steps
- [ ] Review failed tests (if any)
- [ ] Assign defects to development team
- [ ] Schedule retest for fixed defects
- [ ] Generate final test report for release decision

---

## QUICK REFERENCE: ALL COMMANDS

```powershell
# Setup
pip install -r tests/requirements.txt

# Phase 1: Data Quality
pytest tests/automation/data/ -v

# Phase 2: API Core
pytest tests/automation/api/test_api_health.py -v
pytest tests/automation/api/test_api_contract.py -v
pytest tests/automation/api/test_api_holdings.py -v
pytest tests/automation/api/test_api_risk.py -v
pytest tests/automation/api/test_api_performance.py -v
pytest tests/automation/api/test_api_allocation.py -v
pytest tests/automation/api/test_api_dashboard.py -v

# Phase 3: Error & Security
pytest tests/automation/api/test_negative_scenarios.py -v
pytest tests/automation/api/test_security.py -v

# Phase 4: Performance
pytest tests/automation/api/test_performance.py -v

# Phase 5: UI (Optional)
pytest tests/automation/ui/ -v -m asyncio

# All Tests with Reports
pytest tests/ -v --cov=tests --html=tests/reports/report.html --self-contained-html

# View Reports
start tests/reports/report.html
```

---

## SUCCESS CRITERIA

✓ **All tests PASS**  
✓ **No Critical defects**  
✓ **Code coverage ≥80%**  
✓ **Performance within baselines**  
✓ **Security validation complete**  
✓ **Full traceability matrix updated**  
✓ **Evidence documented**  

**Release Decision**: **READY FOR RELEASE** ✓

---

**Execution Date**: _______________  
**Executed By**: _______________  
**Results**: _______________  
**Status**: _______________
