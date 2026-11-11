# Тема: `threading` — базовые примитивы → `threading.local` — thread-local storage
# Запуск из папки lecture: python3 1_threading/18_thread_local.py

import threading

data = threading.local()

def worker(value: int) -> None:
    data.x = value
    # ... много кода где data.x читается ...
    print(f"[{threading.current_thread().name}] data.x = {data.x}")

threads = [threading.Thread(target=worker, args=(i,), name=f"T{i}") for i in range(3)]
for t in threads: t.start()
for t in threads: t.join()
