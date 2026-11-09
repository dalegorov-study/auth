# Тема: Race conditions, deadlock, livelock → Livelock
# Запуск из папки lecture: python3 1_threading/27_livelock_backoff.py

import threading
import time
import random

lock_a = threading.Lock()
lock_b = threading.Lock()

attempts = {"worker_1": 0, "worker_2": 0}
DEADLINE = 1.0

def with_backoff(first: threading.Lock, second: threading.Lock, key: str) -> None:
    delay = 0.001
    end = time.perf_counter() + DEADLINE
    while time.perf_counter() < end:
        attempts[key] += 1
        with first:
            if second.acquire(timeout=0.001):
                second.release()
                print(f"{key}: SUCCESS on attempt {attempts[key]}")
                return
        time.sleep(delay * random.random())     # <-- jitter
        delay = min(delay * 2, 0.05)            # <-- exponential

t1 = threading.Thread(target=with_backoff, args=(lock_a, lock_b, "worker_1"))
t2 = threading.Thread(target=with_backoff, args=(lock_b, lock_a, "worker_2"))
t1.start(); t2.start()
t1.join(); t2.join()

print(f"attempts: {attempts}")
