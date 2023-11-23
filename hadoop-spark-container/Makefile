DOCKER_NETWORK = docker-hadoop_default
ENV_FILE = hadoop.env
build:
	docker build -t addz/hadoop-base:amd64 ./base
	docker build -t addz/hadoop-namenode:amd64 ./namenode
	docker build -t addz/hadoop-datanode:amd64 ./datanode
	docker build -t addz/hadoop-resourcemanager:amd64 ./resourcemanager
	docker build -t addz/hadoop-nodemanager:amd64 ./nodemanager
	docker build -t addz/hadoop-historyserver:amd64 ./historyserver