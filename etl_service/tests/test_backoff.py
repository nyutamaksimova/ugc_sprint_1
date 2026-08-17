import pytest

from src.backoff import backoff


def test_backoff_retries_five_times_then_reraises():
    attempts = 0
    delays = []

    @backoff(max_attempts=5, sleep=delays.append, uniform=lambda _start, end: end)
    def insert():
        nonlocal attempts
        attempts += 1
        raise OSError("down")

    with pytest.raises(OSError, match="down"):
        insert()

    assert attempts == 5
    assert delays == [1, 2, 4, 8]
