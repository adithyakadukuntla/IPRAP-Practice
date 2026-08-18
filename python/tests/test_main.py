"""
Integration tests for the Participant 2 validation pipeline.
"""

from datetime import date

import pandas as pd

from python.validation.main import (
    PipelineIssue,
    ValidationPipeline,
)


# =====================================================================
# Helpers
# =====================================================================


def test_pipeline_issue_has_common_structure():

    issue = PipelineIssue(
        dataset_name="clients",
        row_index=5,
        column_name="risk_profile",
        rule_id="DOM-001",
        severity="ERROR",
        message="Invalid risk profile.",
    )

    assert issue.dataset_name == "clients"
    assert issue.row_index == 5
    assert issue.column_name == "risk_profile"
    assert issue.rule_id == "DOM-001"
    assert issue.severity == "ERROR"


# =====================================================================
# Pipeline execution
# =====================================================================


def test_pipeline_runs_against_actual_project_data(
    tmp_path,
):

    pipeline = ValidationPipeline(
        raw_data_dir="data/raw",
        processed_root=(
            tmp_path / "processed"
        ),
        rejected_root=(
            tmp_path / "rejected"
        ),
        quality_reports_root=(
            tmp_path / "quality_reports"
        ),
    )

    result = pipeline.run(
        current_business_date=date(
            2026,
            8,
            15,
        )
    )

    assert len(
        result.datasets
    ) == 5

    assert set(
        result.datasets.keys()
    ) == {
        "clients",
        "portfolios",
        "securities",
        "holdings",
        "portfolio_performance",
    }


def test_actual_data_has_no_rejected_records(
    tmp_path,
):

    pipeline = ValidationPipeline(
        raw_data_dir="data/raw",
        processed_root=(
            tmp_path / "processed"
        ),
        rejected_root=(
            tmp_path / "rejected"
        ),
        quality_reports_root=(
            tmp_path / "quality_reports"
        ),
    )

    result = pipeline.run(
        current_business_date=date(
            2026,
            8,
            15,
        )
    )

    for processing_result in (
        result.processing_results.values()
    ):
        assert (
            processing_result.invalid_records
            == 0
        )


def test_actual_data_is_100_percent_quality(
    tmp_path,
):

    pipeline = ValidationPipeline(
        raw_data_dir="data/raw",
        processed_root=(
            tmp_path / "processed"
        ),
        rejected_root=(
            tmp_path / "rejected"
        ),
        quality_reports_root=(
            tmp_path / "quality_reports"
        ),
    )

    result = pipeline.run(
        current_business_date=date(
            2026,
            8,
            15,
        )
    )

    assert all(
        result.quality_summary[
            "quality_score"
        ]
        == 100.0
    )

    assert all(
        result.quality_summary[
            "quality_status"
        ]
        == "EXCELLENT"
    )


# =====================================================================
# Required output files
# =====================================================================


def test_profile_file_is_created(
    tmp_path,
):

    pipeline = ValidationPipeline(
        raw_data_dir="data/raw",
        processed_root=(
            tmp_path / "processed"
        ),
        rejected_root=(
            tmp_path / "rejected"
        ),
        quality_reports_root=(
            tmp_path / "quality_reports"
        ),
    )

    result = pipeline.run()

    assert (
        result.profile_path.exists()
    )


def test_validation_errors_file_is_created(
    tmp_path,
):

    pipeline = ValidationPipeline(
        raw_data_dir="data/raw",
        processed_root=(
            tmp_path / "processed"
        ),
        rejected_root=(
            tmp_path / "rejected"
        ),
        quality_reports_root=(
            tmp_path / "quality_reports"
        ),
    )

    result = pipeline.run()

    assert (
        result.validation_errors_path.exists()
    )


def test_quality_summary_file_is_created(
    tmp_path,
):

    pipeline = ValidationPipeline(
        raw_data_dir="data/raw",
        processed_root=(
            tmp_path / "processed"
        ),
        rejected_root=(
            tmp_path / "rejected"
        ),
        quality_reports_root=(
            tmp_path / "quality_reports"
        ),
    )

    result = pipeline.run()

    assert (
        result.quality_summary_path.exists()
    )


# =====================================================================
# Validation error schema
# =====================================================================


def test_validation_error_report_has_required_columns(
    tmp_path,
):

    pipeline = ValidationPipeline(
        raw_data_dir="data/raw",
        processed_root=(
            tmp_path / "processed"
        ),
        rejected_root=(
            tmp_path / "rejected"
        ),
        quality_reports_root=(
            tmp_path / "quality_reports"
        ),
    )

    result = pipeline.run()

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
        result.validation_errors.columns
    ) == expected_columns


