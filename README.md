# Hadoop Spark Cluster - Analyzing big data

## Project Description

This project aims to develop a versatile data pipeline capable of processing datasets large in size, utilizing Docker containers and Hadoop + Spark.

## About

For our practical implementation, we selected the [May 2015 Reddit Comments Dataset](https://www.kaggle.com/datasets/kaggle/reddit-comments-may-2015/) available on Kaggle. However, the pipeline's flexibility allows for the incorporation of various datasets. This adaptability is achieved by adjusting the NAMENODE_DATA_DIR variable in the ./hadoop-spark-cluster/Makefile and setting the namenode HDFS URL in scripts/spark/config.json.

Leveraging Apache Spark for data processing and HDFS on a Hadoop cluster for data storage, each node operates within its own container, ensuring efficient data handling.

The pipeline is designed to generate an output.csv file (prior to uploading it in parts as Parquet parts to the virtual HDFS container), located in the /data directory at the project's root. Should you opt to use the SQLite database from the provided link, a handy conversion script scripts/utils/csv_converter.py is available to convert the data from SQLite to CSV format before running the initialization script.

## Prerequisites

- A comments.csv file under /data/output.csv (not included in the repository due to size), which can be downloaded from [May 2015 Reddit Comments](https://www.kaggle.com/datasets/kaggle/reddit-comments-may-2015/) and then manually parsed to a csv file with the helper script csv_converter.py under scripts/.
- Pipenv (for installing dependencies)
- Docker
- Docker Compose

## How to run

1. Create a python virtual environment

    ```sh
    pipenv install
    ```

2. Source the virtual environment

    ```sh
    pipenv shell
    ```

3. If necessary, exit safe mode in the namenode container with

    ```sh
    docker exec -it namenode hdfs dfsadmin -safemode leave
    ```

4. Run the 'init.sh' script to move the output.csv file to HDFS as Parquet parts

    ```sh
    chmod +x init.sh
    ./init.sh
    ```

## Authors

- [Adis Veletanlic](https://github.com/adisve)
- [Dzenis Madzovic](https://github.com/psychicplatypus)
