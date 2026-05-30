import os

class Config:

    POSTGRES_USER = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_DB = os.getenv("POSTGRES_DB")
    POSTGRES_HOST = os.getenv("POSTGRES_HOST")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT")

    RAW_DATA_PATH = os.getenv("RAW_DATA_PATH")
    EXTRACTED_DATA_PATH = os.getenv("EXTRACTED_DATA_PATH")
    PROCESSED_DATA_PATH = os.getenv("PROCESSED_DATA_PATH")

    BATCH_SIZE = int(os.getenv("BATCH_SIZE", 50000))