# Тема: `threading` — базовые примитивы → Зачем `join()`?
# Запуск из папки lecture: python3 1_threading/07_thread_exception.py

import threading

def broken() -> None:
    raise ValueError("боль")

t = threading.Thread(target=broken)
t.start()
t.join()   # exception залогген в stderr, но join НЕ бросит его в main
print("main думает что всё ок")
