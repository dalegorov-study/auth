# Тема: `threading` — базовые примитивы → `Thread` — ручное управление
# Запуск из папки lecture: python3 1_threading/04_thread_basic.py

import threading
import time

def worker(name: str, delay: float) -> None:
    print(f"[{name}] start")
    time.sleep(delay)
    print(f"[{name}] done after {delay}s")

t1 = threading.Thread(target=worker, args=("A", 0.3))
t2 = threading.Thread(target=worker, args=("B", 0.1))

start = time.perf_counter()
t1.start()
t2.start()
t1.join()
t2.join()
elapsed = time.perf_counter() - start

print(f"total: {elapsed:.2f}s (sum was 0.4s → параллельно = ~max)")
