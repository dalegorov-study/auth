# Тема: asyncio API → `asyncio.gather` — параллельное выполнение
# Запуск из папки lecture: python3 3_asyncio/09_async_gather.py

import asyncio
import time

async def fetch(url: str, delay: float) -> str:
    await asyncio.sleep(delay)
    return f"{url} OK"

async def main() -> None:
    start = time.perf_counter()
    results = await asyncio.gather(
        fetch("a", 0.2),
        fetch("b", 0.1),
        fetch("c", 0.3),
    )
    elapsed = time.perf_counter() - start
    print(f"results: {results}")
    print(f"total: {elapsed:.2f}s (max delay was 0.3s → параллельно)")

asyncio.run(main())
