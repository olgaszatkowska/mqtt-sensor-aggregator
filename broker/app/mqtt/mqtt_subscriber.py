import json
from typing import Any, Dict
import paho.mqtt.client as mqtt
from influxdb_client import Point

from broker.app.database.databse import DataBase
from logging_config import setup_logging

logging = setup_logging("mqtt_subscriber")


class MqttWeatherSubscriber:
    def __init__(self, broker_address: str, topic: str = "weather") -> None:
        self.broker_address = broker_address
        self.topic = topic
        self.client = mqtt.Client()
        self.db = DataBase()

        # Register callbacks
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def on_connect(self, client: mqtt.Client, userdata: Any, flags: Dict[str, Any], rc: int) -> None:
        if rc == 0:
            logging.info("Connected successfully to broker.")
            client.subscribe(self.topic)
        else:
            logging.error(f"Connection failed with code {rc}")

    def on_message(self, client: mqtt.Client, userdata: Any, msg: mqtt.MQTTMessage) -> None:
        try:
            data: Dict[str, Any] = json.loads(msg.payload.decode())
            logging.debug(f"Received data on topic '{msg.topic}': {data}")
            self.save_to_influx(data)
        except Exception as e:
            logging.exception(f"Error processing message: {e}")

    def save_to_influx(self, data: Dict[str, Any]) -> None:
        try:
            point = (
                Point("weather_data")
                .field("avg_temperature", float(data["avg_temperature"]))
                .field("avg_humidity", float(data["avg_humidity"]))
                .time(data["timestamp"])
            )
            self.db.write_point(point)
            logging.info("Data point written to InfluxDB.")
        except Exception as e:
            logging.exception(f"Error saving to InfluxDB: {e}")

    def start(self) -> None:
        try:
            logging.info(f"Connecting to MQTT broker at {self.broker_address}...")
            self.client.connect(self.broker_address, 1883, 60)
            self.client.loop_forever()
        except Exception as e:
            logging.exception(f"Error starting subscriber: {e}")
