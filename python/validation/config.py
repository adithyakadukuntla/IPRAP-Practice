"""
Configuration for the Participant 2 Data Quality framework.

This file contains configuration only.
Validation implementation belongs in the individual validation modules.
"""

# ---------------------------------------------------------------------------
# Dataset definitions
# ---------------------------------------------------------------------------

DATASETS = [
    "clients",
    "portfolios",
    "securities",
    "holdings",
    "portfolio_performance",
]


# ---------------------------------------------------------------------------
# Raw data configuration
# ---------------------------------------------------------------------------

RAW_DATA_DIR = "data/raw"

RAW_DATA_FILES = {
    "clients": {
        "filename": "clients.csv",
        "format": "csv",
    },

    "portfolios": {
        "filename": "portfolios.csv",
        "format": "csv",
    },

    "securities": {
        "filename": "securities.json",
        "format": "json",
    },

    "holdings": {
        "filename": "holdings.csv",
        "format": "csv",
    },

    "portfolio_performance": {
        "filename": "portfolio_performance.csv",
        "format": "csv",
    },
}


# ---------------------------------------------------------------------------
# Output directories
# ---------------------------------------------------------------------------

PROCESSED_DATA_DIR = "data/processed"

REJECTED_DATA_DIR = "data/rejected"

QUALITY_REPORTS_DIR = "data/quality_reports"


# ---------------------------------------------------------------------------
# Supported file formats
# ---------------------------------------------------------------------------

SUPPORTED_FILE_EXTENSIONS = [
    ".csv",
    ".json",
]


# ---------------------------------------------------------------------------
# Expected schemas
#
# These are the schemas defined by the Participant 2 requirements.
# Actual validation logic will be implemented in Phase 5+ modules.
# ---------------------------------------------------------------------------

EXPECTED_COLUMNS = {
    "clients": [
        "client_id",
        "client_name",
        "client_type",
        "country",
        "risk_profile",
        "created_date",
        "status",
    ],

    "portfolios": [
        "portfolio_id",
        "client_id",
        "portfolio_name",
        "portfolio_type",
        "base_currency",
        "risk_profile",
        "initial_value",
        "current_value",
        "inception_date",
        "status",
    ],

    "securities": [
        "security_id",
        "ticker_symbol",
        "security_name",
        "security_type",
        "sector",
        "country",
        "currency",
        "current_price",
        "status",
    ],

    "holdings": [
        "holding_id",
        "portfolio_id",
        "security_id",
        "quantity",
        "purchase_price",
        "current_price",
        "market_value",
        "as_of_date",
    ],

    "portfolio_performance": [
        "performance_id",
        "portfolio_id",
        "as_of_date",
        "beginning_value",
        "ending_value",
        "return_amount",
        "return_percent",
    ],
}
# ---------------------------------------------------------------------------
# Expected data types
#
# Type validation is based on the logical type of the field rather than
# blindly trusting the pandas dtype produced by CSV/JSON loading.
#
# Supported logical types:
#     string
#     numeric
#     date
# ---------------------------------------------------------------------------

EXPECTED_DATA_TYPES = {
    "clients": {
        "client_id": "string",
        "client_name": "string",
        "client_type": "string",
        "country": "string",
        "risk_profile": "string",
        "created_date": "date",
        "status": "string",
    },

    "portfolios": {
        "portfolio_id": "string",
        "client_id": "string",
        "portfolio_name": "string",
        "portfolio_type": "string",
        "base_currency": "string",
        "risk_profile": "string",
        "initial_value": "numeric",
        "current_value": "numeric",
        "inception_date": "date",
        "status": "string",
    },

    "securities": {
        "security_id": "string",
        "ticker_symbol": "string",
        "security_name": "string",
        "security_type": "string",
        "sector": "string",
        "country": "string",
        "currency": "string",
        "current_price": "numeric",
        "status": "string",
    },

    "holdings": {
        "holding_id": "string",
        "portfolio_id": "string",
        "security_id": "string",
        "quantity": "numeric",
        "purchase_price": "numeric",
        "current_price": "numeric",
        "market_value": "numeric",
        "as_of_date": "date",
    },

    "portfolio_performance": {
        "performance_id": "string",
        "portfolio_id": "string",
        "as_of_date": "date",
        "beginning_value": "numeric",
        "ending_value": "numeric",
        "return_amount": "numeric",
        "return_percent": "numeric",
    },
}


# ---------------------------------------------------------------------------
# Date format
# ---------------------------------------------------------------------------

EXPECTED_DATE_FORMAT = "%Y-%m-%d"

# ---------------------------------------------------------------------------
# Domain values
#
# These reflect the actual Participant 1 source data found in the uploaded
# project files.
#
# INDEX and FIXED_INCOME are explicitly supported source values.
# CAD and SGD are explicitly supported source currencies.
# ---------------------------------------------------------------------------

CLIENT_TYPES = [
    "INDIVIDUAL",
    "INSTITUTIONAL",
]

RISK_PROFILES = [
    "LOW",
    "MEDIUM",
    "HIGH",
]

CLIENT_STATUSES = [
    "ACTIVE",
    "INACTIVE",
]

PORTFOLIO_TYPES = [
    "EQUITY_GROWTH",
    "BALANCED",
    "INCOME",
    "INDEX",
    "FIXED_INCOME",
]

SUPPORTED_CURRENCIES = [
    "USD",
    "EUR",
    "GBP",
    "INR",
    "JPY",
    "CAD",
    "SGD",
]

SECURITY_TYPES = [
    "EQUITY",
    "BOND",
    "ETF",
]

SECURITY_STATUSES = [
    "ACTIVE",
    "INACTIVE",
]


