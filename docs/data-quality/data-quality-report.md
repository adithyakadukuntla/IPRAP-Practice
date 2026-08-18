# Data Quality Report

## 1. Report Purpose

This report describes the data-quality outputs produced by
Participant 2.

The framework generates three quality artifacts:

1. data_profile.csv
2. validation_errors.csv
3. data_quality_summary.csv

---

# 2. Data Profile

Location:

`data/quality_reports/data_profile.csv`

The profile describes the incoming datasets and their columns,
including record counts, data types, null information, distinct
values and numeric statistics where applicable.

---

# 3. Validation Errors

Location:

`data/quality_reports/validation_errors.csv`

This report contains record-level validation failures.

Columns:

- dataset_name
- record_identifier
- row_index
- column_name
- rule_id
- severity
- error_message

An empty report with the required columns indicates that the
current input contains no validation failures.

---

# 4. Quality Summary

Location:

`data/quality_reports/data_quality_summary.csv`

Columns:

- dataset_name
- total_records
- valid_records
- invalid_records
- error_count
- warning_count
- quality_score
- quality_status
- validation_timestamp

---

# 5. Quality Score

Quality score:

valid_records / total_records × 100

Classification:

| Score | Status |
|---|---|
| 95–100 | EXCELLENT |
| 90–94.99 | GOOD |
| 80–89.99 | WARNING |
| <80 | POOR |

These thresholds are project-defined.

---

# 6. Current Validation Run

Current source datasets:

| Dataset | Records | Valid | Invalid | Score | Status |
|---|---:|---:|---:|---:|---|
| clients | 50 | 50 | 0 | 100.00% | EXCELLENT |
| portfolios | 100 | 100 | 0 | 100.00% | EXCELLENT |
| securities | 120 | 120 | 0 | 100.00% | EXCELLENT |
| holdings | 600 | 600 | 0 | 100.00% | EXCELLENT |
| portfolio_performance | 1200 | 1200 | 0 | 100.00% | EXCELLENT |

---

# 7. Interpretation

The current Participant 1 source data passed the implemented
validation rules.

No records were rejected during the current execution.

No validation errors were generated.

All five datasets achieved an EXCELLENT quality classification.