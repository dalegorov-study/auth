# Тема: `threading` — базовые примитивы → `Condition` — Lock + wait/notify
# Запуск из папки lecture: python3 1_threading/14_condition.py

import threading
import time
from collections import deque

buffer: deque[int] = deque()
cond = threading.Condition()

def producer() -> None:
    for i in range(5):
        with cond:
            buffer.append(i)
            print(f"produced {i}")
            cond.notify()           # разбудить одного consumer'а
        time.sleep(0.05)

def consumer() -> None:
    while True:
        with cond:
            while not buffer:       # <-- ЦИКЛ, не if (см. ниже)
                cond.wait()         # атомарно: release lock + ждать notify + take lock
            item = buffer.popleft()
            print(f"consumed {item}")
            if item == 4:
                return

t_prod = threading.Thread(target=producer)
t_cons = threading.Thread(target=consumer)
t_prod.start(); t_cons.start()
t_prod.join(); t_cons.join()
