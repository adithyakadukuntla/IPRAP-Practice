"""
Tests for Participant 2 duplicate validation.
"""

import pandas as pd
import pytest

from python.validation.data_loader import (
    RawDataLoader,
)
from python.validation.duplicate_validator import (
    DuplicateValidationError,
    DuplicateValidator,
)


# ---------------------------------------------------------------------------
# Client duplicate tests
# ---------------------------------------------------------------------------

def test_unique_client_ids_are_valid():
    dataframe = pd.DataFrame(
        {
            "client_id": [
                "C10001",
                "C10002",
                "C10003",
            ],
            "client_name": [
                "Alice",
                "Bob",
                "Charlie",
            ],
        }
    )

    validator = DuplicateValidator(
        {
            "clients": [
                "client_id",
            ]
        }
    )

    result = validator.validate_dataset(
        "clients",
        dataframe,
    )

    assert result.valid is True
    assert result.error_count == 0


def test_duplicate_client_id_is_detected():
    dataframe = pd.DataFrame(
        {
            "client_id": [
                "C10001",
                "C10001",
                "C10002",
            ]
        }
    )

    validator = DuplicateValidator(
        {
            "clients": [
                "client_id",
            ]
        }
    )

    result = validator.validate_dataset(
        "clients",
        dataframe,
    )

    assert result.valid is False
    assert result.error_count == 1
    assert result.issues[0].duplicate_count == 2
    assert result.issues[0].row_indices == [
        0,
        1,
    ]


# ---------------------------------------------------------------------------
# Portfolio duplicate tests
# ---------------------------------------------------------------------------

def test_duplicate_portfolio_id_is_detected():
    dataframe = pd.DataFrame(
        {
            "portfolio_id": [
                "P10001",
                "P10001",
                "P10002",
            ]
        }
    )

    validator = DuplicateValidator(
        {
            "portfolios": [
                "portfolio_id",
            ]
        }
    )

    result = validator.validate_dataset(
        "portfolios",
        dataframe,
    )

    assert result.valid is False
    assert result.error_count == 1
    assert (
        result.issues[0].key_values[
            "portfolio_id"
        ]
        == "P10001"
    )


def test_different_portfolio_ids_are_valid():
    dataframe = pd.DataFrame(
        {
            "portfolio_id": [
                "P10001",
                "P10002",
                "P10003",
            ]
        }
    )

    validator = DuplicateValidator(
        {
            "portfolios": [
                "portfolio_id",
            ]
        }
    )

    result = validator.validate_dataset(
        "portfolios",
        dataframe,
    )

    assert result.valid is True


# ---------------------------------------------------------------------------
# Security duplicate tests
# ---------------------------------------------------------------------------

def test_duplicate_security_id_is_detected():
    dataframe = pd.DataFrame(
        {
            "security_id": [
                "SEC10001",
                "SEC10001",
            ]
        }
    )

    validator = DuplicateValidator(
        {
            "securities": [
                "security_id",
            ]
        }
    )

    result = validator.validate_dataset(
        "securities",
        dataframe,
    )

    assert result.valid is False
    assert result.error_count == 1


# ---------------------------------------------------------------------------
# Holdings primary key tests
# ---------------------------------------------------------------------------

def test_duplicate_holding_id_is_detected():
    dataframe = pd.DataFrame(
        {
            "holding_id": [
                "H10001",
                "H10001",
            ],
            "portfolio_id": [
                "P10001",
                "P10001",
            ],
            "security_id": [
                "SEC10001",
                "SEC10001",
            ],
            "as_of_date": [
                "2026-08-01",
                "2026-08-01",
            ],
        }
    )

    validator = DuplicateValidator(
        {
            "holdings": [
                "holding_id",
            ]
        },
        [
            "portfolio_id",
            "security_id",
            "as_of_date",
        ],
    )

    result = validator.validate_dataset(
        "holdings",
        dataframe,
    )

    assert result.valid is False

    duplicate_types = [
        issue.duplicate_type
        for issue in result.issues
    ]

    assert "BUSINESS_KEY" in duplicate_types


# ---------------------------------------------------------------------------
# Holdings composite-key tests
# ---------------------------------------------------------------------------

def test_holdings_composite_duplicate_is_detected():
    dataframe = pd.DataFrame(
        {
            "holding_id": [
                "H10001",
                "H10002",
            ],
            "portfolio_id": [
                "P10001",
                "P10001",
            ],
            "security_id": [
                "SEC10001",
                "SEC10001",
            ],
            "as_of_date": [
                "2026-08-01",
                "2026-08-01",
            ],
        }
    )

    validator = DuplicateValidator(
        {
            "holdings": [
                "holding_id",
            ]
        },
        [
            "portfolio_id",
            "security_id",
            "as_of_date",
        ],
    )

    result = validator.validate_dataset(
        "holdings",
        dataframe,
    )

    assert result.valid is False

    composite_issues = [
        issue
        for issue in result.issues
        if issue.duplicate_type
        == "HOLDINGS_COMPOSITE_KEY"
    ]

    assert len(composite_issues) == 1
    assert (
        composite_issues[0].duplicate_count
        == 2
    )


