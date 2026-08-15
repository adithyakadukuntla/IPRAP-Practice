# Participant 2 — Evidence Index

## Data Quality & Validation

| Evidence | Description | Requirement |
|---|---|---|
| E1 | End-to-end pipeline execution | Validation execution |
| E2 | Automated test suite | 25+ meaningful tests |
| E3 | Generated data profile | Data profiling |
| E4 | Data quality summary and scores | Quality scoring |
| E5 | Validation error report | Validation exceptions |
| E6 | Trusted processed datasets | Participant 3 handoff |
| E7 | Rejected datasets | Exception handling |

## Final Test Result

Full automated test suite:

- 265 tests passed
- 0 failures

## Final Data Quality Result

| Dataset | Records | Valid | Invalid | Quality |
|---|---:|---:|---:|---|
| clients | 50 | 50 | 0 | 100% |
| portfolios | 100 | 100 | 0 | 100% |
| securities | 120 | 120 | 0 | 100% |
| holdings | 600 | 600 | 0 | 100% |
| portfolio_performance | 1200 | 1200 | 0 | 100% |

## Handoff Outputs

Trusted:

- `clients_clean.csv`
- `portfolios_clean.csv`
- `securities_clean.csv`
- `holdings_clean.csv`
- `portfolio_performance_clean.csv`

Rejected:

- `clients_rejected.csv`
- `portfolios_rejected.csv`
- `securities_rejected.csv`
- `holdings_rejected.csv`
- `portfolio_performance_rejected.csv`

Quality reports:

- `data_profile.csv`
- `data_quality_summary.csv`
- `validation_errors.csv`