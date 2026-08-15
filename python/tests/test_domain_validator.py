"""
Tests for Participant 2 domain validation.
"""

import pandas as pd
import pytest

from python.validation.config import (
    CLIENT_TYPES,
    CLIENT_STATUSES,
    PORTFOLIO_TYPES,
    RISK_PROFILES,
    SECURITY_STATUSES,
    SECURITY_TYPES,
    SUPPORTED_CURRENCIES,
)
from python.validation.data_loader import (
    RawDataLoader,
)
from python.validation.domain_validator import (
    DomainValidationError,
    DomainValidator,
)


# ---------------------------------------------------------------------------
# Client tests
# ---------------------------------------------------------------------------


def test_valid_client_type():
    dataframe = pd.DataFrame(
        {
            "client_type": [
                "INDIVIDUAL",
                "INSTITUTIONAL",
            ]
        }
    )

    validator = DomainValidator(
        {
            "clients": {
                "client_type": CLIENT_TYPES,
            }
        }
    )

    result = validator.validate_dataset(
        "clients",
        dataframe,
    )

    assert result.valid is True
    assert result.error_count == 0


def test_invalid_client_type():
    dataframe = pd.DataFrame(
        {
            "client_type": [
                "INDIVIDUAL",
                "INVALID_TYPE",
            ]
        }
    )

    validator = DomainValidator(
        {
            "clients": {
                "client_type": CLIENT_TYPES,
            }
        }
    )

    result = validator.validate_dataset(
        "clients",
        dataframe,
    )

    assert result.valid is False
    assert result.error_count == 1
    assert result.issues[0].row_index == 1
    assert (
        result.issues[0].column_name
        == "client_type"
    )


def test_valid_risk_profile():
    dataframe = pd.DataFrame(
        {
            "risk_profile": [
                "LOW",
                "MEDIUM",
                "HIGH",
            ]
        }
    )

    validator = DomainValidator(
        {
            "clients": {
                "risk_profile": RISK_PROFILES,
            }
        }
    )

    result = validator.validate_dataset(
        "clients",
        dataframe,
    )

    assert result.valid is True


def test_invalid_risk_profile():
    dataframe = pd.DataFrame(
        {
            "risk_profile": [
                "LOW",
                "EXTREME",
            ]
        }
    )

    validator = DomainValidator(
        {
            "clients": {
                "risk_profile": RISK_PROFILES,
            }
        }
    )

    result = validator.validate_dataset(
        "clients",
        dataframe,
    )

    assert result.valid is False
    assert result.error_count == 1


def test_valid_client_status():
    dataframe = pd.DataFrame(
        {
            "status": [
                "ACTIVE",
                "INACTIVE",
            ]
        }
    )

    validator = DomainValidator(
        {
            "clients": {
                "status": CLIENT_STATUSES,
            }
        }
    )

    result = validator.validate_dataset(
        "clients",
        dataframe,
    )

    assert result.valid is True


def test_invalid_client_status():
    dataframe = pd.DataFrame(
        {
            "status": [
                "ACTIVE",
                "CLOSED",
            ]
        }
    )

    validator = DomainValidator(
        {
            "clients": {
                "status": CLIENT_STATUSES,
            }
        }
    )

    result = validator.validate_dataset(
        "clients",
        dataframe,
    )

    assert result.valid is False


# ---------------------------------------------------------------------------
# Portfolio tests
# ---------------------------------------------------------------------------


def test_valid_portfolio_types():
    dataframe = pd.DataFrame(
        {
            "portfolio_type": PORTFOLIO_TYPES,
        }
    )

    validator = DomainValidator(
        {
            "portfolios": {
                "portfolio_type": PORTFOLIO_TYPES,
            }
        }
    )

    result = validator.validate_dataset(
        "portfolios",
        dataframe,
    )

    assert result.valid is True


def test_invalid_portfolio_type():
    dataframe = pd.DataFrame(
        {
            "portfolio_type": [
                "EQUITY_GROWTH",
                "CRYPTO_SPECULATIVE",
            ]
        }
    )

    validator = DomainValidator(
        {
            "portfolios": {
                "portfolio_type": PORTFOLIO_TYPES,
            }
        }
    )

    result = validator.validate_dataset(
        "portfolios",
        dataframe,
    )

    assert result.valid is False
    assert result.error_count == 1


