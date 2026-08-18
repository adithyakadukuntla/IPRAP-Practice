"""
Domain-value validation for Participant 2.

Responsibilities:
    - Validate configured categorical/domain fields.
    - Detect values outside the allowed domain.
    - Preserve row-level information about invalid values.
    - Return reusable validation results.

This module does NOT:
    - modify source data
    - standardize values
    - perform business calculations
    - perform referential checks
    - remove invalid records
"""

from dataclasses import dataclass
from typing import Dict, List

import pandas as pd

from .config import DOMAIN_RULES


@dataclass
class DomainValidationIssue:
    """Represents one invalid domain value."""

    dataset_name: str
    row_index: int
    column_name: str
    actual_value: object
    allowed_values: List[str]
    message: str


@dataclass
class DomainValidationResult:
    """Result of domain validation for one dataset."""

    dataset_name: str
    valid: bool
    issues: List[DomainValidationIssue]

    @property
    def error_count(self) -> int:
        """Return the number of invalid domain values."""

        return len(self.issues)


class DomainValidationError(Exception):
    """Raised when domain validation cannot be performed."""


class DomainValidator:
    """Reusable validator for configured categorical domains."""

    def __init__(
        self,
        domain_rules: Dict | None = None,
    ):
        self.domain_rules = (
            domain_rules
            if domain_rules is not None
            else DOMAIN_RULES
        )

    # ------------------------------------------------------------------
    # Single dataset
    # ------------------------------------------------------------------

    def validate_dataset(
        self,
        dataset_name: str,
        dataframe: pd.DataFrame,
    ) -> DomainValidationResult:
        """
        Validate all configured domain fields for one dataset.
        """

        if dataset_name not in self.domain_rules:
            # Datasets without categorical rules are considered
            # valid for this validation category.
            return DomainValidationResult(
                dataset_name=dataset_name,
                valid=True,
                issues=[],
            )

        if not isinstance(
            dataframe,
            pd.DataFrame,
        ):
            raise DomainValidationError(
                f"Expected pandas DataFrame for "
                f"dataset: {dataset_name}"
            )

        issues = []

        dataset_rules = self.domain_rules[
            dataset_name
        ]

        for column_name, allowed_values in (
            dataset_rules.items()
        ):

            if column_name not in dataframe.columns:
                raise DomainValidationError(
                    f"Column '{column_name}' is missing "
                    f"from dataset '{dataset_name}'. "
                    f"Run schema validation first."
                )

            allowed_set = set(
                allowed_values
            )

            series = dataframe[column_name]

            for row_index, value in series.items():

                # Null/blank values are handled by the
                # NullValidator.
                if self._is_missing(value):
                    continue

                if value not in allowed_set:
                    issues.append(
                        DomainValidationIssue(
                            dataset_name=dataset_name,
                            row_index=int(row_index),
                            column_name=column_name,
                            actual_value=value,
                            allowed_values=list(
                                allowed_values
                            ),
                            message=(
                                f"Value {value!r} is not "
                                f"allowed for "
                                f"{dataset_name}."
                                f"{column_name}. "
                                f"Allowed values: "
                                f"{allowed_values}"
                            ),
                        )
                    )

        return DomainValidationResult(
            dataset_name=dataset_name,
            valid=len(issues) == 0,
            issues=issues,
        )

    # ------------------------------------------------------------------
    # Missing-value helper
    # ------------------------------------------------------------------

    @staticmethod
    def _is_missing(value) -> bool:
        """
        Determine whether a value should be skipped by domain validation.

        Null and blank values belong to null validation.
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
    # All datasets
    # ------------------------------------------------------------------

    def validate_all(
        self,
        datasets: Dict[str, pd.DataFrame],
    ) -> Dict[str, DomainValidationResult]:
        """Validate domain values across all datasets."""

        if not datasets:
            raise DomainValidationError(
                "No datasets were provided for "
                "domain validation."
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
        """Return True when all configured domain values are valid."""

        return self.validate_dataset(
            dataset_name,
            dataframe,
        ).valid