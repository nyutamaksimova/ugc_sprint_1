import json

from src.consumer import KafkaConsumerAdapter


class Message:
    def __init__(self, payload):
        self._payload = payload

    def value(self):
        return self._payload


class Client:
    def __init__(self):
        self.committed = []

    def poll(self, timeout):
        return Message(json.dumps({"event_type": "video_started"}).encode())

    def commit(self, message, asynchronous):
        self.committed.append((message, asynchronous))


def test_consumer_decodes_message_and_commits_synchronously():
    client = Client()
    adapter = KafkaConsumerAdapter(client)

    messages = adapter.poll()
    adapter.commit(messages)

    assert messages == [{"event_type": "video_started"}]
    assert client.committed[0][1] is False
