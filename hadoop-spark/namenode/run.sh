#!/bin/bash

namedir=`echo $HDFS_CONF_dfs_namenode_name_dir | perl -pe 's#file://##'`
if [ ! -d $namedir ]; then
  echo "Namenode name directory not found: $namedir"
  exit 2
fi

if [ -z "$CLUSTER_NAME" ]; then
  echo "Cluster name not specified"
  exit 2
fi

echo "remove lost+found from $namedir"
rm -rf $namedir/lost+found

if [ "`ls -A $namedir`" == "" ]; then
  echo "Formatting namenode name directory: $namedir"
  $HADOOP_HOME/bin/hdfs --config $HADOOP_CONF_DIR namenode -format $CLUSTER_NAME
fi

$HADOOP_HOME/bin/hdfs --config $HADOOP_CONF_DIR namenode &

# Wait for Namenode to start
echo "Waiting for Namenode to start..."
sleep 10

# Create the HDFS directory
echo "Creating /user/spark/reddit_comments directory in HDFS..."
$HADOOP_HOME/bin/hdfs dfs -mkdir -p /user/spark/reddit_comments

# Change the ownership to the 'spark' user
echo "Changing ownership of /user/spark/reddit_comments to spark:spark"
$HADOOP_HOME/bin/hdfs dfs -chown spark:spark /user/spark/reddit_comments

wait
