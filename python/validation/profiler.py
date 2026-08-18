"""
Data profiling module for Participant 2.

The profiler describes the incoming raw datasets before validation.

Responsibilities:
    - Record dataset size
    - Record column count
    - Record column names
    - Record pandas data types
    - Count null values
    - Calculate null percentages
    - Count distinct values
    - Calculate minimum and maximum where meaningful
    - Calculate average where meaningful
    - Write data_profile.csv

Important:
    This module does not modify raw data.
    This module does not reject records.
    This module does not perform business validation.
"""

from pathlib import Path
from typing import Dict

import pandas as pd

from .config import QUALITY_REPORTS_DIR


class ProfilingError(Exception):
    """Raised when dataset profiling fails."""


class DataProfiler:
    """Generate column-level profiles for the five datasets."""

    PROFILE_COLUMNS = [
        "dataset_name",
        "column_name",
        "data_type",
        "record_count",
        "column_count",
        "null_count",
        "null_percentage",
        "distinct_count",
        "min_value",
        "max_value",
        "average_value",
    ]

    def __init__(
        self,
        output_dir: str = QUALITY_REPORTS_DIR,
    ):
        self.output_dir = Path(output_dir)

    # ------------------------------------------------------------------
    # Individual column statistics
    # ------------------------------------------------------------------

    @staticmethod
    def _calculate_minimum(
        series: pd.Series,
    ):
        """
        Calculate the minimum value when meaningful.

        For numeric and datetime-like columns, minimum is meaningful.
        For strings/categories, minimum is left blank because lexical
        ordering is not useful as a data-quality statistic.
        """

        non_null = series.dropna()

        if non_null.empty:
            return None

        if pd.api.types.is_numeric_dtype(series):
            return non_null.min()

        if pd.api.types.is_datetime64_any_dtype(series):
            return non_null.min()

        return None

    @staticmethod
    def _calculate_maximum(
        series: pd.Series,
    ):
        """
        Calculate the maximum value when meaningful.
        """

        non_null = series.dropna()

        if non_null.empty:
            return None

        if pd.api.types.is_numeric_dtype(series):
            return non_null.max()

        if pd.api.types.is_datetime64_any_dtype(series):
            return non_null.max()

        return None

    @staticmethod
    def _calculate_average(
        series: pd.Series,
    ):
        """
        Calculate the average for numeric columns only.
        """

        if not pd.api.types.is_numeric_dtype(series):
            return None

        non_null = series.dropna()

        if non_null.empty:
            return None

        return non_null.mean()

    # ------------------------------------------------------------------
    # Single-column profiling
    # ------------------------------------------------------------------

    def profile_column(
        self,
        dataset_name: str,
        dataframe: pd.DataFrame,
        column_name: str,
    ) -> Dict:
        """
        Generate profile statistics for one column.
        """

        series = dataframe[column_name]

        record_count = len(dataframe)
        column_count = len(dataframe.columns)

        null_count = int(
            series.isna().sum()
        )

        if record_count > 0:
            null_percentage = (
                null_count / record_count
            ) * 100
        else:
            null_percentage = 0.0

        distinct_count = int(
            series.nunique(dropna=True)
        )

        minimum = self._calculate_minimum(
            series
        )

        maximum = self._calculate_maximum(
            series
        )

        average = self._calculate_average(
            series
        )

        return {
            "dataset_name": dataset_name,
            "column_name": column_name,
            "data_type": str(series.dtype),
            "record_count": record_count,
            "column_count": column_count,
            "null_count": null_count,
            "null_percentage": round(
                null_percentage,
                4,
            ),
            "distinct_count": distinct_count,
            "min_value": minimum,
            "max_value": maximum,
            "average_value": average,
        }

    # ------------------------------------------------------------------
    # Single-dataset profiling
    # ------------------------------------------------------------------

    def profile_dataset(
        self,
        dataset_name: str,
        dataframe: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Generate a column-level profile for one dataset.
        """

        if not isinstance(
            dataframe,
            pd.DataFrame,
        ):
            raise ProfilingError(
                f"Expected pandas DataFrame for "
                f"{dataset_name}"
            )

        rows = []

        for column_name in dataframe.columns:
            rows.append(
                self.profile_column(
                    dataset_name,
                    dataframe,
                    column_name,
                )
            )

        return pd.DataFrame(
            rows,
            columns=self.PROFILE_COLUMNS,
        )

    # ------------------------------------------------------------------
    # All-dataset profiling
    # ------------------------------------------------------------------

    def profile_all_datasets(
        self,
        datasets: Dict[str, pd.DataFrame],
    ) -> pd.DataFrame:
        """
        Generate a combined profile for all datasets.
        """

        if not datasets:
            raise ProfilingError(
                "No datasets were provided for profiling."
            )

        profiles = []

        for dataset_name, dataframe in datasets.items():
            profile = self.profile_dataset(
                dataset_name,
                dataframe,
            )

            profiles.append(profile)

        result = pd.concat(
            profiles,
            ignore_index=True,
        )

        return result

    # ------------------------------------------------------------------
    # Output
    # ------------------------------------------------------------------

    def save_profile(
        self,
        profile: pd.DataFrame,
        filename: str = "data_profile.csv",
    ) -> Path:
        """
        Save the generated profile to the quality-report directory.
        """

        self.output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        output_path = (
            self.output_dir / filename
        )

        try:
            profile.to_csv(
                output_path,
                index=False,
            )

        except Exception as exc:
            raise ProfilingError(
                f"Failed to save profile to "
                f"{output_path}: {exc}"
            ) from exc

        return output_path

    # ------------------------------------------------------------------
    # Main public method
    # ------------------------------------------------------------------

    def run(
        self,
        datasets: Dict[str, pd.DataFrame],
    ) -> Path:
        """
        Profile all datasets and save data_profile.csv.
        """

        profile = self.profile_all_datasets(
            datasets
        )

        return self.save_profile(
            profile
        )