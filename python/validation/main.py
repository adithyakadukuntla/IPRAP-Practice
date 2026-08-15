"""
Main orchestration pipeline for Participant 2 data validation.

Phase 14 — Pipeline Integration.

Pipeline:

    Raw Data
        |
        v
    Data Profiling
        |
        v
    Schema Validation
        |
        v
    Type Validation
        |
        v
    Null Validation
        |
        v
    Duplicate Validation
        |
        v
    Domain Validation
        |
        v
    Business Validation
        |
        v
    Referential Validation
        |
        v
    Record-level decision
        |
        +-------------------+
        |                   |
        v                   v
    VALID                INVALID
        |                   |
        v                   v
    Standardize          Rejected
        |                   |
        v                   v
    processed/           rejected/
        |
        +-------------------+
                  |
                  v
          Quality Reporting
                  |
          +-------+--------+
          |                |
          v                v
    validation_errors   data_quality_summary
"""

from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Dict, List

import pandas as pd

from .business_validator import BusinessValidator
from .data_loader import RawDataLoader
from .domain_validator import DomainValidator
from .duplicate_validator import DuplicateValidator
from .null_validator import NullValidator
from .profiler import DataProfiler
from .quality_report import QualityReporter
from .referential_validator import ReferentialValidator
from .rejection_processor import (
    RejectionProcessor,
    RecordProcessingResult,
)
from .schema_validator import SchemaValidator
from .standardizer import DataStandardizer
from .type_validator import TypeValidator


# =====================================================================
# Pipeline issue adapter
# =====================================================================


@dataclass
class PipelineIssue:
    """
    Common issue representation used by the orchestration layer.

    Individual validators intentionally have their own result types.
    This adapter gives the rejection processor and reporting layer one
    consistent representation.
    """

    dataset_name: str
    row_index: int | None
    column_name: str
    rule_id: str
    severity: str
    message: str


# =====================================================================
# Pipeline result
# =====================================================================


@dataclass
class PipelineResult:
    """
    Complete result returned by the validation pipeline.
    """

    datasets: Dict[str, pd.DataFrame]

    validation_results: Dict[str, object]

    processing_results: Dict[
        str,
        RecordProcessingResult,
    ]

    validation_errors: pd.DataFrame

    quality_summary: pd.DataFrame

    profile_path: Path

    validation_errors_path: Path

    quality_summary_path: Path

    def all_valid(self) -> bool:
        """
        Return True when every dataset contains no rejected records.
        """

        return all(
            result.invalid_records == 0
            for result in self.processing_results.values()
        )


# =====================================================================
# Main pipeline
# =====================================================================


