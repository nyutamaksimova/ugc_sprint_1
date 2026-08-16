import json

from src.dlq import DlqPublisher


class Producer:
    def __init__(self):
        self.message = None

    def produce(self, **kwargs):
        self.message = kwargs

    def flush(self, timeout):
        return 0


def test_dlq_publishes_original_message_with_reason():
    producer = Producer()

    DlqPublisher(producer).publish({"event_id": "event-1"}, "invalid payload")

    assert producer.message["topic"] == "video-events-dlq"
    assert json.loads(producer.message["value"])["reason"] == "invalid payload"
