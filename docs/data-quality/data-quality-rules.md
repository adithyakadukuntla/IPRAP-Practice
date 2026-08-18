# Investment Portfolio Risk Analytics Platform
# Data Quality Rules

## 1. Purpose

This document defines the validation rules implemented by
Participant 2 for the Investment Portfolio Risk Analytics Platform.

Participant 2 is responsible for validating and standardizing the
five datasets received from Participant 1.

The five datasets are:

- clients
- portfolios
- securities
- holdings
- portfolio_performance

Raw source data is never modified.

---

# 2. Validation Severity

## ERROR

The record cannot be trusted.

An ERROR causes the record to be rejected.

Examples:

- Missing mandatory field
- Invalid identifier
- Invalid controlled value
- Negative business value
- Missing referenced parent
- Invalid calculation

## WARNING

The record is usable but requires attention.

Warnings do not automatically reject a record.

## INFO

Informational observation.

Informational observations do not reject a record.

---

# 3. Clients

Dataset:

`clients`

Expected columns:

- client_id
- client_name
- client_type
- country
- risk_profile
- created_date
- status

## Required Fields

The following fields must not be null:

- client_id
- client_name
- client_type
- country
- risk_profile
- created_date
- status

## Client ID

Expected format:

`C` followed by five digits.

Pattern:

`^C[0-9]{5}$`

Example:

`C10001`

## Client Type

Allowed values:

- INDIVIDUAL
- INSTITUTIONAL

## Risk Profile

Allowed values:

- LOW
- MEDIUM
- HIGH

Case variations may be standardized.

Example:

`high` → `HIGH`

## Status

Allowed values:

- ACTIVE
- INACTIVE

---

# 4. Portfolios

Dataset:

`portfolios`

Expected columns:

- portfolio_id
- client_id
- portfolio_name
- portfolio_type
- base_currency
- risk_profile
- initial_value
- current_value
- inception_date
- status

## Portfolio ID

Expected format:

`P` followed by five digits.

## Portfolio → Client

Every `portfolio.client_id` must exist in
`clients.client_id`.

A missing client reference causes the portfolio record to
be rejected.

## Portfolio Type

Allowed values:

- EQUITY_GROWTH
- BALANCED
- INCOME

## Base Currency

Supported values:

- USD
- EUR
- GBP
- INR
- JPY

## Risk Profile

Allowed values:

- LOW
- MEDIUM
- HIGH

## Portfolio Values

`initial_value >= 0`

`current_value >= 0`

Negative portfolio values are ERROR conditions.

## Inception Date

The date must:

- be valid
- not be blank
- not be later than the current business date

## Status

Allowed values:

- ACTIVE
- INACTIVE

---

# 5. Securities

Dataset:

`securities`

Expected columns:

- security_id
- ticker_symbol
- security_name
- security_type
- sector
- country
- currency
- current_price
- status

## Security ID

Expected format:

`SEC` followed by five digits.

## Security Type

Allowed values:

- EQUITY
- BOND
- ETF

## Current Price

The current price must satisfy the configured
business validation rules.

A zero or invalid price is rejected.

## Status

Allowed values:

- ACTIVE
- INACTIVE

---

# 6. Holdings

Dataset:

`holdings`

Expected columns:

- holding_id
- portfolio_id
- security_id
- quantity
- purchase_price
- current_price
- market_value
- as_of_date

## Holding ID

Expected format:

`H` followed by six digits.

## Portfolio Reference

Every `holding.portfolio_id` must exist in
`portfolios.portfolio_id`.

## Security Reference

Every `holding.security_id` must exist in
`securities.security_id`.

## Quantity

Requirement:

`quantity > 0`

## Purchase Price

Requirement:

`purchase_price > 0`

## Current Price

Requirement:

`current_price > 0`

## Market Value

Expected relationship:

`market_value ≈ quantity × current_price`

A project-defined tolerance is applied to accommodate
rounding.

---

# 7. Portfolio Performance

Dataset:

`portfolio_performance`

Expected columns:

- performance_id
- portfolio_id
- as_of_date
- beginning_value
- ending_value
- return_amount
- return_percent

## Portfolio Reference

Every `portfolio_id` must exist in
`portfolios.portfolio_id`.

## Beginning Value

Requirement:

`beginning_value >= 0`

## Ending Value

Requirement:

`ending_value >= 0`

## Return Amount

Expected:

`return_amount = ending_value - beginning_value`

## Return Percentage

Expected:

`return_percent =
(return_amount / beginning_value) × 100`

A small configured tolerance is permitted for rounding.

---

# 8. Duplicate Detection

Primary business keys:

| Dataset | Business Key |
|---|---|
| clients | client_id |
| portfolios | portfolio_id |
| securities | security_id |
| holdings | holding_id |
| portfolio_performance | performance_id |

Holdings also receive a composite duplicate check using:

- portfolio_id
- security_id
- as_of_date

Duplicate records are rejected and preserved for traceability.

---

# 9. Referential Integrity

Validation follows the dependency order:

clients
↓
portfolios
↓
securities
↓
holdings
↓
portfolio_performance

Records referencing missing parent entities are rejected.

---

# 10. Standardization

Standardization applies only to accepted records.

Examples:

`" high "` → `"HIGH"`

`" individual "` → `"INDIVIDUAL"`

Leading and trailing whitespace is removed where appropriate.

Standardization does not alter the original raw source.

---

# 11. Golden Rule

Raw source data must never be modified.

Invalid business values are rejected rather than silently corrected.

Example:

`quantity = -100`

must not be changed to:

`quantity = 100`

The original source value must remain traceable.