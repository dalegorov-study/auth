# Тема: `threading` — базовые примитивы → `RLock` — reentrant lock
# Запуск из папки lecture: python3 1_threading/12_rlock.py

import threading

lock = threading.RLock()   # с обычным Lock задедлочилось бы

counter = 0

def increment() -> None:
    global counter
    with lock:
        counter += 1

def double_increment() -> None:
    with lock:              # взяли lock
        increment()         # <-- внутри снова with lock:
                            # RLock: тот же поток пропускается счётчиком
                            # Lock:  этот же поток ждал бы сам себя навсегда

t = threading.Thread(target=double_increment)
t.start()
t.join()
print(f"counter = {counter}")
