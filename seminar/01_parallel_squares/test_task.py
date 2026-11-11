"""Все тесты задачи."""

import time

import pytest

from squares import (
    calc_squares_multiprocessing,
    calc_squares_multithreading,
    calc_squares_simple,
    very_slow_function,
)


# ==================== correctness ====================


def test_simple_returns_squares() -> None:
    assert calc_squares_simple(5) == [0, 1, 4, 9, 16]


def test_simple_empty_bound() -> None:
    assert calc_squares_simple(0) == []


def test_threading_returns_squares() -> None:
    """Результат должен быть в правильном ПОРЯДКЕ (idx→value)."""
    result = calc_squares_multithreading(20)
    assert result == [i * i for i in range(20)]


def test_multiprocessing_returns_squares() -> None:
    result = calc_squares_multiprocessing(20)
    assert result == [i * i for i in range(20)]


def test_multiprocessing_empty() -> None:
    """Границы: 0 и малые значения не должны падать."""
    assert calc_squares_multiprocessing(0) == []


# ==================== speed ====================


@pytest.mark.parametrize("bound", [12])
def test_multiprocessing_faster_than_simple(bound: int) -> None:
    """multiprocessing должен обходить simple по времени.

    Для simple: bound * 0.1s ≈ bound/10 секунд.
    Для multiproc: bound / cpu_count * 0.1s.
    Ставим порог: multiproc быстрее simple хотя бы в 1.5 раза.
    """
    start = time.perf_counter()
    calc_squares_simple(bound)
    simple_time = time.perf_counter() - start

    start = time.perf_counter()
    calc_squares_multiprocessing(bound)
    mp_time = time.perf_counter() - start

    print(f"\n  simple: {simple_time:.2f}s, multiproc: {mp_time:.2f}s")
    assert mp_time < simple_time / 1.5, (
        f"multiprocessing ({mp_time:.2f}s) должен быть быстрее simple "
        f"({simple_time:.2f}s) хотя бы в 1.5 раза"
    )


def test_threading_faster_than_simple() -> None:
    """threading тоже быстрее simple: time.sleep освобождает GIL."""
    start = time.perf_counter()
    calc_squares_simple(12)
    simple_time = time.perf_counter() - start

    start = time.perf_counter()
    calc_squares_multithreading(12)
    th_time = time.perf_counter() - start

    print(f"\n  simple: {simple_time:.2f}s, threading: {th_time:.2f}s")
    assert th_time < simple_time / 1.5


# ==================== structural ====================


def test_uses_threading_module() -> None:
    """calc_squares_multithreading должна реально использовать threading."""
    import inspect

    import squares

    src = inspect.getsource(squares)
    assert "threading" in src, "должен использоваться модуль threading"


def test_uses_multiprocessing_module() -> None:
    """calc_squares_multiprocessing должна реально использовать multiprocessing."""
    import inspect

    import squares

    src = inspect.getsource(squares)
    assert "multiprocessing" in src, "должен использоваться модуль multiprocessing"


def test_very_slow_function_unchanged() -> None:
    """very_slow_function не менять — тест эталонного поведения."""
    assert very_slow_function(3) == 9
    assert very_slow_function(4) == 16
