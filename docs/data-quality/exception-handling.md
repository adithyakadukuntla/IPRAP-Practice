# Exception Handling

## 1. Purpose

The validation framework preserves invalid source records and
records the reason for rejection.

Invalid data is never silently deleted.

---

# 2. Severity

## ERROR

An ERROR means the record cannot be trusted.

An ERROR causes automatic rejection.

## WARNING

A WARNING indicates that the record is usable but requires
attention.

Warnings do not automatically reject the record.

## INFO

An INFO message records an informational observation.

---

# 3. Rejected Records

Rejected records are written under:

`data/rejected/`

Each dataset has its own directory.

Example:

`data/rejected/clients/clients_rejected.csv`

Rejected records retain their source values.

---

# 4. Validation Error Report

All validation exceptions are consolidated into:

`data/quality_reports/validation_errors.csv`

The report contains:

- dataset_name
- record_identifier
- row_index
- column_name
- rule_id
- severity
- error_message

---

# 5. Traceability

Every validation failure should provide enough information to
identify:

- dataset
- record
- field where applicable
- validation rule
- severity
- human-readable error message

Rule IDs are used for consistent tracking and reporting.

---

# 6. Business Value Errors

Business values must not be silently corrected.

Example:

quantity = -100

The system must reject the record rather than converting:

-100 → 100

This preserves source-data lineage.

---

# 7. Missing Parent

If a portfolio references an unknown client:

portfolio → C99999

and C99999 does not exist, the portfolio is rejected.

The system does not create a synthetic client.

---

# 8. Invalid Child

If a holding references an unknown security:

holding → SEC99999

and SEC99999 does not exist, the holding is rejected.

The system does not substitute another security.

---

# 9. Duplicate Records

Duplicate records are flagged and rejected according to the
configured duplicate rules.

Records are preserved for investigation rather than silently
deleted.

---

# 10. Raw Data Protection

The original files under:

`data/raw/`

must never be modified by the validation framework.

All transformations occur on copies or generated trusted outputs.