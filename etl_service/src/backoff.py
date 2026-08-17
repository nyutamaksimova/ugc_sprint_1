import random
import time
from collections.abc import Callable
from functools import wraps
from typing import Any


def backoff(
    start_sleep_time: float = 1,
    factor: float = 2,
    border_sleep_time: float = 16,
    max_attempts: int = 5,
    sleep: Callable[[float], None] = time.sleep,
    uniform: Callable[[float, float], float] = random.uniform,
):

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapped(*args: Any, **kwargs: Any) -> Any:
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    if attempt == max_attempts - 1:
                        raise
                    limit = min(start_sleep_time * factor**attempt, border_sleep_time)
                    sleep(uniform(0, limit))
        return wrapped
    return decorator
