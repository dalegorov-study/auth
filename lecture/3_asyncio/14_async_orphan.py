# Тема: Structured concurrency
# Запуск из папки lecture: python3 3_asyncio/14_async_orphan.py

import asyncio

async def buggy():
    await asyncio.sleep(0.05)
    raise ValueError("oops")

async def main_orphan() -> None:
    # ANTI-PATTERN — не await'им task
    asyncio.create_task(buggy())
    await asyncio.sleep(0.2)
    print("main done — но исключение из buggy было потеряно!")

asyncio.run(main_orphan())
