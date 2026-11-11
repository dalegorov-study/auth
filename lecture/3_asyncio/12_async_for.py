# Тема: Async iterators и context managers → async for
# Запуск из папки lecture: python3 3_asyncio/12_async_for.py

import asyncio

class Ticker:
    def __init__(self, n: int, interval: float):
        self.n = n
        self.interval = interval
        self.i = 0

    def __aiter__(self):
        return self

    async def __anext__(self) -> int:
        if self.i >= self.n:
            raise StopAsyncIteration
        await asyncio.sleep(self.interval)
        self.i += 1
        return self.i

async def main() -> None:
    async for tick in Ticker(3, 0.05):
        print(f"tick {tick}")

asyncio.run(main())
