# Тема: Multiprocessing: обходим GIL через процессы → `multiprocessing.Pool` — классический API
# Запуск из папки lecture: python3 2_multiprocessing/08_mp_pool.py

import multiprocessing as mp

def square(x: int) -> int:
    return x * x

if __name__ == "__main__":
    with mp.Pool(processes=4) as pool:
        result = pool.map(square, range(10))
        print("map:", result)

        # imap_unordered — итерация по мере готовности, не по порядку
        for r in pool.imap_unordered(square, range(5)):
            print("got:", r)
