import os

from mqtt.mqtt_subscriber import MqttWeatherSubscriber
from logging_config import setup_logging

logging = setup_logging("main")

BROKER_ADDRESS = os.environ.get("BROKER_ADDRESS")
MQTT_TOPIC = os.environ.get("MQTT_TOPIC")

def check_env():
    REQUIRED_ENV_VARS = [
        "BROKER_ADDRESS",
        "MQTT_TOPIC",
        "DOCKER_INFLUXDB_URL",
        "DOCKER_INFLUXDB_INIT_ADMIN_TOKEN",
        "DOCKER_INFLUXDB_INIT_ORG",
        "DOCKER_INFLUXDB_INIT_BUCKET",
    ]

    missing_vars = [
        var for var in REQUIRED_ENV_VARS
        if not os.getenv(var)
    ]

    if missing_vars:
        for var in missing_vars:
            logging.error(f"Missing or empty environment variable: {var}")
        raise Exception("Missing settings configuration. Please see readme or .env file.")


if __name__ == "__main__":
    subscriber = MqttWeatherSubscriber(broker_address=BROKER_ADDRESS, topic=MQTT_TOPIC)
    subscriber.start()