# ---------------------------------------------------------------------------
# Business-rule configuration
# ---------------------------------------------------------------------------

MARKET_VALUE_TOLERANCE_PERCENT = 1.0

RETURN_PERCENT_TOLERANCE = 0.01

MIN_PORTFOLIO_VALUE = 0

MIN_SECURITY_PRICE = 0

MIN_HOLDING_QUANTITY = 0


# ---------------------------------------------------------------------------
# Quality score configuration
#
# These thresholds are project-defined thresholds, not industry standards.
# ---------------------------------------------------------------------------

QUALITY_SCORE_EXCELLENT = 95.0
QUALITY_SCORE_GOOD = 90.0
QUALITY_SCORE_WARNING = 80.0

# ---------------------------------------------------------------------------
# Duplicate detection configuration
# ---------------------------------------------------------------------------

DUPLICATE_KEYS = {
    "clients": [
        "client_id",
    ],

    "portfolios": [
        "portfolio_id",
    ],

    "securities": [
        "security_id",
    ],

    "holdings": [
        "holding_id",
    ],

    "portfolio_performance": [
        "performance_id",
    ],
}


# Secondary business-quality check for holdings.
#
# A portfolio holding the same security more than once on the same
# valuation date should be flagged for investigation.
#
# This is separate from the primary holding_id duplicate check.

HOLDINGS_COMPOSITE_DUPLICATE_KEY = [
    "portfolio_id",
    "security_id",
    "as_of_date",
]
# ---------------------------------------------------------------------------
# Domain validation rules
# ---------------------------------------------------------------------------

DOMAIN_RULES = {
    "clients": {
        "client_type": CLIENT_TYPES,
        "risk_profile": RISK_PROFILES,
        "status": CLIENT_STATUSES,
    },

    "portfolios": {
        "portfolio_type": PORTFOLIO_TYPES,
        "base_currency": SUPPORTED_CURRENCIES,
        "risk_profile": RISK_PROFILES,
        "status": CLIENT_STATUSES,
    },

    "securities": {
        "security_type": SECURITY_TYPES,
        "status": SECURITY_STATUSES,
    },
}
# ---------------------------------------------------------------------------
# Business validation configuration
# ---------------------------------------------------------------------------

# Financial calculations may contain small rounding differences.
MARKET_VALUE_TOLERANCE = 0.01       # ±1%
RETURN_AMOUNT_TOLERANCE = 0.01      # ±1%
RETURN_PERCENT_TOLERANCE = 0.05     # ±1%

# Portfolio and security business rules.
MIN_PORTFOLIO_VALUE = 0
MIN_SECURITY_PRICE = 0

# Holdings require strictly positive quantities and prices.
MIN_HOLDING_QUANTITY = 0
MIN_HOLDING_PURCHASE_PRICE = 0
MIN_HOLDING_CURRENT_PRICE = 0

# Performance values may not be negative.
MIN_PERFORMANCE_VALUE = 0
# ---------------------------------------------------------------------------
# Business rule IDs
# ---------------------------------------------------------------------------

BUSINESS_RULE_IDS = {
    "portfolios": {
        "initial_value": "POR-004",
        "current_value": "POR-005",
        "inception_date": "POR-006",
    },

    "securities": {
        "current_price": "SEC-003",
    },

    "holdings": {
        "quantity": "HLD-003",
        "purchase_price": "HLD-004",
        "current_price": "HLD-005",
        "market_value": "HLD-006",
    },

    "portfolio_performance": {
        "beginning_value": "PER-003",
        "ending_value": "PER-004",
        "return_amount": "PER-005",
        "return_percent": "PER-006",
    },
}
# ---------------------------------------------------------------------------
# Referential integrity configuration
# ---------------------------------------------------------------------------

REFERENTIAL_RULES = [
    {
        "child_dataset": "portfolios",
        "child_column": "client_id",
        "parent_dataset": "clients",
        "parent_column": "client_id",
        "rule_id": "REF-001",
        "rule_name": "PORTFOLIO_CLIENT_EXISTS",
    },

    {
        "child_dataset": "holdings",
        "child_column": "portfolio_id",
        "parent_dataset": "portfolios",
        "parent_column": "portfolio_id",
        "rule_id": "REF-002",
        "rule_name": "HOLDING_PORTFOLIO_EXISTS",
    },

    {
        "child_dataset": "holdings",
        "child_column": "security_id",
        "parent_dataset": "securities",
        "parent_column": "security_id",
        "rule_id": "REF-003",
        "rule_name": "HOLDING_SECURITY_EXISTS",
    },

    {
        "child_dataset": "portfolio_performance",
        "child_column": "portfolio_id",
        "parent_dataset": "portfolios",
        "parent_column": "portfolio_id",
        "rule_id": "REF-004",
        "rule_name": "PERFORMANCE_PORTFOLIO_EXISTS",
    },
]
# ---------------------------------------------------------------------------
# Data standardization configuration
# ---------------------------------------------------------------------------

STANDARDIZE_UPPERCASE_COLUMNS = {
    "clients": [
        "client_type",
        "risk_profile",
        "status",
    ],

    "portfolios": [
        "portfolio_type",
        "base_currency",
        "risk_profile",
        "status",
    ],

    "securities": [
        "security_type",
        "currency",
        "status",
    ],

    "holdings": [],

    "portfolio_performance": [],
}


STANDARDIZE_DATE_COLUMNS = {
    "clients": [
        "created_date",
    ],

    "portfolios": [
        "inception_date",
    ],

    "securities": [],

    "holdings": [
        "as_of_date",
    ],

    "portfolio_performance": [
        "as_of_date",
    ],
}