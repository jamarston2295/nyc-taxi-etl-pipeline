import pandas as pd

from scripts.transform import transform_dataframe


def test_negative_durations_removed():

    df = pd.DataFrame(
        {
            "tpep_pickup_datetime": [
                "2024-01-01 10:00:00"
            ],
            "tpep_dropoff_datetime": [
                "2024-01-01 09:00:00"
            ],
            "trip_distance": [5],
            "fare_amount": [10],
            "total_amount": [12],
            "VendorID": [1],
            "passenger_count": [1]
        }
    )

    result = transform_dataframe(df)

    assert len(result) == 0

def test_trip_duration_calculated():

    df = pd.DataFrame({
        "tpep_pickup_datetime": ["2024-01-01 10:00:00"],
        "tpep_dropoff_datetime": ["2024-01-01 10:30:00"],
        "trip_distance": [5],
        "fare_amount": [10],
        "total_amount": [12],
        "VendorID": [1],
        "passenger_count": [1]
    })

    result = transform_dataframe(df)

    assert result.iloc[0]["trip_duration_minutes"] == 30

def test_trip_category_short():

    df = pd.DataFrame({
        "tpep_pickup_datetime": ["2024-01-01 10:00:00"],
        "tpep_dropoff_datetime": ["2024-01-01 10:30:00"],
        "trip_distance": [1],
        "fare_amount": [10],
        "total_amount": [12],
        "VendorID": [1],
        "passenger_count": [1]
    })

    result = transform_dataframe(df)

    assert result.iloc[0]["trip_category"] == "short"