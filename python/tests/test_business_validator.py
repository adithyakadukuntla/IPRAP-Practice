"""
Tests for Phase 10 business validation.
"""

from datetime import date

import pandas as pd
import pytest

from python.validation.business_validator import (
    BusinessValidationError,
    BusinessValidator,
)


# =====================================================================
# Portfolio tests
# =====================================================================


def test_valid_portfolio_values():
    dataframe = pd.DataFrame(
        {
            "initial_value": [
                100000,
            ],
            "current_value": [
                110000,
            ],
            "inception_date": [
                "2026-01-01",
            ],
        }
    )

    validator = BusinessValidator()

    result = validator.validate_dataset(
        "portfolios",
        dataframe,
        current_business_date=date(
            2026,
            8,
            15,
        ),
    )

    assert result.valid is True
    assert result.error_count == 0


def test_negative_initial_portfolio_value():
    dataframe = pd.DataFrame(
        {
            "initial_value": [
                -1000,
            ],
            "current_value": [
                100000,
            ],
            "inception_date": [
                "2026-01-01",
            ],
        }
    )

    validator = BusinessValidator()

    result = validator.validate_dataset(
        "portfolios",
        dataframe,
        current_business_date=date(
            2026,
            8,
            15,
        ),
    )

    assert result.valid is False
    assert result.error_count == 1
    assert (
        result.issues[0].rule_id
        == "POR-004"
    )


def test_negative_current_portfolio_value():
    dataframe = pd.DataFrame(
        {
            "initial_value": [
                100000,
            ],
            "current_value": [
                -500,
            ],
            "inception_date": [
                "2026-01-01",
            ],
        }
    )

    validator = BusinessValidator()

    result = validator.validate_dataset(
        "portfolios",
        dataframe,
        current_business_date=date(
            2026,
            8,
            15,
        ),
    )

    assert result.valid is False
    assert result.error_count == 1
    assert (
        result.issues[0].rule_id
        == "POR-005"
    )


def test_zero_portfolio_value_is_allowed():
    dataframe = pd.DataFrame(
        {
            "initial_value": [
                0,
            ],
            "current_value": [
                0,
            ],
            "inception_date": [
                "2026-01-01",
            ],
        }
    )

    validator = BusinessValidator()

    result = validator.validate_dataset(
        "portfolios",
        dataframe,
        current_business_date=date(
            2026,
            8,
            15,
        ),
    )

    assert result.valid is True


def test_future_inception_date():
    dataframe = pd.DataFrame(
        {
            "initial_value": [
                100000,
            ],
            "current_value": [
                110000,
            ],
            "inception_date": [
                "2026-12-31",
            ],
        }
    )

    validator = BusinessValidator()

    result = validator.validate_dataset(
        "portfolios",
        dataframe,
        current_business_date=date(
            2026,
            8,
            15,
        ),
    )

    assert result.valid is False

    assert (
        result.issues[0].rule_id
        == "POR-006"
    )


def test_inception_date_on_business_date_is_valid():
    dataframe = pd.DataFrame(
        {
            "initial_value": [
                100000,
            ],
            "current_value": [
                100000,
            ],
            "inception_date": [
                "2026-08-15",
            ],
        }
    )

    validator = BusinessValidator()

    result = validator.validate_dataset(
        "portfolios",
        dataframe,
        current_business_date=date(
            2026,
            8,
            15,
        ),
    )

    assert result.valid is True


# =====================================================================
# Security tests
# =====================================================================


def test_positive_security_price():
    dataframe = pd.DataFrame(
        {
            "current_price": [
                125.50,
            ]
        }
    )

    validator = BusinessValidator()

    result = validator.validate_dataset(
        "securities",
        dataframe,
    )

    assert result.valid is True


def test_zero_security_price():
    dataframe = pd.DataFrame(
        {
            "current_price": [
                0,
            ]
        }
    )

    validator = BusinessValidator()

    result = validator.validate_dataset(
        "securities",
        dataframe,
    )

    assert result.valid is False
    assert result.error_count == 1
    assert (
        result.issues[0].rule_id
        == "SEC-003"
    )


