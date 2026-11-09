# Демо-код к лекции: threading, multiprocessing, asyncio

Каждый файл — отдельный пример к лекции. Запускать из этой папки:

```bash
python3 1_threading/04_thread_basic.py
```

Код написан под Python 3.14 — лучше запускать на нём. Минимальная версия для отдельных примеров указана в таблице и в шапке файла.
Для `3_asyncio/18_test_async.py` нужен `pip install pytest pytest-asyncio`, запуск — `pytest 3_asyncio/18_test_async.py -v`.


## Threading

| Файл | Тема |
| --- | --- |
| `1_threading/01_cpu_count.py` | `threading` — базовые примитивы → Что такое поток |
| `1_threading/02_cpu_topology.py` | `threading` — базовые примитивы → Что такое поток |
| `1_threading/03_thread_ids.py` | `threading` — базовые примитивы → Что такое поток |
| `1_threading/04_thread_basic.py` | `threading` — базовые примитивы → `Thread` — ручное управление |
| `1_threading/05_join_result.py` | `threading` — базовые примитивы → Зачем `join()`? |
| `1_threading/06_daemon_demo.py` | `threading` — базовые примитивы → Зачем `join()`? |
| `1_threading/07_thread_exception.py` | `threading` — базовые примитивы → Зачем `join()`? |
| `1_threading/08_join_timeout.py` | `threading` — базовые примитивы → Зачем `join()`? |
| `1_threading/09_race_counter.py` | `threading` — базовые примитивы → Синхронизация: `Lock` |
| `1_threading/10_race_counter_sleep.py` | `threading` — базовые примитивы → Синхронизация: `Lock` |
| `1_threading/11_lock_fix.py` | `threading` — базовые примитивы → Синхронизация: `Lock` |
| `1_threading/12_rlock.py` | `threading` — базовые примитивы → `RLock` — reentrant lock |
| `1_threading/13_event.py` | `threading` — базовые примитивы → `Event` — one-shot флаг для сигналов |
| `1_threading/14_condition.py` | `threading` — базовые примитивы → `Condition` — Lock + wait/notify |
| `1_threading/15_semaphore.py` | `threading` — базовые примитивы → `Semaphore` — лимит N одновременных |
| `1_threading/16_barrier.py` | `threading` — базовые примитивы → `Barrier` — синхронизация N потоков в одной точке |
| `1_threading/17_queue.py` | `threading` — базовые примитивы → `queue.Queue` — thread-safe FIFO |
| `1_threading/18_thread_local.py` | `threading` — базовые примитивы → `threading.local` — thread-local storage |
| `1_threading/19_threadpool.py` | `ThreadPoolExecutor` — почти всегда так |
| `1_threading/20_as_completed.py` | `ThreadPoolExecutor` — почти всегда так → Futures API |
| `1_threading/21_future_errors.py` | `ThreadPoolExecutor` — почти всегда так → Обработка ошибок в futures |
| `1_threading/22_gil_cpu_bound.py` | GIL basics → Живой пример: CPU vs IO в threads |
| `1_threading/23_gil_io_bound.py` | GIL basics → Живой пример: CPU vs IO в threads |
| `1_threading/24_switch_interval.py` | GIL basics → `sys.getswitchinterval` |
| `1_threading/25_deadlock_timeout.py` | Race conditions, deadlock, livelock → Deadlock |
| `1_threading/26_livelock.py` | Race conditions, deadlock, livelock → Livelock |
| `1_threading/27_livelock_backoff.py` | Race conditions, deadlock, livelock → Livelock |

## Multiprocessing

