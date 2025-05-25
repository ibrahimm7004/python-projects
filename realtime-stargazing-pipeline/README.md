# 🌌 Real-Time Stargazing Suitability Tracker

This project is a real-time data pipeline built with **Apache Kafka**, **Apache Spark**, and **Python** to help users determine the best stargazing conditions based on their current location and nearby cities. It collects weather-related data using the OpenWeatherMap API, streams it through Kafka, and processes it using Spark Structured Streaming.

---

## 📁 Project Structure

```
project/
│
├── kafka/
│   ├── docker-compose.yml         # Kafka + Zookeeper + Spark services
│   ├── weather_producer.py        # Python Kafka producer for weather data
│
├── spark/
│   ├── Dockerfile                 # Custom Spark image with Kafka connectors
│   └── spark_consumer.py          # Spark Structured Streaming consumer
│
├── data/                          # Folder for processed data output
│   └── weather_output.json        # (example) Spark JSON sink output
│
├── scripts/                       # Placeholder for helper scripts
├── tests/                         # Jupyter notebooks and reports
│
├── README.md                      # Project readme and setup guide
├── requirements.txt               # Python dependencies
└── ...
```

---

## ⚙️ Requirements

- Docker
- Docker Compose
- Python 3.9+
- Internet access (for OpenWeatherMap API)
- OpenWeatherMap API Key (free from https://openweathermap.org/api)

---

## 🚀 Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/stargazing-pipeline.git
cd stargazing-pipeline
```

### 2. Get your OpenWeatherMap API key

- Sign up at https://openweathermap.org/api
- Generate a One Call API key (v3.0)
- Update `weather_producer.py` with your API key:

```python
API_KEY = "example"
```

---

## 🐳 Step-by-Step Docker Workflow

### 3. Start Kafka, Zookeeper, and Spark

From inside the `/kafka` directory:

```bash
cd kafka
docker-compose up -d
```

### 4. Create Kafka Topic

```bash
docker exec -it <kafka_container_id> kafka-topics.sh --create --topic weather --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
```

You can get the Kafka container ID using:

```bash
docker ps --filter "name=kafka"
```

---

### 5. Start the Spark Streaming Consumer

```bash
docker logs -f <spark_container_id>
```

> It should show streaming logs with parsed weather data.

---

### 6. Start the Weather Producer

In a new terminal:

```bash
cd kafka
python weather_producer.py
```

---

## 🧪 Output Example

Sample row printed by Spark Consumer:

```json
{
  "city": "Lahore",
  "timestamp": 1748102067,
  "clouds": 75,
  "humidity": 78,
  "visibility": 4000,
  "score": 0.022,
  "summary": "broken clouds"
}
```

---

## 📂 Output Storage

By default, Spark can also write the stream to a file in `/data/` directory as `weather_output.json` every 60 seconds.

---

## 📄 License & Citations

See `academic_integrity.md` for details on licenses, library references, and API usage.

---