def test_negative_security_price():
    dataframe = pd.DataFrame(
        {
            "current_price": [
                -25,
            ]
        }
    )

    validator = BusinessValidator()

    result = validator.validate_dataset(
        "securities",
        dataframe,
    )

    assert result.valid is False


# =====================================================================
# Holdings tests
# =====================================================================


def test_valid_holding():
    dataframe = pd.DataFrame(
        {
            "quantity": [
                100,
            ],
            "purchase_price": [
                45,
            ],
            "current_price": [
                50,
            ],
            "market_value": [
                5000,
            ],
        }
    )

    validator = BusinessValidator()

    result = validator.validate_dataset(
        "holdings",
        dataframe,
    )

    assert result.valid is True


def test_negative_holding_quantity():
    dataframe = pd.DataFrame(
        {
            "quantity": [
                -100,
            ],
            "purchase_price": [
                45,
            ],
            "current_price": [
                50,
            ],
            "market_value": [
                5000,
            ],
        }
    )

    validator = BusinessValidator()

    result = validator.validate_dataset(
        "holdings",
        dataframe,
    )

    assert result.valid is False
    assert any(
        issue.rule_id == "HLD-003"
        for issue in result.issues
    )


def test_zero_holding_quantity():
    dataframe = pd.DataFrame(
        {
            "quantity": [
                0,
            ],
            "purchase_price": [
                45,
            ],
            "current_price": [
                50,
            ],
            "market_value": [
                0,
            ],
        }
    )

    validator = BusinessValidator()

    result = validator.validate_dataset(
        "holdings",
        dataframe,
    )

    assert result.valid is False


def test_negative_purchase_price():
    dataframe = pd.DataFrame(
        {
            "quantity": [
                100,
            ],
            "purchase_price": [
                -45,
            ],
            "current_price": [
                50,
            ],
            "market_value": [
                5000,
            ],
        }
    )

    validator = BusinessValidator()

    result = validator.validate_dataset(
        "holdings",
        dataframe,
    )

    assert result.valid is False


def test_zero_current_price():
    dataframe = pd.DataFrame(
        {
            "quantity": [
                100,
            ],
            "purchase_price": [
                45,
            ],
            "current_price": [
                0,
            ],
            "market_value": [
                5000,
            ],
        }
    )

    validator = BusinessValidator()

    result = validator.validate_dataset(
        "holdings",
        dataframe,
    )

    assert result.valid is False


def test_correct_market_value():
    dataframe = pd.DataFrame(
        {
            "quantity": [
                100,
            ],
            "purchase_price": [
                45,
            ],
            "current_price": [
                50,
            ],
            "market_value": [
                5000,
            ],
        }
    )

    validator = BusinessValidator()

    result = validator.validate_dataset(
        "holdings",
        dataframe,
    )

    assert result.valid is True


def test_market_value_within_one_percent():
    dataframe = pd.DataFrame(
        {
            "quantity": [
                100,
            ],
            "purchase_price": [
                45,
            ],
            "current_price": [
                50,
            ],
            "market_value": [
                5025,
            ],
        }
    )

    validator = BusinessValidator()

    result = validator.validate_dataset(
        "holdings",
        dataframe,
    )

    assert result.valid is True


def test_incorrect_market_value():
    dataframe = pd.DataFrame(
        {
            "quantity": [
                100,
            ],
            "purchase_price": [
                45,
            ],
            "current_price": [
                50,
            ],
            "market_value": [
                500000,
            ],
        }
    )

    validator = BusinessValidator()

    result = validator.validate_dataset(
        "holdings",
        dataframe,
    )

    assert result.valid is False

    assert any(
        issue.rule_id == "HLD-006"
        for issue in result.issues
    )


# =====================================================================
# Performance tests
# =====================================================================


def test_valid_performance_calculation():
    dataframe = pd.DataFrame(
        {
            "beginning_value": [
                1000000,
            ],
            "ending_value": [
                1080000,
            ],
            "return_amount": [
                80000,
            ],
            "return_percent": [
                8.0,
            ],
        }
    )

    validator = BusinessValidator()

    result = validator.validate_dataset(
        "portfolio_performance",
        dataframe,
    )

    assert result.valid is True


