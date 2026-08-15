"""
Tests for Participant 2 data-type validation.
"""

import pandas as pd
import pytest

from python.validation.config import (
    EXPECTED_DATA_TYPES,
)
from python.validation.data_loader import (
    RawDataLoader,
)
from python.validation.type_validator import (
    TypeValidationError,
    TypeValidator,
)


def test_valid_numeric_column():
    dataframe = pd.DataFrame(
        {
            "value": [10.0, 20.5, 30.0],
        }
    )

    validator = TypeValidator(
        {
            "test": {
                "value": "numeric",
            }
        }
    )

    result = validator.validate_dataset(
        "test",
        dataframe,
    )

    assert result.valid is True
    assert result.error_count == 0


def test_invalid_numeric_value():
    dataframe = pd.DataFrame(
        {
            "value": [10.0, "ABC", 30.0],
        }
    )

    validator = TypeValidator(
        {
            "test": {
                "value": "numeric",
            }
        }
    )

    result = validator.validate_dataset(
        "test",
        dataframe,
    )

    assert result.valid is False
    assert result.error_count == 1
    assert result.issues[0].row_index == 1
    assert (
        result.issues[0].expected_type
        == "numeric"
    )


def test_valid_string_column():
    dataframe = pd.DataFrame(
        {
            "status": [
                "ACTIVE",
                "INACTIVE",
            ],
        }
    )

    validator = TypeValidator(
        {
            "test": {
                "status": "string",
            }
        }
    )

    result = validator.validate_dataset(
        "test",
        dataframe,
    )

    assert result.valid is True


def test_invalid_string_value():
    dataframe = pd.DataFrame(
        {
            "status": [
                "ACTIVE",
                123,
            ],
        }
    )

    validator = TypeValidator(
        {
            "test": {
                "status": "string",
            }
        }
    )

    result = validator.validate_dataset(
        "test",
        dataframe,
    )

    assert result.valid is False
    assert result.error_count == 1


def test_valid_date_values():
    dataframe = pd.DataFrame(
        {
            "date": [
                "2026-01-01",
                "2026-08-15",
                "2025-12-31",
            ],
        }
    )

    validator = TypeValidator(
        {
            "test": {
                "date": "date",
            }
        }
    )

    result = validator.validate_dataset(
        "test",
        dataframe,
    )

    assert result.valid is True


def test_malformed_date():
    dataframe = pd.DataFrame(
        {
            "date": [
                "2026-01-01",
                "not-a-date",
                "2026-08-15",
            ],
        }
    )

    validator = TypeValidator(
        {
            "test": {
                "date": "date",
            }
        }
    )

    result = validator.validate_dataset(
        "test",
        dataframe,
    )

    assert result.valid is False
    assert result.error_count == 1
    assert (
        result.issues[0].row_index
        == 1
    )


def test_wrong_date_format():
    dataframe = pd.DataFrame(
        {
            "date": [
                "01-08-2026",
            ],
        }
    )

    validator = TypeValidator(
        {
            "test": {
                "date": "date",
            }
        }
    )

    result = validator.validate_dataset(
        "test",
        dataframe,
    )

    assert result.valid is False


def test_null_is_not_type_error():
    dataframe = pd.DataFrame(
        {
            "value": [
                10.0,
                None,
                30.0,
            ],
        }
    )

    validator = TypeValidator(
        {
            "test": {
                "value": "numeric",
            }
        }
    )

    result = validator.validate_dataset(
        "test",
        dataframe,
    )

    assert result.valid is True
    assert result.error_count == 0


def test_boolean_is_not_numeric():
    dataframe = pd.DataFrame(
        {
            "value": [
                10,
                True,
                30,
            ],
        }
    )

    validator = TypeValidator(
        {
            "test": {
                "value": "numeric",
            }
        }
    )

    result = validator.validate_dataset(
        "test",
        dataframe,
    )

    assert result.valid is False


def test_unknown_type_configuration():
    dataframe = pd.DataFrame(
        {
            "value": [1],
        }
    )

    validator = TypeValidator(
        {
            "test": {
                "value": "unknown_type",
            }
        }
    )

    with pytest.raises(
        TypeValidationError
    ):
        validator.validate_dataset(
            "test",
            dataframe,
        )


def test_missing_type_configuration_column():
    dataframe = pd.DataFrame(
        {
            "id": ["A1"],
        }
    )

    validator = TypeValidator(
        {
            "test": {
                "value": "numeric",
            }
        }
    )

    with pytest.raises(
        TypeValidationError
    ):
        validator.validate_dataset(
            "test",
            dataframe,
        )


def test_actual_participant_data_has_valid_types():
    loader = RawDataLoader()

    datasets = (
        loader.load_all_datasets()
    )

    validator = TypeValidator()

    results = validator.validate_all(
        datasets
    )

    for dataset_name, result in (
        results.items()
    ):
        assert result.valid is True, (
            f"{dataset_name} has type errors: "
            f"{result.issues}"
        )


def test_empty_dataset_collection():
    validator = TypeValidator()

    with pytest.raises(
        TypeValidationError
    ):
        validator.validate_all({})


def test_is_valid():
    dataframe = pd.DataFrame(
        {
            "value": [1.0, 2.0],
        }
    )

    validator = TypeValidator(
        {
            "test": {
                "value": "numeric",
            }
        }
    )

    assert (
        validator.is_valid(
            "test",
            dataframe,
        )
        is True
    )