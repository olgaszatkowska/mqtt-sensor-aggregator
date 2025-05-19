import os

from mqtt.mqtt_subscriber import MqttWeatherSubscriber
from logging_config import setup_logging

logging = setup_logging("main")

BROKER_ADDRESS = os.environ.get("BROKER_ADDRESS")
MQTT_TOPIC = os.environ.get("MQTT_TOPIC")

def check_env():
    if not (
        BROKER_ADDRESS,
        MQTT_TOPIC
    ):
        logging.error("Missing settings configuration. Please see readme.")
        raise Exception("Missing settings configuration. Please see readme.")


if __name__ == "__main__":
    subscriber = MqttWeatherSubscriber(broker_address=BROKER_ADDRESS, topic=MQTT_TOPIC)
    subscriber.start()
