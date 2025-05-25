from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StringType, IntegerType, DoubleType

# Create Spark session
spark = SparkSession.builder \
    .appName("WeatherKafkaConsumer") \
    .master("local[*]") \
    .config("spark.sql.streaming.forceDeleteTempCheckpointLocation", "true") \
    .getOrCreate()

# Define schema for the JSON messages
schema = StructType() \
    .add("city", StringType()) \
    .add("timestamp", IntegerType()) \
    .add("clouds", IntegerType()) \
    .add("humidity", IntegerType()) \
    .add("visibility", IntegerType()) \
    .add("score", DoubleType()) \
    .add("summary", StringType())

# Read stream from Kafka topic "weather"
df_raw = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "weather") \
    .option("startingOffsets", "latest") \
    .load()

# Parse the JSON from the Kafka "value" column
df_parsed = df_raw.selectExpr("CAST(value AS STRING) as json") \
    .select(from_json(col("json"), schema).alias("data")) \
    .select("data.*")

query = df_parsed.writeStream \
    .outputMode("append") \
    .format("json") \
    .option("path", "/opt/bitnami/spark/jobs/output") \
    .option("checkpointLocation", "/opt/bitnami/spark/jobs/checkpoints") \
    .trigger(processingTime='60 seconds') \
    .start()


query.awaitTermination()
