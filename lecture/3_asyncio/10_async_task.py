# Тема: asyncio API → `asyncio.create_task` — планируем в фоне
# Запуск из папки lecture: python3 3_asyncio/10_async_task.py

import asyncio

async def background(name: str) -> None:
    for i in range(3):
        await asyncio.sleep(0.05)
        print(f"[{name}] tick {i}")

async def main() -> None:
    task = asyncio.create_task(background("bg"))
    print("main: task started, doing other work")
    await asyncio.sleep(0.1)
    print("main: work done, waiting for task")
    await task
    print("main: everything done")

asyncio.run(main())
