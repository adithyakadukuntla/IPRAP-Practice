"""
Tests for Phase 12 data standardization.
"""

import pandas as pd
import pytest

from python.validation.standardizer import (
    DataStandardizer,
    StandardizationError,
)


# =====================================================================
# Basic controlled-vocabulary standardization
# =====================================================================


def test_risk_profile_lowercase_becomes_uppercase():

    dataframe = pd.DataFrame(
        {
            "client_id": ["C10001"],
            "client_type": ["INDIVIDUAL"],
            "risk_profile": ["high"],
            "status": ["ACTIVE"],
        }
    )

    result = DataStandardizer().standardize_dataset(
        "clients",
        dataframe,
    )

    assert result.loc[
        0,
        "risk_profile",
    ] == "HIGH"


def test_risk_profile_mixed_case_becomes_uppercase():

    dataframe = pd.DataFrame(
        {
            "client_id": ["C10001"],
            "client_type": ["Individual"],
            "risk_profile": ["High"],
            "status": ["Active"],
        }
    )

    result = DataStandardizer().standardize_dataset(
        "clients",
        dataframe,
    )

    assert result.loc[
        0,
        "client_type",
    ] == "INDIVIDUAL"

    assert result.loc[
        0,
        "risk_profile",
    ] == "HIGH"

    assert result.loc[
        0,
        "status",
    ] == "ACTIVE"


def test_leading_and_trailing_whitespace_is_removed():

    dataframe = pd.DataFrame(
        {
            "client_id": ["C10001"],
            "client_type": [
                "  individual  "
            ],
            "risk_profile": [
                "  high  "
            ],
            "status": [
                "  active  "
            ],
        }
    )

    result = DataStandardizer().standardize_dataset(
        "clients",
        dataframe,
    )

    assert result.loc[
        0,
        "client_type",
    ] == "INDIVIDUAL"

    assert result.loc[
        0,
        "risk_profile",
    ] == "HIGH"

    assert result.loc[
        0,
        "status",
    ] == "ACTIVE"


# =====================================================================
# Portfolio standardization
# =====================================================================


def test_portfolio_controlled_values_are_standardized():

    dataframe = pd.DataFrame(
        {
            "portfolio_id": ["P10001"],
            "portfolio_type": [
                " balanced "
            ],
            "base_currency": [
                " inr "
            ],
            "risk_profile": [
                " medium "
            ],
            "status": [
                " active "
            ],
        }
    )

    result = DataStandardizer().standardize_dataset(
        "portfolios",
        dataframe,
    )

    assert result.loc[
        0,
        "portfolio_type",
    ] == "BALANCED"

    assert result.loc[
        0,
        "base_currency",
    ] == "INR"

    assert result.loc[
        0,
        "risk_profile",
    ] == "MEDIUM"

    assert result.loc[
        0,
        "status",
    ] == "ACTIVE"


# =====================================================================
# Security standardization
# =====================================================================


def test_security_controlled_values_are_standardized():

    dataframe = pd.DataFrame(
        {
            "security_id": ["SEC10001"],
            "security_type": [" equity "],
            "currency": [" usd "],
            "status": [" active "],
        }
    )

    result = DataStandardizer().standardize_dataset(
        "securities",
        dataframe,
    )

    assert result.loc[
        0,
        "security_type",
    ] == "EQUITY"

    assert result.loc[
        0,
        "currency",
    ] == "USD"

    assert result.loc[
        0,
        "status",
    ] == "ACTIVE"


# =====================================================================
# Date standardization
# =====================================================================


def test_client_created_date_is_standardized():

    dataframe = pd.DataFrame(
        {
            "client_id": ["C10001"],
            "created_date": [
                "2026-08-05"
            ],
        }
    )

    result = DataStandardizer().standardize_dataset(
        "clients",
        dataframe,
    )

    assert result.loc[
        0,
        "created_date",
    ] == "2026-08-05"


def test_portfolio_inception_date_is_standardized():

    dataframe = pd.DataFrame(
        {
            "portfolio_id": ["P10001"],
            "inception_date": [
                "2026-08-05"
            ],
        }
    )

    result = DataStandardizer().standardize_dataset(
        "portfolios",
        dataframe,
    )

    assert result.loc[
        0,
        "inception_date",
    ] == "2026-08-05"


def test_holding_as_of_date_is_standardized():

    dataframe = pd.DataFrame(
        {
            "holding_id": ["H100001"],
            "as_of_date": [
                "2026-08-05"
            ],
        }
    )

    result = DataStandardizer().standardize_dataset(
        "holdings",
        dataframe,
    )

    assert result.loc[
        0,
        "as_of_date",
    ] == "2026-08-05"


def test_performance_as_of_date_is_standardized():

    dataframe = pd.DataFrame(
        {
            "performance_id": ["PER001"],
            "as_of_date": [
                "2026-08-05"
            ],
        }
    )

    result = DataStandardizer().standardize_dataset(
        "portfolio_performance",
        dataframe,
    )

    assert result.loc[
        0,
        "as_of_date",
    ] == "2026-08-05"


# =====================================================================
# IDs must NOT be changed
# =====================================================================


def test_client_id_is_not_modified():

    dataframe = pd.DataFrame(
        {
            "client_id": [" C10001 "],
            "client_type": ["individual"],
            "risk_profile": ["high"],
            "status": ["active"],
        }
    )

    result = DataStandardizer().standardize_dataset(
        "clients",
        dataframe,
    )

    # Whitespace is removed, but no ID format is invented.
    assert result.loc[
        0,
        "client_id",
    ] == "C10001"


