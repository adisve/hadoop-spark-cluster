# Big Data Project

## Project Description

This project is a part of the Big Data course at the University of HKR. The goal of the project is to create a data pipeline that can be used to analyze the data from [May 2015 Reddit Comments](https://www.kaggle.com/datasets/kaggle/reddit-comments-may-2015/). The data pipeline is created using Apache Spark and the data is stored in HDFS on a Hadoop. The data pipeline is run in a Docker container.

## How to run

### Prerequisites

- database.sqlite file under /data/database.sqlite (not included in the repository due to size)
- Pipenv (for installing dependencies)
- Docker
- Docker Compose

### Steps

1. Clone the repository
2. Create a python virtual environment using `pipenv install`
3. Run the `run.sh` file in the root of the repository
4. The data pipeline will start running and will create all necessary containers as well as a shared network for the containers to communicate with each other.
5. When the data pipeline is done running, the results will be stored in the `results` folder in the root of the repository.

## Authors

- [Adis Veletanlic](https://github.com/adisve)
- [Dzenis Madzovic](https://github.com/psychicplatypus)
