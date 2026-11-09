# Тема: Start methods: spawn / fork / forkserver
# Запуск из папки lecture: python3 2_multiprocessing/09_start_methods.py

import multiprocessing as mp
print(f'default start method: {mp.get_start_method()}')
print(f'available methods: {mp.get_all_start_methods()}')
