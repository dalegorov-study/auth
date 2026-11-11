# Тема: Освежаем генераторы → `yield from` — делегирование
# Запуск из папки lecture: python3 3_asyncio/03_yield_from.py

def inner():
    yield 1
    yield 2
    return "done"

def outer():
    result = yield from inner()  # проксирует yield/send/throw
    yield f"inner returned: {result}"

for x in outer():
    print(x)
