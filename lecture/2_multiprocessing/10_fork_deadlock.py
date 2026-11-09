# Тема: Start methods: spawn / fork / forkserver → Живой deadlock: `fork` из многопоточного main
# Запуск из папки lecture: python3 2_multiprocessing/10_fork_deadlock.py

import multiprocessing as mp
import threading
import time

lock = threading.Lock()

def hold_lock() -> None:
    lock.acquire()      # захватываем и сидим
    time.sleep(60)

def child_job() -> None:
    print("child: пытаюсь взять lock...")
    with lock:          # <-- в parent захвачен hold_lock-тредом
        print("child: got it")   # никогда не напечатается при fork

if __name__ == "__main__":
    mp.set_start_method("fork", force=True)

    threading.Thread(target=hold_lock, daemon=True).start()
    time.sleep(0.1)     # даём треду взять lock

    p = mp.Process(target=child_job)
    p.start()
    p.join(timeout=3)
    if p.is_alive():
        print("main: child ЗАВИС - deadlock (fork() унаследовал held lock)")
        p.terminate()
    else:
        print("main: unexpectedly finished")
