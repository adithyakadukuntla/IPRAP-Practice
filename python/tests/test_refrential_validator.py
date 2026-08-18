"""
Tests for Phase 11 referential-integrity validation.
"""

import pandas as pd
import pytest

from python.validation.data_loader import (
    RawDataLoader,
)
from python.validation.referential_validator import (
    ReferentialValidationError,
    ReferentialValidator,
)


# =====================================================================
# Helper dataset factory
# =====================================================================


def make_valid_datasets():
    """Create a minimal valid relationship graph."""

    clients = pd.DataFrame(
        {
            "client_id": [
                "C001",
                "C002",
            ]
        }
    )

    portfolios = pd.DataFrame(
        {
            "portfolio_id": [
                "P001",
                "P002",
            ],
            "client_id": [
                "C001",
                "C002",
            ],
        }
    )

    securities = pd.DataFrame(
        {
            "security_id": [
                "S001",
                "S002",
            ]
        }
    )

    holdings = pd.DataFrame(
        {
            "holding_id": [
                "H001",
                "H002",
            ],
            "portfolio_id": [
                "P001",
                "P002",
            ],
            "security_id": [
                "S001",
                "S002",
            ],
        }
    )

    performance = pd.DataFrame(
        {
            "performance_id": [
                "PER001",
                "PER002",
            ],
            "portfolio_id": [
                "P001",
                "P002",
            ],
        }
    )

    return {
        "clients": clients,
        "portfolios": portfolios,
        "securities": securities,
        "holdings": holdings,
        "portfolio_performance": performance,
    }


# =====================================================================
# Valid relationship tests
# =====================================================================


def test_all_valid_relationships():
    datasets = make_valid_datasets()

    validator = ReferentialValidator()

    results = validator.validate(
        datasets
    )

    for result in results.values():
        assert result.valid is True
        assert result.error_count == 0


def test_existing_client_parent_is_valid():
    datasets = make_valid_datasets()

    validator = ReferentialValidator()

    result = validator.validate(
        datasets
    )["portfolios"]

    assert result.valid is True


def test_existing_portfolio_for_holding_is_valid():
    datasets = make_valid_datasets()

    validator = ReferentialValidator()

    result = validator.validate(
        datasets
    )["holdings"]

    assert result.valid is True


def test_existing_security_for_holding_is_valid():
    datasets = make_valid_datasets()

    validator = ReferentialValidator()

    result = validator.validate(
        datasets
    )["holdings"]

    assert result.valid is True


def test_existing_portfolio_for_performance_is_valid():
    datasets = make_valid_datasets()

    validator = ReferentialValidator()

    result = validator.validate(
        datasets
    )["portfolio_performance"]

    assert result.valid is True


# =====================================================================
# Missing client parent
# =====================================================================


def test_unknown_client_id_is_detected():
    datasets = make_valid_datasets()

    datasets["portfolios"].loc[
        0,
        "client_id",
    ] = "C999"

    validator = ReferentialValidator()

    results = validator.validate(
        datasets
    )

    result = results["portfolios"]

    assert result.valid is False
    assert result.error_count == 1

    issue = result.issues[0]

    assert issue.rule_id == "REF-001"
    assert issue.rule_name == (
        "PORTFOLIO_CLIENT_EXISTS"
    )
    assert issue.actual_value == "C999"
    assert issue.parent_dataset == "clients"
    assert issue.parent_column == "client_id"
    assert issue.severity == "ERROR"


# =====================================================================
# Missing portfolio parent
# =====================================================================


def test_unknown_portfolio_id_in_holdings_is_detected():
    datasets = make_valid_datasets()

    datasets["holdings"].loc[
        0,
        "portfolio_id",
    ] = "P999"

    validator = ReferentialValidator()

    results = validator.validate(
        datasets
    )

    result = results["holdings"]

    assert result.valid is False

    issues = [
        issue
        for issue in result.issues
        if issue.rule_id == "REF-002"
    ]

    assert len(issues) == 1
    assert issues[0].actual_value == "P999"
    assert (
        issues[0].parent_dataset
        == "portfolios"
    )


# =====================================================================
# Missing security parent
# =====================================================================


def test_unknown_security_id_in_holdings_is_detected():
    datasets = make_valid_datasets()

    datasets["holdings"].loc[
        0,
        "security_id",
    ] = "S999"

    validator = ReferentialValidator()

    results = validator.validate(
        datasets
    )

    result = results["holdings"]

    assert result.valid is False

    issues = [
        issue
        for issue in result.issues
        if issue.rule_id == "REF-003"
    ]

    assert len(issues) == 1
    assert issues[0].actual_value == "S999"
    assert (
        issues[0].parent_dataset
        == "securities"
    )


# =====================================================================
# Missing performance portfolio parent
# =====================================================================


def test_unknown_portfolio_id_in_performance_is_detected():
    datasets = make_valid_datasets()

    datasets[
        "portfolio_performance"
    ].loc[
        0,
        "portfolio_id",
    ] = "P999"

    validator = ReferentialValidator()

    results = validator.validate(
        datasets
    )

    result = results[
        "portfolio_performance"
    ]

    assert result.valid is False

    issue = result.issues[0]

    assert issue.rule_id == "REF-004"
    assert issue.actual_value == "P999"
    assert (
        issue.parent_dataset
        == "portfolios"
    )


# =====================================================================
# Multiple missing references
# =====================================================================


