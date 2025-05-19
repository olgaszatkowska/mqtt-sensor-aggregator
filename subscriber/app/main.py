import os
import time
from datetime import datetime
from statistics import mean

from sensors.collect_data import CollectDataService
from sensors.weather_data_point import WeatherDataPoint
from mqtt.publish import PublishDataService
from logging_config import setup_logging

logging = setup_logging("main")


DATA_PUBLISH_INTERVAL_SECONDS = os.environ.get("DATA_PUBLISH_INTERVAL_SECONDS")
DATA_COLLECT_INTERVAL_SECONDS = os.environ.get("DATA_COLLECT_INTERVAL_SECONDS")
BROKER_ADDRESS = os.environ.get("BROKER_ADDRESS")
MQTT_TOPIC = os.environ.get("MQTT_TOPIC")

def check_env():
    env = [
        DATA_PUBLISH_INTERVAL_SECONDS,
        DATA_COLLECT_INTERVAL_SECONDS,
        BROKER_ADDRESS,
        MQTT_TOPIC
    ]
    if '' in env:
        logging.error("Missing settings configuration. Please see readme.")
        raise Exception("Missing settings configuration. Please see readme.")


def average_data(points: list[WeatherDataPoint]) -> WeatherDataPoint:
    avg_temp = mean(p.avg_temperature for p in points)
    avg_humidity = mean(p.avg_humidity for p in points)
    timestamp = datetime.now()

    return WeatherDataPoint(
        timestamp=timestamp,
        avg_temperature=avg_temp,
        avg_humidity=avg_humidity,
    )


def main():
    logging.info("App started")

    collect_service = CollectDataService()
    publish_service = PublishDataService(broker_address=BROKER_ADDRESS)

    collected_data: list[WeatherDataPoint] = []

    last_collect_time = time.time()
    last_publish_time = time.time()

    while True:
        now = time.time()

        if now - last_collect_time >= float(DATA_COLLECT_INTERVAL_SECONDS):
            point = collect_service.collect()
            collected_data.append(point)
            logging.debug(f"Collected data: {point}")
            last_collect_time = now

        if now - last_publish_time >= float(DATA_PUBLISH_INTERVAL_SECONDS):
            if collected_data:
                averaged_point = average_data(collected_data)
                publish_service.publish(topic=MQTT_TOPIC, data_point=averaged_point)
                logging.info(f"Published averaged data from {len(collected_data)} samples")

                collected_data.clear()
            last_publish_time = now

        time.sleep(0.5)

if __name__ == "__main__":
    check_env()
    main()
