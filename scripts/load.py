import pandas as pd
import os
from sqlalchemy import create_engine, text
from datetime import datetime
from utils.logger import get_logger
from utils.config import Config

logger = get_logger(__name__)


def load():

    logger.info("Starting load step")

    # -----------------------------
    # Read processed parquet data
    # -----------------------------

    df = pd.read_parquet(
        Config.PROCESSED_DATA_PATH
    )

    logger.info(f"Rows loaded from parquet: {len(df)}")

    # -----------------------------
    # Add pipeline metadata
    # -----------------------------

    # Add timestamp showing when the pipeline loaded the data
    df["loaded_at"] = datetime.utcnow()

    logger.info("Pipeline metadata column added")

    # -----------------------------
    # Create Postgres connection
    # -----------------------------

    connection_string = (
        f"postgresql+psycopg2://"
        f"{Config.POSTGRES_USER}:"
        f"{Config.POSTGRES_PASSWORD}@"
        f"{Config.POSTGRES_HOST}:"
        f"{Config.POSTGRES_PORT}/"
        f"{Config.POSTGRES_DB}"
    )

    engine = create_engine(connection_string)

    logger.info("Connected to Postgres")

    # -----------------------------
    # Optional: create schema
    # -----------------------------

    with engine.begin() as connection:

        connection.execute(text("""
            CREATE TABLE IF NOT EXISTS taxi_trips (
                "VendorID" FLOAT,
                passenger_count FLOAT,
                trip_distance FLOAT,
                fare_amount FLOAT,
                total_amount FLOAT,
                trip_duration_minutes FLOAT,
                average_speed_mph FLOAT,
                pickup_hour INTEGER,
                pickup_day_name TEXT,
                is_weekend BOOLEAN,
                trip_category TEXT,
                loaded_at TIMESTAMP
            )
        """))

    logger.info("Verified taxi_trips table exists")

    # -----------------------------
    # Load data into Postgres
    # -----------------------------

    df.to_sql(
        name="taxi_trips",
        con=engine,
        if_exists="append",
        index=False,
        method="multi",
        chunksize=5000
    )

    logger.info("Data successfully loaded to Postgres")

    logger.info("Load step completed successfully")