"""
Data quality scoring and summary reporting.

Phase 14 — Participant 2.

Responsibilities:
    - Calculate dataset-level quality scores.
    - Classify quality scores using project-defined thresholds.
    - Count validation errors and warnings.
    - Generate data_quality_summary.csv.
    - Preserve validation timestamps.
    - Provide reusable reporting methods.

Quality score:

    valid_records / total_records * 100

Project-defined classifications:

    95.00 - 100.00  -> EXCELLENT
    90.00 - 94.99   -> GOOD
    80.00 - 89.99   -> WARNING
    below 80.00     -> POOR
"""

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List

import pandas as pd


# =====================================================================
# Exceptions
# =====================================================================


class QualityReportError(Exception):
    """Raised when quality reporting cannot be completed."""


# =====================================================================
# Constants
# =====================================================================


EXCELLENT_MIN = 95.0
GOOD_MIN = 90.0
WARNING_MIN = 80.0


SUMMARY_COLUMNS = [
    "dataset_name",
    "total_records",
    "valid_records",
    "invalid_records",
    "error_count",
    "warning_count",
    "quality_score",
    "quality_status",
    "validation_timestamp",
]


# =====================================================================
# Result object
# =====================================================================


@dataclass
class QualityScoreResult:
    """
    Quality result for one dataset.
    """

    dataset_name: str
    total_records: int
    valid_records: int
    invalid_records: int
    error_count: int
    warning_count: int
    quality_score: float
    quality_status: str
    validation_timestamp: str

    def to_dict(self) -> dict:
        """Convert the result into a dictionary."""

        return {
            "dataset_name": self.dataset_name,
            "total_records": self.total_records,
            "valid_records": self.valid_records,
            "invalid_records": self.invalid_records,
            "error_count": self.error_count,
            "warning_count": self.warning_count,
            "quality_score": self.quality_score,
            "quality_status": self.quality_status,
            "validation_timestamp": (
                self.validation_timestamp
            ),
        }


# =====================================================================
# Main quality reporter
# =====================================================================


