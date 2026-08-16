import json
from typing import Any


class DlqPublisher:
    def __init__(self, producer: Any) -> None:
        self._producer = producer

    def publish(self, message: dict, reason: str) -> None:
        self._producer.produce(
            topic="video-events-dlq",
            key=message.get("user_id", ""),
            value=json.dumps({"message": message, "reason": reason}),
        )
        if self._producer.flush(5) != 0:
            raise RuntimeError("DLQ delivery was not confirmed")
