#!/bin/bash

python py_injector/create.py

if [ $? -ne 0 ]; then
    echo "Error in creating networks and containers"
    exit 1
fi

echo "Waiting for namenode container to become healthy..."
while true; do
    health_status=$(docker inspect --format='{{json .State.Health.Status}}' namenode)
    if [ "$health_status" == "\"healthy\"" ]; then
        echo "namenode is healthy."
        break
    else
        echo "namenode status: $health_status. Waiting..."
        sleep 10
    fi
done

docker exec -it namenode hdfs dfs -mkdir -p /user/spark
docker exec -it namenode hdfs dfs -chown spark:spark /user/spark
docker exec -it namenode hdfs dfs -mkdir -p /user/spark/reddit_comments
docker exec -it namenode hdfs dfs -chown spark:spark /user/spark/reddit_comments
docker exec -it namenode hdfs dfs -mkdir -p /tmp

python ./py_injector/process.py

docker cp ./data/output.csv namenode:/tmp/output.csv

docker exec -it namenode hdfs dfs -put /tmp/output.csv /user/spark/reddit_comments > /dev/null

if [ $? -ne 0 ]; then
    echo "Error in processing"
    exit 1
fi

echo "Process completed successfully"