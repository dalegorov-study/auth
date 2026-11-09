# Тема: Когда async, а когда нет → Deadlock в async: concurrency ≠ параллелизм
# Запуск из папки lecture: python3 3_asyncio/17_async_deadlock.py
# Нужен Python 3.11+

import asyncio

async def main() -> None:
    lock_a = asyncio.Lock()
    lock_b = asyncio.Lock()

    async def worker_ab() -> None:
        async with lock_a:
            print("worker_ab: держу A, беру B")
            await asyncio.sleep(0.01)     # даём worker_ba взять lock_b
            async with lock_b:
                print("worker_ab: держу оба")

    async def worker_ba() -> None:
        async with lock_b:
            print("worker_ba: держу B, беру A")
            await asyncio.sleep(0.01)     # даём worker_ab взять lock_a
            async with lock_a:
                print("worker_ba: держу оба")

    # asyncio.timeout() ловит зависание за 1 секунду.
    try:
        async with asyncio.timeout(1.0):
            await asyncio.gather(worker_ab(), worker_ba())
    except TimeoutError:
        print("DEADLOCK: worker_ab держит A ждёт B, worker_ba держит B ждёт A")

asyncio.run(main())
