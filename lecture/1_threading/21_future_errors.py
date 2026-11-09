# Тема: `ThreadPoolExecutor` — почти всегда так → Обработка ошибок в futures
# Запуск из папки lecture: python3 1_threading/21_future_errors.py

from concurrent.futures import ThreadPoolExecutor

def risky(x: int) -> int:
    if x == 3:
        raise ValueError(f"boom on {x}")
    return x * 10

with ThreadPoolExecutor(max_workers=3) as pool:
    futures = [pool.submit(risky, i) for i in range(5)]
    for i, fut in enumerate(futures):
        try:
            print(f"item {i} → {fut.result()}")
        except ValueError as e:
            print(f"item {i} → ERROR: {e}")
