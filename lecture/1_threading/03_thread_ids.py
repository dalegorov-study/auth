# Тема: `threading` — базовые примитивы → Что такое поток
# Запуск из папки lecture: python3 1_threading/03_thread_ids.py

import os
import threading

def show_ids(who: str) -> None:
    print(f"{who:6}  pid={os.getpid()}  tid={threading.get_native_id()}")

show_ids("main")
t = threading.Thread(target=show_ids, args=("child",))
t.start()
t.join()
