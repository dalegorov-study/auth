# Тема: `threading` — базовые примитивы → `Barrier` — синхронизация N потоков в одной точке
# Запуск из папки lecture: python3 1_threading/16_barrier.py

import threading
import time
import random

N = 4
barrier = threading.Barrier(N)

def worker(idx: int) -> None:
    time.sleep(random.random() * 0.5)     # каждый готовится своё время
    print(f"[{idx}] ready, waiting for others")
    barrier.wait()                        # блок пока все N не дойдут
    print(f"[{idx}] GO")                  # все стартуют одновременно

threads = [threading.Thread(target=worker, args=(i,)) for i in range(N)]
for t in threads: t.start()
for t in threads: t.join()
