from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from typing import Any


@dataclass(frozen=True)
class VideoEvent:
    event_id: str
    event_type: str
    movie_id: str
    user_id: str
    session_id: str
    occurred_at: str
    received_at: str
    duration_seconds: int | None
    ingested_at: str

    def to_row(self) -> dict[str, Any]:
        return asdict(self)


def transform_event(message: dict[str, Any]) -> VideoEvent | None:
    if message.get("event_type") not in {"video_started", "video_completed"}:
        return None
    payload = message["payload"]
    return VideoEvent(
        event_id=message["event_id"],
        event_type=message["event_type"],
        movie_id=payload["movie_id"],
        user_id=message["user_id"],
        session_id=message["session_id"],
        occurred_at=message["occurred_at"],
        received_at=message["received_at"],
        duration_seconds=payload.get("duration_seconds"),
        ingested_at=datetime.now(UTC).isoformat(),
    )
