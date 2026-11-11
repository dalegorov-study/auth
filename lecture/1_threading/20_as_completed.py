# Тема: `ThreadPoolExecutor` — почти всегда так → Futures API
# Запуск из папки lecture: python3 1_threading/20_as_completed.py

from concurrent.futures import ThreadPoolExecutor, as_completed
import time

def work(item: int) -> int:
    time.sleep(0.1 * (item % 3 + 1))  # разные задержки
    return item * item

with ThreadPoolExecutor(max_workers=4) as pool:
    futures = {pool.submit(work, i): i for i in range(10)}
    for fut in as_completed(futures):
        i = futures[fut]
        print(f"item {i} → {fut.result()}")