def test_multiple_missing_references_are_all_reported():
    datasets = make_valid_datasets()

    datasets["portfolios"].loc[
        0,
        "client_id",
    ] = "C999"

    datasets["portfolios"].loc[
        1,
        "client_id",
    ] = "C998"

    validator = ReferentialValidator()

    results = validator.validate(
        datasets
    )

    result = results["portfolios"]

    assert result.valid is False
    assert result.error_count == 2

    actual_values = {
        issue.actual_value
        for issue in result.issues
    }

    assert actual_values == {
        "C999",
        "C998",
    }


def test_multiple_holding_relationship_errors():
    datasets = make_valid_datasets()

    datasets["holdings"].loc[
        0,
        "portfolio_id",
    ] = "P999"

    datasets["holdings"].loc[
        1,
        "security_id",
    ] = "S999"

    validator = ReferentialValidator()

    results = validator.validate(
        datasets
    )

    result = results["holdings"]

    assert result.valid is False
    assert result.error_count == 2

    rule_ids = {
        issue.rule_id
        for issue in result.issues
    }

    assert rule_ids == {
        "REF-002",
        "REF-003",
    }


# =====================================================================
# Null separation
# =====================================================================


def test_null_client_id_is_not_reported_as_referential_error():
    datasets = make_valid_datasets()

    datasets["portfolios"].loc[
        0,
        "client_id",
    ] = None

    validator = ReferentialValidator()

    results = validator.validate(
        datasets
    )

    result = results["portfolios"]

    assert result.valid is True
    assert result.error_count == 0


def test_blank_client_id_is_not_reported_as_referential_error():
    datasets = make_valid_datasets()

    datasets["portfolios"].loc[
        0,
        "client_id",
    ] = ""

    validator = ReferentialValidator()

    results = validator.validate(
        datasets
    )

    result = results["portfolios"]

    assert result.valid is True
    assert result.error_count == 0


# =====================================================================
# Parent duplicates
# =====================================================================


def test_existing_parent_remains_valid_if_parent_has_duplicate_ids():
    datasets = make_valid_datasets()

    datasets["clients"] = pd.DataFrame(
        {
            "client_id": [
                "C001",
                "C001",
                "C002",
            ]
        }
    )

    validator = ReferentialValidator()

    results = validator.validate(
        datasets
    )

    assert results[
        "portfolios"
    ].valid is True


# =====================================================================
# Unknown dataset
# =====================================================================


def test_missing_child_dataset_raises_error():
    datasets = make_valid_datasets()

    del datasets["portfolios"]

    validator = ReferentialValidator()

    with pytest.raises(
        ReferentialValidationError
    ):
        validator.validate(
            datasets
        )


def test_missing_parent_dataset_raises_error():
    datasets = make_valid_datasets()

    del datasets["clients"]

    validator = ReferentialValidator()

    with pytest.raises(
        ReferentialValidationError
    ):
        validator.validate(
            datasets
        )


def test_missing_child_column_raises_error():
    datasets = make_valid_datasets()

    datasets["portfolios"] = pd.DataFrame(
        {
            "portfolio_id": [
                "P001",
            ]
        }
    )

    validator = ReferentialValidator()

    with pytest.raises(
        ReferentialValidationError
    ):
        validator.validate(
            datasets
        )


def test_missing_parent_column_raises_error():
    datasets = make_valid_datasets()

    datasets["clients"] = pd.DataFrame(
        {
            "wrong_column": [
                "C001",
            ]
        }
    )

    validator = ReferentialValidator()

    with pytest.raises(
        ReferentialValidationError
    ):
        validator.validate(
            datasets
        )


# =====================================================================
# Empty datasets
# =====================================================================


def test_empty_dataset_collection_raises_error():
    validator = ReferentialValidator()

    with pytest.raises(
        ReferentialValidationError
    ):
        validator.validate({})


# =====================================================================
# Convenience methods
# =====================================================================


def test_is_valid_returns_true_for_valid_data():
    datasets = make_valid_datasets()

    validator = ReferentialValidator()

    assert (
        validator.is_valid(
            datasets
        )
        is True
    )


def test_is_valid_returns_false_for_invalid_data():
    datasets = make_valid_datasets()

    datasets["holdings"].loc[
        0,
        "security_id",
    ] = "UNKNOWN"

    validator = ReferentialValidator()

    assert (
        validator.is_valid(
            datasets
        )
        is False
    )


def test_get_all_issues():
    datasets = make_valid_datasets()

    datasets["portfolios"].loc[
        0,
        "client_id",
    ] = "UNKNOWN_CLIENT"

    datasets["holdings"].loc[
        0,
        "security_id",
    ] = "UNKNOWN_SECURITY"

    validator = ReferentialValidator()

    issues = validator.get_all_issues(
        datasets
    )

    assert len(issues) == 2

    rule_ids = {
        issue.rule_id
        for issue in issues
    }

    assert "REF-001" in rule_ids
    assert "REF-003" in rule_ids


# =====================================================================
# Actual Participant 1 data
# =====================================================================


def test_actual_participant_data_referential_integrity():
    loader = RawDataLoader()

    datasets = (
        loader.load_all_datasets()
    )

    validator = ReferentialValidator()

    results = validator.validate(
        datasets
    )

    for dataset_name, result in (
        results.items()
    ):
        assert result.valid is True, (
            f"{dataset_name} has referential "
            f"integrity errors: "
            f"{result.issues}"
        )