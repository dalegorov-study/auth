# Тема: GIL basics → Живой пример: CPU vs IO в threads
# Запуск из папки lecture: python3 1_threading/23_gil_io_bound.py

from concurrent.futures import ThreadPoolExecutor
import time

def io_task(delay: float) -> None:
    time.sleep(delay)  # sleep отпускает GIL

# Sequential
start = time.perf_counter()
for _ in range(4):
    io_task(0.5)
seq_time = time.perf_counter() - start

# Threaded
start = time.perf_counter()
with ThreadPoolExecutor(max_workers=4) as pool:
    list(pool.map(io_task, [0.5] * 4))
par_time = time.perf_counter() - start

print(f"IO-bound: sequential={seq_time:.2f}s, threaded(4)={par_time:.2f}s")
print(f"speedup = {seq_time / par_time:.2f}x")
