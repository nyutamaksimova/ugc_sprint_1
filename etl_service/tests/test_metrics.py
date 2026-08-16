from prometheus_client import CollectorRegistry, generate_latest

from src.metrics import Metrics


def test_metrics_expose_processed_events_and_resident_memory():
    metrics = Metrics(registry=CollectorRegistry())

    metrics.record_processed(2)
    rendered = generate_latest(metrics.registry).decode()

    assert "etl_messages_processed_total 2.0" in rendered
    assert "process_resident_memory_bytes" in rendered
