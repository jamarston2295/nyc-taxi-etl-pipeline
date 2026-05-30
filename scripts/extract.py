# import pandas as pd
# import logging

# logger = logging.getLogger(__name__)


# def extract():

#     logger.info("Starting extract step")

#     df = pd.read_parquet(
#         "/opt/airflow/data/raw/yellow_tripdata_2026-01.parquet"
#     )

#     logger.info(f"Rows extracted: {len(df)}")

#     # Optional: sample down for local development
#     df = df.head(10000)

#     df.to_parquet(
#         "/opt/airflow/data/raw/extracted_data.parquet",
#         index=False
#     )

#     logger.info("Extract complete")

import pandas as pd
import pyarrow.parquet as pq
from utils.logger import get_logger
from utils.config import Config

logger = get_logger(__name__)


def extract():

    logger.info("Starting extract step")

    parquet_file = pq.ParquetFile(
    Config.RAW_DATA_PATH
    )

    # Read only first batch
    first_batch = next(
        parquet_file.iter_batches(
            batch_size=Config.BATCH_SIZE
        )
    )

    df = first_batch.to_pandas()

    logger.info(f"Rows extracted: {len(df)}")

    df.to_parquet(
    Config.EXTRACTED_DATA_PATH,
    index=False
    )

    logger.info("Extract complete")