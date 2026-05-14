import os
import sqlite3

import pandas as pd

try:
    from logger import setup_logger
except ImportError:
    from src.logger import setup_logger


logger = setup_logger()


def load_airports(df, db_path="metadata/airports.db", table_name="airports"):
    try:
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        with sqlite3.connect(db_path) as connection:
            df.to_sql(table_name, connection, if_exists="replace", index=False)

        logger.info(f"Loaded {len(df)} rows into {db_path}:{table_name}")
        print(f"Loaded {len(df)} rows into {db_path}:{table_name}")
    except Exception as exc:
        logger.error(f"Load failed: {exc}")
        raise


if __name__ == "__main__":
    try:
        clean_df = pd.read_parquet("data/processed/airports_clean.parquet")
        load_airports(clean_df)
    except FileNotFoundError:
        logger.error("Processed parquet file not found")
        raise
    except Exception as exc:
        logger.error(f"Unexpected load error: {exc}")
        raise