import pandas as pd
from pathlib import Path


def read_csv_file(file_path: str, required_columns: list[str]) -> pd.DataFrame:
    """
    Read a CSV file and validate that all required columns exist.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"CSV file not found: {path}")

    if not path.is_file():
        raise ValueError(f"Path is not a file: {path}")

    try:
        df = pd.read_csv(path)
    except Exception as e:
        raise RuntimeError(
            f"Unable to read CSV file {path}: {e}"
        ) from e

    # Check required columns
    missing_columns = [
        column for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"CSV file {path} is missing required columns: "
            f"{missing_columns}. "
            f"Available columns: {list(df.columns)}"
        )

    return df


def read_all_csv_files(raw_data_path: str):
    """
    Read and validate all CSV datasets from the raw data directory.
    """

    base_path = Path(raw_data_path)

    clients_path = base_path / "clients" / "clients.csv"
    portfolios_path = base_path / "portfolios" / "portfolios.csv"
    holdings_path = base_path / "holdings" / "holdings.csv"
    performance_path = (
        base_path
        / "portfolio_performance"
        / "portfolio_performance.csv"
    )

    clients = read_csv_file(
        clients_path,
        required_columns=[
            "client_id",
            "client_name",
            "email"
        ]
    )

    portfolios = read_csv_file(
        portfolios_path,
        required_columns=[
            "portfolio_id",
            "client_id",
            "portfolio_name"
        ]
    )

    holdings = read_csv_file(
        holdings_path,
        required_columns=[
            "portfolio_id",
            "asset_id",
            "quantity"
        ]
    )

    performance = read_csv_file(
        performance_path,
        required_columns=[
            "portfolio_id",
            "date",
            "return"
        ]
    )

    return {
        "clients": clients,
        "portfolios": portfolios,
        "holdings": holdings,
        "portfolio_performance": performance
    }
