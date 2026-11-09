# Тема: `threading` — базовые примитивы → `queue.Queue` — thread-safe FIFO
# Запуск из папки lecture: python3 1_threading/17_queue.py

import threading
import queue
import time

q: queue.Queue[int | None] = queue.Queue(maxsize=10)

def producer() -> None:
    for i in range(5):
        q.put(i)                    # блок если full (maxsize достигнут)
        print(f"produced {i}")
        time.sleep(0.05)
    q.put(None)                     # sentinel: "конец потока"

def consumer() -> None:
    while True:
        item = q.get()              # блок если empty
        if item is None:
            break
        print(f"consumed {item}")
        q.task_done()               # опционально: отметить обработку

t_prod = threading.Thread(target=producer)
t_cons = threading.Thread(target=consumer)
t_prod.start(); t_cons.start()
t_prod.join(); t_cons.join()
