# Big Data Project

## Project Description

This project is a part of the Big Data course at the University of HKR. The goal of the project is to create a data pipeline that can be used to analyze the data from [May 2015 Reddit Comments](https://www.kaggle.com/datasets/kaggle/reddit-comments-may-2015/). The data pipeline is created using Apache Spark and the data is stored in HDFS on a Hadoop. The data pipeline is run in a Docker container.

### Prerequisites

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

3. Create the necessary images for the containers:
```sh
make build -C hadoop-spark-cluster
```

4. Export the HADOOP_ARCHITECTURE variable based on the architecture of your machine, stored in the hadoop.env file:
```sh
export HADOOP_ARCHITECTURE=$(awk -F '=' '/^HADOOP_ARCHITECTURE/ {print $2}' ./hadoop-spark-cluster/hadoop.env)
```

5. Create the network and containers:
```sh
python3 scripts/setup_cluster.py
```

6. Move the comments.csv file to the Hadoop HDFS folder in the namenode container using spark:
```sh
./spark_jobs/spark-transfer.sh
```

## Authors

- [Adis Veletanlic](https://github.com/adisve)
- [Dzenis Madzovic](https://github.com/psychicplatypus)
