# Тема: `threading` — базовые примитивы → `Semaphore` — лимит N одновременных
# Запуск из папки lecture: python3 1_threading/15_semaphore.py

import threading
import time

# Максимум 3 "download'а" одновременно
sem = threading.Semaphore(3)

def download(url: str) -> None:
    with sem:                       # acquire; блок если 3 уже качают
        print(f"[start ] {url}")
        time.sleep(0.5)
        print(f"[finish] {url}")

threads = [threading.Thread(target=download, args=(f"url-{i}",)) for i in range(8)]
for t in threads: t.start()
for t in threads: t.join()