# =====================================================================
# Quality summary schema
# =====================================================================


def test_quality_summary_has_required_columns(
    tmp_path,
):

    pipeline = ValidationPipeline(
        raw_data_dir="data/raw",
        processed_root=(
            tmp_path / "processed"
        ),
        rejected_root=(
            tmp_path / "rejected"
        ),
        quality_reports_root=(
            tmp_path / "quality_reports"
        ),
    )

    result = pipeline.run()

    expected_columns = [
        "dataset_name",
        "total_records",
        "valid_records",
        "invalid_records",
        "error_count",
        "warning_count",
        "quality_score",
        "quality_status",
        "validation_timestamp",
    ]

    assert list(
        result.quality_summary.columns
    ) == expected_columns


# =====================================================================
# Dataset counts
# =====================================================================


def test_dataset_counts_match_actual_data(
    tmp_path,
):

    pipeline = ValidationPipeline(
        raw_data_dir="data/raw",
        processed_root=(
            tmp_path / "processed"
        ),
        rejected_root=(
            tmp_path / "rejected"
        ),
        quality_reports_root=(
            tmp_path / "quality_reports"
        ),
    )

    result = pipeline.run()

    expected_counts = {
        "clients": 50,
        "portfolios": 100,
        "securities": 120,
        "holdings": 600,
        "portfolio_performance": 1200,
    }

    for (
        dataset_name,
        expected_count,
    ) in expected_counts.items():

        assert (
            result.processing_results[
                dataset_name
            ].total_records
            == expected_count
        )


# =====================================================================
# Processed output
# =====================================================================


def test_processed_outputs_are_created(
    tmp_path,
):

    processed_root = (
        tmp_path / "processed"
    )

    pipeline = ValidationPipeline(
        raw_data_dir="data/raw",
        processed_root=processed_root,
        rejected_root=(
            tmp_path / "rejected"
        ),
        quality_reports_root=(
            tmp_path / "quality_reports"
        ),
    )

    pipeline.run()

    datasets = [
        "clients",
        "portfolios",
        "securities",
        "holdings",
        "portfolio_performance",
    ]

    for dataset_name in datasets:

        path = (
            processed_root
            / dataset_name
            / f"{dataset_name}_clean.csv"
        )

        assert path.exists()

        dataframe = pd.read_csv(
            path
        )

        assert len(dataframe) > 0


# =====================================================================
# Rejected output
# =====================================================================


def test_rejected_outputs_are_created(
    tmp_path,
):

    rejected_root = (
        tmp_path / "rejected"
    )

    pipeline = ValidationPipeline(
        raw_data_dir="data/raw",
        processed_root=(
            tmp_path / "processed"
        ),
        rejected_root=rejected_root,
        quality_reports_root=(
            tmp_path / "quality_reports"
        ),
    )

    pipeline.run()

    datasets = [
        "clients",
        "portfolios",
        "securities",
        "holdings",
        "portfolio_performance",
    ]

    for dataset_name in datasets:

        path = (
            rejected_root
            / dataset_name
            / f"{dataset_name}_rejected.csv"
        )

        assert path.exists()


# =====================================================================
# Standardization integration
# =====================================================================


def test_processed_client_values_are_standardized(
    tmp_path,
):

    processed_root = (
        tmp_path / "processed"
    )

    pipeline = ValidationPipeline(
        raw_data_dir="data/raw",
        processed_root=processed_root,
        rejected_root=(
            tmp_path / "rejected"
        ),
        quality_reports_root=(
            tmp_path / "quality_reports"
        ),
    )

    pipeline.run()

    clients = pd.read_csv(
        processed_root
        / "clients"
        / "clients_clean.csv"
    )

    assert set(
        clients["client_type"].dropna()
    ).issubset(
        {
            "INDIVIDUAL",
            "INSTITUTIONAL",
        }
    )

    assert set(
        clients["risk_profile"].dropna()
    ).issubset(
        {
            "LOW",
            "MEDIUM",
            "HIGH",
        }
    )

    assert set(
        clients["status"].dropna()
    ).issubset(
        {
            "ACTIVE",
            "INACTIVE",
        }
    )


# =====================================================================
# Overall validity
# =====================================================================


def test_pipeline_result_reports_all_valid(
    tmp_path,
):

    pipeline = ValidationPipeline(
        raw_data_dir="data/raw",
        processed_root=(
            tmp_path / "processed"
        ),
        rejected_root=(
            tmp_path / "rejected"
        ),
        quality_reports_root=(
            tmp_path / "quality_reports"
        ),
    )

    result = pipeline.run()

    assert result.all_valid() is True