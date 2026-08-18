"""
Duplicate detection for Participant 2.

Responsibilities:
    - Detect duplicate business keys.
    - Detect the special Holdings composite duplicate condition.
    - Preserve all duplicate records.
    - Report duplicate groups without modifying the source data.

This module does NOT:
    - delete duplicates
    - modify records
    - decide whether a duplicate is ultimately accepted
    - perform domain validation
    - perform business-value validation
"""

from dataclasses import dataclass
from typing import Dict, List

import pandas as pd

from .config import (
    DUPLICATE_KEYS,
    HOLDINGS_COMPOSITE_DUPLICATE_KEY,
)


@dataclass
class DuplicateIssue:
    """Represents one duplicate business-key group."""

    dataset_name: str
    duplicate_type: str
    key_columns: List[str]
    key_values: Dict[str, object]
    row_indices: List[int]
    duplicate_count: int
    message: str


@dataclass
class DuplicateValidationResult:
    """Result of duplicate validation for one dataset."""

    dataset_name: str
    valid: bool
    issues: List[DuplicateIssue]

    @property
    def error_count(self) -> int:
        """Number of duplicate groups detected."""

        return len(self.issues)

    @property
    def duplicate_record_count(self) -> int:
        """
        Number of records belonging to duplicate groups.

        If a key appears three times, all three records are counted.
        """

        total = 0

        for issue in self.issues:
            total += issue.duplicate_count

        return total


class DuplicateValidationError(Exception):
    """Raised when duplicate validation cannot be performed."""


class DuplicateValidator:
    """Reusable business-key duplicate validator."""

    def __init__(
        self,
        duplicate_keys: Dict[str, List[str]] | None = None,
        holdings_composite_key: List[str] | None = None,
    ):
        self.duplicate_keys = (
            duplicate_keys
            if duplicate_keys is not None
            else DUPLICATE_KEYS
        )

        self.holdings_composite_key = (
            holdings_composite_key
            if holdings_composite_key is not None
            else HOLDINGS_COMPOSITE_DUPLICATE_KEY
        )

    # ------------------------------------------------------------------
    # Primary duplicate detection
    # ------------------------------------------------------------------

    def validate_dataset(
        self,
        dataset_name: str,
        dataframe: pd.DataFrame,
    ) -> DuplicateValidationResult:
        """
        Detect duplicate records using the configured business key.
        """

        if dataset_name not in self.duplicate_keys:
            raise DuplicateValidationError(
                f"No duplicate-key configuration found "
                f"for dataset: {dataset_name}"
            )

        if not isinstance(
            dataframe,
            pd.DataFrame,
        ):
            raise DuplicateValidationError(
                f"Expected pandas DataFrame for "
                f"dataset: {dataset_name}"
            )

        key_columns = self.duplicate_keys[
            dataset_name
        ]

        self._validate_key_columns(
            dataset_name,
            dataframe,
            key_columns,
        )

        issues = self._find_duplicate_groups(
            dataset_name=dataset_name,
            dataframe=dataframe,
            key_columns=key_columns,
            duplicate_type="BUSINESS_KEY",
        )

        # --------------------------------------------------------------
        # Special Holdings composite check
        # --------------------------------------------------------------

        if dataset_name == "holdings":

            composite_issues = (
                self._find_duplicate_groups(
                    dataset_name=dataset_name,
                    dataframe=dataframe,
                    key_columns=(
                        self.holdings_composite_key
                    ),
                    duplicate_type=(
                        "HOLDINGS_COMPOSITE_KEY"
                    ),
                )
            )

            issues.extend(
                composite_issues
            )

        return DuplicateValidationResult(
            dataset_name=dataset_name,
            valid=len(issues) == 0,
            issues=issues,
        )

    # ------------------------------------------------------------------
    # Duplicate group detection
    # ------------------------------------------------------------------

    def _find_duplicate_groups(
        self,
        dataset_name: str,
        dataframe: pd.DataFrame,
        key_columns: List[str],
        duplicate_type: str,
    ) -> List[DuplicateIssue]:
        """
        Find duplicate groups using one or more business-key columns.

        Every record belonging to the duplicate group is preserved.
        """

        grouped = (
            dataframe
            .groupby(
                key_columns,
                dropna=False,
                sort=False,
            )
        )

        issues = []

        for key_values, group in grouped:

            # A single record is not a duplicate.
            if len(group) <= 1:
                continue

            if not isinstance(
                key_values,
                tuple,
            ):
                key_values = (
                    key_values,
                )

            key_value_dict = dict(
                zip(
                    key_columns,
                    key_values,
                )
            )

            row_indices = [
                int(index)
                for index in group.index
            ]

            issues.append(
                DuplicateIssue(
                    dataset_name=dataset_name,
                    duplicate_type=duplicate_type,
                    key_columns=key_columns.copy(),
                    key_values=key_value_dict,
                    row_indices=row_indices,
                    duplicate_count=len(group),
                    message=(
                        f"Duplicate {duplicate_type.lower()} "
                        f"detected for key "
                        f"{key_value_dict}. "
                        f"Records must remain traceable."
                    ),
                )
            )

        return issues

    # ------------------------------------------------------------------
    # Key validation
    # ------------------------------------------------------------------

    @staticmethod
    def _validate_key_columns(
        dataset_name: str,
        dataframe: pd.DataFrame,
        key_columns: List[str],
    ) -> None:
        """Ensure all configured key columns exist."""

        missing_columns = [
            column
            for column in key_columns
            if column not in dataframe.columns
        ]

        if missing_columns:
            raise DuplicateValidationError(
                f"Dataset '{dataset_name}' is missing "
                f"duplicate-key columns: "
                f"{missing_columns}. "
                f"Run schema validation first."
            )

    # ------------------------------------------------------------------
    # All datasets
    # ------------------------------------------------------------------

    def validate_all(
        self,
        datasets: Dict[str, pd.DataFrame],
    ) -> Dict[str, DuplicateValidationResult]:
        """Validate duplicates across all supplied datasets."""

        if not datasets:
            raise DuplicateValidationError(
                "No datasets were provided for "
                "duplicate validation."
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
        """Return True when no duplicate groups exist."""

        return self.validate_dataset(
            dataset_name,
            dataframe,
        ).valid