from pathlib import Path
import pandas as pd
import json


# ============================================================
# FILE CHECKS
# ============================================================

def check_file_exists(file_path: str) -> bool:

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"File does not exist: {path}"
        )

    return True


def check_file_readable(file_path: str) -> bool:

    path = Path(file_path)

    check_file_exists(file_path)

    try:
        with open(path, "rb") as file:
            file.read(1)

        return True

    except PermissionError as e:
        raise PermissionError(
            f"File is not readable: {path}"
        ) from e


def check_file_not_empty(file_path: str) -> bool:

    path = Path(file_path)

    check_file_exists(file_path)

    if path.stat().st_size == 0:
        raise ValueError(
            f"File is empty: {path}"
        )

    return True


# ============================================================
# FILE NAME VALIDATION
# ============================================================

EXPECTED_FILES = {
    "CLIENTS": "clients.csv",
    "PORTFOLIOS": "portfolios.csv",
    "HOLDINGS": "holdings.csv",
    "PORTFOLIO_PERFORMANCE": "portfolio_performance.csv",
}


def check_file_name(
    file_path: str,
    dataset_name: str
) -> bool:

    path = Path(file_path)

    expected_file = EXPECTED_FILES.get(dataset_name)

    if expected_file is None:
        return True

    if path.name != expected_file:
        raise ValueError(
            f"{dataset_name}: Invalid file name. "
            f"Expected '{expected_file}', "
            f"received '{path.name}'"
        )

    return True


# ============================================================
# COLUMN CHECK
# ============================================================

def check_required_columns(
    dataframe: pd.DataFrame,
    required_columns: list,
    dataset_name: str
) -> bool:

    actual_columns = set(dataframe.columns)

    missing_columns = [
        column
        for column in required_columns
        if column not in actual_columns
    ]

    if missing_columns:
        raise ValueError(
            f"{dataset_name} is missing required columns: "
            f"{missing_columns}"
        )

    return True


def check_unexpected_columns(
    dataframe: pd.DataFrame,
    required_columns: list,
    dataset_name: str
) -> bool:

    actual_columns = set(dataframe.columns)
    expected_columns = set(required_columns)

    unexpected_columns = sorted(
        actual_columns - expected_columns
    )

    if unexpected_columns:
        raise ValueError(
            f"{dataset_name} contains unexpected columns: "
            f"{unexpected_columns}"
        )

    return True


# ============================================================
# CSV PARSING
# ============================================================

def check_csv_parsing(file_path: str) -> pd.DataFrame:

    try:

        dataframe = pd.read_csv(file_path)

        if dataframe is None:
            raise ValueError(
                f"CSV parsing returned no data: {file_path}"
            )

        return dataframe

    except pd.errors.EmptyDataError as e:

        raise ValueError(
            f"CSV file contains no data: {file_path}"
        ) from e

    except pd.errors.ParserError as e:

        raise ValueError(
            f"CSV parsing failed: {file_path}"
        ) from e


# ============================================================
# EMPTY DATAFRAME CHECK
# ============================================================

def check_dataframe_not_empty(
    dataframe: pd.DataFrame,
    dataset_name: str
) -> bool:

    if dataframe.empty:
        raise ValueError(
            f"{dataset_name}: CSV contains no records"
        )

    return True


# ============================================================
# NULL / MISSING VALUE CHECK
# ============================================================

def check_null_values(
    dataframe: pd.DataFrame,
    required_columns: list,
    dataset_name: str
) -> bool:

    null_errors = {}

    for column in required_columns:

        null_count = dataframe[column].isna().sum()

        if null_count > 0:
            null_errors[column] = int(null_count)

    if null_errors:

        raise ValueError(
            f"{dataset_name}: Required columns contain "
            f"missing/null values: {null_errors}"
        )

    return True


# ============================================================
# EMPTY STRING CHECK
# ============================================================

