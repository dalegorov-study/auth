# Тема: `threading` — базовые примитивы → Зачем `join()`?
# Запуск из папки lecture: python3 1_threading/08_join_timeout.py

import threading, time

def maybe_hangs() -> None:
    time.sleep(10)

t = threading.Thread(target=maybe_hangs, daemon=True)
t.start()
t.join(timeout=1.0)
if t.is_alive():
    print("worker завис — идём дальше, но результата нет")
