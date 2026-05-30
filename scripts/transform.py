import pandas as pd
from utils.logger import get_logger
from utils.config import Config

logger = get_logger(__name__)

def transform_dataframe(df):

    logger.info(f"Initial row count: {len(df)}")

    # -----------------------------
    # Data Quality Checks
    # -----------------------------

    df = df.dropna(
        subset=[
            "tpep_pickup_datetime",
            "tpep_dropoff_datetime",
            "trip_distance",
            "fare_amount"
        ]
    )

    logger.info(f"Row count after null removal: {len(df)}")

    # -----------------------------
    # Datetime Transformations
    # -----------------------------

    df["tpep_pickup_datetime"] = pd.to_datetime(
        df["tpep_pickup_datetime"]
    )

    df["tpep_dropoff_datetime"] = pd.to_datetime(
        df["tpep_dropoff_datetime"]
    )

    df["trip_duration_minutes"] = (
        (
            df["tpep_dropoff_datetime"]
            - df["tpep_pickup_datetime"]
        ).dt.total_seconds()
        / 60
    )

    # -----------------------------
    # Remove Invalid Records
    # -----------------------------

    df = df[df["trip_duration_minutes"] > 0]

    df = df[df["trip_distance"] > 0]

    df = df[df["fare_amount"] >= 0]

    logger.info(f"Row count after validation: {len(df)}")

    # -----------------------------
    # Feature Engineering
    # -----------------------------

    df["average_speed_mph"] = (
        df["trip_distance"]
        / (df["trip_duration_minutes"] / 60)
    )

    df["pickup_hour"] = (
        df["tpep_pickup_datetime"].dt.hour
    )

    df["pickup_day_name"] = (
        df["tpep_pickup_datetime"].dt.day_name()
    )

    df["is_weekend"] = (
        df["pickup_day_name"]
        .isin(["Saturday", "Sunday"])
    )

    df["trip_category"] = df["trip_distance"].apply(
        lambda x: (
            "short"
            if x < 2
            else "medium"
            if x < 10
            else "long"
        )
    )

    logger.info("Feature engineering complete")

    # -----------------------------
    # Select Final Columns
    # -----------------------------

    final_columns = [
        "VendorID",
        "passenger_count",
        "trip_distance",
        "fare_amount",
        "total_amount",
        "trip_duration_minutes",
        "average_speed_mph",
        "pickup_hour",
        "pickup_day_name",
        "is_weekend",
        "trip_category"
    ]

    df = df[final_columns]

    logger.info(f"Final dataset row count: {len(df)}")

    return df


def transform():

    logger.info("Starting transform step")

    df = pd.read_parquet(
        Config.EXTRACTED_DATA_PATH
    )

    transformed_df = transform_dataframe(df)

    # -----------------------------
    # Validation Checks
    # -----------------------------

    assert len(transformed_df) > 0, (
        "No data found after transformation"
    )

    assert (
        transformed_df["trip_duration_minutes"] > 0
    ).all(), (
        "Invalid trip durations detected"
    )

    # -----------------------------
    # Save Processed Data
    # -----------------------------

    transformed_df.to_parquet(
        Config.PROCESSED_DATA_PATH,
        index=False
    )

    logger.info(
        f"Processed data saved to: "
        f"{Config.PROCESSED_DATA_PATH}"
    )

    logger.info(
        "Transform step completed successfully"
    )