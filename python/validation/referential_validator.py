"""
Referential-integrity validation for Participant 2.

This module validates relationships between the five source datasets.

Relationships:
    portfolios.client_id
        -> clients.client_id

    holdings.portfolio_id
        -> portfolios.portfolio_id

    holdings.security_id
        -> securities.security_id

    portfolio_performance.portfolio_id
        -> portfolios.portfolio_id

Responsibilities:
    - Detect child records whose parent identifier does not exist.
    - Preserve row-level traceability.
    - Return standardized validation issues.

This module does NOT:
    - modify source data
    - delete invalid records
    - create missing parent records
    - perform domain validation
    - perform business validation
    - perform duplicate validation
"""

from dataclasses import dataclass
from typing import Dict, List

import pandas as pd

from .config import REFERENTIAL_RULES


@dataclass
class ReferentialValidationIssue:
    """Represents one referential-integrity violation."""

    dataset_name: str
    row_index: int
    column_name: str
    rule_id: str
    rule_name: str
    severity: str
    actual_value: object
    expected_value: object
    parent_dataset: str
    parent_column: str
    message: str


@dataclass
class ReferentialValidationResult:
    """Result of referential validation."""

    dataset_name: str
    valid: bool
    issues: List[ReferentialValidationIssue]

    @property
    def error_count(self) -> int:
        """Return number of referential-integrity errors."""

        return len(self.issues)


class ReferentialValidationError(Exception):
    """Raised when referential validation cannot be performed."""


class ReferentialValidator:
    """Reusable referential-integrity validator."""

    def __init__(
        self,
        referential_rules: List[Dict] | None = None,
    ):
        self.referential_rules = (
            referential_rules
            if referential_rules is not None
            else REFERENTIAL_RULES
        )

    # ==================================================================
    # Public API
    # ==================================================================

    def validate(
        self,
        datasets: Dict[str, pd.DataFrame],
    ) -> Dict[str, ReferentialValidationResult]:
        """
        Validate all configured parent-child relationships.

        Returns results grouped by child dataset.
        """

        if not datasets:
            raise ReferentialValidationError(
                "No datasets were provided for "
                "referential validation."
            )

        results = {}

        for rule in self.referential_rules:

            child_dataset = rule[
                "child_dataset"
            ]

            parent_dataset = rule[
                "parent_dataset"
            ]

            child_column = rule[
                "child_column"
            ]

            parent_column = rule[
                "parent_column"
            ]

            self._validate_dataset_exists(
                datasets,
                child_dataset,
            )

            self._validate_dataset_exists(
                datasets,
                parent_dataset,
            )

            child_dataframe = datasets[
                child_dataset
            ]

            parent_dataframe = datasets[
                parent_dataset
            ]

            self._validate_columns(
                child_dataframe,
                child_dataset,
                [child_column],
            )

            self._validate_columns(
                parent_dataframe,
                parent_dataset,
                [parent_column],
            )

            issues = self._find_missing_parents(
                child_dataframe=child_dataframe,
                parent_dataframe=parent_dataframe,
                child_dataset=child_dataset,
                child_column=child_column,
                parent_dataset=parent_dataset,
                parent_column=parent_column,
                rule_id=rule["rule_id"],
                rule_name=rule["rule_name"],
            )

            if child_dataset not in results:
                results[child_dataset] = (
                    ReferentialValidationResult(
                        dataset_name=child_dataset,
                        valid=True,
                        issues=[],
                    )
                )

            results[
                child_dataset
            ].issues.extend(issues)

            results[
                child_dataset
            ].valid = (
                len(
                    results[
                        child_dataset
                    ].issues
                )
                == 0
            )

        # Include datasets with no configured child relationship.
        for dataset_name in datasets:
            if dataset_name not in results:
                results[dataset_name] = (
                    ReferentialValidationResult(
                        dataset_name=dataset_name,
                        valid=True,
                        issues=[],
                    )
                )

        return results

    # ==================================================================
    # Missing parent detection
    # ==================================================================

    def _find_missing_parents(
        self,
        child_dataframe: pd.DataFrame,
        parent_dataframe: pd.DataFrame,
        child_dataset: str,
        child_column: str,
        parent_dataset: str,
        parent_column: str,
        rule_id: str,
        rule_name: str,
    ) -> List[ReferentialValidationIssue]:
        """
        Find child records whose parent identifier is absent.

        Null values are skipped because null handling belongs to
        the NullValidator.
        """

        parent_values = set(
            parent_dataframe[
                parent_column
            ].dropna()
        )

        issues = []

        for row_index, value in (
            child_dataframe[
                child_column
            ].items()
        ):

            if self._is_missing(value):
                continue

            if value not in parent_values:

                issues.append(
                    ReferentialValidationIssue(
                        dataset_name=child_dataset,
                        row_index=int(row_index),
                        column_name=child_column,
                        rule_id=rule_id,
                        rule_name=rule_name,
                        severity="ERROR",
                        actual_value=value,
                        expected_value=(
                            f"Existing value in "
                            f"{parent_dataset}."
                            f"{parent_column}"
                        ),
                        parent_dataset=parent_dataset,
                        parent_column=parent_column,
                        message=(
                            f"Referenced value "
                            f"{value!r} does not exist "
                            f"in "
                            f"{parent_dataset}."
                            f"{parent_column}."
                        ),
                    )
                )

        return issues

    # ==================================================================
    # Validation helpers
    # ==================================================================

    @staticmethod
    def _is_missing(value) -> bool:
        """
        Determine whether a foreign-key value is missing.

        Missing values belong to null validation and are therefore
        not duplicated as referential-integrity errors.
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

    @staticmethod
    def _validate_dataset_exists(
        datasets: Dict[str, pd.DataFrame],
        dataset_name: str,
    ) -> None:
        """Ensure a configured dataset is available."""

        if dataset_name not in datasets:
            raise ReferentialValidationError(
                f"Dataset '{dataset_name}' is required "
                f"for referential validation but was "
                f"not provided."
            )

        if not isinstance(
            datasets[dataset_name],
            pd.DataFrame,
        ):
            raise ReferentialValidationError(
                f"Dataset '{dataset_name}' must be "
                f"a pandas DataFrame."
            )

    @staticmethod
    def _validate_columns(
        dataframe: pd.DataFrame,
        dataset_name: str,
        columns: List[str],
    ) -> None:
        """Ensure required relationship columns exist."""

        missing = [
            column
            for column in columns
            if column not in dataframe.columns
        ]

        if missing:
            raise ReferentialValidationError(
                f"Dataset '{dataset_name}' is missing "
                f"referential-integrity columns: "
                f"{missing}."
            )

    # ==================================================================
    # Convenience methods
    # ==================================================================

    def is_valid(
        self,
        datasets: Dict[str, pd.DataFrame],
    ) -> bool:
        """Return True when all relationships are valid."""

        results = self.validate(
            datasets
        )

        return all(
            result.valid
            for result in results.values()
        )

    def get_all_issues(
        self,
        datasets: Dict[str, pd.DataFrame],
    ) -> List[ReferentialValidationIssue]:
        """Return all referential issues as one list."""

        results = self.validate(
            datasets
        )

        issues = []

        for result in results.values():
            issues.extend(
                result.issues
            )

        return issues