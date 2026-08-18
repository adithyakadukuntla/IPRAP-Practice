"""
Tests for the Participant 2 raw-data loader.
"""

import json

import pandas as pd
import pytest

from python.validation.data_loader import (
    DataLoaderError,
    RawDataLoader,
)


# ---------------------------------------------------------------------------
# Actual Participant 1 source-file tests
# ---------------------------------------------------------------------------


def test_load_clients():
    loader = RawDataLoader()

    dataframe = loader.load_dataset("clients")

    assert isinstance(dataframe, pd.DataFrame)
    assert len(dataframe) == 50

    assert list(dataframe.columns) == [
        "client_id",
        "client_name",
        "client_type",
        "country",
        "risk_profile",
        "created_date",
        "status",
    ]


def test_load_portfolios():
    loader = RawDataLoader()

    dataframe = loader.load_dataset("portfolios")

    assert isinstance(dataframe, pd.DataFrame)
    assert len(dataframe) == 100

    assert list(dataframe.columns) == [
        "portfolio_id",
        "client_id",
        "portfolio_name",
        "portfolio_type",
        "base_currency",
        "risk_profile",
        "initial_value",
        "current_value",
        "inception_date",
        "status",
    ]


def test_load_securities():
    loader = RawDataLoader()

    dataframe = loader.load_dataset("securities")

    assert isinstance(dataframe, pd.DataFrame)
    assert len(dataframe) == 120

    assert list(dataframe.columns) == [
        "security_id",
        "ticker_symbol",
        "security_name",
        "security_type",
        "sector",
        "country",
        "currency",
        "current_price",
        "status",
    ]


def test_load_holdings():
    loader = RawDataLoader()

    dataframe = loader.load_dataset("holdings")

    assert isinstance(dataframe, pd.DataFrame)
    assert len(dataframe) == 600

    assert list(dataframe.columns) == [
        "holding_id",
        "portfolio_id",
        "security_id",
        "quantity",
        "purchase_price",
        "current_price",
        "market_value",
        "as_of_date",
    ]


def test_load_portfolio_performance():
    loader = RawDataLoader()

    dataframe = loader.load_dataset(
        "portfolio_performance"
    )

    assert isinstance(dataframe, pd.DataFrame)
    assert len(dataframe) == 1200

    assert list(dataframe.columns) == [
        "performance_id",
        "portfolio_id",
        "as_of_date",
        "beginning_value",
        "ending_value",
        "return_amount",
        "return_percent",
    ]


def test_load_all_datasets():
    loader = RawDataLoader()

    datasets = loader.load_all_datasets()

    assert set(datasets.keys()) == {
        "clients",
        "portfolios",
        "securities",
        "holdings",
        "portfolio_performance",
    }

    assert len(datasets["clients"]) == 50
    assert len(datasets["portfolios"]) == 100
    assert len(datasets["securities"]) == 120
    assert len(datasets["holdings"]) == 600
    assert len(
        datasets["portfolio_performance"]
    ) == 1200


# ---------------------------------------------------------------------------
# Error-handling tests
# ---------------------------------------------------------------------------


def test_unknown_dataset(tmp_path):
    loader = RawDataLoader(
        raw_data_dir=str(tmp_path)
    )

    with pytest.raises(DataLoaderError):
        loader.load_dataset("unknown_dataset")


def test_missing_file(tmp_path):
    loader = RawDataLoader(
        raw_data_dir=str(tmp_path)
    )

    with pytest.raises(DataLoaderError):
        loader.load_dataset("clients")


def test_empty_file(tmp_path):
    clients_dir = tmp_path / "clients"
    clients_dir.mkdir()

    file_path = clients_dir / "clients.csv"
    file_path.touch()

    loader = RawDataLoader(
        raw_data_dir=str(tmp_path)
    )

    with pytest.raises(DataLoaderError):
        loader.load_dataset("clients")


def test_empty_dataframe(tmp_path):
    clients_dir = tmp_path / "clients"
    clients_dir.mkdir()

    file_path = clients_dir / "clients.csv"

    file_path.write_text(
        "client_id,client_name,status\n"
    )

    loader = RawDataLoader(
        raw_data_dir=str(tmp_path)
    )

    with pytest.raises(DataLoaderError):
        loader.load_dataset("clients")


def test_wrong_file_format(tmp_path):
    clients_dir = tmp_path / "clients"
    clients_dir.mkdir()

    file_path = clients_dir / "clients.json"

    file_path.write_text(
        json.dumps(
            [
                {
                    "client_id": "C10001"
                }
            ]
        )
    )

    loader = RawDataLoader(
        raw_data_dir=str(tmp_path)
    )

    with pytest.raises(DataLoaderError):
        loader.load_dataset("clients")


def test_unsupported_extension(tmp_path):
    clients_dir = tmp_path / "clients"
    clients_dir.mkdir()

    file_path = clients_dir / "clients.xlsx"

    file_path.write_text(
        "invalid"
    )

    loader = RawDataLoader(
        raw_data_dir=str(tmp_path)
    )

    with pytest.raises(DataLoaderError):
        loader.load_dataset("clients")


def test_json_loader_reads_records(tmp_path):
    securities_dir = tmp_path / "securities"
    securities_dir.mkdir()

    file_path = (
        securities_dir
        / "securities.json"
    )

    file_path.write_text(
        json.dumps(
            [
                {
                    "security_id": "SEC10001",
                    "ticker_symbol": "AAPL",
                    "security_name": "Apple Inc.",
                    "security_type": "EQUITY",
                    "sector": "TECHNOLOGY",
                    "country": "USA",
                    "currency": "USD",
                    "current_price": 100.0,
                    "status": "ACTIVE",
                }
            ]
        )
    )

    loader = RawDataLoader(
        raw_data_dir=str(tmp_path)
    )

    dataframe = loader.load_dataset(
        "securities"
    )

    assert len(dataframe) == 1

    assert (
        dataframe.iloc[0]["security_id"]
        == "SEC10001"
    )


# ---------------------------------------------------------------------------
# Raw-data safety test
# ---------------------------------------------------------------------------


def test_loader_does_not_modify_raw_file(
    tmp_path,
):
    clients_dir = tmp_path / "clients"
    clients_dir.mkdir()

    file_path = clients_dir / "clients.csv"

    original_content = (
        "client_id,client_name,status\n"
        "C10001,Alice,ACTIVE\n"
    )

    file_path.write_text(
        original_content
    )

    loader = RawDataLoader(
        raw_data_dir=str(tmp_path)
    )

    loader.load_dataset("clients")

    assert (
        file_path.read_text()
        == original_content
    )