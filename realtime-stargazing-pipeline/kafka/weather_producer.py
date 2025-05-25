from kafka import KafkaProducer
import json
import requests
import time

API_KEY = ""
LAT, LON = 31.5204, 74.3587
CITY = "Lahore"
KAFKA_TOPIC = "weather"
KAFKA_BROKER = "127.0.0.1:9092"

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)


def get_weather_data():
    url = f"https://api.openweathermap.org/data/3.0/onecall?lat={LAT}&lon={LON}&exclude=minutely,daily,alerts&units=metric&appid={API_KEY}"
    response = requests.get(url)
    if response.status_code != 200:
        print("❌ API Error:", response.status_code)
        return None

    current = response.json()["current"]
    score = (1 - current["clouds"]/100) * (1 -
                                           current["humidity"]/100) * (current["visibility"]/10000)
    return {
        "city": CITY,
        "timestamp": current["dt"],
        "clouds": current["clouds"],
        "humidity": current["humidity"],
        "visibility": current["visibility"],
        "score": round(score, 3),
        "summary": current["weather"][0]["description"]
    }


if __name__ == "__main__":
    while True:
        weather_data = get_weather_data()
        if weather_data:
            producer.send(KAFKA_TOPIC, weather_data)
            print(f"✅ Sent to Kafka: {weather_data}")
        time.sleep(10)
