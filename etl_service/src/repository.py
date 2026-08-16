from typing import Protocol

from .models import VideoEvent


class ClickHouseClient(Protocol):
    def insert(self, table: str, data: list[dict]) -> None: ...


class ClickHouseRepository:
    def __init__(self, client: ClickHouseClient) -> None:
        self._client = client

    def insert(self, events: list[VideoEvent]) -> None:
        if events:
            self._client.insert("video_events", [event.to_row() for event in events])

    def ensure_schema(self) -> None:
        self._client.command(
            """CREATE TABLE IF NOT EXISTS video_events
            (event_id UUID, event_type LowCardinality(String), movie_id String,
             user_id String, session_id UUID, occurred_at DateTime64(3, 'UTC'),
             received_at DateTime64(3, 'UTC'), duration_seconds Nullable(UInt32),
             ingested_at DateTime64(3, 'UTC'))
            ENGINE = ReplacingMergeTree ORDER BY event_id"""
        )
