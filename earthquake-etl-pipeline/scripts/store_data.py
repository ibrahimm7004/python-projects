from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("Store Earthquake Data") \
    .getOrCreate()

df = spark.read.option("header", True).csv("data/temp_transformed/")

df.write.mode("overwrite").parquet("data/final_output.parquet")

print("✅ Final data stored at: data/final_output.parquet")
