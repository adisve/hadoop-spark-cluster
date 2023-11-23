#!/bin/bash

namedir=$(echo $HDFS_CONF_dfs_namenode_name_dir | perl -pe 's#file://##')
if [ ! -d "$namedir" ]; then
  echo "Namenode name directory not found: $namedir"
  exit 2
fi

if [ -z "$CLUSTER_NAME" ]; then
  echo "Cluster name not specified"
  exit 2
fi

if [ -z "$(ls -A $namedir)" ]; then
  echo "Formatting namenode name directory: $namedir"
  $HADOOP_HOME/bin/hdfs --config $HADOOP_CONF_DIR namenode -format $CLUSTER_NAME
fi

$HADOOP_HOME/bin/hdfs --config $HADOOP_CONF_DIR namenode &

echo "Waiting for Namenode to start..."
while ! nc -z localhost 9870; do   
  sleep 5
done
echo "Namenode started."

# Create directories and set permissions
echo "Creating /user/spark/reddit_comments and setting permissions..."
hdfs dfs -mkdir -p /user/spark/reddit_comments
hdfs dfs -chown -R spark:spark /user/spark
hdfs dfs -chmod -R 770 /user/spark
hdfs dfs -setfacl -R -m user:dr.who:r-x /user/spark

wait
