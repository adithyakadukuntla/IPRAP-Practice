"""
Rejected-record processing and exception management.

Phase 13 — Participant 2.

Responsibilities:
    - Convert validation results into record-level VALID/INVALID
      decisions.
    - Preserve invalid source records.
    - Separate valid and invalid records.
    - Generate a standardized validation-error table.
    - Write trusted datasets to data/processed/.
    - Write rejected datasets to data/rejected/.
    - Never modify raw source DataFrames.

This module does NOT:
    - perform validation
    - repair invalid records
    - modify raw files
    - standardize values
    - create missing parent records
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Set

import pandas as pd


# =====================================================================
# Exceptions
# =====================================================================


class RejectionProcessingError(Exception):
    """Raised when rejected-record processing fails."""


# =====================================================================
# Data classes
# =====================================================================


@dataclass
class RecordProcessingResult:
    """
    Result for one dataset after record-level separation.
    """

    dataset_name: str
    total_records: int
    valid_records: int
    invalid_records: int
    valid_dataframe: pd.DataFrame
    rejected_dataframe: pd.DataFrame

    @property
    def valid(self) -> bool:
        """Return True when no records were rejected."""

        return self.invalid_records == 0


@dataclass
class ValidationErrorRecord:
    """
    Standardized representation of one validation failure.
    """

    dataset_name: str
    record_identifier: object
    row_index: int
    column_name: str
    rule_id: str
    severity: str
    error_message: str


# =====================================================================
# Main processor
# =====================================================================


class RejectionProcessor:
    """
    Separate trusted and rejected records based on validation results.
    """

    def __init__(
        self,
        processed_root: str | Path = "data/processed",
        rejected_root: str | Path = "data/rejected",
        quality_reports_root: str | Path = (
            "data/quality_reports"
        ),
    ):
        self.processed_root = Path(
            processed_root
        )

        self.rejected_root = Path(
            rejected_root
        )

        self.quality_reports_root = Path(
            quality_reports_root
        )

    # =================================================================
    # PUBLIC API
    # =================================================================

    def process_dataset(
        self,
        dataset_name: str,
        dataframe: pd.DataFrame,
        validation_results: Iterable,
    ) -> RecordProcessingResult:
        """
        Separate one dataset into valid and rejected records.

        Parameters
        ----------
        dataset_name:
            Name of the dataset.

        dataframe:
            Original/raw DataFrame.

        validation_results:
            Iterable containing validation-result objects.

        Returns
        -------
        RecordProcessingResult

        Important:
            The input dataframe is never modified.
        """

        if not isinstance(
            dataframe,
            pd.DataFrame,
        ):
            raise RejectionProcessingError(
                f"Dataset '{dataset_name}' must be "
                f"a pandas DataFrame."
            )

        # -------------------------------------------------------------
        # Work on independent copies.
        # -------------------------------------------------------------

        source = dataframe.copy(
            deep=True
        )

        issues = self._extract_issues(
            validation_results
        )

        invalid_indices = self._get_invalid_indices(
            issues
        )

        # -------------------------------------------------------------
        # Make sure all issue row indices belong to the DataFrame.
        # -------------------------------------------------------------

        invalid_indices = {
            index
            for index in invalid_indices
            if index in source.index
        }

        # -------------------------------------------------------------
        # Valid records
        # -------------------------------------------------------------

        valid_dataframe = source.loc[
            ~source.index.isin(
                invalid_indices
            )
        ].copy(
            deep=True
        )

        # -------------------------------------------------------------
        # Rejected records
        # -------------------------------------------------------------

        rejected_dataframe = source.loc[
            source.index.isin(
                invalid_indices
            )
        ].copy(
            deep=True
        )

        return RecordProcessingResult(
            dataset_name=dataset_name,
            total_records=len(source),
            valid_records=len(
                valid_dataframe
            ),
            invalid_records=len(
                rejected_dataframe
            ),
            valid_dataframe=valid_dataframe,
            rejected_dataframe=rejected_dataframe,
        )

    def process_all(
        self,
        datasets: Dict[str, pd.DataFrame],
        validation_results: Dict,
    ) -> Dict[str, RecordProcessingResult]:
        """
        Process all datasets.

        validation_results should be grouped by dataset name.
        """

        if not datasets:
            raise RejectionProcessingError(
                "No datasets were provided."
            )

        results = {}

        for dataset_name, dataframe in (
            datasets.items()
        ):
            dataset_results = (
                validation_results.get(
                    dataset_name,
                    [],
                )
            )

            # ---------------------------------------------------------
            # A validation result object may itself contain an
            # `issues` attribute.
            #
            # Convert it into an iterable of issues.
            # ---------------------------------------------------------

            issues = self._extract_issues(
                dataset_results
            )

            results[dataset_name] = (
                self.process_dataset(
                    dataset_name=dataset_name,
                    dataframe=dataframe,
                    validation_results=issues,
                )
            )

        return results

    # =================================================================
    # VALIDATION ERROR EXTRACTION
    # =================================================================

    @staticmethod
    def _extract_issues(
        validation_results,
    ) -> List:
        """
        Extract issue objects from different validator result shapes.

        Supported forms:

            result.issues
            list/tuple/set of issues
            single issue object
            None
        """

        if validation_results is None:
            return []

        # -------------------------------------------------------------
        # Result object containing `.issues`
        # -------------------------------------------------------------

        if hasattr(
            validation_results,
            "issues",
        ):
            issues = validation_results.issues

            if issues is None:
                return []

            return list(issues)

        # -------------------------------------------------------------
        # Collection of result objects/issues
        # -------------------------------------------------------------

        if isinstance(
            validation_results,
            (list, tuple, set),
        ):
            extracted = []

            for item in validation_results:

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

        # -------------------------------------------------------------
        # Single issue object
        # -------------------------------------------------------------

        return [validation_results]

    @staticmethod
    def _get_invalid_indices(
        issues: Iterable,
    ) -> Set[int]:
        """
        Return row indices that have validation errors.

        Only issues with severity ERROR are considered record
        rejection triggers.

        Warnings are documented but do not automatically reject
        a record.
        """

        invalid_indices = set()

        for issue in issues:

            severity = str(
                getattr(
                    issue,
                    "severity",
                    "ERROR",
                )
            ).upper()

            if severity != "ERROR":
                continue

            row_index = getattr(
                issue,
                "row_index",
                None,
            )

            if row_index is None:
                continue

            try:
                invalid_indices.add(
                    int(row_index)
                )
            except (
                TypeError,
                ValueError,
            ):
                continue

        return invalid_indices

    # =================================================================
    # VALIDATION ERROR REPORT
    # =================================================================

    def build_validation_error_dataframe(
        self,
        datasets: Dict[str, pd.DataFrame],
        validation_results: Dict,
    ) -> pd.DataFrame:
        """
        Build the standardized validation_errors.csv DataFrame.

        Required output columns:

            dataset_name
            record_identifier
            column_name
            rule_id
            severity
            error_message

        Additional row_index information is retained for
        traceability.
        """

        rows = []

        for dataset_name, result in (
            validation_results.items()
        ):

            dataframe = datasets.get(
                dataset_name
            )

            issues = self._extract_issues(
                result
            )

            for issue in issues:

                row_index = getattr(
                    issue,
                    "row_index",
                    None,
                )

                record_identifier = (
                    self._get_record_identifier(
                        dataframe,
                        row_index,
                    )
                )

                rows.append(
                    {
                        "dataset_name": (
                            dataset_name
                        ),
                        "record_identifier": (
                            record_identifier
                        ),
                        "row_index": (
                            row_index
                        ),
                        "column_name": (
                            getattr(
                                issue,
                                "column_name",
                                "",
                            )
                        ),
                        "rule_id": (
                            getattr(
                                issue,
                                "rule_id",
                                "",
                            )
                        ),
                        "severity": (
                            getattr(
                                issue,
                                "severity",
                                "ERROR",
                            )
                        ),
                        "error_message": (
                            self._get_error_message(
                                issue
                            )
                        ),
                    }
                )

        columns = [
            "dataset_name",
            "record_identifier",
            "row_index",
            "column_name",
            "rule_id",
            "severity",
            "error_message",
        ]

        return pd.DataFrame(
            rows,
            columns=columns,
        )

    @staticmethod
    def _get_record_identifier(
        dataframe: pd.DataFrame | None,
        row_index,
    ):
        """
        Determine the dataset-specific record identifier.

        Identifier columns are selected in priority order.
        """

        if (
            dataframe is None
            or row_index is None
            or row_index not in dataframe.index
        ):
            return None

        identifier_columns = [
            "client_id",
            "portfolio_id",
            "security_id",
            "holding_id",
            "performance_id",
        ]

        for column in identifier_columns:

            if column in dataframe.columns:

                return dataframe.loc[
                    row_index,
                    column,
                ]

        return None

    @staticmethod
    def _get_error_message(
        issue,
    ) -> str:
        """
        Extract the human-readable validation message.
        """

        message = getattr(
            issue,
            "message",
            None,
        )

        if message is None:
            message = getattr(
                issue,
                "error_message",
                "",
            )

        return str(message)

    # =================================================================
    # FILE OUTPUT
    # =================================================================

    def write_dataset_outputs(
        self,
        result: RecordProcessingResult,
    ) -> tuple[Path, Path]:
        """
        Write trusted and rejected datasets.

        Trusted:
            data/processed/<dataset>/<dataset>_clean.csv

        Rejected:
            data/rejected/<dataset>/<dataset>_rejected.csv
        """

        dataset_name = result.dataset_name

        processed_directory = (
            self.processed_root
            / dataset_name
        )

        rejected_directory = (
            self.rejected_root
            / dataset_name
        )

        processed_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        rejected_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        processed_path = (
            processed_directory
            / f"{dataset_name}_clean.csv"
        )

        rejected_path = (
            rejected_directory
            / f"{dataset_name}_rejected.csv"
        )

        result.valid_dataframe.to_csv(
            processed_path,
            index=False,
        )

        result.rejected_dataframe.to_csv(
            rejected_path,
            index=False,
        )

        return (
            processed_path,
            rejected_path,
        )

    def write_all_dataset_outputs(
        self,
        results: Dict[
            str,
            RecordProcessingResult,
        ],
    ) -> Dict[str, tuple[Path, Path]]:
        """
        Write trusted and rejected files for every dataset.
        """

        output_paths = {}

        for dataset_name, result in (
            results.items()
        ):
            output_paths[dataset_name] = (
                self.write_dataset_outputs(
                    result
                )
            )

        return output_paths

    def write_validation_errors(
        self,
        validation_errors: pd.DataFrame,
    ) -> Path:
        """
        Write validation_errors.csv.
        """

        self.quality_reports_root.mkdir(
            parents=True,
            exist_ok=True,
        )

        output_path = (
            self.quality_reports_root
            / "validation_errors.csv"
        )

        validation_errors.to_csv(
            output_path,
            index=False,
        )

        return output_path

    def write_all(
        self,
        datasets: Dict[str, pd.DataFrame],
        validation_results: Dict,
    ) -> Dict:
        """
        Complete Phase 13 file-output operation.

        Returns paths and processing results.
        """

        results = self.process_all(
            datasets=datasets,
            validation_results=validation_results,
        )

        dataset_paths = (
            self.write_all_dataset_outputs(
                results
            )
        )

        validation_errors = (
            self.build_validation_error_dataframe(
                datasets=datasets,
                validation_results=validation_results,
            )
        )

        validation_error_path = (
            self.write_validation_errors(
                validation_errors
            )
        )

        return {
            "results": results,
            "dataset_paths": dataset_paths,
            "validation_errors": (
                validation_errors
            ),
            "validation_error_path": (
                validation_error_path
            ),
        }