# Тема: `ThreadPoolExecutor` — почти всегда так
# Запуск из папки lecture: python3 1_threading/19_threadpool.py

from concurrent.futures import ThreadPoolExecutor
import time

def fetch_url(url: str) -> str:
    # эмуляция сетевого запроса
    time.sleep(0.2)
    return f"{url} → 200 OK"

urls = [f"https://example.com/page{i}" for i in range(10)]

start = time.perf_counter()
with ThreadPoolExecutor(max_workers=5) as pool:
    results = list(pool.map(fetch_url, urls))
elapsed = time.perf_counter() - start

print(f"10 запросов через pool(5) — {elapsed:.2f}s (sequential было бы 2.0s)")
