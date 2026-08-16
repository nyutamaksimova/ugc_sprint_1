from collections.abc import Callable
from typing import Any

from .models import transform_event


class EtlWorker:
    def __init__(self, consumer, repository, dlq, sleep: Callable[[float], None]) -> None:
        self.consumer = consumer
        self.repository = repository
        self.dlq = dlq
        self.sleep = sleep

    def run_once(self) -> int:
        messages: list[dict[str, Any]] = self.consumer.poll()
        processed = 0
        for message in messages:
            event = transform_event(message)
            if event is None:
                self.consumer.commit([message])
                continue
            if self._insert(event):
                self.consumer.commit([message])
                processed += 1
            else:
                self.dlq.publish(message, "ClickHouse insert failed after 5 attempts")
                self.consumer.commit([message])
        return processed

    def _insert(self, event) -> bool:
        for delay in (1, 2, 4, 8, 16):
            try:
                self.repository.insert([event])
                return True
            except Exception:
                self.sleep(delay)
        return False
