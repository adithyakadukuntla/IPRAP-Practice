import os
import pandas as pd
import snowflake.connector
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

BASE_DIR = Path(__file__).parent.parent
CLEAN_DATA_DIR = BASE_DIR / "data" / "cleaned"

CONN_PARAMS = {
    'account': os.getenv('SNOWFLAKE_ACCOUNT'),
    'user': os.getenv('SNOWFLAKE_USER'),
    'password': os.getenv('SNOWFLAKE_PASSWORD'),
    'warehouse': os.getenv('SNOWFLAKE_WAREHOUSE'),
    'database': os.getenv('SNOWFLAKE_DATABASE'),
    'schema': 'STAGING',
    'role': os.getenv('SNOWFLAKE_ROLE')
}

DATASETS = {
    'clients': {'file': 'clients_clean.csv', 'stage_table': 'CLIENT_STAGE'},
    'portfolios': {'file': 'portfolios_clean.csv', 'stage_table': 'PORTFOLIO_STAGE'},
    'securities': {'file': 'securities_clean.csv', 'stage_table': 'SECURITY_STAGE'},
    'holdings': {'file': 'holdings_clean.csv', 'stage_table': 'HOLDING_STAGE'},
    'performance': {'file': 'portfolio_performance_clean.csv', 'stage_table': 'PERFORMANCE_STAGE'}
}

def load_to_stage(dataset_name, config):
    file_path = CLEAN_DATA_DIR / config['file']
    stage_table = config['stage_table']
    
    if not file_path.exists():
        print(f" File not found: {file_path}")
        return False
    
    df = pd.read_csv(file_path)
    print(f" Loading {dataset_name}: {len(df)} records")
    
    conn = snowflake.connector.connect(**CONN_PARAMS)
    cursor = conn.cursor()
    
    cursor.execute(f"TRUNCATE TABLE IPRA_DB.STAGING.{stage_table}")
    
    for _, row in df.iterrows():
        cols = ', '.join(df.columns)
        placeholders = ', '.join(['%s'] * len(row))
        query = f"INSERT INTO IPRA_DB.STAGING.{stage_table} ({cols}) VALUES ({placeholders})"
        cursor.execute(query, list(row))
    
    cursor.close()
    conn.close()
    print(f" Loaded {len(df)} records to STAGING.{stage_table}")
    return True

if __name__ == "__main__":
    print("=" * 50)
    print("Loading Clean Data to Snowflake Staging")
    print("=" * 50)
    
    success = 0
    for dataset_name, config in DATASETS.items():
        if load_to_stage(dataset_name, config):
            success += 1
    
    print(f" {success}/{len(DATASETS)} datasets loaded successfully")
