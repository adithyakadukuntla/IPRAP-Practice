"""
Tests for Phase 13 — Rejected Record Processing.
"""

from pathlib import Path

import pandas as pd
import pytest

from python.validation.rejection_processor import (
    RejectionProcessingError,
    RejectionProcessor,
)


# =====================================================================
# Test issue helper
# =====================================================================


class FakeIssue:
    """Simple validation issue for unit tests."""

    def __init__(
        self,
        row_index,
        column_name,
        rule_id,
        severity="ERROR",
        message="Validation failed",
    ):
        self.row_index = row_index
        self.column_name = column_name
        self.rule_id = rule_id
        self.severity = severity
        self.message = message


class FakeValidationResult:
    """Simple validator-result wrapper."""

    def __init__(self, issues):
        self.issues = issues


# =====================================================================
# Dataset helper
# =====================================================================


def make_clients():
    return pd.DataFrame(
        {
            "client_id": [
                "C001",
                "C002",
                "C003",
            ],
            "client_type": [
                "INDIVIDUAL",
                "INSTITUTIONAL",
                "INDIVIDUAL",
            ],
            "risk_profile": [
                "LOW",
                "MEDIUM",
                "HIGH",
            ],
            "status": [
                "ACTIVE",
                "ACTIVE",
                "ACTIVE",
            ],
        }
    )


# =====================================================================
# Basic separation
# =====================================================================


def test_all_records_are_valid_when_no_errors_exist():

    dataframe = make_clients()

    processor = RejectionProcessor()

    result = processor.process_dataset(
        "clients",
        dataframe,
        [],
    )

    assert result.total_records == 3
    assert result.valid_records == 3
    assert result.invalid_records == 0

    assert len(
        result.valid_dataframe
    ) == 3

    assert len(
        result.rejected_dataframe
    ) == 0


def test_error_record_is_rejected():

    dataframe = make_clients()

    issue = FakeIssue(
        row_index=1,
        column_name="risk_profile",
        rule_id="CLI-003",
        message="Invalid risk profile",
    )

    processor = RejectionProcessor()

    result = processor.process_dataset(
        "clients",
        dataframe,
        [issue],
    )

    assert result.total_records == 3
    assert result.valid_records == 2
    assert result.invalid_records == 1

    assert (
        result.rejected_dataframe.iloc[
            0
        ]["client_id"]
        == "C002"
    )


def test_valid_records_are_preserved_exactly():

    dataframe = make_clients()

    issue = FakeIssue(
        row_index=1,
        column_name="risk_profile",
        rule_id="CLI-003",
    )

    processor = RejectionProcessor()

    result = processor.process_dataset(
        "clients",
        dataframe,
        [issue],
    )

    expected = dataframe.drop(
        index=[1]
    )

    pd.testing.assert_frame_equal(
        result.valid_dataframe,
        expected,
    )


def test_rejected_record_is_preserved_exactly():

    dataframe = make_clients()

    issue = FakeIssue(
        row_index=1,
        column_name="risk_profile",
        rule_id="CLI-003",
    )

    processor = RejectionProcessor()

    result = processor.process_dataset(
        "clients",
        dataframe,
        [issue],
    )

    expected = dataframe.loc[
        [1]
    ]

    pd.testing.assert_frame_equal(
        result.rejected_dataframe,
        expected,
    )


# =====================================================================
# Multiple invalid records
# =====================================================================


def test_multiple_invalid_records_are_rejected():

    dataframe = make_clients()

    issues = [
        FakeIssue(
            row_index=0,
            column_name="risk_profile",
            rule_id="CLI-003",
        ),
        FakeIssue(
            row_index=2,
            column_name="status",
            rule_id="CLI-004",
        ),
    ]

    processor = RejectionProcessor()

    result = processor.process_dataset(
        "clients",
        dataframe,
        issues,
    )

    assert result.total_records == 3
    assert result.valid_records == 1
    assert result.invalid_records == 2

    assert list(
        result.rejected_dataframe[
            "client_id"
        ]
    ) == [
        "C001",
        "C003",
    ]


# =====================================================================
# Multiple errors on same row
# =====================================================================


def test_multiple_errors_on_same_row_reject_only_one_record():

    dataframe = make_clients()

    issues = [
        FakeIssue(
            row_index=1,
            column_name="risk_profile",
            rule_id="CLI-003",
        ),
        FakeIssue(
            row_index=1,
            column_name="status",
            rule_id="CLI-004",
        ),
    ]

    processor = RejectionProcessor()

    result = processor.process_dataset(
        "clients",
        dataframe,
        issues,
    )

    assert result.invalid_records == 1
    assert result.valid_records == 2


# =====================================================================
# Warnings
# =====================================================================


def test_warning_does_not_reject_record():

    dataframe = make_clients()

    issue = FakeIssue(
        row_index=1,
        column_name="status",
        rule_id="CLI-W001",
        severity="WARNING",
        message="Inactive client",
    )

    processor = RejectionProcessor()

    result = processor.process_dataset(
        "clients",
        dataframe,
        [issue],
    )

    assert result.valid_records == 3
    assert result.invalid_records == 0


