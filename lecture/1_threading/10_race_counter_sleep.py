# Тема: `threading` — базовые примитивы → Синхронизация: `Lock`
# Запуск из папки lecture: python3 1_threading/10_race_counter_sleep.py

import threading
import time
import random

count = 0

def counter() -> None:
    global count
    old = count
    time.sleep(random.random())    # <-- планировщик успевает переключиться
    count = old + 1
    print(count, end=" ")

threads = [threading.Thread(target=counter) for _ in range(10)]
for t in threads: t.start()
for t in threads: t.join()
print()
