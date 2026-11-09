# Тема: Освежаем генераторы → `send` — двусторонняя коммуникация
# Запуск из папки lecture: python3 3_asyncio/02_generator_send.py

def echo():
    msg = "start"
    while True:
        received = yield msg
        msg = f"got: {received}"

g = echo()
print(next(g))          # prime the generator — печатает "start"
print(g.send("hello"))  # печатает "got: hello"
print(g.send("world"))  # печатает "got: world"
