"""
Tests for Participant 2 schema validation.
"""

import pandas as pd
import pytest

from python.validation.config import (
    EXPECTED_COLUMNS,
)
from python.validation.data_loader import (
    RawDataLoader,
)
from python.validation.schema_validator import (
    SchemaValidationError,
    SchemaValidator,
)


# ---------------------------------------------------------------------------
# Test helpers
# ---------------------------------------------------------------------------


def make_dataframe(columns):
    """
    Create a simple DataFrame with the supplied columns.
    """

    return pd.DataFrame(
        {
            column: [1]
            for column in columns
        }
    )


# ---------------------------------------------------------------------------
# Correct schema tests
# ---------------------------------------------------------------------------


def test_clients_correct_schema():
    validator = SchemaValidator()

    dataframe = make_dataframe(
        EXPECTED_COLUMNS["clients"]
    )

    result = validator.validate_dataset(
        "clients",
        dataframe,
    )

    assert result.valid is True
    assert result.missing_columns == []
    assert result.unexpected_columns == []


def test_portfolios_correct_schema():
    validator = SchemaValidator()

    dataframe = make_dataframe(
        EXPECTED_COLUMNS["portfolios"]
    )

    result = validator.validate_dataset(
        "portfolios",
        dataframe,
    )

    assert result.valid is True
    assert result.missing_columns == []
    assert result.unexpected_columns == []


def test_securities_correct_schema():
    validator = SchemaValidator()

    dataframe = make_dataframe(
        EXPECTED_COLUMNS["securities"]
    )

    result = validator.validate_dataset(
        "securities",
        dataframe,
    )

    assert result.valid is True
    assert result.missing_columns == []
    assert result.unexpected_columns == []


def test_holdings_correct_schema():
    validator = SchemaValidator()

    dataframe = make_dataframe(
        EXPECTED_COLUMNS["holdings"]
    )

    result = validator.validate_dataset(
        "holdings",
        dataframe,
    )

    assert result.valid is True
    assert result.missing_columns == []
    assert result.unexpected_columns == []


def test_performance_correct_schema():
    validator = SchemaValidator()

    dataframe = make_dataframe(
        EXPECTED_COLUMNS[
            "portfolio_performance"
        ]
    )

    result = validator.validate_dataset(
        "portfolio_performance",
        dataframe,
    )

    assert result.valid is True
    assert result.missing_columns == []
    assert result.unexpected_columns == []


# ---------------------------------------------------------------------------
# Missing-column tests
# ---------------------------------------------------------------------------


def test_missing_required_column():
    validator = SchemaValidator()

    columns = list(
        EXPECTED_COLUMNS["clients"]
    )

    columns.remove("client_id")

    dataframe = make_dataframe(
        columns
    )

    result = validator.validate_dataset(
        "clients",
        dataframe,
    )

    assert result.valid is False
    assert result.missing_columns == [
        "client_id"
    ]
    assert result.unexpected_columns == []


def test_missing_multiple_required_columns():
    validator = SchemaValidator()

    columns = list(
        EXPECTED_COLUMNS["portfolios"]
    )

    columns.remove("portfolio_id")
    columns.remove("client_id")
    columns.remove("status")

    dataframe = make_dataframe(
        columns
    )

    result = validator.validate_dataset(
        "portfolios",
        dataframe,
    )

    assert result.valid is False

    assert set(
        result.missing_columns
    ) == {
        "portfolio_id",
        "client_id",
        "status",
    }


# ---------------------------------------------------------------------------
# Unexpected-column tests
# ---------------------------------------------------------------------------


def test_unexpected_column():
    validator = SchemaValidator()

    columns = list(
        EXPECTED_COLUMNS["clients"]
    )

    columns.append("phone_number")

    dataframe = make_dataframe(
        columns
    )

    result = validator.validate_dataset(
        "clients",
        dataframe,
    )

    assert result.valid is False
    assert result.missing_columns == []
    assert result.unexpected_columns == [
        "phone_number"
    ]


def test_multiple_unexpected_columns():
    validator = SchemaValidator()

    columns = list(
        EXPECTED_COLUMNS["securities"]
    )

    columns.extend(
        [
            "exchange",
            "market_cap",
        ]
    )

    dataframe = make_dataframe(
        columns
    )

    result = validator.validate_dataset(
        "securities",
        dataframe,
    )

    assert result.valid is False

    assert set(
        result.unexpected_columns
    ) == {
        "exchange",
        "market_cap",
    }


# ---------------------------------------------------------------------------
# Missing + unexpected together
# ---------------------------------------------------------------------------


