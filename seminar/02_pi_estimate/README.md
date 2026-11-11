# pi_estimate — π через Monte Carlo: демо GIL-эффекта

## Задача

Вычислить π методом Monte Carlo — бросаем `n` случайных точек в квадрат
`[-1, 1]²`, считаем сколько попало в единичный круг:

```
π ≈ 4 * hits / n
```

Задача чисто CPU-bound (RNG + арифметика, никакого IO) — идеальный кейс
чтобы **пощупать разницу threading vs multiprocessing** на реальном примере.

## Три функции

- **`estimate_pi_serial(n_points) -> float`** — baseline, один поток.
- **`estimate_pi_threading(n_points, workers=4) -> float`** —
  `ThreadPoolExecutor`. На CPU-bound задаче в CPython с GIL **НЕ ускоряет**.
- **`estimate_pi_multiprocessing(n_points, workers=4) -> float`** —
  `multiprocessing.Pool`. Реально несколько процессов, каждый со своим GIL.

Все три должны возвращать π с точностью `abs_tol ≤ 0.05` на `n=100_000`.

## Cutting-edge: subinterpreters и free-threading

Python 3.13+ даёт **два новых способа** обходить GIL, не спавня процессы:

- **PEP 734 (subinterpreters)**: `from concurrent import interpreters` —
  создаёт subinterpreter внутри процесса, у каждого свой GIL. Overhead
  ниже чем у multiprocessing (нет fork'а), но выше threading. Взаимодействие
  через `interpreters.create_queue()`.
- **PEP 703 (free-threading)**: специальный build Python (`python3.13t`) без
  GIL вообще. Threading начинает реально ускорять CPU-bound.

Обе фичи — экспериментальные (2025-2026). В этой задаче мы их **не используем**
чтобы не блокировать CI, но упоминаем как next step.

## Как проверить локально (из папки задачи)

```bash
pytest -s
ruff check .
mypy --strict .
```

Флаг `-s` покажет реальные времена serial vs threading vs multiprocessing.
Ожидаемое: `serial ≈ threading`, `mp` в 2-4 раза быстрее (на 4-ядерном CPU).

## Материалы

- [multiprocessing docs](https://docs.python.org/3/library/multiprocessing.html)
- [concurrent.futures.ThreadPoolExecutor](https://docs.python.org/3/library/concurrent.futures.html#threadpoolexecutor)
- [Python GIL wiki](https://wiki.python.org/moin/GlobalInterpreterLock)
- [PEP 703 — Making the GIL optional](https://peps.python.org/pep-0703/)
- [PEP 734 — Multiple interpreters in the stdlib](https://peps.python.org/pep-0734/)