def check_empty_strings(
    dataframe: pd.DataFrame,
    required_columns: list,
    dataset_name: str
) -> bool:

    empty_errors = {}

    for column in required_columns:

        if dataframe[column].dtype == "object":

            empty_count = (
                dataframe[column]
                .astype(str)
                .str.strip()
                .eq("")
                .sum()
            )

            if empty_count > 0:
                empty_errors[column] = int(empty_count)

    if empty_errors:

        raise ValueError(
            f"{dataset_name}: Required columns contain "
            f"empty values: {empty_errors}"
        )

    return True


# ============================================================
# INTEGER CHECK
# ============================================================


# ============================================================
# NUMERIC CHECK
# ============================================================

def check_numeric_column(
    dataframe: pd.DataFrame,
    column: str,
    dataset_name: str
) -> bool:

    converted = pd.to_numeric(
        dataframe[column],
        errors="coerce"
    )

    invalid = converted.isna()

    if invalid.any():

        rows = dataframe.index[invalid].tolist()

        raise ValueError(
            f"{dataset_name}: Column '{column}' "
            f"must contain numeric values. "
            f"Invalid rows: {rows}"
        )

    return True


# ============================================================
# POSITIVE NUMBER CHECK
# ============================================================

def check_positive_column(
    dataframe: pd.DataFrame,
    column: str,
    dataset_name: str
) -> bool:

    values = pd.to_numeric(
        dataframe[column],
        errors="coerce"
    )

    invalid = values <= 0

    if invalid.any():

        rows = dataframe.index[invalid].tolist()
        values_found = dataframe.loc[
            invalid,
            column
        ].tolist()

        raise ValueError(
            f"{dataset_name}: Column '{column}' "
            f"must contain values greater than 0. "
            f"Invalid values: {values_found}. "
            f"Rows: {rows}"
        )

    return True


# ============================================================
# NON-NEGATIVE NUMBER CHECK
# ============================================================

def check_non_negative_column(
    dataframe: pd.DataFrame,
    column: str,
    dataset_name: str
) -> bool:

    values = pd.to_numeric(
        dataframe[column],
        errors="coerce"
    )

    invalid = values < 0

    if invalid.any():

        rows = dataframe.index[invalid].tolist()
        values_found = dataframe.loc[
            invalid,
            column
        ].tolist()

        raise ValueError(
            f"{dataset_name}: Column '{column}' "
            f"cannot contain negative values. "
            f"Invalid values: {values_found}. "
            f"Rows: {rows}"
        )

    return True


# ============================================================
# UNIQUE VALUE CHECK
# ============================================================

def check_unique_column(
    dataframe: pd.DataFrame,
    column: str,
    dataset_name: str
) -> bool:

    duplicates = dataframe[
        dataframe[column].duplicated(keep=False)
    ]

    if not duplicates.empty:

        duplicate_values = (
            duplicates[column]
            .unique()
            .tolist()
        )

        raise ValueError(
            f"{dataset_name}: Column '{column}' "
            f"contains duplicate values: "
            f"{duplicate_values}"
        )

    return True


# ============================================================
# DATE CHECK
# ============================================================

def check_date_column(
    dataframe: pd.DataFrame,
    column: str,
    dataset_name: str
) -> bool:

    converted = pd.to_datetime(
        dataframe[column],
        errors="coerce"
    )

    invalid = converted.isna()

    if invalid.any():

        rows = dataframe.index[invalid].tolist()
        values_found = dataframe.loc[
            invalid,
            column
        ].tolist()

        raise ValueError(
            f"{dataset_name}: Column '{column}' "
            f"contains invalid dates. "
            f"Invalid values: {values_found}. "
            f"Rows: {rows}"
        )

    return True


# ============================================================
# ALLOWED VALUES CHECK
# ============================================================

def check_allowed_values(
    dataframe: pd.DataFrame,
    column: str,
    allowed_values: set,
    dataset_name: str
) -> bool:

    invalid = ~dataframe[column].isin(
        allowed_values
    )

    if invalid.any():

        invalid_values = (
            dataframe.loc[
                invalid,
                column
            ]
            .unique()
            .tolist()
        )

        raise ValueError(
            f"{dataset_name}: Column '{column}' "
            f"contains invalid values: "
            f"{invalid_values}. "
            f"Allowed values: "
            f"{sorted(allowed_values)}"
        )

    return True


