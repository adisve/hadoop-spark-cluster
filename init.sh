#!/bin/bash

# Run creation script to create the network and containers on local machine
python3 scripts/create_containers.py

if [ $? -ne 0 ]; then
    echo "Error in creating networks and containers"
    exit 1
fi

echo "Process completed successfully"