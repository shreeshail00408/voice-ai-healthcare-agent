import time
from typing import Callable, Any, Tuple


def timeit_ms(fn: Callable[..., Any]) -> Callable[..., Tuple[Any, float]]:
    def wrapper(*args, **kwargs):
        s = time.time()
        result = fn(*args, **kwargs)
        return result, (time.time() - s) * 1000
    return wrapper
