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
        valid_messages: list[dict[str, Any]] = []
        events = []
        for message in messages:
            try:
                event = transform_event(message)
            except (KeyError, TypeError, ValueError) as error:
                self.dlq.publish(message, f"Malformed event: {error}")
                self.consumer.commit([message])
                continue
            if event is None:
                self.consumer.commit([message])
                continue
            valid_messages.append(message)
            events.append(event)

        if not events:
            return 0
        try:
            self.repository.insert(events)
        except Exception:
            for message in valid_messages:
                self.dlq.publish(message, "ClickHouse insert failed after 5 attempts")
                self.consumer.commit([message])
            return 0
        else:
            self.consumer.commit(valid_messages)
            return len(events)