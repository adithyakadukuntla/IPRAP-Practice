from datetime import datetime
from pathlib import Path

from csv_ingestion import read_csv_file
from ingestion_checks import (
    validate_csv_ingestion,
    CLIENT_COLUMNS,
    PORTFOLIO_COLUMNS,
    HOLDING_COLUMNS,
    PERFORMANCE_COLUMNS
)
from api_ingestion import read_security_json
from ingestion_logger import (
    IngestionLogger,
    generate_run_id
)
RAW_PATH = Path("data/raw")

METADATA_PATH = (
    Path("data/metadata/ingestion_metadata.csv")
)

logger = IngestionLogger(
    METADATA_PATH
)

run_id = generate_run_id()
start_time = datetime.now()

try:

    clients = validate_csv_ingestion(
        RAW_PATH / "clients" / "clients.csv",
        CLIENT_COLUMNS,
        "CLIENTS"
    )

    end_time = datetime.now()

    logger.log(
        run_id=run_id,
        dataset_name="clients",
        source_type="CSV",
        source_name="clients.csv",
        start_time=start_time,
        end_time=end_time,
        records_read=len(clients),
        status="SUCCESS"
    )

    print(
        f"CLIENTS ingestion successful: "
        f"{len(clients)} records"
    )

except Exception as e:

    end_time = datetime.now()

    logger.log(
        run_id=run_id,
        dataset_name="clients",
        source_type="CSV",
        source_name="clients.csv",
        start_time=start_time,
        end_time=end_time,
        records_read=0,
        status="FAILED",
        error_message=str(e)
    )

    print(f"CLIENTS ingestion failed: {e}")
start_time = datetime.now()

try:

    portfolios = validate_csv_ingestion(
        RAW_PATH / "portfolios" / "portfolios.csv",
        PORTFOLIO_COLUMNS,
        "PORTFOLIOS"
    )

    end_time = datetime.now()

    logger.log(
        run_id,
        "portfolios",
        "CSV",
        "portfolios.csv",
        start_time,
        end_time,
        len(portfolios),
        "SUCCESS"
    )

    print(
        f"PORTFOLIOS ingestion successful: "
        f"{len(portfolios)} records"
    )

except Exception as e:

    end_time = datetime.now()

    logger.log(
        run_id,
        "portfolios",
        "CSV",
        "portfolios.csv",
        start_time,
        end_time,
        0,
        "FAILED",
        str(e)
    )

    print(f"PORTFOLIOS ingestion failed: {e}")
start_time = datetime.now()

try:

    holdings = validate_csv_ingestion(
        RAW_PATH / "holdings" / "holdings.csv",
        HOLDING_COLUMNS,
        "HOLDINGS"
    )

    end_time = datetime.now()

    logger.log(
        run_id,
        "holdings",
        "CSV",
        "holdings.csv",
        start_time,
        end_time,
        len(holdings),
        "SUCCESS"
    )

    print(
        f"HOLDINGS ingestion successful: "
        f"{len(holdings)} records"
    )

except Exception as e:

    end_time = datetime.now()

    logger.log(
        run_id,
        "holdings",
        "CSV",
        "holdings.csv",
        start_time,
        end_time,
        0,
        "FAILED",
        str(e)
    )

    print(f"HOLDINGS ingestion failed: {e}")
start_time = datetime.now()

try:

    performance = validate_csv_ingestion(
        RAW_PATH
        / "portfolio_performance"
        / "portfolio_performance.csv",
        PERFORMANCE_COLUMNS,
        "PORTFOLIO_PERFORMANCE"
    )

    end_time = datetime.now()

    logger.log(
        run_id,
        "portfolio_performance",
        "CSV",
        "portfolio_performance.csv",
        start_time,
        end_time,
        len(performance),
        "SUCCESS"
    )

    print(
        f"PERFORMANCE ingestion successful: "
        f"{len(performance)} records"
    )

except Exception as e:

    end_time = datetime.now()

    logger.log(
        run_id,
        "portfolio_performance",
        "CSV",
        "portfolio_performance.csv",
        start_time,
        end_time,
        0,
        "FAILED",
        str(e)
    )

    print(
        f"PERFORMANCE ingestion failed: {e}"
    )
start_time = datetime.now()

try:

    securities = read_security_json(
        RAW_PATH
        / "securities"
        / "securities.json"
    )

    end_time = datetime.now()

    logger.log(
        run_id,
        "securities",
        "JSON",
        "securities.json",
        start_time,
        end_time,
        len(securities),
        "SUCCESS"
    )

    print(
        f"SECURITIES ingestion successful: "
        f"{len(securities)} records"
    )

except Exception as e:

    end_time = datetime.now()

    logger.log(
        run_id,
        "securities",
        "JSON",
        "securities.json",
        start_time,
        end_time,
        0,
        "FAILED",
        str(e)
    )

    print(
        f"SECURITIES ingestion failed: {e}"
    )