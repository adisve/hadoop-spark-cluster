DOCKER_NETWORK = docker-hadoop_default
ENV_FILE = hadoop.env
HADOOP_VERSION = 3.3.6
HADOOP_ARCHITECTURE = 3.3.6
JVM_ARCHITECTURE := $(shell uname -m)

ifeq ($(JVM_ARCHITECTURE),x86_64)
    JVM_ARCHITECTURE := amd64
endif

ifeq ($(JVM_ARCHITECTURE),arm64)
    JVM_ARCHITECTURE := arm64
    HADOOP_ARCHITECTURE := 3.3.6-aarch64
endif

build-env:
	@echo "" >> $(ENV_FILE)
	@if grep -q 'HADOOP_ARCHITECTURE=' $(ENV_FILE); then \
		sed -i'.bak' -e 's/^HADOOP_ARCHITECTURE=.*/HADOOP_ARCHITECTURE=$(HADOOP_ARCHITECTURE)/' $(ENV_FILE) && rm -f $(ENV_FILE).bak; \
	else \
		echo "HADOOP_ARCHITECTURE=$(HADOOP_ARCHITECTURE)" >> $(ENV_FILE); \
	fi

build: build-env
	docker build --build-arg JVM_ARCHITECTURE=$(JVM_ARCHITECTURE) --build-arg HADOOP_VERSION=$(HADOOP_VERSION) --build-arg HADOOP_ARCHITECTURE=$(HADOOP_ARCHITECTURE) --build-arg NAMENODE_DATA_DIR=reddit_comments -t addz/hadoop-base:$(HADOOP_ARCHITECTURE) ./base
	docker build --build-arg HADOOP_ARCHITECTURE=$(HADOOP_ARCHITECTURE) -t addz/hadoop-namenode:$(HADOOP_ARCHITECTURE) ./namenode
	docker build --build-arg HADOOP_ARCHITECTURE=$(HADOOP_ARCHITECTURE) -t addz/hadoop-datanode:$(HADOOP_ARCHITECTURE) ./datanode
	docker build --build-arg HADOOP_ARCHITECTURE=$(HADOOP_ARCHITECTURE) -t addz/hadoop-resourcemanager:$(HADOOP_ARCHITECTURE) ./resourcemanager
	docker build --build-arg HADOOP_ARCHITECTURE=$(HADOOP_ARCHITECTURE) -t addz/hadoop-nodemanager:$(HADOOP_ARCHITECTURE) ./nodemanager
	docker build --build-arg HADOOP_ARCHITECTURE=$(HADOOP_ARCHITECTURE) -t addz/hadoop-historyserver:$(HADOOP_ARCHITECTURE) ./historyserver
