FROM bitnami/spark:latest

USER root

RUN apt-get update && apt-get upgrade

RUN python -m pip install --upgrade pip && pip install pyspark halo pandas

RUN mkdir -p /scripts
RUN mkdir -p /scripts/logs

RUN chmod -R 777 /scripts
