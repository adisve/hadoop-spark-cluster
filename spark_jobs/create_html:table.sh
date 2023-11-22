
# Run the script to transfer the data from the spark container to the namenode container in HDFS
docker exec -it spark-master spark-submit --master spark://spark-master:7077 /scripts/read_partial_df.py

if [ $? -ne 0 ]; then
    echo "Error in processing"
    exit 1
fi

echo "Process completed successfully"