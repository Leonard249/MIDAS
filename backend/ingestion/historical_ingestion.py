import os
import duckdb
import pandas as pd
from moomoo import *
from dotenv import load_dotenv

load_dotenv("../../.env")

MOOMOOOPEND_ADDRESS = os.getenv("MOOMOOOPEND_ADDRESS", "127.0.0.1")
MOOMOOOPEND_PORT = int(os.getenv("MOOMOOOPEND_PORT", 11111))

def initialize_database() -> str:
    current_dir = os.path.dirname(os.path.abspath(__file__))  # backend/ingestion
    backend_dir = os.path.dirname(current_dir)                 # backend
    data_store_dir = os.path.join(backend_dir, "data_store")   # backend/data_store
    
    os.makedirs(data_store_dir, exist_ok=True)
    db_path = os.path.join(data_store_dir, "midas_market_data.duckdb")
    print(f"Target Database Path: {db_path}")

    # Initialize schema with DuckDB 2.0.0 native storage format
    conn = duckdb.connect(
        db_path, 
        config={"storage_compatibility_version": "v2.0.0"}
    )

    try:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS historical_klines (
                code VARCHAR,
                time_key TIMESTAMP,
                open DOUBLE,
                close DOUBLE,
                high DOUBLE,
                low DOUBLE,
                volume DOUBLE,
                turnover DOUBLE,
                PRIMARY KEY (code, time_key)
            );
        """)
        print("✅ Database schema successfully initialized (DuckDB v2.0.0).")
    finally:
        conn.close()
        
    return db_path

def fetch_and_store_klines(quote_context: OpenQuoteContext, db_conn, security: str, start_date: str, end_date: str):
    """Fetches daily K-lines from Moomoo OpenD and inserts them into DuckDB."""
    print(f"Connecting to Moomoo OpenD for {security} ({start_date} to {end_date})...")
    
    ret, data, page_req_key = quote_context.request_history_kline(
        security, 
        start=start_date, 
        end=end_date, 
        ktype=KLType.K_DAY, 
        autype=AuType.QFQ, 
        max_count=1000
    )
    
    if ret != RET_OK:
        print(f"❌ Moomoo API Error: {data}")
        return False

    if data.empty:
        print("⚠️ Warning: Moomoo returned 0 rows for this date range.")
        return False

    print(f"Fetched {len(data)} candles from Moomoo.")

    # Format DataFrame columns for ingestion
    df = data[['code', 'time_key', 'open', 'close', 'high', 'low', 'volume', 'turnover']].copy()
    df['time_key'] = pd.to_datetime(df['time_key'])
    
    initial_count = db_conn.execute("SELECT COUNT(*) FROM historical_klines").fetchone()[0]

    # Insert DataFrame into DuckDB with duplicate key suppression
    db_conn.execute("""
        INSERT OR IGNORE INTO historical_klines 
        SELECT * FROM df
    """)
    
    final_count = db_conn.execute("SELECT COUNT(*) FROM historical_klines").fetchone()[0]
    inserted_rows = final_count - initial_count
    
    print(f"✅ Insertion Complete: {inserted_rows} new rows added (Skipped {len(df) - inserted_rows} existing duplicates).")
    return True

if __name__ == '__main__':
    # init schema and return db path
    db_path = initialize_database()
    
    # init openD context
    quote_ctx = OpenQuoteContext(host=MOOMOOOPEND_ADDRESS, port=MOOMOOOPEND_PORT)
    
    # Open active DuckDB connection using DuckDB 2.0.0 configuration
    db_connection = duckdb.connect(db_path, config={"storage_compatibility_version": "v2.0.0"})
    
    try:
        target_ticker = 'US.AAPL'
        fetch_and_store_klines(
            quote_context=quote_ctx,
            db_conn=db_connection,
            security=target_ticker,
            start_date='2023-01-01',
            end_date='2023-12-31'
        )
        
        # Verify snapshot
        print("\n--- Current Database Snapshot ---")
        result = db_connection.execute(f"SELECT * FROM historical_klines WHERE code='{target_ticker}' LIMIT 5").df()
        print(result)

    finally:
        quote_ctx.close()
        db_connection.close()
        print("\nContexts closed cleanly.")