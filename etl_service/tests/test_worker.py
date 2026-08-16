from src.worker import EtlWorker


class Repository:
    def __init__(self, error=None):
        self.error = error
        self.inserted = []

    def insert(self, events):
        if self.error:
            raise self.error
        self.inserted.extend(events)


class Consumer:
    def __init__(self, messages):
        self.messages = messages
        self.committed = []

    def poll(self):
        return self.messages

    def commit(self, messages):
        self.committed.extend(messages)


class Dlq:
    def __init__(self):
        self.published = []

    def publish(self, message, reason):
        self.published.append((message, reason))


def message():
    return {
        "event_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
        "event_type": "video_started",
        "user_id": "user-1",
        "session_id": "019ffafa-5fd5-7363-8154-84618a0104db",
        "occurred_at": "2026-08-16T10:00:00Z",
        "received_at": "2026-08-16T10:00:01Z",
        "payload": {"movie_id": "movie-1"},
    }


def test_worker_commits_only_after_successful_insert():
    item = message()
    consumer = Consumer([item])
    worker = EtlWorker(consumer, Repository(), Dlq(), sleep=lambda _: None)

    assert worker.run_once() == 1
    assert consumer.committed == [item]


def test_worker_sends_message_to_dlq_after_five_failures():
    item = message()
    consumer = Consumer([item])
    dlq = Dlq()
    worker = EtlWorker(consumer, Repository(OSError("down")), dlq, sleep=lambda _: None)

    assert worker.run_once() == 0
    assert dlq.published[0][0] == item
    assert consumer.committed == [item]
