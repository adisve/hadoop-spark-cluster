from pyspark.sql import SparkSession
from utils.html_utils import dataframe_to_html_with_css

spark = SparkSession.builder \
    .appName("Reddit Comments Analysis") \
    .getOrCreate()

df = spark.read.parquet('hdfs://namenode:9000/user/spark/reddit_comments/')

sampled_df = df.sample(fraction=0.1).limit(20)

pandas_df = sampled_df.toPandas()

html_data_with_css = dataframe_to_html_with_css(pandas_df)

output_path = "/mnt/data/reddit_comments.html"

# Write the HTML data to the file
with open(output_path, 'w') as f:
    f.write(html_data_with_css)