def test_index_and_fixed_income_are_valid():
    dataframe = pd.DataFrame(
        {
            "portfolio_type": [
                "INDEX",
                "FIXED_INCOME",
            ]
        }
    )

    validator = DomainValidator(
        {
            "portfolios": {
                "portfolio_type": PORTFOLIO_TYPES,
            }
        }
    )

    result = validator.validate_dataset(
        "portfolios",
        dataframe,
    )

    assert result.valid is True


def test_valid_portfolio_currency():
    dataframe = pd.DataFrame(
        {
            "base_currency": [
                "USD",
                "EUR",
                "GBP",
                "INR",
                "JPY",
                "CAD",
                "SGD",
            ]
        }
    )

    validator = DomainValidator(
        {
            "portfolios": {
                "base_currency": (
                    SUPPORTED_CURRENCIES
                ),
            }
        }
    )

    result = validator.validate_dataset(
        "portfolios",
        dataframe,
    )

    assert result.valid is True


def test_invalid_portfolio_currency():
    dataframe = pd.DataFrame(
        {
            "base_currency": [
                "USD",
                "XYZ",
            ]
        }
    )

    validator = DomainValidator(
        {
            "portfolios": {
                "base_currency": (
                    SUPPORTED_CURRENCIES
                ),
            }
        }
    )

    result = validator.validate_dataset(
        "portfolios",
        dataframe,
    )

    assert result.valid is False


def test_valid_portfolio_risk_profile():
    dataframe = pd.DataFrame(
        {
            "risk_profile": [
                "LOW",
                "MEDIUM",
                "HIGH",
            ]
        }
    )

    validator = DomainValidator(
        {
            "portfolios": {
                "risk_profile": RISK_PROFILES,
            }
        }
    )

    result = validator.validate_dataset(
        "portfolios",
        dataframe,
    )

    assert result.valid is True


def test_invalid_portfolio_risk_profile():
    dataframe = pd.DataFrame(
        {
            "risk_profile": [
                "LOW",
                "VERY_HIGH",
            ]
        }
    )

    validator = DomainValidator(
        {
            "portfolios": {
                "risk_profile": RISK_PROFILES,
            }
        }
    )

    result = validator.validate_dataset(
        "portfolios",
        dataframe,
    )

    assert result.valid is False


# ---------------------------------------------------------------------------
# Security tests
# ---------------------------------------------------------------------------


def test_valid_security_types():
    dataframe = pd.DataFrame(
        {
            "security_type": [
                "EQUITY",
                "BOND",
                "ETF",
            ]
        }
    )

    validator = DomainValidator(
        {
            "securities": {
                "security_type": SECURITY_TYPES,
            }
        }
    )

    result = validator.validate_dataset(
        "securities",
        dataframe,
    )

    assert result.valid is True


def test_invalid_security_type():
    dataframe = pd.DataFrame(
        {
            "security_type": [
                "EQUITY",
                "CRYPTO",
            ]
        }
    )

    validator = DomainValidator(
        {
            "securities": {
                "security_type": SECURITY_TYPES,
            }
        }
    )

    result = validator.validate_dataset(
        "securities",
        dataframe,
    )

    assert result.valid is False


def test_valid_security_status():
    dataframe = pd.DataFrame(
        {
            "status": [
                "ACTIVE",
                "INACTIVE",
            ]
        }
    )

    validator = DomainValidator(
        {
            "securities": {
                "status": SECURITY_STATUSES,
            }
        }
    )

    result = validator.validate_dataset(
        "securities",
        dataframe,
    )

    assert result.valid is True


def test_invalid_security_status():
    dataframe = pd.DataFrame(
        {
            "status": [
                "ACTIVE",
                "DELISTED",
            ]
        }
    )

    validator = DomainValidator(
        {
            "securities": {
                "status": SECURITY_STATUSES,
            }
        }
    )

    result = validator.validate_dataset(
        "securities",
        dataframe,
    )

    assert result.valid is False


