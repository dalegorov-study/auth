# Тема: От генератора к coroutine
# Запуск из папки lecture: python3 3_asyncio/05_coroutine_object.py

async def greet(name: str) -> str:
    return f"hello {name}"

coro = greet("world")
print(type(coro))
print(coro)
# Coroutine — ОБЪЕКТ. Ещё ничего не выполнилось.
coro.close()  # закрываем чтобы warning не было
