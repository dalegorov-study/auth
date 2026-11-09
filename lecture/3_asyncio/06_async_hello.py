# Тема: От генератора к coroutine → Простейший запуск
# Запуск из папки lecture: python3 3_asyncio/06_async_hello.py

import asyncio

async def greet(name: str) -> str:
    return f"hello {name}"

result = asyncio.run(greet("world"))
print(result)
