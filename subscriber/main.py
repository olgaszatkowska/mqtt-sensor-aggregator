import os
from datetime import datetime

from sensors.collect_data import CollectDataService
from mqtt.publish import PublishDataService
from logging_config import setup_logging

logging = setup_logging("main")


DATA_PUBLISH_INTERVAL_SECONDS = os.environ.get("DATA_PUBLISH_INTERVAL_SECONDS")
BROKER_ADDRESS = os.environ.get("BROKER_ADDRESS")
MQTT_TOPIC = os.environ.get("MQTT_TOPIC")

def check_env():
    if not (
        DATA_PUBLISH_INTERVAL_SECONDS,
        BROKER_ADDRESS,
        MQTT_TOPIC
    ):
        logging.error("Missing settings configuration. Please see readme.")
        raise Exception("Missing settings configuration. Please see readme.")


def main():
    logging.info(f"App start")

    data_publish_interval = int(DATA_PUBLISH_INTERVAL_SECONDS)
    collect_service = CollectDataService()
    publish_service = PublishDataService(broker_address=BROKER_ADDRESS)

    last_save_time = datetime.now()

    while True:
        current_time = datetime.now()

        data_save_time_difference = current_time - last_save_time
        time_to_publish = (
            data_save_time_difference.total_seconds() > data_publish_interval
        )
        if time_to_publish:
            point = collect_service.collect()

            publish_service.publish(topic=MQTT_TOPIC, data_point=point)

            last_save_time = datetime.now()

if __name__ == "__main__":
    check_env()
    main()
