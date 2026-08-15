from pathlib import Path

import pandas as pd


DATASETS = [
    "clients",
    "portfolios",
    "securities",
    "holdings",
    "portfolio_performance",
]


def test_all_trusted_dataset_outputs_exist():

    for dataset in DATASETS:

        path = (
            Path("data")
            / "processed"
            / dataset
            / f"{dataset}_clean.csv"
        )

        assert path.exists()


def test_all_rejected_dataset_outputs_exist():

    for dataset in DATASETS:

        path = (
            Path("data")
            / "rejected"
            / dataset
            / f"{dataset}_rejected.csv"
        )

        assert path.exists()


def test_all_quality_reports_exist():

    reports = [
        "data_profile.csv",
        "validation_errors.csv",
        "data_quality_summary.csv",
    ]

    for report in reports:

        assert (
            Path("data")
            / "quality_reports"
            / report
        ).exists()


def test_quality_summary_has_all_datasets():

    path = (
        Path("data")
        / "quality_reports"
        / "data_quality_summary.csv"
    )

    dataframe = pd.read_csv(path)

    assert set(
        dataframe["dataset_name"]
    ) == set(DATASETS)


def test_validation_error_report_has_required_columns():

    path = (
        Path("data")
        / "quality_reports"
        / "validation_errors.csv"
    )

    dataframe = pd.read_csv(path)

    assert list(
        dataframe.columns
    ) == [
        "dataset_name",
        "record_identifier",
        "row_index",
        "column_name",
        "rule_id",
        "severity",
        "error_message",
    ]


def test_quality_summary_has_required_columns():

    path = (
        Path("data")
        / "quality_reports"
        / "data_quality_summary.csv"
    )

    dataframe = pd.read_csv(path)

    assert list(
        dataframe.columns
    ) == [
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


def test_current_quality_scores_are_excellent():

    path = (
        Path("data")
        / "quality_reports"
        / "data_quality_summary.csv"
    )

    dataframe = pd.read_csv(path)

    assert (
        dataframe["quality_score"]
        == 100.0
    ).all()

    assert (
        dataframe["quality_status"]
        == "EXCELLENT"
    ).all()


def test_current_validation_has_no_errors():

    path = (
        Path("data")
        / "quality_reports"
        / "validation_errors.csv"
    )

    dataframe = pd.read_csv(path)

    assert len(dataframe) == 0