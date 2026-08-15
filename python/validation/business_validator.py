"""
Business-rule validation for Participant 2.

This module validates domain-specific financial/business rules.

Responsibilities:
    - Portfolio financial value validation.
    - Portfolio inception-date validation.
    - Security price validation.
    - Holdings quantity/price/market-value validation.
    - Portfolio-performance calculation validation.

This module does NOT:
    - validate schema
    - validate nulls
    - validate types
    - validate duplicates
    - validate categorical domains
    - modify source data
    - delete invalid records
    - perform referential-integrity checks
"""

from dataclasses import dataclass
from datetime import date
from typing import Dict, List

import pandas as pd

from .config import (
    BUSINESS_RULE_IDS,
    MARKET_VALUE_TOLERANCE,
    MIN_HOLDING_CURRENT_PRICE,
    MIN_HOLDING_PURCHASE_PRICE,
    MIN_HOLDING_QUANTITY,
    MIN_PERFORMANCE_VALUE,
    MIN_PORTFOLIO_VALUE,
    MIN_SECURITY_PRICE,
    RETURN_AMOUNT_TOLERANCE,
    RETURN_PERCENT_TOLERANCE,
)


@dataclass
class BusinessValidationIssue:
    """Represents one business-rule violation."""

    dataset_name: str
    row_index: int
    column_name: str
    rule_id: str
    rule_name: str
    severity: str
    actual_value: object
    expected_value: object
    message: str


@dataclass
class BusinessValidationResult:
    """Result of business validation for one dataset."""

    dataset_name: str
    valid: bool
    issues: List[BusinessValidationIssue]

    @property
    def error_count(self) -> int:
        """Number of business-rule errors."""

        return len(self.issues)


class BusinessValidationError(Exception):
    """Raised when business validation cannot be performed."""


