# Тема: `threading` — базовые примитивы → Зачем `join()`?
# Запуск из папки lecture: python3 1_threading/05_join_result.py

import threading

result: list[int] = []

def worker() -> None:
    result.append(42)

t = threading.Thread(target=worker)
t.start()
# Тут читать result[0] нельзя - worker мог ещё не дописать.
t.join()
print(result[0])  # безопасно: join гарантирует, что worker закончил
