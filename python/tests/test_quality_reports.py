"""
Tests for Phase 14 — Data Quality Scoring.
"""

from pathlib import Path

import pandas as pd
import pytest

from python.validation.quality_report import (
    QualityReportError,
    QualityReporter,
)


# =====================================================================
# Fake issue / processing result helpers
# =====================================================================


class FakeIssue:
    """Minimal validation issue used by tests."""

    def __init__(
        self,
        severity="ERROR",
        message="Validation failed",
    ):
        self.severity = severity
        self.message = message


class FakeProcessingResult:
    """Minimal Phase 13 processing result."""

    def __init__(
        self,
        total_records,
        valid_records,
        invalid_records,
    ):
        self.total_records = total_records
        self.valid_records = valid_records
        self.invalid_records = invalid_records


# =====================================================================
# Quality score
# =====================================================================


def test_quality_score_100_percent():

    reporter = QualityReporter()

    score = reporter.calculate_quality_score(
        100,
        100,
    )

    assert score == 100.0


def test_quality_score_95_percent():

    reporter = QualityReporter()

    score = reporter.calculate_quality_score(
        100,
        95,
    )

    assert score == 95.0


def test_quality_score_97_percent():

    reporter = QualityReporter()

    score = reporter.calculate_quality_score(
        100,
        97,
    )

    assert score == 97.0


def test_quality_score_rounded_to_two_decimals():

    reporter = QualityReporter()

    score = reporter.calculate_quality_score(
        300,
        292,
    )

    assert score == 97.33


def test_zero_records_returns_zero_score():

    reporter = QualityReporter()

    score = reporter.calculate_quality_score(
        0,
        0,
    )

    assert score == 0.0


# =====================================================================
# Quality status classification
# =====================================================================


def test_100_is_excellent():

    reporter = QualityReporter()

    assert (
        reporter.classify_quality_score(
            100
        )
        == "EXCELLENT"
    )


def test_95_is_excellent():

    reporter = QualityReporter()

    assert (
        reporter.classify_quality_score(
            95
        )
        == "EXCELLENT"
    )


def test_94_99_is_good():

    reporter = QualityReporter()

    assert (
        reporter.classify_quality_score(
            94.99
        )
        == "GOOD"
    )


def test_90_is_good():

    reporter = QualityReporter()

    assert (
        reporter.classify_quality_score(
            90
        )
        == "GOOD"
    )


def test_89_99_is_warning():

    reporter = QualityReporter()

    assert (
        reporter.classify_quality_score(
            89.99
        )
        == "WARNING"
    )


def test_80_is_warning():

    reporter = QualityReporter()

    assert (
        reporter.classify_quality_score(
            80
        )
        == "WARNING"
    )


def test_79_99_is_poor():

    reporter = QualityReporter()

    assert (
        reporter.classify_quality_score(
            79.99
        )
        == "POOR"
    )


def test_zero_is_poor():

    reporter = QualityReporter()

    assert (
        reporter.classify_quality_score(
            0
        )
        == "POOR"
    )


# =====================================================================
# Invalid score inputs
# =====================================================================


def test_negative_total_records_raises():

    reporter = QualityReporter()

    with pytest.raises(
        QualityReportError
    ):
        reporter.calculate_quality_score(
            -1,
            0,
        )


def test_negative_valid_records_raises():

    reporter = QualityReporter()

    with pytest.raises(
        QualityReportError
    ):
        reporter.calculate_quality_score(
            100,
            -1,
        )


def test_valid_records_cannot_exceed_total():

    reporter = QualityReporter()

    with pytest.raises(
        QualityReportError
    ):
        reporter.calculate_quality_score(
            10,
            11,
        )


def test_invalid_quality_score_raises():

    reporter = QualityReporter()

    with pytest.raises(
        QualityReportError
    ):
        reporter.classify_quality_score(
            101
        )


# =====================================================================
# Issue counts
# =====================================================================


def test_error_count():

    reporter = QualityReporter()

    result = reporter.count_issues(
        [
            FakeIssue("ERROR"),
            FakeIssue("ERROR"),
            FakeIssue("WARNING"),
        ]
    )

    assert result == (
        2,
        1,
    )


def test_warning_count():

    reporter = QualityReporter()

    result = reporter.count_issues(
        [
            FakeIssue("WARNING"),
            FakeIssue("WARNING"),
            FakeIssue("ERROR"),
        ]
    )

    assert result == (
        1,
        2,
    )


def test_info_is_not_error_or_warning():

    reporter = QualityReporter()

    result = reporter.count_issues(
        [
            FakeIssue("INFO"),
        ]
    )

    assert result == (
        0,
        0,
    )


def test_none_issues_returns_zero_counts():

    reporter = QualityReporter()

    result = reporter.count_issues(
        None
    )

    assert result == (
        0,
        0,
    )


# =====================================================================
# Dataset quality
# =====================================================================


def test_dataset_quality_result():

    reporter = QualityReporter()

    result = (
        reporter.calculate_dataset_quality(
            dataset_name="clients",
            total_records=50,
            valid_records=49,
            validation_result=[
                FakeIssue("ERROR"),
            ],
            validation_timestamp="2026-08-15T12:00:00+00:00",
        )
    )

    assert result.dataset_name == "clients"
    assert result.total_records == 50
    assert result.valid_records == 49
    assert result.invalid_records == 1
    assert result.error_count == 1
    assert result.warning_count == 0
    assert result.quality_score == 98.0
    assert result.quality_status == "EXCELLENT"
    assert (
        result.validation_timestamp
        == "2026-08-15T12:00:00+00:00"
    )


