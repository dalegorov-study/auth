# Тема: `threading` — базовые примитивы → Синхронизация: `Lock`
# Запуск из папки lecture: python3 1_threading/09_race_counter.py

import threading

count = 0

def counter() -> None:
    global count
    count += 1
    print(count, end=" ")

threads = [threading.Thread(target=counter) for _ in range(10)]
for t in threads: t.start()
for t in threads: t.join()
print()
