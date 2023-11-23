#!/bin/bash

make build -C hadoop-spark-cluster && python3 scripts/setup_cluster.py

if [ $? -ne 0 ]; then
    echo "Error in creating networks and containers"
    exit 1
fi

echo "Process completed successfully"