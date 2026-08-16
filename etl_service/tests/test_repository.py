from src.models import transform_event
from src.repository import ClickHouseRepository


class RecordingClickHouse:
    def __init__(self) -> None:
        self.inserted_table = None
        self.rows = []

    def insert(self, table, data):
        self.inserted_table = table
        self.rows = data

    def command(self, query):
        self.query = query


def test_insert_serializes_one_row_per_event():
    event = transform_event(
        {
            "event_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
            "event_type": "video_started",
            "user_id": "user-1",
            "session_id": "019ffafa-5fd5-7363-8154-84618a0104db",
            "occurred_at": "2026-08-16T10:00:00Z",
            "received_at": "2026-08-16T10:00:01Z",
            "payload": {"movie_id": "movie-1"},
        }
    )
    client = RecordingClickHouse()

    ClickHouseRepository(client).insert([event])

    assert client.inserted_table == "video_events"
    assert client.rows[0]["event_id"] == "f47ac10b-58cc-4372-a567-0e02b2c3d479"


def test_ensure_schema_creates_video_events_table():
    client = RecordingClickHouse()

    ClickHouseRepository(client).ensure_schema()

    assert "CREATE TABLE IF NOT EXISTS video_events" in client.query
