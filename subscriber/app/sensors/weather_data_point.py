from dataclasses import dataclass
from datetime import datetime

@dataclass
class WeatherDataPoint:
    timestamp: datetime
    avg_temperature: float
    avg_humidity: float
