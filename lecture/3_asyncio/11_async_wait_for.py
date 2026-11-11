# Тема: asyncio API → `asyncio.wait_for` — timeout
# Запуск из папки lecture: python3 3_asyncio/11_async_wait_for.py

import asyncio

async def slow_op() -> str:
    await asyncio.sleep(1.0)
    return "done"

async def main() -> None:
    try:
        await asyncio.wait_for(slow_op(), timeout=0.2)
    except asyncio.TimeoutError:
        print("timed out!")

asyncio.run(main())
