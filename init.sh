#!/bin/bash

pipenv install

pipenv shell

make build -C hadoop-spark-cluster

export HADOOP_ARCHITECTURE=$(awk -F '=' '/^HADOOP_ARCHITECTURE/{print $2}' ./hadoop-spark-cluster/hadoop.env)

python3 scripts/setup_cluster.py

if [ $? -ne 0 ]; then
    echo "Error in creating networks and containers"
    exit 1
fi

# Move the comments.csv file to the Hadoop HDFS folder in the namenode container
./spark_jobs/spark-transfer.sh

echo "Process completed successfully"