def test_portfolio_id_format_is_not_rewritten():

    dataframe = pd.DataFrame(
        {
            "portfolio_id": ["P10001"],
            "portfolio_type": [
                "balanced"
            ],
            "base_currency": ["USD"],
            "risk_profile": ["high"],
            "status": ["active"],
        }
    )

    result = DataStandardizer().standardize_dataset(
        "portfolios",
        dataframe,
    )

    assert result.loc[
        0,
        "portfolio_id",
    ] == "P10001"


def test_security_id_format_is_not_rewritten():

    dataframe = pd.DataFrame(
        {
            "security_id": ["SEC10001"],
            "security_type": ["equity"],
            "currency": ["usd"],
            "status": ["active"],
        }
    )

    result = DataStandardizer().standardize_dataset(
        "securities",
        dataframe,
    )

    assert result.loc[
        0,
        "security_id",
    ] == "SEC10001"


# =====================================================================
# Business values must not be changed
# =====================================================================


def test_numeric_business_values_are_not_changed():

    dataframe = pd.DataFrame(
        {
            "holding_id": ["H100001"],
            "portfolio_id": ["P10001"],
            "security_id": ["SEC10001"],
            "quantity": [-100],
            "purchase_price": [100.50],
            "current_price": [110.25],
            "market_value": [123.45],
            "as_of_date": [
                "2026-08-05"
            ],
        }
    )

    result = DataStandardizer().standardize_dataset(
        "holdings",
        dataframe,
    )

    assert result.loc[
        0,
        "quantity",
    ] == -100

    assert result.loc[
        0,
        "purchase_price",
    ] == 100.50

    assert result.loc[
        0,
        "current_price",
    ] == 110.25

    assert result.loc[
        0,
        "market_value",
    ] == 123.45


# =====================================================================
# Raw data must never be modified
# =====================================================================


def test_standardization_does_not_modify_input():

    dataframe = pd.DataFrame(
        {
            "client_id": ["C10001"],
            "client_type": [
                " individual "
            ],
            "risk_profile": [
                " high "
            ],
            "status": [
                " active "
            ],
        }
    )

    original = dataframe.copy(
        deep=True
    )

    result = DataStandardizer().standardize_dataset(
        "clients",
        dataframe,
    )

    pd.testing.assert_frame_equal(
        dataframe,
        original,
    )

    assert result.loc[
        0,
        "risk_profile",
    ] == "HIGH"


# =====================================================================
# Deep-copy behavior
# =====================================================================


def test_result_is_independent_from_input():

    dataframe = pd.DataFrame(
        {
            "client_id": ["C10001"],
            "client_type": ["individual"],
            "risk_profile": ["high"],
            "status": ["active"],
        }
    )

    result = DataStandardizer().standardize_dataset(
        "clients",
        dataframe,
    )

    result.loc[
        0,
        "risk_profile",
    ] = "LOW"

    assert dataframe.loc[
        0,
        "risk_profile",
    ] == "high"


# =====================================================================
# Null values
# =====================================================================


def test_null_controlled_value_remains_null():

    dataframe = pd.DataFrame(
        {
            "client_id": ["C10001"],
            "client_type": ["individual"],
            "risk_profile": [None],
            "status": ["active"],
        }
    )

    result = DataStandardizer().standardize_dataset(
        "clients",
        dataframe,
    )

    assert pd.isna(
        result.loc[
            0,
            "risk_profile",
        ]
    )


# =====================================================================
# All datasets
# =====================================================================


def test_standardize_all_datasets():

    datasets = {
        "clients": pd.DataFrame(
            {
                "client_id": ["C10001"],
                "client_type": ["individual"],
                "risk_profile": ["high"],
                "status": ["active"],
                "created_date": [
                    "2026-08-01"
                ],
            }
        ),
        "portfolios": pd.DataFrame(
            {
                "portfolio_id": ["P10001"],
                "portfolio_type": [
                    "balanced"
                ],
                "base_currency": ["usd"],
                "risk_profile": ["medium"],
                "status": ["active"],
                "inception_date": [
                    "2026-08-01"
                ],
            }
        ),
        "securities": pd.DataFrame(
            {
                "security_id": ["SEC10001"],
                "security_type": ["equity"],
                "currency": ["usd"],
                "status": ["active"],
            }
        ),
        "holdings": pd.DataFrame(
            {
                "holding_id": ["H100001"],
                "as_of_date": [
                    "2026-08-01"
                ],
            }
        ),
        "portfolio_performance": pd.DataFrame(
            {
                "performance_id": ["PER001"],
                "as_of_date": [
                    "2026-08-01"
                ],
            }
        ),
    }

    result = DataStandardizer().standardize_all(
        datasets
    )

    assert (
        result["clients"].loc[
            0,
            "risk_profile",
        ]
        == "HIGH"
    )

    assert (
        result["portfolios"].loc[
            0,
            "base_currency",
        ]
        == "USD"
    )

    assert (
        result["securities"].loc[
            0,
            "security_type",
        ]
        == "EQUITY"
    )


# =====================================================================
# Invalid input
# =====================================================================


def test_invalid_dataframe_raises_error():

    validator = DataStandardizer()

    with pytest.raises(
        StandardizationError
    ):
        validator.standardize_dataset(
            "clients",
            None,
        )


def test_missing_configured_column_raises_error():

    dataframe = pd.DataFrame(
        {
            "client_id": ["C10001"],
        }
    )

    validator = DataStandardizer()

    with pytest.raises(
        StandardizationError
    ):
        validator.standardize_dataset(
            "clients",
            dataframe,
        )


def test_empty_dataset_collection_raises_error():

    validator = DataStandardizer()

    with pytest.raises(
        StandardizationError
    ):
        validator.standardize_all({})