class BusinessValidator:
    """Reusable business-rule validator."""

    def __init__(
        self,
        business_rule_ids: Dict | None = None,
        market_value_tolerance: float = (
            MARKET_VALUE_TOLERANCE
        ),
        return_amount_tolerance: float = (
            RETURN_AMOUNT_TOLERANCE
        ),
        return_percent_tolerance: float = (
            RETURN_PERCENT_TOLERANCE
        ),
    ):
        self.business_rule_ids = (
            business_rule_ids
            if business_rule_ids is not None
            else BUSINESS_RULE_IDS
        )

        self.market_value_tolerance = (
            market_value_tolerance
        )

        self.return_amount_tolerance = (
            return_amount_tolerance
        )

        self.return_percent_tolerance = (
            return_percent_tolerance
        )

    # ==================================================================
    # Public API
    # ==================================================================

    def validate_dataset(
        self,
        dataset_name: str,
        dataframe: pd.DataFrame,
        current_business_date: date | None = None,
    ) -> BusinessValidationResult:
        """
        Validate all applicable business rules for one dataset.
        """

        if not isinstance(
            dataframe,
            pd.DataFrame,
        ):
            raise BusinessValidationError(
                f"Expected pandas DataFrame for "
                f"dataset: {dataset_name}"
            )

        if current_business_date is None:
            current_business_date = date.today()

        if dataset_name == "portfolios":
            issues = self._validate_portfolios(
                dataframe,
                current_business_date,
            )

        elif dataset_name == "securities":
            issues = self._validate_securities(
                dataframe
            )

        elif dataset_name == "holdings":
            issues = self._validate_holdings(
                dataframe
            )

        elif dataset_name == "portfolio_performance":
            issues = self._validate_performance(
                dataframe
            )

        else:
            # Clients currently have no Phase-10 financial
            # business rules.
            issues = []

        return BusinessValidationResult(
            dataset_name=dataset_name,
            valid=len(issues) == 0,
            issues=issues,
        )

    # ==================================================================
    # Portfolio rules
    # ==================================================================

    def _validate_portfolios(
        self,
        dataframe: pd.DataFrame,
        current_business_date: date,
    ) -> List[BusinessValidationIssue]:

        required = [
            "initial_value",
            "current_value",
            "inception_date",
        ]

        self._require_columns(
            dataframe,
            "portfolios",
            required,
        )

        issues = []

        for row_index, row in dataframe.iterrows():

            initial_value = row[
                "initial_value"
            ]

            current_value = row[
                "current_value"
            ]

            inception_date = row[
                "inception_date"
            ]

            # ----------------------------------------------------------
            # Initial value
            # ----------------------------------------------------------

            if pd.notna(initial_value):

                if initial_value < MIN_PORTFOLIO_VALUE:
                    issues.append(
                        self._issue(
                            dataset_name="portfolios",
                            row_index=row_index,
                            column_name="initial_value",
                            rule_key="initial_value",
                            rule_name="NON_NEGATIVE_INITIAL_VALUE",
                            severity="ERROR",
                            actual_value=initial_value,
                            expected_value=">= 0",
                            message=(
                                "Portfolio initial value "
                                "cannot be negative."
                            ),
                        )
                    )

            # ----------------------------------------------------------
            # Current value
            # ----------------------------------------------------------

            if pd.notna(current_value):

                if current_value < MIN_PORTFOLIO_VALUE:
                    issues.append(
                        self._issue(
                            dataset_name="portfolios",
                            row_index=row_index,
                            column_name="current_value",
                            rule_key="current_value",
                            rule_name="NON_NEGATIVE_CURRENT_VALUE",
                            severity="ERROR",
                            actual_value=current_value,
                            expected_value=">= 0",
                            message=(
                                "Portfolio current value "
                                "cannot be negative."
                            ),
                        )
                    )

            # ----------------------------------------------------------
            # Inception date
            # ----------------------------------------------------------

            if pd.notna(inception_date):

                parsed_date = (
                    self._parse_date(
                        inception_date
                    )
                )

                if parsed_date is not None:

                    if (
                        parsed_date
                        > current_business_date
                    ):
                        issues.append(
                            self._issue(
                                dataset_name="portfolios",
                                row_index=row_index,
                                column_name="inception_date",
                                rule_key="inception_date",
                                rule_name="INCEPTION_DATE_NOT_FUTURE",
                                severity="ERROR",
                                actual_value=(
                                    inception_date
                                ),
                                expected_value=(
                                    f"<= "
                                    f"{current_business_date}"
                                ),
                                message=(
                                    "Portfolio inception "
                                    "date cannot be later "
                                    "than the current "
                                    "business date."
                                ),
                            )
                        )

        return issues

    # ==================================================================
    # Security rules
    # ==================================================================

    def _validate_securities(
        self,
        dataframe: pd.DataFrame,
    ) -> List[BusinessValidationIssue]:

        required = [
            "current_price",
        ]

        self._require_columns(
            dataframe,
            "securities",
            required,
        )

        issues = []

        for row_index, row in dataframe.iterrows():

            current_price = row[
                "current_price"
            ]

            if pd.notna(current_price):

                if current_price <= MIN_SECURITY_PRICE:
                    issues.append(
                        self._issue(
                            dataset_name="securities",
                            row_index=row_index,
                            column_name="current_price",
                            rule_key="current_price",
                            rule_name="POSITIVE_SECURITY_PRICE",
                            severity="ERROR",
                            actual_value=current_price,
                            expected_value="> 0",
                            message=(
                                "Security current price "
                                "must be greater than zero."
                            ),
                        )
                    )

        return issues

    # ==================================================================
    # Holdings rules
    # ==================================================================

    def _validate_holdings(
        self,
        dataframe: pd.DataFrame,
    ) -> List[BusinessValidationIssue]:

        required = [
            "quantity",
            "purchase_price",
            "current_price",
            "market_value",
        ]

        self._require_columns(
            dataframe,
            "holdings",
            required,
        )

        issues = []

        for row_index, row in dataframe.iterrows():

            quantity = row["quantity"]

            purchase_price = row[
                "purchase_price"
            ]

            current_price = row[
                "current_price"
            ]

            market_value = row[
                "market_value"
            ]

            # ----------------------------------------------------------
            # Quantity
            # ----------------------------------------------------------

            if pd.notna(quantity):

                if quantity <= MIN_HOLDING_QUANTITY:
                    issues.append(
                        self._issue(
                            dataset_name="holdings",
                            row_index=row_index,
                            column_name="quantity",
                            rule_key="quantity",
                            rule_name="POSITIVE_HOLDING_QUANTITY",
                            severity="ERROR",
                            actual_value=quantity,
                            expected_value="> 0",
                            message=(
                                "Holding quantity must "
                                "be greater than zero."
                            ),
                        )
                    )

            # ----------------------------------------------------------
            # Purchase price
            # ----------------------------------------------------------

            if pd.notna(purchase_price):

                if (
                    purchase_price
                    <= MIN_HOLDING_PURCHASE_PRICE
                ):
                    issues.append(
                        self._issue(
                            dataset_name="holdings",
                            row_index=row_index,
                            column_name="purchase_price",
                            rule_key="purchase_price",
                            rule_name="POSITIVE_PURCHASE_PRICE",
                            severity="ERROR",
                            actual_value=purchase_price,
                            expected_value="> 0",
                            message=(
                                "Holding purchase price "
                                "must be greater than zero."
                            ),
                        )
                    )

            # ----------------------------------------------------------
            # Current price
            # ----------------------------------------------------------

            if pd.notna(current_price):

                if (
                    current_price
                    <= MIN_HOLDING_CURRENT_PRICE
                ):
                    issues.append(
                        self._issue(
                            dataset_name="holdings",
                            row_index=row_index,
                            column_name="current_price",
                            rule_key="current_price",
                            rule_name="POSITIVE_HOLDING_CURRENT_PRICE",
                            severity="ERROR",
                            actual_value=current_price,
                            expected_value="> 0",
                            message=(
                                "Holding current price "
                                "must be greater than zero."
                            ),
                        )
                    )

            # ----------------------------------------------------------
            # Market value
            # ----------------------------------------------------------

            if (
                pd.notna(quantity)
                and pd.notna(current_price)
                and pd.notna(market_value)
                and quantity > 0
                and current_price > 0
            ):

                expected_market_value = (
                    quantity * current_price
                )

                if not self._within_tolerance(
                    actual=market_value,
                    expected=expected_market_value,
                    tolerance=(
                        self.market_value_tolerance
                    ),
                ):
                    issues.append(
                        self._issue(
                            dataset_name="holdings",
                            row_index=row_index,
                            column_name="market_value",
                            rule_key="market_value",
                            rule_name="MARKET_VALUE_CALCULATION",
                            severity="ERROR",
                            actual_value=market_value,
                            expected_value=(
                                expected_market_value
                            ),
                            message=(
                                "Holding market value "
                                "does not approximately "
                                "equal quantity × "
                                "current price."
                            ),
                        )
                    )

        return issues

    # ==================================================================
    # Performance rules
    # ==================================================================

    def _validate_performance(
        self,
        dataframe: pd.DataFrame,
    ) -> List[BusinessValidationIssue]:

        required = [
            "beginning_value",
            "ending_value",
            "return_amount",
            "return_percent",
        ]

        self._require_columns(
            dataframe,
            "portfolio_performance",
            required,
        )

        issues = []

        for row_index, row in dataframe.iterrows():

            beginning_value = row[
                "beginning_value"
            ]

            ending_value = row[
                "ending_value"
            ]

            return_amount = row[
                "return_amount"
            ]

            return_percent = row[
                "return_percent"
            ]

            # ----------------------------------------------------------
            # Beginning value
            # ----------------------------------------------------------

            if pd.notna(beginning_value):

                if (
                    beginning_value
                    < MIN_PERFORMANCE_VALUE
                ):
                    issues.append(
                        self._issue(
                            dataset_name=(
                                "portfolio_performance"
                            ),
                            row_index=row_index,
                            column_name=(
                                "beginning_value"
                            ),
                            rule_key="beginning_value",
                            rule_name=(
                                "NON_NEGATIVE_BEGINNING_VALUE"
                            ),
                            severity="ERROR",
                            actual_value=beginning_value,
                            expected_value=">= 0",
                            message=(
                                "Beginning portfolio "
                                "value cannot be negative."
                            ),
                        )
                    )

            # ----------------------------------------------------------
            # Ending value
            # ----------------------------------------------------------

            if pd.notna(ending_value):

                if (
                    ending_value
                    < MIN_PERFORMANCE_VALUE
                ):
                    issues.append(
                        self._issue(
                            dataset_name=(
                                "portfolio_performance"
                            ),
                            row_index=row_index,
                            column_name="ending_value",
                            rule_key="ending_value",
                            rule_name=(
                                "NON_NEGATIVE_ENDING_VALUE"
                            ),
                            severity="ERROR",
                            actual_value=ending_value,
                            expected_value=">= 0",
                            message=(
                                "Ending portfolio value "
                                "cannot be negative."
                            ),
                        )
                    )

            # ----------------------------------------------------------
            # Return amount
            # ----------------------------------------------------------

            if (
                pd.notna(beginning_value)
                and pd.notna(ending_value)
                and pd.notna(return_amount)
            ):

                expected_return_amount = (
                    ending_value
                    - beginning_value
                )

                if not self._within_tolerance(
                    actual=return_amount,
                    expected=expected_return_amount,
                    tolerance=(
                        self.return_amount_tolerance
                    ),
                ):
                    issues.append(
                        self._issue(
                            dataset_name=(
                                "portfolio_performance"
                            ),
                            row_index=row_index,
                            column_name="return_amount",
                            rule_key="return_amount",
                            rule_name=(
                                "RETURN_AMOUNT_CALCULATION"
                            ),
                            severity="ERROR",
                            actual_value=return_amount,
                            expected_value=(
                                expected_return_amount
                            ),
                            message=(
                                "Return amount does not "
                                "match ending value "
                                "minus beginning value."
                            ),
                        )
                    )

            # ----------------------------------------------------------
            # Return percentage
            #
            # IMPORTANT:
            # Use absolute tolerance here instead of relative
            # tolerance. Relative tolerance becomes unstable when
            # the expected percentage is very close to zero.
            # ----------------------------------------------------------

            if (
                pd.notna(beginning_value)
                and pd.notna(return_amount)
                and pd.notna(return_percent)
                and beginning_value > 0
            ):

                expected_return_percent = (
                    return_amount
                    / beginning_value
                    * 100
                )

                if not self._within_absolute_tolerance(
                    actual=return_percent,
                    expected=(
                        expected_return_percent
                    ),
                    tolerance=(
                        self.return_percent_tolerance
                    ),
                ):
                    issues.append(
                        self._issue(
                            dataset_name=(
                                "portfolio_performance"
                            ),
                            row_index=row_index,
                            column_name="return_percent",
                            rule_key="return_percent",
                            rule_name=(
                                "RETURN_PERCENT_CALCULATION"
                            ),
                            severity="ERROR",
                            actual_value=return_percent,
                            expected_value=(
                                expected_return_percent
                            ),
                            message=(
                                "Return percentage does "
                                "not match return amount "
                                "divided by beginning "
                                "value."
                            ),
                        )
                    )

        return issues

    # ==================================================================
    # Tolerance helpers
    # ==================================================================

    @staticmethod
    def _within_tolerance(
        actual: float,
        expected: float,
        tolerance: float,
    ) -> bool:
        """
        Compare values using relative tolerance.

        Example:
            tolerance=0.01 means ±1%.

        Used for:
            - market value
            - return amount
        """

        if expected == 0:
            return abs(actual) <= tolerance

        relative_difference = (
            abs(actual - expected)
            / abs(expected)
        )

        return (
            relative_difference
            <= tolerance
        )

    @staticmethod
    def _within_absolute_tolerance(
        actual: float,
        expected: float,
        tolerance: float,
    ) -> bool:
        """
        Compare values using absolute tolerance.

        This is appropriate for rounded percentages,
        especially when the expected percentage is very
        close to zero.

        Example:
            expected = -0.00047755
            actual   = -0.0005

        Difference:
            approximately 0.00002245

        With a tolerance of 0.0001, this passes.
        """

        return abs(actual - expected) <= tolerance

    # ==================================================================
    # Date helper
    # ==================================================================

    @staticmethod
    def _parse_date(value):
        """Parse a YYYY-MM-DD-style value into a date."""

        if isinstance(
            value,
            pd.Timestamp,
        ):
            return value.date()

        if isinstance(
            value,
            date,
        ):
            return value

        if not isinstance(
            value,
            str,
        ):
            return None

        try:
            parsed = pd.to_datetime(
                value,
                format="%Y-%m-%d",
                errors="raise",
            )

            return parsed.date()

        except (
            ValueError,
            TypeError,
        ):
            return None

    # ==================================================================
    # Issue creation
    # ==================================================================

    def _issue(
        self,
        dataset_name,
        row_index,
        column_name,
        rule_key,
        rule_name,
        severity,
        actual_value,
        expected_value,
        message,
    ):
        """Create a standardized business-rule issue."""

        rule_id = (
            self.business_rule_ids
            .get(dataset_name, {})
            .get(
                rule_key,
                "BUS-UNKNOWN",
            )
        )

        return BusinessValidationIssue(
            dataset_name=dataset_name,
            row_index=int(row_index),
            column_name=column_name,
            rule_id=rule_id,
            rule_name=rule_name,
            severity=severity,
            actual_value=actual_value,
            expected_value=expected_value,
            message=message,
        )

    # ==================================================================
    # Required-column validation
    # ==================================================================

    @staticmethod
    def _require_columns(
        dataframe,
        dataset_name,
        required_columns,
    ):
        """Ensure required business-rule columns exist."""

        missing = [
            column
            for column in required_columns
            if column not in dataframe.columns
        ]

        if missing:
            raise BusinessValidationError(
                f"Dataset '{dataset_name}' is missing "
                f"business-rule columns: {missing}. "
                f"Run schema validation first."
            )

    # ==================================================================
    # All datasets
    # ==================================================================

    def validate_all(
        self,
        datasets: Dict[str, pd.DataFrame],
        current_business_date: date | None = None,
    ) -> Dict[str, BusinessValidationResult]:
        """Validate all datasets."""

        if not datasets:
            raise BusinessValidationError(
                "No datasets were provided for "
                "business validation."
            )

        results = {}

        for dataset_name, dataframe in (
            datasets.items()
        ):
            results[dataset_name] = (
                self.validate_dataset(
                    dataset_name,
                    dataframe,
                    current_business_date,
                )
            )

        return results

    # ==================================================================
    # Convenience
    # ==================================================================

    def is_valid(
        self,
        dataset_name: str,
        dataframe: pd.DataFrame,
        current_business_date: date | None = None,
    ) -> bool:
        """Return True when no business-rule errors exist."""

        return self.validate_dataset(
            dataset_name,
            dataframe,
            current_business_date,
        ).valid