class ValidationPipeline:
    """
    Orchestrates the complete Participant 2 validation pipeline.
    """

    def __init__(
        self,
        raw_data_dir: str | Path = "data/raw",
        processed_root: str | Path = "data/processed",
        rejected_root: str | Path = "data/rejected",
        quality_reports_root: str | Path = (
            "data/quality_reports"
        ),
    ):
        self.raw_data_dir = Path(
            raw_data_dir
        )

        self.processed_root = Path(
            processed_root
        )

        self.rejected_root = Path(
            rejected_root
        )

        self.quality_reports_root = Path(
            quality_reports_root
        )

        # -------------------------------------------------------------
        # Components
        # -------------------------------------------------------------

        self.loader = RawDataLoader(
            raw_data_dir=str(
                self.raw_data_dir
            )
        )

        self.profiler = DataProfiler(
            output_dir=str(
                self.quality_reports_root
            )
        )

        self.schema_validator = (
            SchemaValidator()
        )

        self.type_validator = (
            TypeValidator()
        )

        self.null_validator = (
            NullValidator()
        )

        self.duplicate_validator = (
            DuplicateValidator()
        )

        self.domain_validator = (
            DomainValidator()
        )

        self.business_validator = (
            BusinessValidator()
        )

        self.referential_validator = (
            ReferentialValidator()
        )

        self.standardizer = (
            DataStandardizer()
        )

        self.rejection_processor = (
            RejectionProcessor(
                processed_root=(
                    self.processed_root
                ),
                rejected_root=(
                    self.rejected_root
                ),
                quality_reports_root=(
                    self.quality_reports_root
                ),
            )
        )

        self.quality_reporter = (
            QualityReporter(
                output_root=(
                    self.quality_reports_root
                )
            )
        )

    # =================================================================
    # PUBLIC RUN METHOD
    # =================================================================

    def run(
        self,
        current_business_date: date | None = None,
    ) -> PipelineResult:
        """
        Execute the complete validation pipeline.
        """

        if current_business_date is None:
            current_business_date = date.today()

        # -------------------------------------------------------------
        # 1. LOAD RAW DATA
        # -------------------------------------------------------------

        datasets = (
            self.loader.load_all_datasets()
        )

        # -------------------------------------------------------------
        # 2. PROFILE RAW DATA
        # -------------------------------------------------------------

        profile_path = self._run_profiler(
            datasets
        )

        # -------------------------------------------------------------
        # 3. VALIDATE ALL DATA
        # -------------------------------------------------------------

        validation_results = (
            self._run_validations(
                datasets,
                current_business_date,
            )
        )

        # -------------------------------------------------------------
        # 4. NORMALIZE VALIDATION ISSUES
        # -------------------------------------------------------------

        normalized_issues = (
            self._normalize_validation_results(
                datasets,
                validation_results,
            )
        )

        # -------------------------------------------------------------
        # 5. RECORD-LEVEL DECISION
        # -------------------------------------------------------------

        processing_results = (
            self.rejection_processor.process_all(
                datasets=datasets,
                validation_results=(
                    normalized_issues
                ),
            )
        )

        # -------------------------------------------------------------
        # 6. STANDARDIZE ONLY ACCEPTED RECORDS
        # -------------------------------------------------------------

        self._standardize_valid_records(
            processing_results
        )

        # -------------------------------------------------------------
        # 7. WRITE PROCESSED + REJECTED DATA
        # -------------------------------------------------------------

        self.rejection_processor.write_all_dataset_outputs(
            processing_results
        )

        # -------------------------------------------------------------
        # 8. WRITE VALIDATION ERRORS
        # -------------------------------------------------------------

        validation_errors = (
            self.rejection_processor
            .build_validation_error_dataframe(
                datasets=datasets,
                validation_results=(
                    normalized_issues
                ),
            )
        )

        validation_errors_path = (
            self.rejection_processor
            .write_validation_errors(
                validation_errors
            )
        )

        # -------------------------------------------------------------
        # 9. QUALITY SCORING
        # -------------------------------------------------------------

        quality_results = (
            self.quality_reporter.calculate_all(
                processing_results=(
                    processing_results
                ),
                validation_results=(
                    normalized_issues
                ),
            )
        )

        quality_summary = (
            self.quality_reporter
            .results_to_dataframe(
                quality_results
            )
        )

        # -------------------------------------------------------------
        # 10. WRITE QUALITY SUMMARY
        # -------------------------------------------------------------

        quality_summary_path = (
            self.quality_reporter
            .write_summary(
                quality_summary
            )
        )

        return PipelineResult(
            datasets=datasets,
            validation_results=(
                validation_results
            ),
            processing_results=(
                processing_results
            ),
            validation_errors=(
                validation_errors
            ),
            quality_summary=(
                quality_summary
            ),
            profile_path=profile_path,
            validation_errors_path=(
                validation_errors_path
            ),
            quality_summary_path=(
                quality_summary_path
            ),
        )

    # =================================================================
    # PROFILING
    # =================================================================

    def _run_profiler(
        self,
        datasets: Dict[str, pd.DataFrame],
    ) -> Path:
        """
        Run the existing DataProfiler.
        """

        return self.profiler.run(
            datasets
        )

    # =================================================================
    # VALIDATION
    # =================================================================

    def _run_validations(
        self,
        datasets: Dict[str, pd.DataFrame],
        current_business_date: date,
    ) -> Dict[str, Dict]:
        """
        Run all validators.

        Results remain separated by validation category so that
        the pipeline preserves validator-level information.
        """

        results = {}

        # -------------------------------------------------------------
        # Schema
        # -------------------------------------------------------------

        results["schema"] = (
            self.schema_validator.validate_all(
                datasets
            )
        )

        # -------------------------------------------------------------
        # Only schema-valid datasets should continue into validators
        # that require configured columns to exist.
        # -------------------------------------------------------------

        schema_valid_datasets = {
            dataset_name: dataframe
            for dataset_name, dataframe
            in datasets.items()
            if results["schema"][
                dataset_name
            ].valid
        }

        # -------------------------------------------------------------
        # Type
        # -------------------------------------------------------------

        results["type"] = (
            self.type_validator.validate_all(
                schema_valid_datasets
            )
        )

        # -------------------------------------------------------------
        # Null
        # -------------------------------------------------------------

        results["null"] = (
            self.null_validator.validate_all(
                schema_valid_datasets
            )
        )

        # -------------------------------------------------------------
        # Duplicate
        # -------------------------------------------------------------

        results["duplicate"] = (
            self.duplicate_validator.validate_all(
                schema_valid_datasets
            )
        )

        # -------------------------------------------------------------
        # Domain
        # -------------------------------------------------------------

        results["domain"] = (
            self.domain_validator.validate_all(
                schema_valid_datasets
            )
        )

        # -------------------------------------------------------------
        # Business
        # -------------------------------------------------------------

        results["business"] = (
            self.business_validator.validate_all(
                schema_valid_datasets,
                current_business_date,
            )
        )

        # -------------------------------------------------------------
        # Referential
        #
        # Only datasets with valid schemas are passed here.
        # -------------------------------------------------------------

        results["referential"] = (
            self.referential_validator.validate(
                schema_valid_datasets
            )
        )

        return results

    # =================================================================
    # ISSUE NORMALIZATION
    # =================================================================

    def _normalize_validation_results(
        self,
        datasets: Dict[str, pd.DataFrame],
        validation_results: Dict[str, Dict],
    ) -> Dict[
        str,
        List[PipelineIssue],
    ]:
        """
        Convert all validator-specific issue structures into the
        common PipelineIssue format.
        """

        normalized = {
            dataset_name: []
            for dataset_name in datasets
        }

        # -------------------------------------------------------------
        # Schema results
        # -------------------------------------------------------------

        schema_results = (
            validation_results.get(
                "schema",
                {},
            )
        )

        for dataset_name, result in (
            schema_results.items()
        ):

            if result.valid:
                continue

            dataframe = datasets[
                dataset_name
            ]

            message = result.error_message

            # A schema failure affects the complete dataset.
            #
            # Therefore every existing record is rejected.
            for row_index in dataframe.index:

                normalized[
                    dataset_name
                ].append(
                    PipelineIssue(
                        dataset_name=(
                            dataset_name
                        ),
                        row_index=int(
                            row_index
                        ),
                        column_name=(
                            self._schema_column_name(
                                result
                            )
                        ),
                        rule_id="SCH-001",
                        severity="ERROR",
                        message=message,
                    )
                )

            # Empty dataset: retain a dataset-level error.
            if len(dataframe) == 0:

                normalized[
                    dataset_name
                ].append(
                    PipelineIssue(
                        dataset_name=(
                            dataset_name
                        ),
                        row_index=None,
                        column_name=(
                            self._schema_column_name(
                                result
                            )
                        ),
                        rule_id="SCH-001",
                        severity="ERROR",
                        message=message,
                    )
                )

        # -------------------------------------------------------------
        # Type
        # -------------------------------------------------------------

        self._add_standard_issues(
            normalized,
            validation_results.get(
                "type",
                {},
            ),
            rule_id="TYP-001",
        )

        # -------------------------------------------------------------
        # Null
        # -------------------------------------------------------------

        self._add_standard_issues(
            normalized,
            validation_results.get(
                "null",
                {},
            ),
            rule_id="NUL-001",
        )

        # -------------------------------------------------------------
        # Duplicate
        # -------------------------------------------------------------

        self._add_duplicate_issues(
            normalized,
            validation_results.get(
                "duplicate",
                {},
            ),
        )

        # -------------------------------------------------------------
        # Domain
        # -------------------------------------------------------------

        self._add_standard_issues(
            normalized,
            validation_results.get(
                "domain",
                {},
            ),
            rule_id="DOM-001",
        )

        # -------------------------------------------------------------
        # Business
        # -------------------------------------------------------------

        self._add_standard_issues(
            normalized,
            validation_results.get(
                "business",
                {},
            ),
            use_existing_rule_id=True,
        )

        # -------------------------------------------------------------
        # Referential
        # -------------------------------------------------------------

        self._add_standard_issues(
            normalized,
            validation_results.get(
                "referential",
                {},
            ),
            use_existing_rule_id=True,
        )

        return normalized

    # =================================================================
    # STANDARD ISSUE CONVERSION
    # =================================================================

    @staticmethod
    def _add_standard_issues(
        normalized: Dict[
            str,
            List[PipelineIssue],
        ],
        results: Dict,
        rule_id: str | None = None,
        use_existing_rule_id: bool = False,
    ) -> None:
        """
        Convert normal row-level validator issues.
        """

        for dataset_name, result in (
            results.items()
        ):

            for issue in getattr(
                result,
                "issues",
                [],
            ):

                existing_rule_id = getattr(
                    issue,
                    "rule_id",
                    None,
                )

                if (
                    use_existing_rule_id
                    and existing_rule_id
                ):
                    final_rule_id = (
                        existing_rule_id
                    )
                else:
                    final_rule_id = (
                        rule_id
                        or "VAL-001"
                    )

                severity = str(
                    getattr(
                        issue,
                        "severity",
                        "ERROR",
                    )
                ).upper()

                message = str(
                    getattr(
                        issue,
                        "message",
                        "Validation failed.",
                    )
                )

                normalized[
                    dataset_name
                ].append(
                    PipelineIssue(
                        dataset_name=(
                            dataset_name
                        ),
                        row_index=(
                            getattr(
                                issue,
                                "row_index",
                                None,
                            )
                        ),
                        column_name=(
                            getattr(
                                issue,
                                "column_name",
                                "",
                            )
                        ),
                        rule_id=(
                            final_rule_id
                        ),
                        severity=severity,
                        message=message,
                    )
                )

    # =================================================================
    # DUPLICATE ISSUE CONVERSION
    # =================================================================

    @staticmethod
    def _add_duplicate_issues(
        normalized: Dict[
            str,
            List[PipelineIssue],
        ],
        results: Dict,
    ) -> None:
        """
        Duplicate issues contain multiple row indices.

        Every record belonging to the duplicate group must therefore
        become an invalid record.
        """

        for dataset_name, result in (
            results.items()
        ):

            for issue in getattr(
                result,
                "issues",
                [],
            ):

                row_indices = getattr(
                    issue,
                    "row_indices",
                    [],
                )

                message = str(
                    getattr(
                        issue,
                        "message",
                        "Duplicate record detected.",
                    )
                )

                duplicate_type = str(
                    getattr(
                        issue,
                        "duplicate_type",
                        "DUPLICATE",
                    )
                )

                rule_id = (
                    "DUP-002"
                    if duplicate_type
                    == "HOLDINGS_COMPOSITE_KEY"
                    else "DUP-001"
                )

                for row_index in (
                    row_indices
                ):

                    normalized[
                        dataset_name
                    ].append(
                        PipelineIssue(
                            dataset_name=(
                                dataset_name
                            ),
                            row_index=int(
                                row_index
                            ),
                            column_name="",
                            rule_id=rule_id,
                            severity="ERROR",
                            message=message,
                        )
                    )

    # =================================================================
    # SCHEMA COLUMN
    # =================================================================

    @staticmethod
    def _schema_column_name(
        result,
    ) -> str:
        """
        Return the most useful schema-related column name.
        """

        if getattr(
            result,
            "missing_columns",
            None,
        ):
            return (
                result.missing_columns[0]
            )

        if getattr(
            result,
            "unexpected_columns",
            None,
        ):
            return (
                result.unexpected_columns[0]
            )

        return ""

    # =================================================================
    # STANDARDIZATION
    # =================================================================

    def _standardize_valid_records(
        self,
        processing_results: Dict[
            str,
            RecordProcessingResult,
        ],
    ) -> None:
        """
        Standardize only accepted records.

        Rejected records remain in their original raw representation.
        """

        for dataset_name, result in (
            processing_results.items()
        ):

            if result.valid_records == 0:
                continue

            result.valid_dataframe = (
                self.standardizer.standardize_dataset(
                    dataset_name,
                    result.valid_dataframe,
                )
            )


