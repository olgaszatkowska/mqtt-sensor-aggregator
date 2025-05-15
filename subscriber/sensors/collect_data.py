import os

import adafruit_dht
import board

from datetime import datetime, timezone

from logging_config import setup_logging
from weather_data_point import WeatherDataPoint

logging = setup_logging("collect_data")


class CollectDataService:
    def __init__(self) -> None:
        self.DHT11_SENSOR_1 = adafruit_dht.DHT11(board.D23)
        self.DHT11_SENSOR_2 = adafruit_dht.DHT11(board.D24)

    def collect(self) -> WeatherDataPoint:
        try:
            return self._collect_dht11_data()
        except Exception:
            logging.error("Failed to gather data from dht11 sensor")

    def _collect_dht11_data(self) -> WeatherDataPoint:
        """
        Collect data from air
        """
        current_time = datetime.now(timezone.utc)

        humidity_1, temperature_1 = self.DHT11_SENSOR_1.humidity, self.DHT11_SENSOR_1.temperature 
        humidity_2, temperature_2 = self.DHT11_SENSOR_2.humidity, self.DHT11_SENSOR_2.temperature
        
        average_humidity = (humidity_1+humidity_2)/2
        average_temperature = (temperature_1+temperature_2)/2
        
        logging.info(f"Collected humidity: {float(average_humidity)} and temperature: {float(average_temperature)}")

        return WeatherDataPoint(timestamp=current_time, avg_humidity= average_humidity, avg_temperature=average_temperature)
