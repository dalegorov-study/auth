# parallel_squares — три варианта параллелизма

## Условие

Дана "Очень Медленная Функция" `very_slow_function(x)` (возвращает `x**2`
через `time.sleep(0.1)`). Нужно реализовать три способа посчитать
`[very_slow_function(i) for i in range(bound)]`:

1. **`calc_squares_simple(bound)`** — синхронно, в один поток (базовый case).
2. **`calc_squares_multithreading(bound)`** — через `threading.Thread` +
   `queue.Queue` (для правильного порядка результата).
3. **`calc_squares_multiprocessing(bound)`** — через `multiprocessing.Pool`.

Все три возвращают `list[int]` **в правильном порядке**:
`[0, 1, 4, 9, 16, ...]`.

## Про правильный порядок

- `Queue`-подход: отдавай `(idx, value)`, потом собирай `result[idx] = value`
  — так порядок не зависит от того, какой поток закончил первым.
- `multiprocessing.Pool.starmap` возвращает список в порядке аргументов —
  но у нас чанки, надо развернуть через `(idx, value)` пары.

## Подсказки

- `multiprocessing.cpu_count()` — сколько запускать threads/processes.
- Каждый worker обрабатывает свои индексы `[part_id, part_id+N, part_id+2N, ...]`
  чтобы разгрузка была равномерной.
- **`very_slow_function` НЕ трогать** — тесты полагаются на её точное
  поведение и timing.

## Как проверить локально (из папки задачи)

```bash
pytest -s
ruff check .
mypy --strict .
```

Флаг `-s` — покажет timing-строки из speed-тестов.

## Материалы

- [threading docs](https://docs.python.org/3/library/threading.html)
- [multiprocessing docs](https://docs.python.org/3/library/multiprocessing.html)
- [queue.Queue docs](https://docs.python.org/3/library/queue.html)
