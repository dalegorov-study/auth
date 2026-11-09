# Тема: Structured concurrency → `TaskGroup` (3.11+)
# Запуск из папки lecture: python3 3_asyncio/15_async_taskgroup.py
# Нужен Python 3.11+

import asyncio

async def worker(name: str, delay: float) -> str:
    await asyncio.sleep(delay)
    return f"{name} done"

async def main() -> None:
    async with asyncio.TaskGroup() as tg:
        t1 = tg.create_task(worker("A", 0.1))
        t2 = tg.create_task(worker("B", 0.2))
        # автоматически ждём всех при выходе из async with
    print(f"results: {t1.result()}, {t2.result()}")

asyncio.run(main())