def test_dataset_quality_with_warnings():

    reporter = QualityReporter()

    result = (
        reporter.calculate_dataset_quality(
            dataset_name="portfolios",
            total_records=100,
            valid_records=92,
            validation_result=[
                FakeIssue("ERROR"),
                FakeIssue("WARNING"),
                FakeIssue("WARNING"),
            ],
        )
    )

    assert result.invalid_records == 8
    assert result.error_count == 1
    assert result.warning_count == 2
    assert result.quality_score == 92.0
    assert result.quality_status == "GOOD"


# =====================================================================
# Multiple datasets
# =====================================================================


def test_calculate_all_datasets():

    reporter = QualityReporter()

    processing_results = {
        "clients": FakeProcessingResult(
            50,
            49,
            1,
        ),
        "portfolios": FakeProcessingResult(
            100,
            97,
            3,
        ),
        "securities": FakeProcessingResult(
            100,
            100,
            0,
        ),
    }

    validation_results = {
        "clients": [
            FakeIssue("ERROR"),
        ],
        "portfolios": [
            FakeIssue("ERROR"),
            FakeIssue("WARNING"),
        ],
        "securities": [],
    }

    results = reporter.calculate_all(
        processing_results,
        validation_results,
    )

    assert results["clients"].quality_score == 98.0
    assert results["clients"].quality_status == "EXCELLENT"

    assert results["portfolios"].quality_score == 97.0
    assert results["portfolios"].quality_status == "EXCELLENT"

    assert results["securities"].quality_score == 100.0
    assert results["securities"].quality_status == "EXCELLENT"


# =====================================================================
# DataFrame generation
# =====================================================================


def test_results_to_dataframe_contains_required_columns():

    reporter = QualityReporter()

    processing_results = {
        "clients": FakeProcessingResult(
            50,
            49,
            1,
        )
    }

    results = reporter.calculate_all(
        processing_results,
        {
            "clients": [
                FakeIssue("ERROR")
            ]
        },
    )

    dataframe = (
        reporter.results_to_dataframe(
            results
        )
    )

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
        dataframe.columns
    ) == expected_columns


def test_results_to_dataframe_contains_correct_values():

    reporter = QualityReporter()

    processing_results = {
        "clients": FakeProcessingResult(
            50,
            49,
            1,
        )
    }

    results = reporter.calculate_all(
        processing_results,
        {
            "clients": [
                FakeIssue("ERROR")
            ]
        },
    )

    dataframe = (
        reporter.results_to_dataframe(
            results
        )
    )

    row = dataframe.iloc[0]

    assert row["dataset_name"] == "clients"
    assert row["total_records"] == 50
    assert row["valid_records"] == 49
    assert row["invalid_records"] == 1
    assert row["error_count"] == 1
    assert row["warning_count"] == 0
    assert row["quality_score"] == 98.0
    assert row["quality_status"] == "EXCELLENT"


# =====================================================================
# File output
# =====================================================================


def test_write_summary(tmp_path):

    reporter = QualityReporter(
        output_root=tmp_path
    )

    summary = pd.DataFrame(
        [
            {
                "dataset_name": "clients",
                "total_records": 50,
                "valid_records": 49,
                "invalid_records": 1,
                "error_count": 1,
                "warning_count": 0,
                "quality_score": 98.0,
                "quality_status": "EXCELLENT",
                "validation_timestamp": (
                    "2026-08-15T12:00:00+00:00"
                ),
            }
        ]
    )

    path = reporter.write_summary(
        summary
    )

    assert path.exists()

    assert (
        path.name
        == "data_quality_summary.csv"
    )


def test_written_summary_can_be_read_back(
    tmp_path,
):

    reporter = QualityReporter(
        output_root=tmp_path
    )

    summary = pd.DataFrame(
        [
            {
                "dataset_name": "clients",
                "total_records": 50,
                "valid_records": 49,
                "invalid_records": 1,
                "error_count": 1,
                "warning_count": 0,
                "quality_score": 98.0,
                "quality_status": "EXCELLENT",
                "validation_timestamp": (
                    "2026-08-15T12:00:00+00:00"
                ),
            }
        ]
    )

    path = reporter.write_summary(
        summary
    )

    loaded = pd.read_csv(
        path
    )

    assert loaded.loc[
        0,
        "dataset_name",
    ] == "clients"

    assert loaded.loc[
        0,
        "quality_score",
    ] == 98.0

    assert loaded.loc[
        0,
        "quality_status",
    ] == "EXCELLENT"


def test_missing_summary_column_raises():

    reporter = QualityReporter()

    invalid_summary = pd.DataFrame(
        [
            {
                "dataset_name": "clients",
                "total_records": 50,
            }
        ]
    )

    with pytest.raises(
        QualityReportError
    ):
        reporter.write_summary(
            invalid_summary
        )


# =====================================================================
# Complete report
# =====================================================================


def test_generate_report_creates_output(
    tmp_path,
):

    reporter = QualityReporter(
        output_root=tmp_path
    )

    processing_results = {
        "clients": FakeProcessingResult(
            50,
            49,
            1,
        ),
        "portfolios": FakeProcessingResult(
            100,
            100,
            0,
        ),
    }

    validation_results = {
        "clients": [
            FakeIssue("ERROR"),
        ],
        "portfolios": [],
    }

    results, summary, path = (
        reporter.generate_report(
            processing_results,
            validation_results,
        )
    )

    assert path.exists()

    assert len(results) == 2
    assert len(summary) == 2

    assert (
        summary.loc[
            summary["dataset_name"]
            == "clients",
            "quality_score",
        ].iloc[0]
        == 98.0
    )

    assert (
        summary.loc[
            summary["dataset_name"]
            == "portfolios",
            "quality_score",
        ].iloc[0]
        == 100.0
    )