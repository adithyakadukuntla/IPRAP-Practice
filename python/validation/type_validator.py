"""
Data-type validation for Participant 2.

Responsibilities:
    - Validate logical string fields.
    - Validate numeric fields.
    - Validate date fields.
    - Detect malformed values.
    - Return reusable validation results.

This module does NOT:
    - modify raw data
    - standardize values
    - validate business rules
    - validate domain values
    - validate relationships
    - reject/write records
"""

from dataclasses import dataclass
from typing import Dict, List

import pandas as pd

from .config import (
    EXPECTED_DATA_TYPES,
    EXPECTED_DATE_FORMAT,
)


@dataclass
class TypeValidationIssue:
    """Represents one data-type validation issue."""

    dataset_name: str
    row_index: int
    column_name: str
    expected_type: str
    actual_value: object
    message: str


@dataclass
class TypeValidationResult:
    """Result of type validation for one dataset."""

    dataset_name: str
    valid: bool
    issues: List[TypeValidationIssue]

    @property
    def error_count(self) -> int:
        """Number of type errors."""

        return len(self.issues)


class TypeValidationError(Exception):
    """Raised when type validation cannot be performed."""


class TypeValidator:
    """Reusable logical data-type validator."""

    def __init__(
        self,
        expected_data_types: Dict | None = None,
    ):
        self.expected_data_types = (
            expected_data_types
            if expected_data_types is not None
            else EXPECTED_DATA_TYPES
        )

    # ------------------------------------------------------------------
    # Dataset validation
    # ------------------------------------------------------------------

    def validate_dataset(
        self,
        dataset_name: str,
        dataframe: pd.DataFrame,
    ) -> TypeValidationResult:
        """
        Validate all configured column types for one dataset.
        """

        if dataset_name not in self.expected_data_types:
            raise TypeValidationError(
                f"No type configuration found for "
                f"dataset: {dataset_name}"
            )

        if not isinstance(
            dataframe,
            pd.DataFrame,
        ):
            raise TypeValidationError(
                f"Expected pandas DataFrame for "
                f"dataset: {dataset_name}"
            )

        issues = []

        expected_types = (
            self.expected_data_types[
                dataset_name
            ]
        )

        for column_name, expected_type in (
            expected_types.items()
        ):

            if column_name not in dataframe.columns:
                raise TypeValidationError(
                    f"Column '{column_name}' is missing "
                    f"from dataset '{dataset_name}'. "
                    f"Run schema validation first."
                )

            series = dataframe[column_name]

            for row_index, value in series.items():

                # Missing values are handled by the null validator.
                if pd.isna(value):
                    continue

                if expected_type == "string":
                    valid = self._is_string(value)

                elif expected_type == "numeric":
                    valid = self._is_numeric(value)

                elif expected_type == "date":
                    valid = self._is_date(value)

                else:
                    raise TypeValidationError(
                        f"Unsupported expected type "
                        f"'{expected_type}' for "
                        f"{dataset_name}.{column_name}"
                    )

                if not valid:
                    issues.append(
                        TypeValidationIssue(
                            dataset_name=dataset_name,
                            row_index=int(row_index),
                            column_name=column_name,
                            expected_type=expected_type,
                            actual_value=value,
                            message=(
                                f"Expected {expected_type} "
                                f"value but received "
                                f"{repr(value)}"
                            ),
                        )
                    )

        return TypeValidationResult(
            dataset_name=dataset_name,
            valid=len(issues) == 0,
            issues=issues,
        )

    # ------------------------------------------------------------------
    # Type helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _is_string(value) -> bool:
        """
        Validate string-like values.

        IDs are intentionally treated as strings here.
        Format/pattern validation is a later responsibility.
        """

        return isinstance(
            value,
            str,
        )

    @staticmethod
    def _is_numeric(value) -> bool:
        """
        Validate numeric values.

        Booleans are explicitly rejected because Python considers bool
        a subclass of int, but True/False are not valid financial values.
        """

        if isinstance(value, bool):
            return False

        try:
            numeric_value = float(value)
        except (
            TypeError,
            ValueError,
        ):
            return False

        return pd.notna(
            numeric_value
        ) and pd.api.types.is_number(
            numeric_value
        )

    @staticmethod
    def _is_date(value) -> bool:
        """
        Validate a date using the project's expected YYYY-MM-DD format.

        This validates the representation without modifying the original
        value.
        """

        if isinstance(
            value,
            (
                pd.Timestamp,
                pd.DatetimeIndex,
            ),
        ):
            return True

        if not isinstance(
            value,
            str,
        ):
            return False

        try:
            parsed = pd.to_datetime(
                value,
                format=EXPECTED_DATE_FORMAT,
                errors="raise",
            )

        except (
            ValueError,
            TypeError,
        ):
            return False

        return (
            parsed.strftime(
                EXPECTED_DATE_FORMAT
            )
            == value
        )

    # ------------------------------------------------------------------
    # All-dataset validation
    # ------------------------------------------------------------------

    def validate_all(
        self,
        datasets: Dict[str, pd.DataFrame],
    ) -> Dict[str, TypeValidationResult]:
        """Validate types for all supplied datasets."""

        if not datasets:
            raise TypeValidationError(
                "No datasets were provided for "
                "type validation."
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
        """Return True when the dataset contains no type errors."""

        return self.validate_dataset(
            dataset_name,
            dataframe,
        ).valid