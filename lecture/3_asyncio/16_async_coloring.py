# Тема: Когда async, а когда нет → Async coloring
# Запуск из папки lecture: python3 3_asyncio/16_async_coloring.py

import asyncio
import time

async def bad() -> None:
    print("start")
    time.sleep(0.5)  # blocking! Держит весь loop
    print("done")

async def other() -> None:
    for i in range(5):
        await asyncio.sleep(0.1)
        print(f"other {i}")

async def main() -> None:
    await asyncio.gather(bad(), other())

start = time.perf_counter()
asyncio.run(main())
print(f"total: {time.perf_counter() - start:.2f}s")
