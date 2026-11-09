# Тема: `threading` — базовые примитивы → Синхронизация: `Lock`
# Запуск из папки lecture: python3 1_threading/11_lock_fix.py

import threading
import time
import random

count = 0
lock = threading.Lock()

def counter() -> None:
    global count
    with lock:                     # <-- захват + release автоматически
        old = count
        time.sleep(random.random())
        count = old + 1
        print(count, end=" ")

threads = [threading.Thread(target=counter) for _ in range(10)]
for t in threads: t.start()
for t in threads: t.join()
print()