def test_missing_and_unexpected_columns():
    validator = SchemaValidator()

    columns = list(
        EXPECTED_COLUMNS["holdings"]
    )

    columns.remove("security_id")
    columns.append("security_name")

    dataframe = make_dataframe(
        columns
    )

    result = validator.validate_dataset(
        "holdings",
        dataframe,
    )

    assert result.valid is False

    assert result.missing_columns == [
        "security_id"
    ]

    assert result.unexpected_columns == [
        "security_name"
    ]


# ---------------------------------------------------------------------------
# Column order test
# ---------------------------------------------------------------------------


def test_column_order_does_not_matter():
    validator = SchemaValidator()

    columns = list(
        EXPECTED_COLUMNS["clients"]
    )

    reversed_columns = list(
        reversed(columns)
    )

    dataframe = make_dataframe(
        reversed_columns
    )

    result = validator.validate_dataset(
        "clients",
        dataframe,
    )

    assert result.valid is True


# ---------------------------------------------------------------------------
# Empty-column DataFrame
# ---------------------------------------------------------------------------


def test_empty_dataframe_has_invalid_schema():
    validator = SchemaValidator()

    dataframe = pd.DataFrame()

    result = validator.validate_dataset(
        "clients",
        dataframe,
    )

    assert result.valid is False

    assert set(
        result.missing_columns
    ) == set(
        EXPECTED_COLUMNS["clients"]
    )


# ---------------------------------------------------------------------------
# Invalid dataset configuration
# ---------------------------------------------------------------------------


def test_unknown_dataset_raises_error():
    validator = SchemaValidator()

    dataframe = pd.DataFrame(
        {
            "id": [1]
        }
    )

    with pytest.raises(
        SchemaValidationError
    ):
        validator.validate_dataset(
            "unknown_dataset",
            dataframe,
        )


def test_non_dataframe_raises_error():
    validator = SchemaValidator()

    with pytest.raises(
        SchemaValidationError
    ):
        validator.validate_dataset(
            "clients",
            {
                "client_id": ["C10001"]
            },
        )


def test_empty_dataset_collection_raises_error():
    validator = SchemaValidator()

    with pytest.raises(
        SchemaValidationError
    ):
        validator.validate_all({})


# ---------------------------------------------------------------------------
# Convenience method tests
# ---------------------------------------------------------------------------


def test_is_valid_returns_true():
    validator = SchemaValidator()

    dataframe = make_dataframe(
        EXPECTED_COLUMNS["clients"]
    )

    assert (
        validator.is_valid(
            "clients",
            dataframe,
        )
        is True
    )


def test_is_valid_returns_false():
    validator = SchemaValidator()

    columns = list(
        EXPECTED_COLUMNS["clients"]
    )

    columns.remove("client_id")

    dataframe = make_dataframe(
        columns
    )

    assert (
        validator.is_valid(
            "clients",
            dataframe,
        )
        is False
    )


def test_validate_and_raise_for_invalid_schema():
    validator = SchemaValidator()

    columns = list(
        EXPECTED_COLUMNS["clients"]
    )

    columns.remove("client_id")

    dataframe = make_dataframe(
        columns
    )

    with pytest.raises(
        SchemaValidationError,
        match="client_id",
    ):
        validator.validate_and_raise(
            "clients",
            dataframe,
        )


# ---------------------------------------------------------------------------
# Actual Participant 1 data
# ---------------------------------------------------------------------------


def test_actual_participant_data_has_valid_schema():
    loader = RawDataLoader()

    datasets = (
        loader.load_all_datasets()
    )

    validator = SchemaValidator()

    results = validator.validate_all(
        datasets
    )

    assert set(results.keys()) == {
        "clients",
        "portfolios",
        "securities",
        "holdings",
        "portfolio_performance",
    }

    for dataset_name, result in results.items():
        assert result.valid is True, (
            f"{dataset_name} failed schema validation: "
            f"{result.error_message}"
        )

        assert result.missing_columns == []

        assert result.unexpected_columns == []


def test_actual_schema_column_counts():
    loader = RawDataLoader()

    datasets = (
        loader.load_all_datasets()
    )

    validator = SchemaValidator()

    results = validator.validate_all(
        datasets
    )

    expected_counts = {
        "clients": 7,
        "portfolios": 10,
        "securities": 9,
        "holdings": 8,
        "portfolio_performance": 7,
    }

    for dataset_name, expected_count in (
        expected_counts.items()
    ):
        result = results[
            dataset_name
        ]

        assert len(
            result.expected_columns
        ) == expected_count

        assert len(
            result.actual_columns
        ) == expected_count