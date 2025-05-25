FROM bitnami/spark:3.4.1

USER root

# 👇 Install Python + pip + wget
RUN apt-get update && apt-get install -y python3 python3-pip wget

# 👇 Add Kafka connector jars
ENV SPARK_EXTRA_CLASSPATH=/opt/bitnami/spark/jars
RUN wget https://repo1.maven.org/maven2/org/apache/spark/spark-sql-kafka-0-10_2.12/3.4.1/spark-sql-kafka-0-10_2.12-3.4.1.jar -P /opt/bitnami/spark/jars && \
    wget https://repo1.maven.org/maven2/org/apache/kafka/kafka-clients/3.4.0/kafka-clients-3.4.0.jar -P /opt/bitnami/spark/jars && \
    wget https://repo1.maven.org/maven2/org/apache/spark/spark-token-provider-kafka-0-10_2.12/3.4.1/spark-token-provider-kafka-0-10_2.12-3.4.1.jar -P /opt/bitnami/spark/jars


# 👇 Install Kafka Python client
RUN pip3 install kafka-python

# 👇 Copy your job file
COPY spark_consumer.py /opt/bitnami/spark/jobs/spark_consumer.py

RUN mkdir -p /opt/bitnami/spark/jobs/output /opt/bitnami/spark/jobs/checkpoints

# 👇 Revert back to non-root user
USER 1001
