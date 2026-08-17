import snowflake.connector

from config import settings


class SnowflakeRepository:

    # ============================================================
    # SNOWFLAKE CONNECTION
    # ============================================================

    def get_connection(self):
        """
        Create and return a Snowflake connection.
        """
        try:
            return snowflake.connector.connect(
                account=settings.SNOWFLAKE_ACCOUNT,
                user=settings.SNOWFLAKE_USER,
                password=settings.SNOWFLAKE_PASSWORD,
                warehouse=settings.SNOWFLAKE_WAREHOUSE,
                database=settings.SNOWFLAKE_DATABASE,
                schema=settings.SNOWFLAKE_SCHEMA,
                role=settings.SNOWFLAKE_ROLE,
            )
        except Exception as exc:
            # Raise a clearer error so the API logs make it obvious what's missing
            raise RuntimeError(
                f"Failed to create Snowflake connection. Check SNOWFLAKE_* env vars. Error: {exc}"
            ) from exc

    # ============================================================
    # HEALTH / READINESS
    # ============================================================

    def check_connection(self):
        """
        Check whether the API can connect to Snowflake.
        """

        connection = None
        cursor = None

        try:
            connection = self.get_connection()
            cursor = connection.cursor()

            cursor.execute("SELECT 1")

            result = cursor.fetchone()

            return result[0] == 1

        finally:
            if cursor:
                cursor.close()

            if connection:
                connection.close()

    # ============================================================
    # PORTFOLIO SUMMARY
    # ============================================================

    def get_portfolio(self, portfolio_id: str):
        """
        Get a single portfolio.
        """

        connection = None
        cursor = None

        try:
            connection = self.get_connection()
            cursor = connection.cursor()

            query = """
                SELECT
                    PORTFOLIO_ID,
                    CLIENT_ID,
                    PORTFOLIO_NAME,
                    PORTFOLIO_TYPE,
                    BASE_CURRENCY,
                    RISK_PROFILE,
                    INITIAL_VALUE,
                    CURRENT_VALUE,
                    RETURN_AMOUNT,
                    RETURN_PERCENT,
                    TOTAL_MARKET_VALUE,
                    HOLDING_COUNT,
                    LATEST_PERFORMANCE_DATE,
                    STATUS,
                    INCEPTION_DATE
                FROM IPRA_DB.ANALYTICS.V_PORTFOLIO_SUMMARY
                WHERE PORTFOLIO_ID = %s
            """

            cursor.execute(query, (portfolio_id,))

            row = cursor.fetchone()

            if row is None:
                return None

            columns = [
                column[0].lower()
                for column in cursor.description
            ]

            return dict(zip(columns, row))

        finally:
            if cursor:
                cursor.close()

            if connection:
                connection.close()

    # ============================================================
    # PORTFOLIO LIST
    # ============================================================

    def get_portfolios(
        self,
        page: int = 1,
        page_size: int = 20,
        client_id: str | None = None,
        risk_profile: str | None = None,
        status: str | None = None,
        search: str | None = None,
    ):
        """
        Get paginated portfolios with optional filters.
        """

        connection = None
        cursor = None

        try:
            connection = self.get_connection()
            cursor = connection.cursor()

            where_conditions = []
            filter_params = []

            if client_id:
                where_conditions.append(
                    "CLIENT_ID = %s"
                )
                filter_params.append(client_id)

            if search:
                # Search by portfolio_id or portfolio_name (case-insensitive, partial match)
                where_conditions.append(
                    "(LOWER(PORTFOLIO_ID) LIKE LOWER(%s) OR LOWER(PORTFOLIO_NAME) LIKE LOWER(%s))"
                )
                like_term = f"%{search}%"
                filter_params.extend([like_term, like_term])

            if risk_profile:
                # Use case-insensitive comparison for risk_profile
                where_conditions.append(
                    "LOWER(RISK_PROFILE) = LOWER(%s)"
                )
                filter_params.append(risk_profile)

            if status:
                # Use case-insensitive comparison for status
                where_conditions.append(
                    "LOWER(STATUS) = LOWER(%s)"
                )
                filter_params.append(status)

            where_clause = ""

            if where_conditions:
                where_clause = (
                    "WHERE "
                    + " AND ".join(where_conditions)
                )

            count_query = f"""
                SELECT COUNT(*)
                FROM IPRA_DB.ANALYTICS.V_PORTFOLIO_SUMMARY
                {where_clause}
            """

            cursor.execute(
                count_query,
                tuple(filter_params)
            )

            total_items = cursor.fetchone()[0]

            offset = (page - 1) * page_size

            data_query = f"""
                SELECT
                    PORTFOLIO_ID,
                    CLIENT_ID,
                    PORTFOLIO_NAME,
                    PORTFOLIO_TYPE,
                    BASE_CURRENCY,
                    RISK_PROFILE,
                    INITIAL_VALUE,
                    CURRENT_VALUE,
                    RETURN_AMOUNT,
                    RETURN_PERCENT,
                    TOTAL_MARKET_VALUE,
                    HOLDING_COUNT,
                    LATEST_PERFORMANCE_DATE,
                    STATUS,
                    INCEPTION_DATE
                FROM IPRA_DB.ANALYTICS.V_PORTFOLIO_SUMMARY
                {where_clause}
                ORDER BY PORTFOLIO_ID
                LIMIT %s
                OFFSET %s
            """

            data_params = filter_params + [
                page_size,
                offset
            ]

            cursor.execute(
                data_query,
                tuple(data_params)
            )

            rows = cursor.fetchall()

            columns = [
                column[0].lower()
                for column in cursor.description
            ]

            items = [
                dict(zip(columns, row))
                for row in rows
            ]

            return items, total_items

        finally:
            if cursor:
                cursor.close()

            if connection:
                connection.close()

    # ============================================================
    # HOLDINGS
    # ============================================================

    def get_holdings(
        self,
        portfolio_id: str,
        page: int = 1,
        page_size: int = 20,
    ):
        """
        Get paginated holdings for a portfolio.
        """

        connection = None
        cursor = None

        try:
            connection = self.get_connection()
            cursor = connection.cursor()

            count_query = """
                SELECT COUNT(*)
                FROM IPRA_DB.ANALYTICS.V_PORTFOLIO_HOLDINGS
                WHERE PORTFOLIO_ID = %s
            """

            cursor.execute(
                count_query,
                (portfolio_id,)
            )

            total_items = cursor.fetchone()[0]

            offset = (page - 1) * page_size

            query = """
                SELECT
                    HOLDING_ID,
                    PORTFOLIO_ID,
                    SECURITY_ID,
                    TICKER_SYMBOL,
                    SECURITY_NAME,
                    SECURITY_TYPE,
                    SECTOR,
                    SECURITY_COUNTRY,
                    SECURITY_CURRENCY,
                    QUANTITY,
                    PURCHASE_PRICE,
                    CURRENT_PRICE,
                    MARKET_VALUE,
                    AS_OF_DATE,
                    PORTFOLIO_NAME,
                    CLIENT_ID,
                    CLIENT_NAME
                FROM IPRA_DB.ANALYTICS.V_PORTFOLIO_HOLDINGS
                WHERE PORTFOLIO_ID = %s
                ORDER BY HOLDING_ID
                LIMIT %s
                OFFSET %s
            """

            cursor.execute(
                query,
                (
                    portfolio_id,
                    page_size,
                    offset
                )
            )

            rows = cursor.fetchall()

            columns = [
                column[0].lower()
                for column in cursor.description
            ]

            items = [
                dict(zip(columns, row))
                for row in rows
            ]

            return items, total_items

        finally:
            if cursor:
                cursor.close()

            if connection:
                connection.close()

    # ============================================================
    # ALLOCATION
    # ============================================================

    def get_allocation(
        self,
        portfolio_id: str,
        dimension: str,
    ):
        """
        Get portfolio allocation.

        Supported dimensions:
        - security
        - sector
        - country
        """

        connection = None
        cursor = None

        try:
            valid_dimensions = {
                "security",
                "sector",
                "country",
            }

            if dimension not in valid_dimensions:
                raise ValueError(
                    "Invalid allocation dimension"
                )

            connection = self.get_connection()
            cursor = connection.cursor()

            # Security-level allocation (each security row)
            if dimension == "security":
                query = """
                    SELECT
                        PORTFOLIO_ID,
                        SECURITY_ID,
                        SECURITY_NAME,
                        SECTOR,
                        SECURITY_COUNTRY,
                        SECURITY_MARKET_VALUE,
                        SECURITY_ALLOCATION_PERCENT,
                        SECTOR_ALLOCATION_PERCENT,
                        COUNTRY_ALLOCATION_PERCENT,
                        PORTFOLIO_TOTAL_VALUE,
                        AS_OF_DATE
                    FROM IPRA_DB.ANALYTICS.V_PORTFOLIO_ALLOCATION
                    WHERE PORTFOLIO_ID = %s
                    ORDER BY SECURITY_ID
                """

                cursor.execute(query, (portfolio_id,))

                rows = cursor.fetchall()

                columns = [column[0].lower() for column in cursor.description]

                items = [dict(zip(columns, row)) for row in rows]

                return items

            # Aggregate by sector
            if dimension == "sector":
                query = """
                    SELECT
                        SECTOR,
                        SUM(SECURITY_MARKET_VALUE) AS sector_market_value,
                        CASE WHEN MAX(PORTFOLIO_TOTAL_VALUE) = 0 THEN 0
                             ELSE (SUM(SECURITY_MARKET_VALUE) / MAX(PORTFOLIO_TOTAL_VALUE)) * 100
                        END AS sector_allocation_percent,
                        MAX(PORTFOLIO_TOTAL_VALUE) AS portfolio_total_value,
                        MAX(AS_OF_DATE) AS as_of_date
                    FROM IPRA_DB.ANALYTICS.V_PORTFOLIO_ALLOCATION
                    WHERE PORTFOLIO_ID = %s
                    GROUP BY SECTOR
                    ORDER BY sector_market_value DESC
                """

                cursor.execute(query, (portfolio_id,))

                rows = cursor.fetchall()

                columns = [column[0].lower() for column in cursor.description]

                items = [dict(zip(columns, row)) for row in rows]

                return items

            # Aggregate by country
            if dimension == "country":
                query = """
                    SELECT
                        SECURITY_COUNTRY,
                        SUM(SECURITY_MARKET_VALUE) AS country_market_value,
                        CASE WHEN MAX(PORTFOLIO_TOTAL_VALUE) = 0 THEN 0
                             ELSE (SUM(SECURITY_MARKET_VALUE) / MAX(PORTFOLIO_TOTAL_VALUE)) * 100
                        END AS country_allocation_percent,
                        MAX(PORTFOLIO_TOTAL_VALUE) AS portfolio_total_value,
                        MAX(AS_OF_DATE) AS as_of_date
                    FROM IPRA_DB.ANALYTICS.V_PORTFOLIO_ALLOCATION
                    WHERE PORTFOLIO_ID = %s
                    GROUP BY SECURITY_COUNTRY
                    ORDER BY country_market_value DESC
                """

                cursor.execute(query, (portfolio_id,))

                rows = cursor.fetchall()

                columns = [column[0].lower() for column in cursor.description]

                items = [dict(zip(columns, row)) for row in rows]

                return items

        finally:
            if cursor:
                cursor.close()

            if connection:
                connection.close()

    # ============================================================
    # PERFORMANCE
    # ============================================================

    def get_performance(
        self,
        portfolio_id: str,
        from_date=None,
        to_date=None,
        interval: str = "monthly",
    ):
        """
        Get portfolio performance.
        """

        connection = None
        cursor = None

        try:
            valid_intervals = {
                "daily",
                "weekly",
                "monthly",
            }

            if interval not in valid_intervals:
                raise ValueError(
                    "Invalid performance interval"
                )

            connection = self.get_connection()
            cursor = connection.cursor()

            conditions = [
                "PORTFOLIO_ID = %s"
            ]

            params = [
                portfolio_id
            ]

            if from_date is not None:
                conditions.append(
                    "AS_OF_DATE >= %s"
                )
                params.append(from_date)

            if to_date is not None:
                conditions.append(
                    "AS_OF_DATE <= %s"
                )
                params.append(to_date)

            where_clause = (
                "WHERE " + " AND ".join(conditions)
            )

            query = f"""
                SELECT
                    PERFORMANCE_ID,
                    PORTFOLIO_ID,
                    AS_OF_DATE,
                    BEGINNING_VALUE,
                    ENDING_VALUE,
                    RETURN_AMOUNT,
                    RETURN_PERCENT,
                    PREVIOUS_VALUE,
                    PERIOD_OVER_PERIOD_RETURN,
                    PORTFOLIO_NAME,
                    CLIENT_ID
                FROM IPRA_DB.ANALYTICS.V_PORTFOLIO_PERFORMANCE
                {where_clause}
                ORDER BY AS_OF_DATE
            """

            cursor.execute(
                query,
                tuple(params)
            )

            rows = cursor.fetchall()

            columns = [
                column[0].lower()
                for column in cursor.description
            ]

            items = [
                dict(zip(columns, row))
                for row in rows
            ]

            return items

        finally:
            if cursor:
                cursor.close()

            if connection:
                connection.close()

    # ============================================================
    # RISK
    # ============================================================

    def get_risk(self, portfolio_id: str):
        """
        Get portfolio risk information.
        """

        connection = None
        cursor = None

        try:
            connection = self.get_connection()
            cursor = connection.cursor()

            query = """
                SELECT
                    PORTFOLIO_ID,
                    CLIENT_ID,
                    PORTFOLIO_NAME,
                    PORTFOLIO_RISK_PROFILE,
                    HIGHEST_HOLDING_SECURITY_ID,
                    HIGHEST_HOLDING_VALUE,
                    HIGHEST_WEIGHT_PERCENT,
                    CONCENTRATION_RISK,
                    RISK_STATUS,
                    RISK_EXPLANATION,
                    CURRENT_VALUE,
                    TOTAL_MARKET_VALUE,
                    HOLDING_COUNT,
                    ANALYZED_AT
                FROM IPRA_DB.ANALYTICS.V_PORTFOLIO_RISK
                WHERE PORTFOLIO_ID = %s
            """

            cursor.execute(
                query,
                (portfolio_id,)
            )

            row = cursor.fetchone()

            if row is None:
                return None

            columns = [
                column[0].lower()
                for column in cursor.description
            ]

            return dict(zip(columns, row))

        finally:
            if cursor:
                cursor.close()

            if connection:
                connection.close()

    # ============================================================
    # CLIENT PORTFOLIO SUMMARY
    # ============================================================

    def get_client_portfolios(
        self,
        client_id: str,
    ):
        """
        Get portfolio summary information for a client.
        """

        connection = None
        cursor = None

        try:
            connection = self.get_connection()
            cursor = connection.cursor()

            query = """
                SELECT
                    CLIENT_ID,
                    CLIENT_NAME,
                    CLIENT_TYPE,
                    CLIENT_COUNTRY,
                    CLIENT_RISK_PROFILE,
                    PORTFOLIO_COUNT,
                    TOTAL_PORTFOLIO_VALUE,
                    AVERAGE_RETURN_PERCENT,
                    HIGH_RISK_PORTFOLIO_COUNT,
                    MEDIUM_RISK_PORTFOLIO_COUNT,
                    LOW_RISK_PORTFOLIO_COUNT,
                    CLIENT_STATUS,
                    CREATED_DATE
                FROM IPRA_DB.ANALYTICS.V_CLIENT_PORTFOLIO_SUMMARY
                WHERE CLIENT_ID = %s
            """

            cursor.execute(
                query,
                (client_id,)
            )

            row = cursor.fetchone()

            if row is None:
                return None

            columns = [
                column[0].lower()
                for column in cursor.description
            ]

            return dict(zip(columns, row))

        finally:
            if cursor:
                cursor.close()

            if connection:
                connection.close()

    # ============================================================
    # CLIENTS
    # ============================================================

    def get_clients(self):
        """
        Get a list of clients with portfolio summary information.
        """

        connection = None
        cursor = None

        try:
            connection = self.get_connection()
            cursor = connection.cursor()

            query = """
                SELECT
                    CLIENT_ID,
                    CLIENT_NAME,
                    CLIENT_TYPE,
                    CLIENT_COUNTRY,
                    CLIENT_RISK_PROFILE,
                    PORTFOLIO_COUNT,
                    TOTAL_PORTFOLIO_VALUE,
                    AVERAGE_RETURN_PERCENT,
                    HIGH_RISK_PORTFOLIO_COUNT,
                    MEDIUM_RISK_PORTFOLIO_COUNT,
                    LOW_RISK_PORTFOLIO_COUNT,
                    CLIENT_STATUS,
                    CREATED_DATE
                FROM IPRA_DB.ANALYTICS.V_CLIENT_PORTFOLIO_SUMMARY
                ORDER BY CLIENT_ID
            """

            cursor.execute(query)

            rows = cursor.fetchall()

            columns = [
                column[0].lower()
                for column in cursor.description
            ]

            items = [
                dict(zip(columns, row))
                for row in rows
            ]

            return items

        finally:
            if cursor:
                cursor.close()

            if connection:
                connection.close()