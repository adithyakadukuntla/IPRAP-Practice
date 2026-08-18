"""
Schema validation for the Participant 2 data-quality framework.

Responsibilities:
    - Compare incoming dataset columns with the expected schema.
    - Detect missing required columns.
    - Detect unexpected columns.
    - Validate that the dataset structure is correct.
    - Provide reusable validation results.

This module does NOT:
    - validate data types
    - validate null values
    - validate duplicates
    - validate domain values
    - validate business rules
    - modify raw data
"""

from dataclasses import dataclass
from typing import Dict, List

import pandas as pd

from .config import DATASETS, EXPECTED_COLUMNS


@dataclass
class SchemaValidationResult:
    """
    Result of validating one dataset's schema.
    """

    dataset_name: str
    valid: bool
    expected_columns: List[str]
    actual_columns: List[str]
    missing_columns: List[str]
    unexpected_columns: List[str]

    @property
    def error_count(self) -> int:
        """Return the number of schema problems."""

        return (
            len(self.missing_columns)
            + len(self.unexpected_columns)
        )

    @property
    def error_message(self) -> str:
        """Return a human-readable schema error message."""

        if self.valid:
            return "Schema is valid."

        messages = []

        if self.missing_columns:
            messages.append(
                "Missing required columns: "
                + ", ".join(
                    self.missing_columns
                )
            )

        if self.unexpected_columns:
            messages.append(
                "Unexpected columns: "
                + ", ".join(
                    self.unexpected_columns
                )
            )

        return " | ".join(messages)


class SchemaValidationError(Exception):
    """Raised when schema validation cannot be performed."""


class SchemaValidator:
    """
    Reusable validator for dataset schemas.

    Schema validation is based on column names.

    Column order is intentionally ignored.
    """

    def __init__(
        self,
        expected_columns: Dict[str, List[str]] | None = None,
    ):
        self.expected_columns = (
            expected_columns
            if expected_columns is not None
            else EXPECTED_COLUMNS
        )

    # ------------------------------------------------------------------
    # Configuration validation
    # ------------------------------------------------------------------

    def validate_dataset_name(
        self,
        dataset_name: str,
    ) -> None:
        """Verify that the dataset has an expected schema."""

        if dataset_name not in self.expected_columns:
            raise SchemaValidationError(
                f"No expected schema configured for "
                f"dataset: {dataset_name}"
            )

    # ------------------------------------------------------------------
    # Single-dataset schema validation
    # ------------------------------------------------------------------

    def validate_dataset(
        self,
        dataset_name: str,
        dataframe: pd.DataFrame,
    ) -> SchemaValidationResult:
        """
        Validate one DataFrame against its expected schema.
        """

        self.validate_dataset_name(
            dataset_name
        )

        if not isinstance(
            dataframe,
            pd.DataFrame,
        ):
            raise SchemaValidationError(
                f"Expected pandas DataFrame for "
                f"dataset: {dataset_name}"
            )

        expected = list(
            self.expected_columns[
                dataset_name
            ]
        )

        actual = list(
            dataframe.columns
        )

        expected_set = set(expected)
        actual_set = set(actual)

        missing_columns = [
            column
            for column in expected
            if column not in actual_set
        ]

        unexpected_columns = [
            column
            for column in actual
            if column not in expected_set
        ]

        valid = (
            len(missing_columns) == 0
            and len(unexpected_columns) == 0
        )

        return SchemaValidationResult(
            dataset_name=dataset_name,
            valid=valid,
            expected_columns=expected,
            actual_columns=actual,
            missing_columns=missing_columns,
            unexpected_columns=unexpected_columns,
        )

    # ------------------------------------------------------------------
    # All-dataset validation
    # ------------------------------------------------------------------

    def validate_all(
        self,
        datasets: Dict[str, pd.DataFrame],
    ) -> Dict[str, SchemaValidationResult]:
        """
        Validate all supplied datasets.

        Returns one SchemaValidationResult per dataset.
        """

        if not datasets:
            raise SchemaValidationError(
                "No datasets were provided for "
                "schema validation."
            )

        results = {}

        for dataset_name, dataframe in datasets.items():
            results[dataset_name] = (
                self.validate_dataset(
                    dataset_name,
                    dataframe,
                )
            )

        return results

    # ------------------------------------------------------------------
    # Convenience methods
    # ------------------------------------------------------------------

    def is_valid(
        self,
        dataset_name: str,
        dataframe: pd.DataFrame,
    ) -> bool:
        """Return True if the dataset schema is valid."""

        result = self.validate_dataset(
            dataset_name,
            dataframe,
        )

        return result.valid

    def validate_and_raise(
        self,
        dataset_name: str,
        dataframe: pd.DataFrame,
    ) -> None:
        """
        Validate a dataset and raise an exception if its schema
        is invalid.

        This method is useful when a caller needs fail-fast
        behavior.
        """

        result = self.validate_dataset(
            dataset_name,
            dataframe,
        )

        if not result.valid:
            raise SchemaValidationError(
                f"Invalid schema for "
                f"{dataset_name}: "
                f"{result.error_message}"
            )