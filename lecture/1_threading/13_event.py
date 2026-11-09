# Тема: `threading` — базовые примитивы → `Event` — one-shot флаг для сигналов
# Запуск из папки lecture: python3 1_threading/13_event.py

import threading
import time

ready = threading.Event()   # изначально not set

def waiter(name: str) -> None:
    print(f"[{name}] waits")
    ready.wait()            # блок до set()
    print(f"[{name}] GO")

for n in ["A", "B", "C"]:
    threading.Thread(target=waiter, args=(n,)).start()

time.sleep(0.3)
print("main: signalling")
ready.set()                 # разбудить ВСЕХ waiter'ов сразу
