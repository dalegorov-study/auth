# Тема: Multiprocessing: обходим GIL через процессы → `ProcessPoolExecutor` — современный API
# Запуск из папки lecture: python3 2_multiprocessing/07_mp_procpool.py

from concurrent.futures import ProcessPoolExecutor
import time

def cpu_task(n: int) -> int:
    total = 0
    for i in range(n):
        total += i * i
    return total

if __name__ == "__main__":
    N = 10_000_000

    start = time.perf_counter()
    for _ in range(4):
        cpu_task(N)
    seq_time = time.perf_counter() - start

    start = time.perf_counter()
    with ProcessPoolExecutor(max_workers=4) as pool:
        list(pool.map(cpu_task, [N] * 4))
    par_time = time.perf_counter() - start

    print(f"CPU-bound: sequential={seq_time:.2f}s, processes(4)={par_time:.2f}s")
    print(f"speedup = {seq_time / par_time:.2f}x (у threads на той же задаче было ~1x)")