# ============================================================
# EMAIL CHECK
# ============================================================

def check_email_column(
    dataframe: pd.DataFrame,
    column: str,
    dataset_name: str
) -> bool:

    email_pattern = (
        r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    )

    invalid = ~dataframe[column].astype(str).str.match(
        email_pattern
    )

    if invalid.any():

        rows = dataframe.index[invalid].tolist()
        values_found = dataframe.loc[
            invalid,
            column
        ].tolist()

        raise ValueError(
            f"{dataset_name}: Invalid email values "
            f"in column '{column}': "
            f"{values_found}. "
            f"Rows: {rows}"
        )

    return True


# ============================================================
# CLIENT VALIDATION
# ============================================================

def validate_clients(
    dataframe: pd.DataFrame
) -> bool:

    dataset_name = "CLIENTS"


    check_positive_column(
        dataframe,
        "client_id",
        dataset_name
    )

    check_unique_column(
        dataframe,
        "client_id",
        dataset_name
    )

    check_date_column(
        dataframe,
        "created_date",
        dataset_name
    )

    # Change these values if your actual business rules differ.
    check_allowed_values(
        dataframe,
        "status",
        {
            "ACTIVE",
            "INACTIVE",
            "SUSPENDED"
        },
        dataset_name
    )

    check_allowed_values(
        dataframe,
        "risk_profile",
        {
            "LOW",
            "MEDIUM",
            "HIGH"
        },
        dataset_name
    )

    return True


# ============================================================
# PORTFOLIO VALIDATION
# ============================================================

def validate_portfolios(
    dataframe: pd.DataFrame
) -> bool:

    dataset_name = "PORTFOLIOS"

    check_positive_column(
        dataframe,
        "portfolio_id",
        dataset_name
    )

    check_unique_column(
        dataframe,
        "portfolio_id",
        dataset_name
    )


    check_positive_column(
        dataframe,
        "client_id",
        dataset_name
    )

    check_numeric_column(
        dataframe,
        "initial_value",
        dataset_name
    )

    check_numeric_column(
        dataframe,
        "current_value",
        dataset_name
    )

    check_non_negative_column(
        dataframe,
        "initial_value",
        dataset_name
    )

    check_non_negative_column(
        dataframe,
        "current_value",
        dataset_name
    )

    check_date_column(
        dataframe,
        "inception_date",
        dataset_name
    )

    check_allowed_values(
        dataframe,
        "status",
        {
            "ACTIVE",
            "INACTIVE",
            "CLOSED"
        },
        dataset_name
    )

    check_allowed_values(
        dataframe,
        "risk_profile",
        {
            "LOW",
            "MEDIUM",
            "HIGH"
        },
        dataset_name
    )

    return True


# ============================================================
# HOLDING VALIDATION
# ============================================================

def validate_holdings(
    dataframe: pd.DataFrame
) -> bool:

    dataset_name = "HOLDINGS"


    check_positive_column(
        dataframe,
        "holding_id",
        dataset_name
    )

    check_unique_column(
        dataframe,
        "holding_id",
        dataset_name
    )



    check_positive_column(
        dataframe,
        "portfolio_id",
        dataset_name
    )



    check_positive_column(
        dataframe,
        "security_id",
        dataset_name
    )

    check_numeric_column(
        dataframe,
        "quantity",
        dataset_name
    )

    check_positive_column(
        dataframe,
        "quantity",
        dataset_name
    )

    check_numeric_column(
        dataframe,
        "purchase_price",
        dataset_name
    )

    check_positive_column(
        dataframe,
        "purchase_price",
        dataset_name
    )

    check_numeric_column(
        dataframe,
        "current_price",
        dataset_name
    )

    check_positive_column(
        dataframe,
        "current_price",
        dataset_name
    )

    check_numeric_column(
        dataframe,
        "market_value",
        dataset_name
    )

    check_non_negative_column(
        dataframe,
        "market_value",
        dataset_name
    )

    check_date_column(
        dataframe,
        "as_of_date",
        dataset_name
    )

    return True


# ============================================================
# PERFORMANCE VALIDATION
# ============================================================

