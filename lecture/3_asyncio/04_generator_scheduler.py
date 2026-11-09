# Тема: Освежаем генераторы → Зачем это всё — генератор как "приостановимая задача"
# Запуск из папки lecture: python3 3_asyncio/04_generator_scheduler.py

from collections import deque

def worker(name: str, steps: int):
    for i in range(steps):
        print(f"[{name}] step {i}")
        yield  # <-- добровольная приостановка, control возвращается scheduler'у

def scheduler(tasks):
    q = deque(tasks)
    while q:
        task = q.popleft()
        try:
            next(task)     # запускаем до следующего yield
            q.append(task) # снова в очередь
        except StopIteration:
            pass           # задача завершилась

scheduler([worker("A", 3), worker("B", 3), worker("C", 2)])