class QualityReporter:
    """
    Calculate and report dataset-level quality.
    """

    def __init__(
        self,
        output_root: str | Path = (
            "data/quality_reports"
        ),
    ):
        self.output_root = Path(
            output_root
        )

    # =================================================================
    # SCORE CALCULATION
    # =================================================================

    @staticmethod
    def calculate_quality_score(
        total_records: int,
        valid_records: int,
    ) -> float:
        """
        Calculate dataset quality score.

        Formula:

            valid_records / total_records * 100

        Returns a value rounded to two decimal places.
        """

        if total_records < 0:
            raise QualityReportError(
                "total_records cannot be negative."
            )

        if valid_records < 0:
            raise QualityReportError(
                "valid_records cannot be negative."
            )

        if valid_records > total_records:
            raise QualityReportError(
                "valid_records cannot exceed "
                "total_records."
            )

        if total_records == 0:
            return 0.0

        score = (
            valid_records
            / total_records
            * 100.0
        )

        return round(
            score,
            2,
        )

    # =================================================================
    # STATUS CLASSIFICATION
    # =================================================================

    @staticmethod
    def classify_quality_score(
        quality_score: float,
    ) -> str:
        """
        Classify a quality score using the project-defined
        thresholds.

        95-100       EXCELLENT
        90-94.99     GOOD
        80-89.99     WARNING
        <80          POOR
        """

        if not 0 <= quality_score <= 100:
            raise QualityReportError(
                "quality_score must be between "
                "0 and 100."
            )

        if quality_score >= EXCELLENT_MIN:
            return "EXCELLENT"

        if quality_score >= GOOD_MIN:
            return "GOOD"

        if quality_score >= WARNING_MIN:
            return "WARNING"

        return "POOR"

    # =================================================================
    # TIMESTAMP
    # =================================================================

    @staticmethod
    def current_timestamp() -> str:
        """
        Return the current UTC timestamp in ISO-8601 format.
        """

        return (
            datetime.now(
                timezone.utc
            )
            .isoformat()
        )

    # =================================================================
    # ISSUE EXTRACTION
    # =================================================================

    @staticmethod
    def _extract_issues(
        validation_result,
    ) -> List:
        """
        Extract issue objects from the validation-result formats
        already used by Participant 2 validators.

        Supported:

            result.issues
            list / tuple / set
            single issue
            None
        """

        if validation_result is None:
            return []

        if hasattr(
            validation_result,
            "issues",
        ):
            issues = validation_result.issues

            if issues is None:
                return []

            return list(issues)

        if isinstance(
            validation_result,
            (list, tuple, set),
        ):
            extracted = []

            for item in validation_result:

                if hasattr(
                    item,
                    "issues",
                ):
                    nested = item.issues

                    if nested:
                        extracted.extend(
                            list(nested)
                        )
                else:
                    extracted.append(
                        item
                    )

            return extracted

        return [validation_result]

    # =================================================================
    # ISSUE COUNTS
    # =================================================================

    @classmethod
    def count_issues(
        cls,
        validation_result,
    ) -> tuple[int, int]:
        """
        Count ERROR and WARNING issues.

        Returns:

            (error_count, warning_count)
        """

        issues = cls._extract_issues(
            validation_result
        )

        error_count = 0
        warning_count = 0

        for issue in issues:

            severity = str(
                getattr(
                    issue,
                    "severity",
                    "",
                )
            ).upper()

            if severity == "ERROR":
                error_count += 1

            elif severity == "WARNING":
                warning_count += 1

        return (
            error_count,
            warning_count,
        )

    # =================================================================
    # SINGLE DATASET REPORT
    # =================================================================

    def calculate_dataset_quality(
        self,
        dataset_name: str,
        total_records: int,
        valid_records: int,
        validation_result=None,
        validation_timestamp: str | None = None,
    ) -> QualityScoreResult:
        """
        Calculate complete quality information for one dataset.
        """

        if total_records < 0:
            raise QualityReportError(
                f"Dataset '{dataset_name}' has "
                f"negative total_records."
            )

        if valid_records < 0:
            raise QualityReportError(
                f"Dataset '{dataset_name}' has "
                f"negative valid_records."
            )

        if valid_records > total_records:
            raise QualityReportError(
                f"Dataset '{dataset_name}' has "
                f"more valid records than total "
                f"records."
            )

        invalid_records = (
            total_records
            - valid_records
        )

        error_count, warning_count = (
            self.count_issues(
                validation_result
            )
        )

        quality_score = (
            self.calculate_quality_score(
                total_records=total_records,
                valid_records=valid_records,
            )
        )

        quality_status = (
            self.classify_quality_score(
                quality_score
            )
        )

        if validation_timestamp is None:
            validation_timestamp = (
                self.current_timestamp()
            )

        return QualityScoreResult(
            dataset_name=dataset_name,
            total_records=total_records,
            valid_records=valid_records,
            invalid_records=invalid_records,
            error_count=error_count,
            warning_count=warning_count,
            quality_score=quality_score,
            quality_status=quality_status,
            validation_timestamp=(
                validation_timestamp
            ),
        )

    # =================================================================
    # MULTIPLE DATASETS
    # =================================================================

    def calculate_all(
        self,
        processing_results: Dict,
        validation_results: Dict | None = None,
    ) -> Dict[
        str,
        QualityScoreResult,
    ]:
        """
        Calculate quality scores for all datasets.

        processing_results is expected to contain the
        RecordProcessingResult objects produced by Phase 13.

        Each result provides:

            total_records
            valid_records
            invalid_records
        """

        if not processing_results:
            raise QualityReportError(
                "No processing results were provided."
            )

        if validation_results is None:
            validation_results = {}

        results = {}

        timestamp = (
            self.current_timestamp()
        )

        for dataset_name, processing_result in (
            processing_results.items()
        ):

            validation_result = (
                validation_results.get(
                    dataset_name
                )
            )

            results[dataset_name] = (
                self.calculate_dataset_quality(
                    dataset_name=dataset_name,
                    total_records=(
                        processing_result.total_records
                    ),
                    valid_records=(
                        processing_result.valid_records
                    ),
                    validation_result=(
                        validation_result
                    ),
                    validation_timestamp=timestamp,
                )
            )

        return results

    # =================================================================
    # DATAFRAME GENERATION
    # =================================================================

    @staticmethod
    def results_to_dataframe(
        results: Dict[
            str,
            QualityScoreResult,
        ],
    ) -> pd.DataFrame:
        """
        Convert quality results to the required summary DataFrame.
        """

        rows = [
            result.to_dict()
            for result in results.values()
        ]

        return pd.DataFrame(
            rows,
            columns=SUMMARY_COLUMNS,
        )

    # =================================================================
    # FILE OUTPUT
    # =================================================================

    def write_summary(
        self,
        summary: pd.DataFrame,
    ) -> Path:
        """
        Write data_quality_summary.csv.
        """

        if not isinstance(
            summary,
            pd.DataFrame,
        ):
            raise QualityReportError(
                "summary must be a pandas DataFrame."
            )

        missing_columns = [
            column
            for column in SUMMARY_COLUMNS
            if column not in summary.columns
        ]

        if missing_columns:
            raise QualityReportError(
                "Summary is missing required "
                f"columns: {missing_columns}"
            )

        self.output_root.mkdir(
            parents=True,
            exist_ok=True,
        )

        output_path = (
            self.output_root
            / "data_quality_summary.csv"
        )

        summary.to_csv(
            output_path,
            index=False,
        )

        return output_path

    # =================================================================
    # COMPLETE REPORT
    # =================================================================

    def generate_report(
        self,
        processing_results: Dict,
        validation_results: Dict | None = None,
    ) -> tuple[
        Dict[str, QualityScoreResult],
        pd.DataFrame,
        Path,
    ]:
        """
        Calculate scores, generate summary DataFrame,
        and write the required CSV.

        Returns:

            results
            summary DataFrame
            output path
        """

        results = self.calculate_all(
            processing_results=processing_results,
            validation_results=validation_results,
        )

        summary = (
            self.results_to_dataframe(
                results
            )
        )

        output_path = (
            self.write_summary(
                summary
            )
        )

        return (
            results,
            summary,
            output_path,
        )