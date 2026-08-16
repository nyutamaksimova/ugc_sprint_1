import logging

import clickhouse_connect
from confluent_kafka import Consumer, Producer
from prometheus_client import start_http_server

from .config import Settings
from .consumer import KafkaConsumerAdapter
from .dlq import DlqPublisher
from .metrics import Metrics
from .repository import ClickHouseRepository
from .worker import EtlWorker


def main() -> None:
    settings = Settings()
    logging.basicConfig(level=logging.INFO)
    consumer = Consumer({
        "bootstrap.servers": settings.kafka_bootstrap_servers,
        "group.id": settings.kafka_group_id,
        "auto.offset.reset": "earliest",
        "enable.auto.commit": False,
    })
    consumer.subscribe(["video-events"])
    client = clickhouse_connect.get_client(host=settings.clickhouse_host, port=settings.clickhouse_port)
    repository = ClickHouseRepository(client)
    repository.ensure_schema()
    Metrics()
    worker = EtlWorker(
        KafkaConsumerAdapter(consumer), repository,
        DlqPublisher(Producer({"bootstrap.servers": settings.kafka_bootstrap_servers})),
        sleep=__import__("time").sleep,
    )
    start_http_server(settings.metrics_port)
    try:
        while True:
            worker.run_once()
    finally:
        consumer.close()
        client.close()


if __name__ == "__main__":
    main()