def validate_performance(
    dataframe: pd.DataFrame
) -> bool:

    dataset_name = "PORTFOLIO_PERFORMANCE"

    

    check_positive_column(
        dataframe,
        "performance_id",
        dataset_name
    )

    check_unique_column(
        dataframe,
        "performance_id",
        dataset_name
    )



    check_positive_column(
        dataframe,
        "portfolio_id",
        dataset_name
    )

    check_date_column(
        dataframe,
        "as_of_date",
        dataset_name
    )

    check_numeric_column(
        dataframe,
        "beginning_value",
        dataset_name
    )

    check_numeric_column(
        dataframe,
        "ending_value",
        dataset_name
    )

    check_numeric_column(
        dataframe,
        "return_amount",
        dataset_name
    )

    check_numeric_column(
        dataframe,
        "return_percent",
        dataset_name
    )

    check_non_negative_column(
        dataframe,
        "beginning_value",
        dataset_name
    )

    check_non_negative_column(
        dataframe,
        "ending_value",
        dataset_name
    )

    return True


# ============================================================
# COLUMN DEFINITIONS
# ============================================================

CLIENT_COLUMNS = [
    "client_id",
    "client_name",
    "client_type",
    "country",
    "risk_profile",
    "created_date",
    "status"
]


PORTFOLIO_COLUMNS = [
    "portfolio_id",
    "client_id",
    "portfolio_name",
    "portfolio_type",
    "base_currency",
    "risk_profile",
    "initial_value",
    "current_value",
    "inception_date",
    "status"
]


HOLDING_COLUMNS = [
    "holding_id",
    "portfolio_id",
    "security_id",
    "quantity",
    "purchase_price",
    "current_price",
    "market_value",
    "as_of_date"
]


PERFORMANCE_COLUMNS = [
    "performance_id",
    "portfolio_id",
    "as_of_date",
    "beginning_value",
    "ending_value",
    "return_amount",
    "return_percent"
]


# ============================================================
# MAIN CSV VALIDATION FUNCTION
# ============================================================

def validate_csv_ingestion(
    file_path: str,
    required_columns: list,
    dataset_name: str
):

    # --------------------------------------------------------
    # FILE VALIDATION
    # --------------------------------------------------------

    check_file_exists(file_path)

    check_file_readable(file_path)

    check_file_not_empty(file_path)

    check_file_name(
        file_path,
        dataset_name
    )

    # --------------------------------------------------------
    # CSV PARSING
    # --------------------------------------------------------

    dataframe = check_csv_parsing(file_path)

    # --------------------------------------------------------
    # DATAFRAME VALIDATION
    # --------------------------------------------------------

    check_dataframe_not_empty(
        dataframe,
        dataset_name
    )

    # --------------------------------------------------------
    # COLUMN VALIDATION
    # --------------------------------------------------------

    check_required_columns(
        dataframe,
        required_columns,
        dataset_name
    )

    check_unexpected_columns(
        dataframe,
        required_columns,
        dataset_name
    )

    # --------------------------------------------------------
    # VALUE VALIDATION
    # --------------------------------------------------------

    check_null_values(
        dataframe,
        required_columns,
        dataset_name
    )

    check_empty_strings(
        dataframe,
        required_columns,
        dataset_name
    )

    # --------------------------------------------------------
    # DATASET-SPECIFIC VALIDATION
    # --------------------------------------------------------

    if dataset_name == "CLIENTS":

        validate_clients(dataframe)

    elif dataset_name == "PORTFOLIOS":

        validate_portfolios(dataframe)

    elif dataset_name == "HOLDINGS":

        validate_holdings(dataframe)

    elif dataset_name == "PORTFOLIO_PERFORMANCE":

        validate_performance(dataframe)

    else:

        raise ValueError(
            f"Unknown dataset: {dataset_name}"
        )

    return dataframe


# ============================================================
# JSON VALIDATION
# ============================================================

def check_json_parsing(file_path: str):

    try:

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

        return data

    except json.JSONDecodeError as e:

        raise ValueError(
            f"Invalid JSON file: {file_path}"
        ) from e
