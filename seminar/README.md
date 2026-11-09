# Семинар: threading, multiprocessing, asyncio

Подготовка: `pip install -r requirements.txt`. В каждой папке — условие (`README.md`),
заготовка решения и тесты (`test_task.py`). Запуск из папки задачи: `pytest -s`.

## Задание 1. Потоки vs процессы на медленной функции — `01_parallel_squares/`

1. Посчитайте `very_slow_function(i)` для `i in range(bound)` синхронно.
2. То же через `Thread` + `queue.Queue`.
3. То же через `multiprocessing.Pool`.
4. Результат — в правильном порядке.
5. Сравните время трёх вариантов.

## Задание 2. π методом Монте-Карло — `02_pi_estimate/`

1. Оцените π по случайным точкам: π ≈ 4 · hits / n.
2. Последовательная версия.
3. Версия через `ThreadPoolExecutor`.
4. Версия через `multiprocessing.Pool`.
5. Сравните время и объясните, почему потоки не ускоряют.

## Задание 3. Параллельные HTTP-запросы — `03_sync_vs_async/`

1. Скачайте список URL через `aiohttp` + `asyncio.gather`.
2. То же через `requests` + `ThreadPoolExecutor`.
3. Одна сессия на весь список.
4. Прогоните тесты, сравните подходы.
