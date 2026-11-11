"""Все тесты задачи."""

import inspect
import math
import time

import pytest

from pi import (
    estimate_pi_multiprocessing,
    estimate_pi_serial,
    estimate_pi_threading,
)

TOL = 0.05


# ==================== correctness ====================


def test_serial_estimate() -> None:
    est = estimate_pi_serial(100_000)
    assert math.isclose(est, math.pi, abs_tol=TOL), (
        f"π estimate {est:.4f} слишком далеко от {math.pi:.4f}"
    )


def test_threading_estimate() -> None:
    est = estimate_pi_threading(100_000, workers=4)
    assert math.isclose(est, math.pi, abs_tol=TOL)


def test_multiprocessing_estimate() -> None:
    est = estimate_pi_multiprocessing(100_000, workers=4)
    assert math.isclose(est, math.pi, abs_tol=TOL)


@pytest.mark.parametrize("workers", [1, 2, 4])
def test_multiprocessing_various_workers(workers: int) -> None:
    est = estimate_pi_multiprocessing(50_000, workers=workers)
    assert math.isclose(est, math.pi, abs_tol=TOL)


# ==================== GIL effect ====================


def test_threading_does_not_speed_up_cpu_bound() -> None:
    """Ключевой демо-тест: threading НЕ ускоряет CPU-bound задачу.

    Все треды делят один GIL, только один за раз выполняет байткод.
    Ожидаем что threading по времени сопоставим с serial (не быстрее).
    """
    n = 400_000

    start = time.perf_counter()
    estimate_pi_serial(n)
    serial_time = time.perf_counter() - start

    start = time.perf_counter()
    estimate_pi_threading(n, workers=4)
    thread_time = time.perf_counter() - start

    print(f"\n  serial: {serial_time * 1000:.0f}ms  threading: {thread_time * 1000:.0f}ms")
    # Threading не должен быть В РАЗЫ быстрее (GIL). Допускаем ~1.5x
    # (thread scheduling иногда даёт мелкую wins), но не более.
    assert thread_time > serial_time / 1.5, (
        f"threading ({thread_time:.2f}s) неожиданно намного быстрее serial "
        f"({serial_time:.2f}s). Возможно ты запустил на free-threading build "
        f"Python (см. PEP 703) — там GIL можно отключить."
    )


def test_multiprocessing_faster_than_serial() -> None:
    """multiprocessing даёт реальный speedup — обходит GIL через процессы."""
    n = 4_000_000

    start = time.perf_counter()
    estimate_pi_serial(n)
    serial_time = time.perf_counter() - start

    start = time.perf_counter()
    estimate_pi_multiprocessing(n, workers=4)
    mp_time = time.perf_counter() - start

    print(f"\n  serial: {serial_time * 1000:.0f}ms  mp: {mp_time * 1000:.0f}ms")
    # min 1.3x speedup — mp overhead около 100-200ms на macOS spawn.
    assert mp_time < serial_time / 1.3, (
        f"multiprocessing ({mp_time:.2f}s) должен быть хотя бы в 1.3x "
        f"быстрее serial ({serial_time:.2f}s)"
    )


# ==================== structure ====================


def test_multiprocessing_uses_pool() -> None:
    src = inspect.getsource(estimate_pi_multiprocessing)
    assert "Pool" in src or "multiprocessing" in src, "должен использоваться multiprocessing.Pool"


def test_threading_uses_thread_pool() -> None:
    src = inspect.getsource(estimate_pi_threading)
    assert "ThreadPool" in src or "Thread" in src or "threading" in src, (
        "должен использоваться ThreadPoolExecutor или threading.Thread"
    )
