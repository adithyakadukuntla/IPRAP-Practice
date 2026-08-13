Participant 1 — Data Ingestion & Source Data Engineering
1. Objective

Build a reusable Python ingestion layer that collects investment data from CSV files and REST APIs, performs basic source-level checks, preserves raw data, records metadata/logs, handles failures/retries, and hands data to Participant 2.

Flow:
Source → CSV/REST API → Python Ingestion → Basic Checks → Raw Data → Metadata/Logs → Participant 2

2. Responsibilities
Synthetic source-data generation
CSV and REST API ingestion
JSON parsing
File/header/empty-input checks
API timeout, HTTP-error handling, and limited retry
Raw-data preservation
Ingestion metadata and logging
Main ingestion entry point
Unit tests
Documentation
Git branch, commits, PR, and handoff

Not responsible for: detailed business/data-quality validation owned by Participant 2.

3. Required Synthetic Datasets
Dataset	Source	Minimum
Clients	CSV	50+
Portfolios	CSV	100+
Securities	REST API/JSON	100+
Holdings	CSV	500+
Portfolio Performance	CSV	1,000+
Required Fields

Clients
client_id, client_name, client_type, country, risk_profile, created_date, status

Portfolios
portfolio_id, client_id, portfolio_name, portfolio_type, base_currency, risk_profile, initial_value, current_value, inception_date, status

Securities
security_id, ticker_symbol, security_name, security_type, sector, country, currency, current_price, status

Holdings
holding_id, portfolio_id, security_id, quantity, purchase_price, current_price, market_value, as_of_date

Portfolio Performance
performance_id, portfolio_id, as_of_date, beginning_value, ending_value, return_amount, return_percent

4. Relationships

Maintain valid IDs:

Client → Portfolio → Holding → Security

Portfolio → Performance

Generate data in this order:

Clients
Portfolios using valid client IDs
Securities
Holdings using valid portfolio/security IDs
Performance using valid portfolio IDs

Use realistic synthetic data only. Make generation reproducible where possible (random.seed(42)).

5. Environment Setup
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install pandas requests python-dotenv pytest
pip freeze > requirements.txt

6. Configuration

Store configurable values in .env:

SECURITY_API_URL=<provided-api-url>


Load with:

import os
from dotenv import load_dotenv

load_dotenv()
SECURITY_API_URL = os.getenv("SECURITY_API_URL")


Never hardcode API URLs or commit .env, credentials, or secrets.

7. CSV Ingestion

Create one reusable CSV ingestion engine rather than separate duplicated implementations.

Workflow:

File Exists → Readable → Non-empty → Read CSV → Check Headers → Parse → Count → Preserve Raw → Log

Handle:

Missing file → FAILED
Empty file → FAILED
Missing required header → FAILED
Malformed CSV → FAILED + logged error

Only perform structural/source-level checks; detailed business validation belongs to Participant 2.

8. REST API Ingestion

Securities must demonstrate REST API ingestion.

Workflow:

API Request → HTTP Status Check → JSON Parse → Structure Check → Preserve Raw Response → Metadata

API URL must come from environment configuration.

Always use a timeout:

requests.get(url, timeout=30)

HTTP Handling
Status	Action
200	Parse
400, 401, 403, 404	Fail + log
408, 429	Retry
500, 502, 503, 504	Retry

Do not assume every response is valid JSON. Invalid JSON must result in FAILED and be logged.

Retry

Retry only transient failures, with a maximum of 3 attempts. Never retry indefinitely.

9. Raw Data Preservation

Preserve the original source before transformation:

SOURCE → RAW → PROCESSING → PROCESSED

Do not modify source values before saving the raw copy. Participant 2 may need the raw data for quality validation.

10. Ingestion Logging

Every run must record:

run_id
dataset_name
source_type
source_name
start_time
end_time
records_read
status
error_message


Example statuses: SUCCESS, FAILED.

11. Main Ingestion

Create one entry point for all five datasets:

MAIN
 ├── Clients CSV
 ├── Portfolios CSV
 ├── Securities REST API
 ├── Holdings CSV
 └── Portfolio Performance CSV
        ↓
   Ingestion Summary


Run:

python -m python.ingestion.main


A partial failure must not hide other results; failed datasets must be logged and reported.

12. Unit Tests
CSV
Valid CSV
Valid headers/records
Correct record count
Missing file
Empty file
Missing header
Malformed CSV
REST API
HTTP 200
Valid JSON
Expected structure
HTTP 404/500
Timeout
Invalid JSON
Retry behavior

Run:

pytest -v

13. Documentation

Document:

Data sources, formats, fields, and expected record counts
Ingestion architecture
Execution instructions
Error handling/retry
Troubleshooting
Raw-data location
Handoff/access instructions for Participant 2
14. Git Workflow

Branch:

git checkout -b feature/participant-01-data-ingestion


Do not develop directly on main.

Suggested commits:

git add .
git commit -m "feat: create data ingestion setup"

git add .
git commit -m "feat: generate synthetic investment data"

git add .
git commit -m "feat: add reusable csv ingestion"

git add .
git commit -m "feat: add security api ingestion"

git add .
git commit -m "feat: add ingestion logging"

git add .
git commit -m "feat: add error handling and retry"

git add .
git commit -m "test: add ingestion unit tests"

git add .
git commit -m "docs: add participant 1 documentation"


Before pushing:

git status


Ensure .env, .venv/, __pycache__/, and secrets are not committed.

Push:

git push -u origin feature/participant-01-data-ingestion


Create a PR to main describing implementation, testing, successful/failed ingestion evidence, and limitations. Obtain code review before merging.

15. Final Demo

Demonstrate:

All five synthetic datasets and relationships.
Complete ingestion:
python -m python.ingestion.main

CSV ingestion success.
REST API + JSON ingestion.
Raw-data preservation.
Failure handling, e.g. missing CSV or invalid API URL.
Ingestion log with run ID, timestamps, record count, status, and errors.
Unit tests:
pytest -v

Git branch, commits, and PR.
16. Acceptance Checklist
Source Data
 50+ clients
 100+ portfolios
 100+ securities
 500+ holdings
 1,000+ performance records
 Relationships maintained
 Synthetic data only
Ingestion
 Reusable CSV ingestion
 REST API ingestion
 JSON parsing
 Required-header checks
 Empty/missing-file handling
 API error handling
 Timeout handling
 Limited retry
 Raw-data preservation
Logging
 Unique run ID
 Start/end time
 Dataset/source
 Record count
 Status
 Error message
Testing
 CSV positive/negative tests
 API positive/negative tests
 Retry tests
 All tests pass
Git & Documentation
 Feature branch
 Meaningful commits
 No secrets committed
 Branch pushed
 PR created/reviewed
 Data sources documented
 Troubleshooting documented
 Handoff documented
17. Definition of Done
SOURCE DATA
    ↓
CSV + REST API
    ↓
PYTHON INGESTION
    ↓
BASIC INGESTION CHECKS
    ↓
RAW DATA PRESERVED
    ↓
LOGGING + METADATA
    ↓
ERROR HANDLING + RETRY
    ↓
UNIT TESTS
    ↓
DOCUMENTATION
    ↓
GIT FEATURE BRANCH
    ↓
PULL REQUEST
    ↓
CODE REVIEW
    ↓
HANDOFF TO PARTICIPANT 2


Participant 2 must know where the data is, its format and fields, how ingestion runs, what succeeded/failed, and how to access the ingested data.

18. Final Commands
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python <data-generation-script>
python -m python.ingestion.main
pytest -v
git status
git branch
git log --oneline
git push -u origin feature/participant-01-data-ingestion