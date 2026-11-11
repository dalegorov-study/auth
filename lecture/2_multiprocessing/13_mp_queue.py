# Тема: IPC — как процессы обмениваются данными → `multiprocessing.Queue` — pickle через pipe
# Запуск из папки lecture: python3 2_multiprocessing/13_mp_queue.py
# Нужен свежий Python (рекомендуется 3.14): на 3.10 падает на аннотации Queue[...]

import multiprocessing as mp
from multiprocessing.queues import Queue   # реальный класс для аннотаций
                                            # (mp.Queue - это factory-method,
                                            # не subscriptable)

def producer(q: Queue[int | None]) -> None:
    for i in range(5):
        q.put(i)
    q.put(None)  # sentinel — "конец"

def consumer(q: Queue[int | None]) -> None:
    while True:
        item = q.get()
        if item is None:
            break
        print(f"consumed: {item * 10}")

if __name__ == "__main__":
    ctx = mp.get_context("spawn")
    q = ctx.Queue()
    p_prod = ctx.Process(target=producer, args=(q,))
    p_cons = ctx.Process(target=consumer, args=(q,))
    p_prod.start(); p_cons.start()
    p_prod.join(); p_cons.join()