def test_mixed_warning_and_error_rejects_record():

    dataframe = make_clients()

    issues = [
        FakeIssue(
            row_index=1,
            column_name="status",
            rule_id="CLI-W001",
            severity="WARNING",
        ),
        FakeIssue(
            row_index=1,
            column_name="risk_profile",
            rule_id="CLI-003",
            severity="ERROR",
        ),
    ]

    processor = RejectionProcessor()

    result = processor.process_dataset(
        "clients",
        dataframe,
        issues,
    )

    assert result.invalid_records == 1


# =====================================================================
# Raw data preservation
# =====================================================================


def test_processing_does_not_modify_raw_dataframe():

    dataframe = make_clients()

    original = dataframe.copy(
        deep=True
    )

    issue = FakeIssue(
        row_index=1,
        column_name="risk_profile",
        rule_id="CLI-003",
    )

    processor = RejectionProcessor()

    processor.process_dataset(
        "clients",
        dataframe,
        [issue],
    )

    pd.testing.assert_frame_equal(
        dataframe,
        original,
    )


def test_result_is_independent_from_source():

    dataframe = make_clients()

    issue = FakeIssue(
        row_index=1,
        column_name="risk_profile",
        rule_id="CLI-003",
    )

    processor = RejectionProcessor()

    result = processor.process_dataset(
        "clients",
        dataframe,
        [issue],
    )

    result.valid_dataframe.loc[
        0,
        "risk_profile",
    ] = "HIGH"

    assert dataframe.loc[
        0,
        "risk_profile",
    ] == "LOW"


# =====================================================================
# Issue extraction
# =====================================================================


def test_validation_result_wrapper_is_supported():

    dataframe = make_clients()

    validation_result = FakeValidationResult(
        [
            FakeIssue(
                row_index=0,
                column_name="status",
                rule_id="CLI-004",
            )
        ]
    )

    processor = RejectionProcessor()

    result = processor.process_dataset(
        "clients",
        dataframe,
        validation_result,
    )

    assert result.invalid_records == 1


def test_none_validation_result_means_no_errors():

    dataframe = make_clients()

    processor = RejectionProcessor()

    result = processor.process_dataset(
        "clients",
        dataframe,
        None,
    )

    assert result.invalid_records == 0


# =====================================================================
# Validation error report
# =====================================================================


def test_validation_error_dataframe_contains_required_columns():

    dataframe = make_clients()

    validation_results = {
        "clients": FakeValidationResult(
            [
                FakeIssue(
                    row_index=1,
                    column_name="risk_profile",
                    rule_id="CLI-003",
                    message="Invalid risk profile",
                )
            ]
        )
    }

    processor = RejectionProcessor()

    errors = (
        processor.build_validation_error_dataframe(
            {"clients": dataframe},
            validation_results,
        )
    )

    expected_columns = [
        "dataset_name",
        "record_identifier",
        "row_index",
        "column_name",
        "rule_id",
        "severity",
        "error_message",
    ]

    assert list(
        errors.columns
    ) == expected_columns


def test_validation_error_contains_record_identifier():

    dataframe = make_clients()

    validation_results = {
        "clients": FakeValidationResult(
            [
                FakeIssue(
                    row_index=1,
                    column_name="risk_profile",
                    rule_id="CLI-003",
                    message="Invalid risk profile",
                )
            ]
        )
    }

    processor = RejectionProcessor()

    errors = (
        processor.build_validation_error_dataframe(
            {"clients": dataframe},
            validation_results,
        )
    )

    assert (
        errors.loc[
            0,
            "record_identifier",
        ]
        == "C002"
    )


def test_validation_error_preserves_rule_id():

    dataframe = make_clients()

    validation_results = {
        "clients": FakeValidationResult(
            [
                FakeIssue(
                    row_index=1,
                    column_name="risk_profile",
                    rule_id="CLI-003",
                )
            ]
        )
    }

    processor = RejectionProcessor()

    errors = (
        processor.build_validation_error_dataframe(
            {"clients": dataframe},
            validation_results,
        )
    )

    assert (
        errors.loc[
            0,
            "rule_id",
        ]
        == "CLI-003"
    )


def test_validation_error_preserves_severity():

    dataframe = make_clients()

    validation_results = {
        "clients": FakeValidationResult(
            [
                FakeIssue(
                    row_index=1,
                    column_name="status",
                    rule_id="CLI-W001",
                    severity="WARNING",
                )
            ]
        )
    }

    processor = RejectionProcessor()

    errors = (
        processor.build_validation_error_dataframe(
            {"clients": dataframe},
            validation_results,
        )
    )

    assert (
        errors.loc[
            0,
            "severity",
        ]
        == "WARNING"
    )


