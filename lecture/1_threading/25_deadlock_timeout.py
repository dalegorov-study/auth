# Тема: Race conditions, deadlock, livelock → Deadlock
# Запуск из папки lecture: python3 1_threading/25_deadlock_timeout.py

import threading
import time

lock_a = threading.Lock()
lock_b = threading.Lock()

def worker_ab() -> None:
    with lock_a:
        time.sleep(0.05)
        # Пытаемся взять B, но с таймаутом чтобы не зависнуть навсегда
        got = lock_b.acquire(timeout=0.5)
        if got:
            print("worker_ab: got both")
            lock_b.release()
        else:
            print("worker_ab: TIMEOUT waiting for B")

def worker_ba() -> None:
    with lock_b:
        time.sleep(0.05)
        got = lock_a.acquire(timeout=0.5)
        if got:
            print("worker_ba: got both")
            lock_a.release()
        else:
            print("worker_ba: TIMEOUT waiting for A")

t1 = threading.Thread(target=worker_ab)
t2 = threading.Thread(target=worker_ba)
t1.start(); t2.start()
t1.join(); t2.join()