def test_holdings_different_dates_are_not_composite_duplicates():
    dataframe = pd.DataFrame(
        {
            "holding_id": [
                "H10001",
                "H10002",
            ],
            "portfolio_id": [
                "P10001",
                "P10001",
            ],
            "security_id": [
                "SEC10001",
                "SEC10001",
            ],
            "as_of_date": [
                "2026-08-01",
                "2026-08-02",
            ],
        }
    )

    validator = DuplicateValidator(
        {
            "holdings": [
                "holding_id",
            ]
        },
        [
            "portfolio_id",
            "security_id",
            "as_of_date",
        ],
    )

    result = validator.validate_dataset(
        "holdings",
        dataframe,
    )

    assert result.valid is True


# ---------------------------------------------------------------------------
# Performance tests
# ---------------------------------------------------------------------------

def test_duplicate_performance_id_is_detected():
    dataframe = pd.DataFrame(
        {
            "performance_id": [
                "PER10001",
                "PER10001",
            ]
        }
    )

    validator = DuplicateValidator(
        {
            "portfolio_performance": [
                "performance_id",
            ]
        }
    )

    result = validator.validate_dataset(
        "portfolio_performance",
        dataframe,
    )

    assert result.valid is False
    assert result.error_count == 1


# ---------------------------------------------------------------------------
# Different rows, same business key
# ---------------------------------------------------------------------------

def test_duplicate_does_not_require_identical_rows():
    dataframe = pd.DataFrame(
        {
            "portfolio_id": [
                "P10001",
                "P10001",
            ],
            "current_value": [
                100000,
                105000,
            ],
        }
    )

    validator = DuplicateValidator(
        {
            "portfolios": [
                "portfolio_id",
            ]
        }
    )

    result = validator.validate_dataset(
        "portfolios",
        dataframe,
    )

    assert result.valid is False
    assert result.error_count == 1


# ---------------------------------------------------------------------------
# Duplicate group with three records
# ---------------------------------------------------------------------------

def test_three_records_with_same_business_key():
    dataframe = pd.DataFrame(
        {
            "client_id": [
                "C10001",
                "C10001",
                "C10001",
            ]
        }
    )

    validator = DuplicateValidator(
        {
            "clients": [
                "client_id",
            ]
        }
    )

    result = validator.validate_dataset(
        "clients",
        dataframe,
    )

    assert result.valid is False
    assert result.error_count == 1
    assert (
        result.issues[0].duplicate_count
        == 3
    )
    assert result.duplicate_record_count == 3


# ---------------------------------------------------------------------------
# Missing key configuration
# ---------------------------------------------------------------------------

def test_unknown_dataset_raises_error():
    dataframe = pd.DataFrame(
        {
            "id": [
                "A1",
            ]
        }
    )

    validator = DuplicateValidator()

    with pytest.raises(
        DuplicateValidationError
    ):
        validator.validate_dataset(
            "unknown",
            dataframe,
        )


def test_missing_key_column_raises_error():
    dataframe = pd.DataFrame(
        {
            "other_column": [
                "A1",
            ]
        }
    )

    validator = DuplicateValidator(
        {
            "clients": [
                "client_id",
            ]
        }
    )

    with pytest.raises(
        DuplicateValidationError
    ):
        validator.validate_dataset(
            "clients",
            dataframe,
        )


# ---------------------------------------------------------------------------
# All datasets
# ---------------------------------------------------------------------------

def test_empty_dataset_collection():
    validator = DuplicateValidator()

    with pytest.raises(
        DuplicateValidationError
    ):
        validator.validate_all({})


def test_actual_participant_data():
    loader = RawDataLoader()

    datasets = (
        loader.load_all_datasets()
    )

    validator = DuplicateValidator()

    results = validator.validate_all(
        datasets
    )

    for dataset_name, result in (
        results.items()
    ):
        assert result.valid is True, (
            f"{dataset_name} has duplicate "
            f"issues: {result.issues}"
        )


def test_is_valid():
    dataframe = pd.DataFrame(
        {
            "client_id": [
                "C10001",
                "C10002",
            ]
        }
    )

    validator = DuplicateValidator()

    assert (
        validator.is_valid(
            "clients",
            dataframe,
        )
        is True
    )