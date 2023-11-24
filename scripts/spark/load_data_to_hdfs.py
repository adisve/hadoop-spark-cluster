from pyspark.sql import SparkSession
from halo import Halo
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, FloatType, DoubleType, BooleanType, LongType, DateType, TimestampType
import logging
import json
import os

data_type_mapping = {
    "string": StringType(),
    "integer": IntegerType(),
    "float": FloatType(),
    "double": DoubleType(),
    "boolean": BooleanType(),
    "long": LongType(),
    "date": DateType(),
    "timestamp": TimestampType()
}

class DataTransfer:
    """
    Class to transfer data from CSV to HDFS via shared Docker network

    Attributes
    ----------
    schema_file : str
        path to the schema file
    hdfs_path : str
        path to the HDFS directory
    log_directory : str
        path to the log directory
    spark : SparkSession
        Spark session object
    """
    def __init__(self):
        self.schema_file = "/scripts/config/schema.json"
        self.hdfs_path, self.log_directory = self.parse_config_file()
        self.spark = None
        self.setup_logging()

    def setup_logging(self):
        logging.basicConfig(
            filename=f"{self.log_directory}/data_transfer.log",
            level=logging.INFO,
            format="%(asctime)s:%(levelname)s:%(message)s",
        )

    def start_spark_session(self):
        spinner = Halo(text=f"Starting Spark session for data transfer")
        spinner.start()
        logging.info("Starting Spark session for data transfer")
        self.spark = SparkSession.builder.appName("Data transfer to HDFS").getOrCreate()
        spinner.succeed("Spark session started successfully")
        
    def parse_schema_file(self):
        with open(self.schema_file, 'r') as file:
            schema_json = json.load(file)
        fields = [
            StructField(field["name"], data_type_mapping[field["type"].lower()], field.get("nullable", True))
            for field in schema_json
        ]
        return StructType(fields)
    
    def parse_config_file(self):
        with open("/scripts/config/config.json", "r") as file:
            config_json = json.load(file)
        return config_json["hdfs_path"], config_json["log_directory"]

    def get_schema(self):
        return self.parse_schema_file()

    def transfer_data(self):
        try:
            self.start_spark_session()
            schema = self.get_schema()

            logging.info(f"Reading and writing data from /data/output.csv to {self.hdfs_path}")
            spinner = Halo(text=f"Reading and writing data from /data/output.csv to {self.hdfs_path}")
            spinner.start()
            df = (self.spark.read.option("header", "true")
                  .option("mode", "DROPMALFORMED")
                  .option("overwrite", "true")
                  .schema(schema)
                  .csv("/data/output.csv"))

            logging.info(f"Writing data to {self.hdfs_path}")
            df.write.format("parquet").mode("overwrite").save(f"{self.hdfs_path}")
            logging.info("Data transfer completed successfully")
            spinner.succeed("Data transfer completed successfully")

        except IOError as ioe:
            logging.error(f"IO Error: {ioe}", exc_info=True)
            spinner.fail("Data transfer failed. See logs in /scripts/logs/data_transfer.log for details")
        except Exception as e:
            logging.error(f"Unexpected Error: {e}", exc_info=True)
            spinner.fail("Data transfer failed. See logs in /scripts/logs/data_transfer.log for details")
        finally:
            if self.spark:
                self.spark.stop()
                logging.info("Spark session stopped")

if __name__ == "__main__":
    data_transfer = DataTransfer()
    data_transfer.transfer_data()
