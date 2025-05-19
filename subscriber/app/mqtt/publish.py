import json
import paho.mqtt.client as mqtt

from sensors.weather_data_point import WeatherDataPoint
from logging_config import setup_logging

logging = setup_logging("publish")


class PublishDataService:
    def __init__(self, broker_address: str):
        self.broker_address = broker_address
        self.client = mqtt.Client()
        self.failed_uploads = []

    def publish(self, topic: str, data_point: WeatherDataPoint) -> None:
        data_dict = {
            "timestamp": data_point.timestamp.isoformat(),
            "avg_temperature": data_point.avg_temperature,
            "avg_humidity": data_point.avg_humidity,
        }

        json_data = json.dumps(data_dict)

        try:
            self.client.connect(self.broker_address)
        except Exception as e:
            logging.error("Failed to connect to broker, aborting")
            self.failed_uploads.append(json_data)
            return

        self.client.publish(topic, json_data)

        if len(self.failed_uploads):
            for upload in self.failed_uploads:
                self.client.publish(upload, json_data)

            self.failed_uploads = []

        self.client.disconnect()

        logging.info(f"Successfully published to {topic} at {self.broker_address}")
