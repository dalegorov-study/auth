# Тема: Event loop изнутри — mini_asyncio → Concept: system call через yield
# Запуск из папки lecture: python3 3_asyncio/08_mini_asyncio.py

"""Мини-scheduler на генераторах — модель того что делает asyncio."""
from collections import deque
from dataclasses import dataclass
from typing import Any, Generator
import time

# ---- Syscall: единственный объект что уходит наружу через yield ----

@dataclass
class Sleep:
    duration: float

# ---- Scheduler + глобальный "current running loop" ----

_current: "Scheduler | None" = None   # аналог asyncio._running_loop

class Scheduler:
    def __init__(self) -> None:
        self.ready: deque[Generator[Any, Any, Any]] = deque()
        self.sleeping: list[tuple[float, Generator[Any, Any, Any]]] = []

    def create_task(self, coro: Generator[Any, Any, Any]) -> None:
        """Синхронно регистрирует task в loop'е. Не отдаёт control.
        Аналог asyncio.create_task(coro)."""
        self.ready.append(coro)

    def run(self, main: Generator[Any, Any, Any]) -> None:
        global _current
        _current = self
        try:
            self.create_task(main)
            while self.ready or self.sleeping:
                self._wake_sleeping()
                if not self.ready:
                    self._idle_wait()
                    continue
                self._step_one()
        finally:
            _current = None

    def _wake_sleeping(self) -> None:
        """Переносит проснувшихся из sleeping в ready."""
        now = time.monotonic()
        still: list[tuple[float, Generator[Any, Any, Any]]] = []
        for wake_at, task in self.sleeping:
            if wake_at <= now:
                self.ready.append(task)
            else:
                still.append((wake_at, task))
        self.sleeping = still

    def _idle_wait(self) -> None:
        """Спим ровно до ближайшего таймера. НЕ time.sleep(0.01) - это был бы
        busy-poll с шагом 10ms (100 wakeup/s на пустом loop'е). Реальный
        asyncio делает так же - один syscall до min(wake_at), idle loop
        не жрёт CPU."""
        if not self.sleeping:
            return
        next_wake = min(wake_at for wake_at, _ in self.sleeping)
        time.sleep(max(0.0, next_wake - time.monotonic()))

    def _step_one(self) -> None:
        """Взять готовую task, запустить до следующего yield, обработать syscall."""
        task = self.ready.popleft()
        try:
            syscall = next(task)
        except StopIteration:
            return   # task завершилась
        self._handle_syscall(task, syscall)

    def _handle_syscall(self, task: Generator[Any, Any, Any], syscall: Any) -> None:
        if isinstance(syscall, Sleep):
            self.sleeping.append((time.monotonic() + syscall.duration, task))
        else:
            raise RuntimeError(f"unknown syscall: {syscall}")

# ---- Публичный API - имитируем asyncio ----

def sleep(duration: float) -> Generator[Any, Any, None]:
    """Аналог asyncio.sleep(). В user-коде вызывается как `yield from sleep(...)`."""
    yield Sleep(duration)

def create_task(coro: Generator[Any, Any, Any]) -> None:
    """Аналог asyncio.create_task(). Синхронно, БЕЗ yield - регистрирует
    задачу в running loop'е и возвращает управление сразу."""
    if _current is None:
        raise RuntimeError("нет running loop'а (вызови из main через run())")
    _current.create_task(coro)

def run(main: Generator[Any, Any, Any]) -> None:
    """Аналог asyncio.run(). Создаёт scheduler, запускает main."""
    Scheduler().run(main)

# ---- Пользовательские "coroutines" на генераторах ----

def worker(name: str, steps: int, delay: float) -> Generator[Any, Any, None]:
    """Печатает свой step'ы, спит delay между ними. Разные delay'и у разных
    worker'ов -> порядок шагов чередуется в scheduler'е."""
    start = time.monotonic()
    for i in range(steps):
        print(f"[{name}] step {i} at t={time.monotonic() - start:.2f}")
        yield from sleep(delay)     # <-- как `await asyncio.sleep(delay)`

def main() -> Generator[Any, Any, None]:
    # create_task - синхронно (нет yield), как asyncio.create_task().
    # Разные периоды: B в 2 раза быстрее A, C в 1.5 раза медленнее A.
    create_task(worker("A", steps=3, delay=0.10))
    create_task(worker("B", steps=4, delay=0.05))
    create_task(worker("C", steps=2, delay=0.15))
    yield from sleep(0.01)
    print("[main] all spawned")

run(main())
print("scheduler done")
