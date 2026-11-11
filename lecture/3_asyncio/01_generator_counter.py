# Тема: Освежаем генераторы
# Запуск из папки lecture: python3 3_asyncio/01_generator_counter.py

def counter(start: int, stop: int):
    i = start
    while i < stop:
        yield i
        i += 1

c = counter(0, 3)
print(next(c), next(c), next(c))
try:
    next(c)
except StopIteration:
    print("done")