# ---------------------------------------------------------------------------
# Null separation
# ---------------------------------------------------------------------------


def test_null_is_handled_by_null_validator():
    dataframe = pd.DataFrame(
        {
            "risk_profile": [
                "LOW",
                None,
            ]
        }
    )

    validator = DomainValidator(
        {
            "clients": {
                "risk_profile": RISK_PROFILES,
            }
        }
    )

    result = validator.validate_dataset(
        "clients",
        dataframe,
    )

    # Null is not a domain error.
    assert result.valid is True


# ---------------------------------------------------------------------------
# Blank separation
# ---------------------------------------------------------------------------


def test_blank_value_is_handled_by_null_validation():
    dataframe = pd.DataFrame(
        {
            "status": [
                "ACTIVE",
                "",
            ]
        }
    )

    validator = DomainValidator(
        {
            "clients": {
                "status": CLIENT_STATUSES,
            }
        }
    )

    result = validator.validate_dataset(
        "clients",
        dataframe,
    )

    assert result.valid is True


# ---------------------------------------------------------------------------
# Multiple invalid values
# ---------------------------------------------------------------------------


def test_multiple_invalid_domain_values():
    dataframe = pd.DataFrame(
        {
            "risk_profile": [
                "LOW",
                "INVALID_A",
                "HIGH",
                "INVALID_B",
            ]
        }
    )

    validator = DomainValidator(
        {
            "clients": {
                "risk_profile": RISK_PROFILES,
            }
        }
    )

    result = validator.validate_dataset(
        "clients",
        dataframe,
    )

    assert result.valid is False
    assert result.error_count == 2


# ---------------------------------------------------------------------------
# Unknown dataset
# ---------------------------------------------------------------------------


def test_dataset_without_domain_rules_is_valid():
    dataframe = pd.DataFrame(
        {
            "portfolio_id": [
                "P10001",
            ]
        }
    )

    validator = DomainValidator(
        {
            "clients": {
                "status": CLIENT_STATUSES,
            }
        }
    )

    result = validator.validate_dataset(
        "portfolios",
        dataframe,
    )

    assert result.valid is True


def test_non_dataframe_raises_error():
    validator = DomainValidator()

    with pytest.raises(
        DomainValidationError
    ):
        validator.validate_dataset(
            "clients",
            {
                "status": [
                    "ACTIVE"
                ]
            },
        )


def test_missing_domain_column_raises_error():
    dataframe = pd.DataFrame(
        {
            "other_column": [
                "ACTIVE",
            ]
        }
    )

    validator = DomainValidator(
        {
            "clients": {
                "status": CLIENT_STATUSES,
            }
        }
    )

    with pytest.raises(
        DomainValidationError
    ):
        validator.validate_dataset(
            "clients",
            dataframe,
        )


def test_empty_dataset_collection():
    validator = DomainValidator()

    with pytest.raises(
        DomainValidationError
    ):
        validator.validate_all({})


# ---------------------------------------------------------------------------
# Actual Participant 1 data
# ---------------------------------------------------------------------------


def test_actual_participant_data_has_valid_domains():
    loader = RawDataLoader()

    datasets = (
        loader.load_all_datasets()
    )

    validator = DomainValidator()

    results = validator.validate_all(
        datasets
    )

    for dataset_name, result in (
        results.items()
    ):
        assert result.valid is True, (
            f"{dataset_name} has domain errors: "
            f"{result.issues}"
        )


def test_actual_client_domains():
    loader = RawDataLoader()

    dataframe = loader.load_dataset(
        "clients"
    )

    validator = DomainValidator()

    result = validator.validate_dataset(
        "clients",
        dataframe,
    )

    assert result.valid is True


def test_actual_portfolio_domains():
    loader = RawDataLoader()

    dataframe = loader.load_dataset(
        "portfolios"
    )

    validator = DomainValidator()

    result = validator.validate_dataset(
        "portfolios",
        dataframe,
    )

    assert result.valid is True


def test_actual_security_domains():
    loader = RawDataLoader()

    dataframe = loader.load_dataset(
        "securities"
    )

    validator = DomainValidator()

    result = validator.validate_dataset(
        "securities",
        dataframe,
    )

    assert result.valid is True