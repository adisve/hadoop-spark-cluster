# Big Data Project

## Project Description

This project is a part of the Big Data course at the University of HKR. The goal of the project is to create a data pipeline that can be used to analyze the data from [May 2015 Reddit Comments](https://www.kaggle.com/datasets/kaggle/reddit-comments-may-2015/). The data pipeline is created using Apache Spark and the data is stored in HDFS on a Hadoop. The data pipeline is run in a Docker container.

### Prerequisites

- A comments.csv file under /data/output.csv (not included in the repository due to size), which can be downloaded from [May 2015 Reddit Comments](https://www.kaggle.com/datasets/kaggle/reddit-comments-may-2015/) and then manually parsed to a csv file with the helper script csv_converter.py under scripts/.
- Pipenv (for installing dependencies)
- Docker
- Docker Compose

## How to run

1. Create a python virtual environment
```sh
pipenv install
```

2. Source the virtual environment
```sh
pipenv shell
```

3. Run the 'init.sh' script to move the output.csv file to HDFS as Parquet parts
```sh
chmod +x init.sh
./init.sh
```

## Authors

- [Adis Veletanlic](https://github.com/adisve)
- [Dzenis Madzovic](https://github.com/psychicplatypus)
