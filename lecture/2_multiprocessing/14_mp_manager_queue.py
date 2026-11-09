# Тема: IPC — как процессы обмениваются данными → Полная семья Queue/Pipe
# Запуск из папки lecture: python3 2_multiprocessing/14_mp_manager_queue.py

import multiprocessing as mp

def worker(q, name: str) -> None:
    q.put(f"hello from {name}")

if __name__ == "__main__":
    with mp.Manager() as mgr:
        q = mgr.Queue()       # <-- живёт в manager-процессе

        procs = [
            mp.Process(target=worker, args=(q, f"worker-{i}"))
            for i in range(3)
        ]
        for p in procs: p.start()
        for p in procs: p.join()

        while not q.empty():
            print(q.get())
