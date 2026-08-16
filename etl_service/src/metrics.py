import os

import psutil
from prometheus_client import CollectorRegistry, Counter, Gauge, Histogram


class Metrics:
    def __init__(self, registry: CollectorRegistry | None = None) -> None:
        self.registry = registry or CollectorRegistry()
        self.processed = Counter("etl_messages_processed", "Processed events", registry=self.registry)
        self.failed = Counter("etl_messages_failed", "Failed events", registry=self.registry)
        self.dlq = Counter("etl_messages_sent_to_dlq", "DLQ events", registry=self.registry)
        self.insert_seconds = Histogram("etl_clickhouse_insert_seconds", "Insert duration", registry=self.registry)
        self.memory = Gauge(
            "process_resident_memory_bytes", "Resident process memory", registry=self.registry
        )
        self.memory.set_function(lambda: psutil.Process(os.getpid()).memory_info().rss)

    def record_processed(self, count: int = 1) -> None:
        self.processed.inc(count)
