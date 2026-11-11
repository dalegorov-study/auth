# Тема: Race conditions, deadlock, livelock → Livelock
# Запуск из папки lecture: python3 1_threading/26_livelock.py

import threading
import time

lock_a = threading.Lock()
lock_b = threading.Lock()

attempts = {"worker_1": 0, "worker_2": 0}
DEADLINE = 1.0     # секунда - хватит показать livelock

def polite_1() -> None:
    end = time.perf_counter() + DEADLINE
    while time.perf_counter() < end:
        attempts["worker_1"] += 1
        with lock_a:
            if lock_b.acquire(timeout=0.001):
                lock_b.release()
                print(f"worker 1: SUCCESS on attempt {attempts['worker_1']}")
                return
        # вежливо отпустили A, сразу retry - тут-то и ловушка

def polite_2() -> None:
    end = time.perf_counter() + DEADLINE
    while time.perf_counter() < end:
        attempts["worker_2"] += 1
        with lock_b:
            if lock_a.acquire(timeout=0.001):
                lock_a.release()
                print(f"worker 2: SUCCESS on attempt {attempts['worker_2']}")
                return

t1 = threading.Thread(target=polite_1)
t2 = threading.Thread(target=polite_2)
t1.start(); t2.start()
t1.join(); t2.join()

print(f"attempts: {attempts}")