| Файл | Тема |
| --- | --- |
| `2_multiprocessing/01_subprocess_run.py` | `subprocess` — с чего начнём → `subprocess.run` — простой случай |
| `2_multiprocessing/02_popen_stream.py` | `subprocess` — с чего начнём → `Popen` — контроль над процессом |
| `2_multiprocessing/03_injection_demo.py` | `subprocess` — с чего начнём → `shell=True` — почему опасно |
| `2_multiprocessing/04_injection_safe.py` | `subprocess` — с чего начнём → `shell=True` — почему опасно |
| `2_multiprocessing/05_shlex_quote.py` | `subprocess` — с чего начнём → `shell=True` — почему опасно |
| `2_multiprocessing/06_git_version.py` | `subprocess` — с чего начнём → Практический пример: вызов git |
| `2_multiprocessing/07_mp_procpool.py` | Multiprocessing: обходим GIL через процессы → `ProcessPoolExecutor` — современный API |
| `2_multiprocessing/08_mp_pool.py` | Multiprocessing: обходим GIL через процессы → `multiprocessing.Pool` — классический API |
| `2_multiprocessing/09_start_methods.py` | Start methods: spawn / fork / forkserver |
| `2_multiprocessing/10_fork_deadlock.py` | Start methods: spawn / fork / forkserver → Живой deadlock: `fork` из многопоточного main |
| `2_multiprocessing/11_fork_deadlock_fix.py` | Start methods: spawn / fork / forkserver → Живой deadlock: `fork` из многопоточного main |
| `2_multiprocessing/12_pickle_limits.py` | IPC — как процессы обмениваются данными → Ограничение: pickle-only |
| `2_multiprocessing/13_mp_queue.py` | IPC — как процессы обмениваются данными → `multiprocessing.Queue` — pickle через pipe |
| `2_multiprocessing/14_mp_manager_queue.py` | IPC — как процессы обмениваются данными → Полная семья Queue/Pipe |
| `2_multiprocessing/15_shared_memory.py` | IPC — как процессы обмениваются данными → `shared_memory` — zero-copy для bytes |
| `2_multiprocessing/16_subinterpreter.py` | Subinterpreters — PEP 684 (Python 3.14+) |
| `2_multiprocessing/17_subinterpreter_queue.py` | Subinterpreters — PEP 684 → Обмен данными между интерпретаторами (Python 3.14+) |

## Asyncio

| Файл | Тема |
| --- | --- |
| `3_asyncio/01_generator_counter.py` | Освежаем генераторы |
| `3_asyncio/02_generator_send.py` | Освежаем генераторы → `send` — двусторонняя коммуникация |
| `3_asyncio/03_yield_from.py` | Освежаем генераторы → `yield from` — делегирование |
| `3_asyncio/04_generator_scheduler.py` | Освежаем генераторы → Зачем это всё — генератор как "приостановимая задача" |
| `3_asyncio/05_coroutine_object.py` | От генератора к coroutine |
| `3_asyncio/06_async_hello.py` | От генератора к coroutine → Простейший запуск |
| `3_asyncio/07_async_await.py` | От генератора к coroutine → await = "приостанови меня пока не готово" |
| `3_asyncio/08_mini_asyncio.py` | Event loop изнутри — mini_asyncio → Concept: system call через yield |
| `3_asyncio/09_async_gather.py` | asyncio API → `asyncio.gather` — параллельное выполнение |
| `3_asyncio/10_async_task.py` | asyncio API → `asyncio.create_task` — планируем в фоне |
| `3_asyncio/11_async_wait_for.py` | asyncio API → `asyncio.wait_for` — timeout |
| `3_asyncio/12_async_for.py` | Async iterators и context managers → async for |
| `3_asyncio/13_async_with.py` | Async iterators и context managers → async with |
| `3_asyncio/14_async_orphan.py` | Structured concurrency |
| `3_asyncio/15_async_taskgroup.py` | Structured concurrency → `TaskGroup` (3.11+) (Python 3.11+) |
| `3_asyncio/16_async_coloring.py` | Когда async, а когда нет → Async coloring |
| `3_asyncio/17_async_deadlock.py` | Когда async, а когда нет → Deadlock в async: concurrency ≠ параллелизм (Python 3.11+) |
| `3_asyncio/18_test_async.py` | Тестирование async: `pytest-asyncio` |
