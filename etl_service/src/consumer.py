import json
from typing import Any


class KafkaConsumerAdapter:
    def __init__(self, client: Any, timeout: float = 1.0) -> None:
        self._client = client
        self._timeout = timeout
        self._original: dict[int, Any] = {}

    def poll(self) -> list[dict]:
        message = self._client.poll(self._timeout)
        if message is None:
            return []
        payload = json.loads(message.value().decode("utf-8"))
        self._original[id(payload)] = message
        return [payload]

    def commit(self, messages: list[dict]) -> None:
        for payload in messages:
            self._client.commit(self._original.pop(id(payload), payload), asynchronous=False)
