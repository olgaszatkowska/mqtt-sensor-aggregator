import os

from influxdb_client import InfluxDBClient, Point
from dataclasses import dataclass
from typing import Any


@dataclass
class KeyValue:
    key: str
    value: Any


class DataBase:
    def get_client(self) -> InfluxDBClient:
        influxdb_url = os.getenv("DOCKER_INFLUXDB_URL")
        influxdb_token = os.getenv("DOCKER_INFLUXDB_INIT_ADMIN_TOKEN")
        influxdb_org = os.getenv("DOCKER_INFLUXDB_INIT_ORG")

        return InfluxDBClient(url=influxdb_url, token=influxdb_token, org=influxdb_org, timeout=30_000)

    def get_bucket(self) -> str:
        influxdb_bucket = os.getenv("DOCKER_INFLUXDB_INIT_BUCKET")
        return influxdb_bucket

    def write_point(self, point: Point | list[Point]) -> None:
        with self.get_client() as client:
            write_api = client.write_api()
            write_api.write(bucket=self.get_bucket(), record=point)
