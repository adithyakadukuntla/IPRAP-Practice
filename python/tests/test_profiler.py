"""
Tests for Participant 2 data profiling.
"""

from pathlib import Path

import pandas as pd
import pytest

from python.validation.data_loader import (
    RawDataLoader,
)
from python.validation.profiler import (
    DataProfiler,
    ProfilingError,
)


# ---------------------------------------------------------------------------
# Basic profiler tests
# ---------------------------------------------------------------------------


def test_profile_column_numeric():
    dataframe = pd.DataFrame(
        {
            "value": [10, 20, 30, None],
        }
    )

    profiler = DataProfiler()

    result = profiler.profile_column(
        "test",
        dataframe,
        "value",
    )

    assert result["dataset_name"] == "test"
    assert result["column_name"] == "value"
    assert result["record_count"] == 4
    assert result["column_count"] == 1
    assert result["null_count"] == 1
    assert result["null_percentage"] == 25.0
    assert result["distinct_count"] == 3
    assert result["min_value"] == 10
    assert result["max_value"] == 30
    assert result["average_value"] == 20


def test_profile_column_text():
    dataframe = pd.DataFrame(
        {
            "status": [
                "ACTIVE",
                "ACTIVE",
                "INACTIVE",
            ],
        }
    )

    profiler = DataProfiler()

    result = profiler.profile_column(
        "clients",
        dataframe,
        "status",
    )

    assert result["record_count"] == 3
    assert result["null_count"] == 0
    assert result["null_percentage"] == 0.0
    assert result["distinct_count"] == 2

    # Min/max/average are not meaningful for categorical text.
    assert result["min_value"] is None
    assert result["max_value"] is None
    assert result["average_value"] is None


def test_profile_column_all_null():
    dataframe = pd.DataFrame(
        {
            "value": [
                None,
                None,
                None,
            ],
        }
    )

    profiler = DataProfiler()

    result = profiler.profile_column(
        "test",
        dataframe,
        "value",
    )

    assert result["record_count"] == 3
    assert result["null_count"] == 3
    assert result["null_percentage"] == 100.0
    assert result["distinct_count"] == 0
    assert result["min_value"] is None
    assert result["max_value"] is None
    assert result["average_value"] is None


# ---------------------------------------------------------------------------
# Dataset profiling tests
# ---------------------------------------------------------------------------


def test_profile_dataset():
    dataframe = pd.DataFrame(
        {
            "id": [1, 2, 3],
            "value": [100.0, 200.0, 300.0],
            "status": [
                "ACTIVE",
                "ACTIVE",
                "INACTIVE",
            ],
        }
    )

    profiler = DataProfiler()

    result = profiler.profile_dataset(
        "test",
        dataframe,
    )

    assert len(result) == 3

    assert list(result.columns) == [
        "dataset_name",
        "column_name",
        "data_type",
        "record_count",
        "column_count",
        "null_count",
        "null_percentage",
        "distinct_count",
        "min_value",
        "max_value",
        "average_value",
    ]


def test_profile_all_datasets():
    datasets = {
        "clients": pd.DataFrame(
            {
                "client_id": ["C1", "C2"],
                "value": [10, 20],
            }
        ),
        "portfolios": pd.DataFrame(
            {
                "portfolio_id": ["P1"],
                "value": [100],
            }
        ),
    }

    profiler = DataProfiler()

    result = profiler.profile_all_datasets(
        datasets
    )

    assert len(result) == 4

    assert set(
        result["dataset_name"]
    ) == {
        "clients",
        "portfolios",
    }


# ---------------------------------------------------------------------------
# Empty input test
# ---------------------------------------------------------------------------


def test_profile_empty_dataset_collection():
    profiler = DataProfiler()

    with pytest.raises(ProfilingError):
        profiler.profile_all_datasets({})


# ---------------------------------------------------------------------------
# Actual Participant 1 data tests
# ---------------------------------------------------------------------------


def test_profile_actual_datasets():
    loader = RawDataLoader()

    datasets = (
        loader.load_all_datasets()
    )

    profiler = DataProfiler()

    result = profiler.profile_all_datasets(
        datasets
    )

    # Actual Participant 1 schema:
    # clients = 7
    # portfolios = 10
    # securities = 9
    # holdings = 8
    # performance = 7
    #
    # Total = 41 columns.
    assert len(result) == 41

    assert (
        result[
            result["dataset_name"]
            == "clients"
        ].shape[0]
        == 7
    )

    assert (
        result[
            result["dataset_name"]
            == "portfolios"
        ].shape[0]
        == 10
    )

    assert (
        result[
            result["dataset_name"]
            == "securities"
        ].shape[0]
        == 9
    )

    assert (
        result[
            result["dataset_name"]
            == "holdings"
        ].shape[0]
        == 8
    )

    assert (
        result[
            result["dataset_name"]
            == "portfolio_performance"
        ].shape[0]
        == 7
    )


def test_actual_record_counts():
    loader = RawDataLoader()

    datasets = (
        loader.load_all_datasets()
    )

    profiler = DataProfiler()

    result = profiler.profile_all_datasets(
        datasets
    )

    for dataset_name, expected_count in {
        "clients": 50,
        "portfolios": 100,
        "securities": 120,
        "holdings": 600,
        "portfolio_performance": 1200,
    }.items():

        dataset_profile = result[
            result["dataset_name"]
            == dataset_name
        ]

        assert (
            dataset_profile[
                "record_count"
            ].unique().tolist()
            == [expected_count]
        )


def test_actual_source_has_no_nulls():
    loader = RawDataLoader()

    datasets = (
        loader.load_all_datasets()
    )

    profiler = DataProfiler()

    result = profiler.profile_all_datasets(
        datasets
    )

    assert (
        result["null_count"].sum()
        == 0
    )

    assert (
        result["null_percentage"].sum()
        == 0
    )


def test_actual_profile_contains_required_columns():
    loader = RawDataLoader()

    datasets = (
        loader.load_all_datasets()
    )

    profiler = DataProfiler()

    result = profiler.profile_all_datasets(
        datasets
    )

    required_columns = {
        "dataset_name",
        "column_name",
        "data_type",
        "record_count",
        "column_count",
        "null_count",
        "null_percentage",
        "distinct_count",
        "min_value",
        "max_value",
        "average_value",
    }

    assert required_columns.issubset(
        set(result.columns)
    )


# ---------------------------------------------------------------------------
# Output test
# ---------------------------------------------------------------------------


def test_save_profile(tmp_path):
    profile = pd.DataFrame(
        {
            "dataset_name": ["clients"],
            "column_name": ["client_id"],
            "data_type": ["object"],
            "record_count": [50],
            "column_count": [7],
            "null_count": [0],
            "null_percentage": [0.0],
            "distinct_count": [50],
            "min_value": [None],
            "max_value": [None],
            "average_value": [None],
        }
    )

    profiler = DataProfiler(
        output_dir=str(tmp_path)
    )

    output_path = profiler.save_profile(
        profile
    )

    assert output_path.exists()

    loaded = pd.read_csv(
        output_path
    )

    assert len(loaded) == 1
    assert (
        loaded.iloc[0]["dataset_name"]
        == "clients"
    )


def test_run_creates_profile_file(tmp_path):
    loader = RawDataLoader()

    datasets = (
        loader.load_all_datasets()
    )

    profiler = DataProfiler(
        output_dir=str(tmp_path)
    )

    output_path = profiler.run(
        datasets
    )

    assert output_path.exists()

    assert (
        output_path.name
        == "data_profile.csv"
    )

    profile = pd.read_csv(
        output_path
    )

    assert len(profile) == 41