import pandas as pd

try:
    from logger import setup_logger
except ImportError:
    from src.logger import setup_logger


logger = setup_logger()


def transform_airports(df):
    try:
        logger.info("Transform started")

        df = df[
            [
                "id",
                "ident",
                "type",
                "name",
                "latitude_deg",
                "longitude_deg",
                "elevation_ft",
                "continent",
                "iso_country",
                "iso_region",
                "municipality",
                "scheduled_service",
                "gps_code",
                "iata_code",
                "local_code",
            ]
        ].copy()

        df.columns = [
            "airport_id",
            "ident",
            "airport_type",
            "airport_name",
            "latitude",
            "longitude",
            "elevation_ft",
            "continent",
            "country_code",
            "region_code",
            "city",
            "scheduled_service",
            "gps_code",
            "iata_code",
            "local_code",
        ]

        df = df.dropna(subset=["latitude", "longitude"])

        text_columns = [
            "ident",
            "airport_type",
            "airport_name",
            "continent",
            "country_code",
            "region_code",
            "city",
            "scheduled_service",
            "gps_code",
            "iata_code",
            "local_code",
        ]

        for col in text_columns:
            df[col] = df[col].fillna("").astype(str).str.strip()

        df["scheduled_service"] = df["scheduled_service"].str.lower()
        df["has_iata_code"] = df["iata_code"] != ""
        df["has_scheduled_service"] = df["scheduled_service"] == "yes"

        valid_types = [
            "small_airport",
            "medium_airport",
            "large_airport",
            "heliport",
            "seaplane_base",
            "closed",
            "balloonport",
        ]

        df = df[df["airport_type"].isin(valid_types)]
        df = df.drop_duplicates(subset=["airport_id"])

        logger.info(f"Transformed {len(df)} rows")
        return df
    except Exception as exc:
        logger.error(f"Transform failed: {exc}")
        raise


if __name__ == "__main__":
    try:
        raw_df = pd.read_csv("data/raw/airports.csv")
        clean_df = transform_airports(raw_df)
        clean_df.to_parquet("data/processed/airports_clean.parquet", index=False)
        logger.info("Parquet file saved successfully")
        print("Saved clean data to data/processed/airports_clean.parquet")
    except FileNotFoundError:
        print("Raw CSV file not found")
        raise
    except Exception as exc:
        print(f"Unexpected error: {exc}")
        raise