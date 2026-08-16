from src.models import transform_event


def test_transform_started_event_to_clickhouse_row():
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

    assert event.to_row()["event_type"] == "video_started"
    assert event.to_row()["movie_id"] == "movie-1"


def test_transform_ignores_video_quality_change():
    assert transform_event({"event_type": "video_quality_changed"}) is None
