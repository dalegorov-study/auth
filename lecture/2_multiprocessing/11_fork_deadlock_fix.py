# Тема: Start methods: spawn / fork / forkserver → Живой deadlock: `fork` из многопоточного main
# Запуск из папки lecture: python3 2_multiprocessing/11_fork_deadlock_fix.py

import multiprocessing as mp
import threading
import time

lock = threading.Lock()

def hold_lock() -> None:
    lock.acquire()
    time.sleep(60)

def child_job() -> None:
    print("child: беру lock (свежий, из forkserver'а)")
    with lock:
        print("child: got it")

if __name__ == "__main__":
    mp.set_start_method("forkserver", force=True)

    threading.Thread(target=hold_lock, daemon=True).start()
    time.sleep(0.1)

    p = mp.Process(target=child_job)
    p.start()
    p.join(timeout=3)
    print(f"main: child alive? {p.is_alive()}")
