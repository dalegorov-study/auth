# Тема: `threading` — базовые примитивы → Зачем `join()`?
# Запуск из папки lecture: python3 1_threading/06_daemon_demo.py

import threading, time

def slow():
    time.sleep(2)
    print("worker done")

t = threading.Thread(target=slow, daemon=True)
t.start()
print("main done")
# main выходит немедленно, daemon-тред убит - "worker done" не напечатается
