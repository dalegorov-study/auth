"""3 варианта посчитать квадраты. См. README.md."""

import time


def very_slow_function(x: int) -> int:
    """Возвращает x**2 с задержкой 0.1s — НЕ менять."""
    time.sleep(0.1)
    return x**2


def calc_squares_simple(bound: int) -> list[int]:
    ...


def calc_squares_multithreading(bound: int) -> list[int]:
    ...


def calc_squares_multiprocessing(bound: int) -> list[int]:
    ...
