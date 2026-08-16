from dataclasses import dataclass
import os


@dataclass(frozen=True)
class Settings:
    kafka_bootstrap_servers: str = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
    kafka_group_id: str = os.getenv("KAFKA_GROUP_ID", "analytics-etl")
    clickhouse_host: str = os.getenv("CLICKHOUSE_HOST", "clickhouse")
    clickhouse_port: int = int(os.getenv("CLICKHOUSE_PORT", "8123"))
    metrics_port: int = int(os.getenv("METRICS_PORT", "8002"))
