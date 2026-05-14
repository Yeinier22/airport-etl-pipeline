import os

try:
    from extract import extract_airports
    from load import load_airports
    from logger import setup_logger
    from transform import transform_airports
except ImportError:
    from src.extract import extract_airports
    from src.load import load_airports
    from src.logger import setup_logger
    from src.transform import transform_airports


RAW_OUTPUT_PATH = "data/raw/airports.csv"
PROCESSED_OUTPUT_PATH = "data/processed/airports_clean.parquet"

logger = setup_logger()


def run_pipeline():
    logger.info("Pipeline execution started")

    os.makedirs("data/raw", exist_ok=True)
    os.makedirs("data/processed", exist_ok=True)
    os.makedirs("metadata", exist_ok=True)

    raw_df = extract_airports()
    clean_df = transform_airports(raw_df)

    clean_df.to_parquet(PROCESSED_OUTPUT_PATH, index=False)
    logger.info(f"Saved clean data to {PROCESSED_OUTPUT_PATH}")

    load_airports(clean_df)

    logger.info("Pipeline execution completed")
    print("Pipeline completed successfully")


if __name__ == "__main__":
    run_pipeline()