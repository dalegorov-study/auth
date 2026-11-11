# Тема: GIL basics → Живой пример: CPU vs IO в threads
# Запуск из папки lecture: python3 1_threading/22_gil_cpu_bound.py

from concurrent.futures import ThreadPoolExecutor
import time

def cpu_task(n: int) -> int:
    total = 0
    for i in range(n):
        total += i * i
    return total

N = 10_000_000

# Sequential
start = time.perf_counter()
for _ in range(4):
    cpu_task(N)
seq_time = time.perf_counter() - start

# Threaded (4 workers)
start = time.perf_counter()
with ThreadPoolExecutor(max_workers=4) as pool:
    list(pool.map(cpu_task, [N] * 4))
par_time = time.perf_counter() - start

print(f"CPU-bound: sequential={seq_time:.2f}s, threaded(4)={par_time:.2f}s")
print(f"speedup = {seq_time / par_time:.2f}x (ожидали бы ~4x если бы масштабировалось)")