def test_multiple_errors_are_all_written_to_error_report():

    dataframe = make_clients()

    validation_results = {
        "clients": FakeValidationResult(
            [
                FakeIssue(
                    row_index=0,
                    column_name="risk_profile",
                    rule_id="CLI-003",
                ),
                FakeIssue(
                    row_index=0,
                    column_name="status",
                    rule_id="CLI-004",
                ),
                FakeIssue(
                    row_index=2,
                    column_name="client_type",
                    rule_id="CLI-002",
                ),
            ]
        )
    }

    processor = RejectionProcessor()

    errors = (
        processor.build_validation_error_dataframe(
            {"clients": dataframe},
            validation_results,
        )
    )

    assert len(errors) == 3


# =====================================================================
# Multiple datasets
# =====================================================================


def test_process_all_datasets():

    clients = make_clients()

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

    datasets = {
        "clients": clients,
        "portfolios": portfolios,
    }

    validation_results = {
        "clients": FakeValidationResult(
            [
                FakeIssue(
                    row_index=1,
                    column_name="risk_profile",
                    rule_id="CLI-003",
                )
            ]
        ),
        "portfolios": FakeValidationResult(
            []
        ),
    }

    processor = RejectionProcessor()

    results = processor.process_all(
        datasets,
        validation_results,
    )

    assert set(
        results.keys()
    ) == {
        "clients",
        "portfolios",
    }

    assert (
        results["clients"].invalid_records
        == 1
    )

    assert (
        results["portfolios"].invalid_records
        == 0
    )


# =====================================================================
# File output
# =====================================================================


def test_write_dataset_outputs(tmp_path):

    dataframe = make_clients()

    issue = FakeIssue(
        row_index=1,
        column_name="risk_profile",
        rule_id="CLI-003",
    )

    processor = RejectionProcessor(
        processed_root=tmp_path / "processed",
        rejected_root=tmp_path / "rejected",
    )

    result = processor.process_dataset(
        "clients",
        dataframe,
        [issue],
    )

    processed_path, rejected_path = (
        processor.write_dataset_outputs(
            result
        )
    )

    assert processed_path.exists()
    assert rejected_path.exists()

    assert (
        processed_path.name
        == "clients_clean.csv"
    )

    assert (
        rejected_path.name
        == "clients_rejected.csv"
    )


def test_written_processed_dataset_contains_only_valid_records(
    tmp_path,
):

    dataframe = make_clients()

    issue = FakeIssue(
        row_index=1,
        column_name="risk_profile",
        rule_id="CLI-003",
    )

    processor = RejectionProcessor(
        processed_root=tmp_path / "processed",
        rejected_root=tmp_path / "rejected",
    )

    result = processor.process_dataset(
        "clients",
        dataframe,
        [issue],
    )

    processed_path, _ = (
        processor.write_dataset_outputs(
            result
        )
    )

    written = pd.read_csv(
        processed_path
    )

    assert len(written) == 2

    assert "C002" not in set(
        written["client_id"]
    )


def test_written_rejected_dataset_contains_original_record(
    tmp_path,
):

    dataframe = make_clients()

    issue = FakeIssue(
        row_index=1,
        column_name="risk_profile",
        rule_id="CLI-003",
    )

    processor = RejectionProcessor(
        processed_root=tmp_path / "processed",
        rejected_root=tmp_path / "rejected",
    )

    result = processor.process_dataset(
        "clients",
        dataframe,
        [issue],
    )

    _, rejected_path = (
        processor.write_dataset_outputs(
            result
        )
    )

    written = pd.read_csv(
        rejected_path
    )

    assert len(written) == 1
    assert (
        written.loc[
            0,
            "client_id",
        ]
        == "C002"
    )


def test_write_validation_errors(tmp_path):

    dataframe = make_clients()

    validation_results = {
        "clients": FakeValidationResult(
            [
                FakeIssue(
                    row_index=1,
                    column_name="risk_profile",
                    rule_id="CLI-003",
                )
            ]
        )
    }

    processor = RejectionProcessor(
        quality_reports_root=(
            tmp_path / "quality_reports"
        )
    )

    errors = (
        processor.build_validation_error_dataframe(
            {"clients": dataframe},
            validation_results,
        )
    )

    path = processor.write_validation_errors(
        errors
    )

    assert path.exists()

    written = pd.read_csv(
        path
    )

    assert len(written) == 1
    assert (
        written.loc[
            0,
            "rule_id",
        ]
        == "CLI-003"
    )


# =====================================================================
# Input validation
# =====================================================================


def test_invalid_dataframe_raises_error():

    processor = RejectionProcessor()

    with pytest.raises(
        RejectionProcessingError
    ):
        processor.process_dataset(
            "clients",
            None,
            [],
        )


def test_empty_dataset_collection_raises_error():

    processor = RejectionProcessor()

    with pytest.raises(
        RejectionProcessingError
    ):
        processor.process_all(
            {},
            {},
        )