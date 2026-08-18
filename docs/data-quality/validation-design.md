# Validation Framework Design

## 1. Overview

Participant 2 implements a reusable Python-based data-quality
framework between Participant 1 ingestion and Participant 3
Snowflake loading.

The framework uses modular validators rather than placing all
validation logic in the main orchestration module.

---

# 2. Architecture

Participant 1
    |
    v
data/raw/
    |
    v
RawDataLoader
    |
    v
DataProfiler
    |
    v
SchemaValidator
    |
    v
TypeValidator
    |
    v
NullValidator
    |
    v
DuplicateValidator
    |
    v
DomainValidator
    |
    v
BusinessValidator
    |
    v
ReferentialValidator
    |
    v
DataStandardizer
    |
    +------------------+
    |                  |
    v                  v
processed/           rejected/
    |
    v
QualityReporter
    |
    v
quality_reports/

---

# 3. Modules

## data_loader.py

Loads the five raw datasets produced by Participant 1.

## profiler.py

Generates dataset and column-level profiling information.

## schema_validator.py

Validates required and unexpected columns.

## type_validator.py

Validates configured data types and malformed values.

## null_validator.py

Checks mandatory fields for null values.

## duplicate_validator.py

Detects duplicate business keys and composite duplicates.

## domain_validator.py

Validates controlled vocabulary and identifier formats.

## business_validator.py

Validates investment-specific business rules.

## referential_validator.py

Validates relationships between datasets.

## standardizer.py

Standardizes accepted records without modifying raw source data.

## rejection_processor.py

Separates valid and invalid records and preserves validation
issues.

## quality_report.py

Calculates quality scores and generates the quality summary.

## main.py

Orchestrates the complete pipeline.

---

# 4. Validation Order

The validation sequence is:

1. Load raw datasets
2. Profile datasets
3. Schema validation
4. Type validation
5. Null validation
6. Duplicate validation
7. Domain validation
8. Business validation
9. Referential integrity
10. Record-level decision
11. Standardization of accepted records
12. Trusted output
13. Rejected output
14. Validation error report
15. Quality scoring
16. Quality summary

---

# 5. Record-Level Decision

For the first implementation:

ERROR
    ↓
INVALID
    ↓
rejected/

No ERROR
    ↓
VALID
    ↓
standardization
    ↓
processed/

WARNING does not automatically reject a record.

---

# 6. Data Lineage

The raw files are treated as source-of-record input.

The framework never overwrites:

`data/raw/`

Standardized values are written only to trusted output.

Rejected records are preserved separately for investigation.

---

# 7. Referential Dependency

Relationships are evaluated in dependency order:

CLIENT
↓
PORTFOLIO
↓
SECURITY
↓
HOLDING
↓
PERFORMANCE

A child record referencing a missing parent is rejected.

---

# 8. Configuration

Validation configuration is separated from validator
implementation.

Business rule thresholds and controlled values should therefore
be maintained in configuration rather than duplicated throughout
the validation code.

---

# 9. Testing

Automated tests cover:

- schema validation
- null validation
- type validation
- duplicate detection
- domain validation
- business rules
- referential integrity
- standardization
- rejection processing
- quality scoring
- complete pipeline integration

Negative testing is included for invalid source records.