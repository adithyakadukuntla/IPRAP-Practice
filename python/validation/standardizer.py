"""
Data standardization for Participant 2.

Standardization is performed ONLY on accepted/validated data.

Responsibilities:
    - Trim leading/trailing whitespace from string values.
    - Normalize controlled vocabulary values to uppercase.
    - Normalize accepted date values to YYYY-MM-DD.
    - Preserve identifiers and business values.
    - Never modify raw source DataFrames.

This module does NOT:
    - repair invalid business values
    - change identifier formats
    - create missing values
    - delete records
    - perform validation
    - modify raw source files
"""

from typing import Dict, List

import pandas as pd

from .config import (
    STANDARDIZE_DATE_COLUMNS,
    STANDARDIZE_UPPERCASE_COLUMNS,
)


class StandardizationError(Exception):
    """Raised when standardization cannot be performed."""


class DataStandardizer:
    """Reusable data-standardization component."""

    def __init__(
        self,
        uppercase_columns: Dict[str, List[str]] | None = None,
        date_columns: Dict[str, List[str]] | None = None,
    ):
        """
        Initialize the standardizer.

        Parameters
        ----------
        uppercase_columns:
            Mapping of dataset names to columns whose values should
            be normalized to uppercase.

        date_columns:
            Mapping of dataset names to columns whose values should
            be normalized to YYYY-MM-DD.
        """

        self.uppercase_columns = (
            uppercase_columns
            if uppercase_columns is not None
            else STANDARDIZE_UPPERCASE_COLUMNS
        )

        self.date_columns = (
            date_columns
            if date_columns is not None
            else STANDARDIZE_DATE_COLUMNS
        )

    # ==================================================================
    # PUBLIC API
    # ==================================================================

    def standardize_dataset(
        self,
        dataset_name: str,
        dataframe: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Standardize one dataset.

        A NEW DataFrame is returned.

        The input DataFrame is never modified.

        Standardization is applied only to configured columns
        that actually exist in the supplied DataFrame.

        Missing required columns are not handled here because
        schema validation is responsible for detecting missing
        required columns earlier in the pipeline.

        However, if NONE of the configured standardization
        columns exist, a StandardizationError is raised because
        the supplied DataFrame is not compatible with the
        requested dataset standardization.
        """

        # --------------------------------------------------------------
        # Validate input type
        # --------------------------------------------------------------

        if not isinstance(
            dataframe,
            pd.DataFrame,
        ):
            raise StandardizationError(
                f"Expected pandas DataFrame for "
                f"dataset '{dataset_name}'."
            )

        # --------------------------------------------------------------
        # Always work on a deep copy.
        #
        # Raw/source data must never be modified.
        # --------------------------------------------------------------

        standardized = dataframe.copy(
            deep=True
        )

        # --------------------------------------------------------------
        # Get configured columns.
        # --------------------------------------------------------------

        configured_uppercase_columns = (
            self.uppercase_columns.get(
                dataset_name,
                [],
            )
        )

        configured_date_columns = (
            self.date_columns.get(
                dataset_name,
                [],
            )
        )

        # --------------------------------------------------------------
        # Find configured columns that are actually present.
        #
        # Some configured columns may legitimately be absent from
        # a focused DataFrame used by a unit test.
        #
        # Example:
        #
        # clients test DataFrame:
        #     client_id
        #     risk_profile
        #     status
        #
        # created_date may not be present.
        #
        # We standardize what is available.
        # --------------------------------------------------------------

        uppercase_columns = [
            column
            for column in configured_uppercase_columns
            if column in standardized.columns
        ]

        date_columns = [
            column
            for column in configured_date_columns
            if column in standardized.columns
        ]

        # --------------------------------------------------------------
        # If this dataset has standardization rules but NONE of the
        # configured columns are present, the DataFrame is incompatible
        # with the requested dataset.
        #
        # Example:
        #
        # clients DataFrame:
        #
        #     client_id
        #
        # There is no:
        #     client_type
        #     risk_profile
        #     status
        #     created_date
        #
        # Therefore raise an error.
        # --------------------------------------------------------------

        configured_columns = (
            list(configured_uppercase_columns)
            + list(configured_date_columns)
        )

        present_standardization_columns = (
            list(uppercase_columns)
            + list(date_columns)
        )

        if (
            configured_columns
            and not present_standardization_columns
        ):
            raise StandardizationError(
                f"Dataset '{dataset_name}' does not "
                f"contain any configured "
                f"standardization columns. "
                f"Expected one or more of: "
                f"{configured_columns}."
            )

        # --------------------------------------------------------------
        # Step 1:
        # Remove leading/trailing whitespace from string values.
        #
        # Examples:
        #
        # " high "      -> "high"
        # " Active "    -> "Active"
        # " balanced "  -> "balanced"
        #
        # This does NOT invent a new identifier format.
        # --------------------------------------------------------------

        standardized = (
            self._strip_string_values(
                standardized
            )
        )

        # --------------------------------------------------------------
        # Step 2:
        # Normalize controlled vocabulary values.
        #
        # Examples:
        #
        # individual -> INDIVIDUAL
        # Individual -> INDIVIDUAL
        # high       -> HIGH
        # High       -> HIGH
        # active     -> ACTIVE
        # --------------------------------------------------------------

        for column in uppercase_columns:

            standardized[column] = (
                self._uppercase_column(
                    standardized[column]
                )
            )

        # --------------------------------------------------------------
        # Step 3:
        # Normalize date columns.
        #
        # Example:
        #
        # 2026/08/05 -> 2026-08-05
        #
        # Invalid dates are NOT repaired here.
        # Date validation belongs to the validation stage.
        # --------------------------------------------------------------

        for column in date_columns:

            standardized[column] = (
                self._standardize_date_column(
                    standardized[column]
                )
            )

        return standardized

    def standardize_all(
        self,
        datasets: Dict[str, pd.DataFrame],
    ) -> Dict[str, pd.DataFrame]:
        """
        Standardize all supplied datasets.

        Returns a NEW dictionary containing NEW DataFrames.

        The original dataset dictionary and DataFrames are not
        modified.
        """

        if not datasets:
            raise StandardizationError(
                "No datasets were provided "
                "for standardization."
            )

        standardized_datasets = {}

        for dataset_name, dataframe in (
            datasets.items()
        ):

            standardized_datasets[
                dataset_name
            ] = self.standardize_dataset(
                dataset_name,
                dataframe,
            )

        return standardized_datasets

    # ==================================================================
    # STRING STANDARDIZATION
    # ==================================================================

    @staticmethod
    def _strip_string_values(
        dataframe: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Remove leading/trailing whitespace from string values.

        Non-string values remain unchanged.

        Returns a new DataFrame.
        """

        result = dataframe.copy(
            deep=True
        )

        for column in result.columns:

            result[column] = result[
                column
            ].map(
                lambda value: (
                    value.strip()
                    if isinstance(
                        value,
                        str,
                    )
                    else value
                )
            )

        return result

    @staticmethod
    def _uppercase_column(
        series: pd.Series,
    ) -> pd.Series:
        """
        Convert string values in a Series to uppercase.

        Null values remain null.

        Non-string values remain unchanged.
        """

        return series.map(
            lambda value: (
                value.upper()
                if isinstance(
                    value,
                    str,
                )
                else value
            )
        )

    # ==================================================================
    # DATE STANDARDIZATION
    # ==================================================================

    @staticmethod
    def _standardize_date_column(
        series: pd.Series,
    ) -> pd.Series:
        """
        Convert valid date values to YYYY-MM-DD strings.

        Null values remain missing.

        Invalid dates are converted to missing values rather than
        being guessed or repaired.

        Invalid-date detection belongs to the validation stage.
        """

        parsed = pd.to_datetime(
            series,
            errors="coerce",
        )

        result = parsed.dt.strftime(
            "%Y-%m-%d"
        )

        return result

    # ==================================================================
    # CONVENIENCE API
    # ==================================================================

    def standardize(
        self,
        dataset_name: str,
        dataframe: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Alias for standardize_dataset().
        """

        return self.standardize_dataset(
            dataset_name,
            dataframe,
        )