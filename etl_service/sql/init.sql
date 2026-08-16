CREATE TABLE IF NOT EXISTS video_events
(
    event_id UUID,
    event_type LowCardinality(String),
    movie_id String,
    user_id String,
    session_id UUID,
    occurred_at DateTime64(3, 'UTC'),
    received_at DateTime64(3, 'UTC'),
    duration_seconds Nullable(UInt32),
    ingested_at DateTime64(3, 'UTC')
)
ENGINE = ReplacingMergeTree
ORDER BY event_id;
