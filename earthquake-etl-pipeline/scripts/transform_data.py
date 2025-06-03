from pyspark.sql import SparkSession
from pyspark.sql.functions import col, year, month, avg

spark = SparkSession.builder \
    .appName("Earthquake Data Transformation") \
    .getOrCreate()

df = spark.read.option("header", True).option(
    "inferSchema", True).csv("data/earthquake_data.csv")

# --- TRANSFORMATIONS ---

# 1. Filter: Remove records with null or zero magnitude
df_filtered = df.filter((col("mag").isNotNull()) & (col("mag") > 0))

# 2. Extract year and month from timestamp
df_with_time = df_filtered.withColumn("year", year(col("time"))) \
                          .withColumn("month", month(col("time")))

# 3. Group by month and compute average magnitude
df_agg = df_with_time.groupBy("year", "month").agg(
    avg("mag").alias("average_magnitude")
)

df_agg.show()


# Store temp data file because spark dfs don't persist across scripts
df_agg.write.mode("overwrite").option(
    "header", True).csv("data/temp_transformed")

print("✅ Transformation complete: saved to data/temp_transformed/")