def test_negative_beginning_value():
    dataframe = pd.DataFrame(
        {
            "beginning_value": [
                -100000,
            ],
            "ending_value": [
                100000,
            ],
            "return_amount": [
                200000,
            ],
            "return_percent": [
                -200,
            ],
        }
    )

    validator = BusinessValidator()

    result = validator.validate_dataset(
        "portfolio_performance",
        dataframe,
    )

    assert result.valid is False


def test_negative_ending_value():
    dataframe = pd.DataFrame(
        {
            "beginning_value": [
                100000,
            ],
            "ending_value": [
                -50000,
            ],
            "return_amount": [
                -150000,
            ],
            "return_percent": [
                -150,
            ],
        }
    )

    validator = BusinessValidator()

    result = validator.validate_dataset(
        "portfolio_performance",
        dataframe,
    )

    assert result.valid is False


def test_incorrect_return_amount():
    dataframe = pd.DataFrame(
        {
            "beginning_value": [
                1000000,
            ],
            "ending_value": [
                1080000,
            ],
            "return_amount": [
                10000,
            ],
            "return_percent": [
                1.0,
            ],
        }
    )

    validator = BusinessValidator()

    result = validator.validate_dataset(
        "portfolio_performance",
        dataframe,
    )

    assert result.valid is False

    assert any(
        issue.rule_id == "PER-005"
        for issue in result.issues
    )


def test_incorrect_return_percent():
    dataframe = pd.DataFrame(
        {
            "beginning_value": [
                1000000,
            ],
            "ending_value": [
                1080000,
            ],
            "return_amount": [
                80000,
            ],
            "return_percent": [
                20.0,
            ],
        }
    )

    validator = BusinessValidator()

    result = validator.validate_dataset(
        "portfolio_performance",
        dataframe,
    )

    assert result.valid is False

    assert any(
        issue.rule_id == "PER-006"
        for issue in result.issues
    )


def test_return_percent_rounding_is_allowed():
    dataframe = pd.DataFrame(
        {
            "beginning_value": [
                1000000,
            ],
            "ending_value": [
                1080000,
            ],
            "return_amount": [
                80000,
            ],
            "return_percent": [
                8.04,
            ],
        }
    )

    validator = BusinessValidator()

    result = validator.validate_dataset(
        "portfolio_performance",
        dataframe,
    )

    assert result.valid is True


def test_zero_beginning_value_does_not_divide_by_zero():
    dataframe = pd.DataFrame(
        {
            "beginning_value": [
                0,
            ],
            "ending_value": [
                100,
            ],
            "return_amount": [
                100,
            ],
            "return_percent": [
                0,
            ],
        }
    )

    validator = BusinessValidator()

    result = validator.validate_dataset(
        "portfolio_performance",
        dataframe,
    )

    # The return-percent rule cannot be evaluated when beginning
    # value is zero. The project does not define an additional
    # beginning_value > 0 rule.
    assert result.valid is True


# =====================================================================
# Separation / framework tests
# =====================================================================


def test_clients_have_no_phase_10_rules():
    dataframe = pd.DataFrame(
        {
            "client_id": [
                "C10001",
            ]
        }
    )

    validator = BusinessValidator()

    result = validator.validate_dataset(
        "clients",
        dataframe,
    )

    assert result.valid is True
    assert result.error_count == 0


def test_missing_business_column_raises_error():
    dataframe = pd.DataFrame(
        {
            "quantity": [
                100,
            ]
        }
    )

    validator = BusinessValidator()

    with pytest.raises(
        BusinessValidationError
    ):
        validator.validate_dataset(
            "holdings",
            dataframe,
        )


def test_non_dataframe_raises_error():
    validator = BusinessValidator()

    with pytest.raises(
        BusinessValidationError
    ):
        validator.validate_dataset(
            "holdings",
            {
                "quantity": [100]
            },
        )


def test_empty_dataset_collection_raises_error():
    validator = BusinessValidator()

    with pytest.raises(
        BusinessValidationError
    ):
        validator.validate_all({})