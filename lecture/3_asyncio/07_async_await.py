# Тема: От генератора к coroutine → await = "приостанови меня пока не готово"
# Запуск из папки lecture: python3 3_asyncio/07_async_await.py

import asyncio

async def slow_greet(name: str, delay: float) -> str:
    await asyncio.sleep(delay)   # приостановка — loop может запускать другие coroutines
    return f"hello {name}"

async def main() -> None:
    result = await slow_greet("world", 0.1)
    print(result)

asyncio.run(main())
