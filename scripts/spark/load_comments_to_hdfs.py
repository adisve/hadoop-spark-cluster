from pyspark.sql import SparkSession
from halo import Halo
from pyspark.sql.types import StructType, StructField, StringType, IntegerType
import logging
import os
import getpass


def setup_logging():
    log_directory = "/scripts/logs"
    logging.basicConfig(
        filename=f'{log_directory}/data_transfer.log',
        level=logging.INFO,
        format='%(asctime)s:%(levelname)s:%(message)s'
    )


def transfer_data_to_namenode():
    print("Running as user:", getpass.getuser())


    hdfs_path = 'hdfs://namenode:9000/user/spark/reddit_comments/'
    spark = None
    try:
        spinner = Halo(text=f'Starting Spark session for data transfer')
        logging.info("Starting Spark session for data transfer")
        spark = SparkSession.builder \
            .appName('Data transfer to HDFS') \
            .getOrCreate()
        spinner.succeed("Spark session started successfully")

        schema = StructType([
            StructField("created_utc", IntegerType(), True),
            StructField("ups", IntegerType(), True),
            StructField("subreddit_id", StringType(), True),
            StructField("link_id", StringType(), True),
            StructField("name", StringType(), True),
            StructField("score_hidden", StringType(), True),
            StructField("author_flair_css_class", StringType(), True),
            StructField("author_flair_text", StringType(), True),
            StructField("subreddit", StringType(), True),
            StructField("id", StringType(), True),
            StructField("removal_reason", StringType(), True),
            StructField("gilded", IntegerType(), True),
            StructField("downs", IntegerType(), True),
            StructField("archived", StringType(), True),
            StructField("author", StringType(), True),
            StructField("score", IntegerType(), True),
            StructField("retrieved_on", IntegerType(), True),
            StructField("body", StringType(), True),
            StructField("distinguished", StringType(), True),
            StructField("edited", StringType(), True),
            StructField("controversiality", IntegerType(), True),
            StructField("parent_id", StringType(), True)
        ])

        logging.info(f"Reading and writing data from /data/comments.csv to {hdfs_path}")
        spinner = Halo(text=f"Reading and writing data from /data/comments.csv to {hdfs_path}")
        df = spark.read \
            .option('header', 'true') \
            .option('mode', 'DROPMALFORMED') \
            .schema(schema) \
            .csv('/data/comments.csv')

        logging.info(f"Writing data to {hdfs_path}")
        df.write \
            .format('json') \
            .mode('overwrite') \
            .save(f'{hdfs_path}')
        logging.info("Data transfer completed successfully")
        spinner.succeed("Data transfer completed successfully")

    except IOError as ioe:
        logging.error(f'IO Error: {ioe}', exc_info=True)
    except Exception as e:
        logging.error(f'Unexpected Error: {e}', exc_info=True)
    finally:
        spinner.fail("Data transfer failed. See logs in /scripts/logs/data_transfer.log for details")
        if spark:
            spark.stop()
            logging.info("Spark session stopped")


if __name__ == '__main__':
    setup_logging()
    transfer_data_to_namenode()
