FROM bde2020/hadoop-namenode:2.0.0-hadoop3.2.1-java8

ENV HDFS_CONF_dfs_namenode_name_dir=file:///hadoop/dfs/name
RUN mkdir -p /hadoop/dfs/name
VOLUME /hadoop/dfs/name

COPY ./config/hdfs-site.xml /etc/hadoop/

CMD ["/run.sh"]