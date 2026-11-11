"""3 варианта посчитать квадраты. См. README.md."""

import time
import queue
import multiprocessing
import threading

async def very_slow_function(x: int) -> int:
    """Возвращает x**2 с задержкой 0.1s — НЕ менять."""
    await asyncio.sleep(0.1)

    return x**100


def calc_squares_simple(bound: int) -> list[int]:
    return [very_slow_function(x) for x in range(bound)]

def _thread_worker(part_id: int, n_workers: int, bound: int, out: queue.Queue):
    for i in range(part_id, bound, n_workers):
        out.put((i, very_slow_function(i)))



def calc_squares_multithreading(bound: int) -> list[int]:
    N_WORKERS = multiprocessing.cpu_count()

    out = queue.Queue()

    threads = [
        threading.Thread(target=_thread_worker, 
                         args= (part_id, N_WORKERS, bound, out)) for part_id in range(N_WORKERS)
    ]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    results = [0] * bound

    while not out.empty():
        idx, value = out.get()
        results[idx] = value

    return results


def calc_squares_multiprocessing(bound: int) -> list[int]:
    N_PROCESSES = multiprocessing.cpu_count()

    tasks = [(i,) for i in range(bound)]

    with multiprocessing.Pool(processes=N_PROCESSES) as pool:
        results = pool.starmap(very_slow_function, tasks)

    return results

if __name__ == "__main__":
    BOUND = 12
    for fn in (calc_squares_simple, calc_squares_multithreading, calc_squares_multiprocessing):
        start = time.perf_counter()
        result = fn(BOUND)
        elapsed = time.perf_counter() - start
        print(f"{fn.__name__:30} {elapsed:.2f}s  {result}")