# Тема: Async iterators и context managers → async with
# Запуск из папки lecture: python3 3_asyncio/13_async_with.py

import asyncio

class DBConnection:
    async def __aenter__(self):
        print("connecting...")
        await asyncio.sleep(0.05)
        return self

    async def __aexit__(self, *exc_info):
        print("closing...")
        await asyncio.sleep(0.05)

    async def query(self, sql: str) -> str:
        await asyncio.sleep(0.02)
        return f"result of: {sql}"

async def main() -> None:
    async with DBConnection() as db:
        r = await db.query("SELECT 1")
        print(r)

asyncio.run(main())
