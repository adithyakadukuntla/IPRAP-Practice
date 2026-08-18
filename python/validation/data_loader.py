"""
Raw data loader for Participant 2.

Responsibilities:
    - Locate configured raw files
    - Validate file existence
    - Validate file format
    - Load CSV files
    - Load JSON files
    - Return pandas DataFrames

Important:
    This module NEVER modifies files under data/raw/.
"""

from pathlib import Path
from typing import Dict

import pandas as pd

from .config import (
    DATASETS,
    RAW_DATA_DIR,
    RAW_DATA_FILES,
    SUPPORTED_FILE_EXTENSIONS,
)


class DataLoaderError(Exception):
    """Raised when a raw dataset cannot be loaded safely."""


class RawDataLoader:
    """Loads the five raw datasets supplied by Participant 1."""

    def __init__(self, raw_data_dir: str = RAW_DATA_DIR):
        self.raw_data_dir = Path(raw_data_dir)

    # ------------------------------------------------------------------
    # Dataset paths
    # ------------------------------------------------------------------

    def get_dataset_directory(self, dataset_name: str) -> Path:
        """Return the raw-data directory for a dataset."""

        if dataset_name not in DATASETS:
            raise DataLoaderError(
                f"Unknown dataset: {dataset_name}"
            )

        return self.raw_data_dir / dataset_name

    def get_file_path(self, dataset_name: str) -> Path:
        """Return the configured raw source-file path."""

        if dataset_name not in RAW_DATA_FILES:
            raise DataLoaderError(
                f"No file configuration found for dataset: "
                f"{dataset_name}"
            )

        filename = RAW_DATA_FILES[dataset_name]["filename"]

        if not filename:
            raise DataLoaderError(
                f"No filename configured for dataset: "
                f"{dataset_name}"
            )

        return (
            self.get_dataset_directory(dataset_name)
            / filename
        )

    # ------------------------------------------------------------------
    # File validation
    # ------------------------------------------------------------------

    def validate_file_exists(self, dataset_name: str) -> Path:
        """Validate that the configured raw file exists."""

        file_path = self.get_file_path(dataset_name)

        if not file_path.exists():
            raise DataLoaderError(
                f"Raw file does not exist: {file_path}"
            )

        if not file_path.is_file():
            raise DataLoaderError(
                f"Raw path is not a file: {file_path}"
            )

        return file_path

    def validate_file_format(
        self,
        dataset_name: str,
        file_path: Path,
    ) -> None:
        """Validate the file extension against configuration."""

        actual_format = (
            file_path.suffix.lower().lstrip(".")
        )

        supported_formats = {
            extension.lower().lstrip(".")
            for extension in SUPPORTED_FILE_EXTENSIONS
        }

        if actual_format not in supported_formats:
            raise DataLoaderError(
                f"Unsupported file format for "
                f"{dataset_name}: "
                f".{actual_format}"
            )

        expected_format = RAW_DATA_FILES[
            dataset_name
        ]["format"]

        if actual_format != expected_format.lower():
            raise DataLoaderError(
                f"Unexpected file format for "
                f"{dataset_name}. "
                f"Expected: {expected_format}, "
                f"Actual: {actual_format}"
            )

    def validate_not_empty(self, file_path: Path) -> None:
        """Validate that the source file is not empty."""

        if file_path.stat().st_size == 0:
            raise DataLoaderError(
                f"Raw file is empty: {file_path}"
            )

    # ------------------------------------------------------------------
    # Readers
    # ------------------------------------------------------------------

    def load_csv(self, file_path: Path) -> pd.DataFrame:
        """Load a CSV file."""

        try:
            return pd.read_csv(file_path)

        except Exception as exc:
            raise DataLoaderError(
                f"Failed to read CSV file "
                f"{file_path}: {exc}"
            ) from exc

    def load_json(self, file_path: Path) -> pd.DataFrame:
        """Load a JSON file containing records."""

        try:
            return pd.read_json(file_path)

        except Exception as exc:
            raise DataLoaderError(
                f"Failed to read JSON file "
                f"{file_path}: {exc}"
            ) from exc

    def load_file(self, file_path: Path) -> pd.DataFrame:
        """Load a file using its extension."""

        extension = file_path.suffix.lower()

        if extension == ".csv":
            return self.load_csv(file_path)

        if extension == ".json":
            return self.load_json(file_path)

        raise DataLoaderError(
            f"No loader implemented for "
            f"file type: {extension}"
        )

    # ------------------------------------------------------------------
    # DataFrame validation
    # ------------------------------------------------------------------

    def validate_dataframe_not_empty(
        self,
        dataset_name: str,
        dataframe: pd.DataFrame,
    ) -> None:
        """Validate that the loaded dataset contains records."""

        if dataframe.empty:
            raise DataLoaderError(
                f"Dataset contains no records: "
                f"{dataset_name}"
            )

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def load_dataset(
        self,
        dataset_name: str,
    ) -> pd.DataFrame:
        """Load one configured raw dataset."""

        file_path = self.validate_file_exists(
            dataset_name
        )

        self.validate_file_format(
            dataset_name,
            file_path,
        )

        self.validate_not_empty(file_path)

        dataframe = self.load_file(file_path)

        self.validate_dataframe_not_empty(
            dataset_name,
            dataframe,
        )

        return dataframe

    def load_all_datasets(
        self,
    ) -> Dict[str, pd.DataFrame]:
        """Load all five configured raw datasets."""

        datasets = {}

        for dataset_name in DATASETS:
            datasets[dataset_name] = (
                self.load_dataset(dataset_name)
            )

        return datasets