# =====================================================================
# Convenience function
# =====================================================================


def run_pipeline(
    current_business_date: date | None = None,
) -> PipelineResult:
    """
    Run the default Participant 2 validation pipeline.
    """

    pipeline = ValidationPipeline()

    return pipeline.run(
        current_business_date=(
            current_business_date
        )
    )


# =====================================================================
# CLI entry point
# =====================================================================


if __name__ == "__main__":

    result = run_pipeline()

    print()
    print("=" * 70)
    print("IPRAP PARTICIPANT 2 DATA QUALITY PIPELINE")
    print("=" * 70)

    print()
    print("Dataset results:")

    for (
        dataset_name,
        processing_result,
    ) in result.processing_results.items():

        print(
            f"  {dataset_name}: "
            f"total={processing_result.total_records}, "
            f"valid={processing_result.valid_records}, "
            f"invalid={processing_result.invalid_records}"
        )

    print()
    print(
        "Profile:",
        result.profile_path,
    )

    print(
        "Validation errors:",
        result.validation_errors_path,
    )

    print(
        "Quality summary:",
        result.quality_summary_path,
    )

    print()
    print(
        "Overall status:",
        (
            "VALID"
            if result.all_valid()
            else "INVALID RECORDS FOUND"
        ),
    )

    print("=" * 70)