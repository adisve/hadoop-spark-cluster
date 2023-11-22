# Run the script to transfer the data from the spark container to the namenode container in HDFS
docker exec -it spark-master spark-submit --master spark://spark-master:7077 /scripts/load_comments_to_hdfs.py # > /dev/null 2>&1

if [ $? -ne 0 ]; then
    echo "Error in processing"
    exit 1
fi

echo "Process completed successfully"