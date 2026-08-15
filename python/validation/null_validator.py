"""
Null and mandatory-field validation for Participant 2.

Responsibilities:
    - Determine which fields are mandatory.
    - Detect null values.
    - Detect blank string values for mandatory fields.
    - Return reusable validation results.

The source raw files are never modified.
"""

from dataclasses import dataclass
from typing import Dict, List

import pandas as pd

from .config import EXPECTED_COLUMNS


@dataclass
class NullValidationIssue:
    """Represents one mandatory-field null issue."""

    dataset_name: str
    row_index: int
    column_name: str
    actual_value: object
    message: str


@dataclass
class NullValidationResult:
    """Result of null validation for one dataset."""

    dataset_name: str
    valid: bool
    issues: List[NullValidationIssue]

    @property
    def error_count(self) -> int:
        """Number of null/mandatory-field errors."""

        return len(self.issues)


class NullValidationError(Exception):
    """Raised when null validation cannot be performed."""


class NullValidator:
    """
    Reusable mandatory-field validator.

    Unless a field is explicitly configured as optional, every field
    in the project's expected schema is treated as mandatory.
    """

    def __init__(
        self,
        mandatory_columns: Dict[str, List[str]] | None = None,
    ):
        self.mandatory_columns = (
            mandatory_columns
            if mandatory_columns is not None
            else EXPECTED_COLUMNS
        )

    # ------------------------------------------------------------------
    # Missing-value helper
    # ------------------------------------------------------------------

    @staticmethod
    def _is_missing(value) -> bool:
        """
        Determine whether a value should be treated as missing.

        Missing means:
            - None
            - NaN / pandas NA
            - empty string
            - whitespace-only string
        """

        if value is None:
            return True

        try:
            if pd.isna(value):
                return True
        except (
            TypeError,
            ValueError,
        ):
            pass

        if isinstance(
            value,
            str,
        ):
            return value.strip() == ""

        return False

    # ------------------------------------------------------------------
    # Single-dataset validation
    # ------------------------------------------------------------------

    def validate_dataset(
        self,
        dataset_name: str,
        dataframe: pd.DataFrame,
    ) -> NullValidationResult:
        """
        Validate all mandatory fields for one dataset.
        """

        if dataset_name not in self.mandatory_columns:
            raise NullValidationError(
                f"No mandatory-field configuration "
                f"found for dataset: {dataset_name}"
            )

        if not isinstance(
            dataframe,
            pd.DataFrame,
        ):
            raise NullValidationError(
                f"Expected pandas DataFrame for "
                f"dataset: {dataset_name}"
            )

        issues = []

        required_columns = (
            self.mandatory_columns[
                dataset_name
            ]
        )

        for column_name in required_columns:

            if column_name not in dataframe.columns:
                raise NullValidationError(
                    f"Column '{column_name}' is missing "
                    f"from dataset '{dataset_name}'. "
                    f"Run schema validation first."
                )

            series = dataframe[column_name]

            for row_index, value in series.items():

                if self._is_missing(value):
                    issues.append(
                        NullValidationIssue(
                            dataset_name=dataset_name,
                            row_index=int(row_index),
                            column_name=column_name,
                            actual_value=value,
                            message=(
                                f"Mandatory field "
                                f"'{column_name}' "
                                f"must not be null or blank."
                            ),
                        )
                    )

        return NullValidationResult(
            dataset_name=dataset_name,
            valid=len(issues) == 0,
            issues=issues,
        )

    # ------------------------------------------------------------------
    # All-dataset validation
    # ------------------------------------------------------------------

    def validate_all(
        self,
        datasets: Dict[str, pd.DataFrame],
    ) -> Dict[str, NullValidationResult]:
        """Validate mandatory fields across all datasets."""

        if not datasets:
            raise NullValidationError(
                "No datasets were provided for "
                "null validation."
            )

        results = {}

        for dataset_name, dataframe in (
            datasets.items()
        ):
            results[dataset_name] = (
                self.validate_dataset(
                    dataset_name,
                    dataframe,
                )
            )

        return results

    # ------------------------------------------------------------------
    # Convenience
    # ------------------------------------------------------------------

    def is_valid(
        self,
        dataset_name: str,
        dataframe: pd.DataFrame,
    ) -> bool:
        """Return True when no mandatory fields are missing."""

        return self.validate_dataset(
            dataset_name,
            dataframe,
        ).valid