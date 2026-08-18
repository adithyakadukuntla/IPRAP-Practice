# Participant 2 → Participant 3
# Snowflake Data Handoff Contract

## 1. Purpose

This document defines the contract between Participant 2
(Data Quality, Validation & Standardization) and Participant 3
(Snowflake Data Engineering).

Participant 2 receives raw source data from Participant 1,
validates and standardizes it, separates trusted and rejected
records, and provides trusted datasets for Snowflake loading.

---

# 2. Input

Source:

Participant 1 — Data Ingestion

Location:

`data/raw/`

Datasets:

- clients
- portfolios
- securities
- holdings
- portfolio_performance

The raw source data is never modified by Participant 2.

---

# 3. Processing

Participant 2 performs:

1. Data loading
2. Data profiling
3. Schema validation
4. Data-type validation
5. Null validation
6. Duplicate detection
7. Domain validation
8. Business-rule validation
9. Referential-integrity validation
10. Standardization
11. Record-level acceptance/rejection
12. Quality scoring
13. Exception reporting

---

# 4. Trusted Output

Participant 3 should consume only the trusted datasets.

Location:

`data/processed/`

Files:

- clients/clients_clean.csv
- portfolios/portfolios_clean.csv
- securities/securities_clean.csv
- holdings/holdings_clean.csv
- portfolio_performance/portfolio_performance_clean.csv

These files contain records that passed the configured validation
rules.

Controlled values and formatting may have been standardized.

---

# 5. Rejected Output

Location:

`data/rejected/`

Files:

- clients/clients_rejected.csv
- portfolios/portfolios_rejected.csv
- securities/securities_rejected.csv
- holdings/holdings_rejected.csv
- portfolio_performance/portfolio_performance_rejected.csv

Rejected records must not be loaded as trusted Snowflake data.

They are retained for investigation and remediation.

---

# 6. Record-Level Contract

## VALID

A record without an ERROR is accepted.

Flow:

VALID
↓
standardization
↓
processed/

## INVALID

A record containing an ERROR is rejected.

Flow:

INVALID
↓
rejected/

The source record is preserved.

---

# 7. Quality Reports

Location:

`data/quality_reports/`

Required artifacts:

- data_profile.csv
- validation_errors.csv
- data_quality_summary.csv

---

# 8. Validation Error Contract

`validation_errors.csv`

Columns:

- dataset_name
- record_identifier
- row_index
- column_name
- rule_id
- severity
- error_message

The `rule_id` identifies the validation rule that generated the
exception.

---

# 9. Quality Summary Contract

`data_quality_summary.csv`

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

Quality score:

valid_records / total_records × 100

---

# 10. Dataset Dependency Order

Referential integrity follows:

clients
↓
portfolios
↓
securities
↓
holdings
↓
portfolio_performance

Portfolio records reference clients.

Holdings reference portfolios and securities.

Portfolio performance records reference portfolios.

---

# 11. Snowflake Loading Recommendation

Participant 3 should load trusted files from:

`data/processed/`

Rejected files should remain outside the trusted Snowflake
loading path unless required for an exception/audit workflow.

---

# 12. Data Lineage

Source:

Participant 1 raw data

↓

Participant 2 validation

↓

Participant 2 standardization

↓

Trusted / rejected separation

↓

Participant 3 Snowflake

The raw source remains unchanged.

---

# 13. Current Handoff Status

Current validation execution:

- clients: 50 valid / 50 total
- portfolios: 100 valid / 100 total
- securities: 120 valid / 120 total
- holdings: 600 valid / 600 total
- portfolio_performance: 1200 valid / 1200 total

Current quality status:

`EXCELLENT`

Current validation errors:

`0`

Current rejected records:

`0`

---

# 14. Consumer Responsibility

Participant 3 can consume the trusted datasets without requiring
knowledge of Participant 2's internal Python implementation.

Participant 3 should rely on:

- trusted datasets for Snowflake loading
- rejected datasets for exception investigation
- validation_errors.csv for validation traceability
- data_quality_summary.csv for quality status
- data_profile.csv for source-data characteristics

---

# 15. Contract Summary

Participant 2 guarantees:

1. Raw data is not modified.
2. Trusted records are separated from rejected records.
3. Validation failures are documented.
4. Validation severity is assigned.
5. Rule IDs provide traceability.
6. Trusted datasets are standardized.
7. Quality reports are generated.
8. The trusted output is ready for downstream consumption.